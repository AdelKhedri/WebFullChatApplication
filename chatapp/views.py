from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View, generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PrivateChat, PrivateMessage, GroupChat, GroupMessage
from user.models import User
from django.db.models import Q
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from websocket.consumers import send_message_group


class ChatView(LoginRequiredMixin, View):
    template_name = 'chat/chat.html'

    def setup(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.context = {
                'private_chats': PrivateChat.objects.filter(Q(user1=request.user) | Q(user2=request.user)),
                'group_chats': GroupChat.objects.prefetch_related('members').filter(members=request.user),
            }
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        username_receive = request.POST.get('receive', None)

        if username_receive:
            try:
                receive = User.objects.get(username=username_receive)
                private_chat = PrivateChat.objects.get_or_create(user1=request.user, user2=receive)
                return redirect('chat:private-chat', username=username_receive)
            except:
                self.context.update({'msg': 'user not found'})
        
        group_name = request.POST.get('group_name', None)
        group_description = request.POST.get('group_description', None)
        if group_name:
            new_group = GroupChat(name = group_name, description=group_description, manager=request.user)
            new_group.save()
            new_group.members.add(request.user)
            new_group.save()
            redirect('chat:group-chat', address=new_group.address)
        return render(request, self.template_name, self.context)


class PrivateChateView(LoginRequiredMixin, generic.ListView):
    template_name = 'chat/private_chat.html'
    context_object_name = 'messages'
    
    def get_queryset(self):
        chat = get_object_or_404(PrivateChat.objects.select_related('user1', 'user2').filter(Q(user1=self.request.user, user2__username=self.kwargs['username'])|Q(user1__username=self.kwargs['username'], user2=self.request.user)))
        return PrivateMessage.objects.select_related('chat').filter(chat=chat)
    
    def get_context_data(self):
        context = super().get_context_data()
        context['private_chats'] = PrivateChat.objects.select_related('user1', 'user2').filter(Q(user1=self.request.user) | Q(user2=self.request.user))
        context['group_chats'] = GroupChat.objects.prefetch_related('members').filter(members=self.request.user)
        context['target_user'] = User.objects.get(username=self.kwargs['username'])
        return context


class GroupChatView(LoginRequiredMixin, View):
    template_name = 'chat/group_chat.html'
    context_object_name = 'messages'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.all_groups = GroupChat.objects.prefetch_related('members')
            self.group = get_object_or_404(self.all_groups, address=kwargs['address'])
            private_chats = PrivateChat.objects.select_related('user1', 'user2').filter(Q(user1=self.request.user) | Q(user2=self.request.user))
            self.joined_groups = self.all_groups.filter(members=request.user)
            message = GroupMessage.objects.select_related('chat').filter(chat=self.group)
            self.contex = {
                'private_chats': private_chats,
                'group_chats': self.joined_groups,
                'group': self.group,
                'messages': message,
            }
            if request.user not in self.group.members.all():
                return redirect(reverse('chat:request-join') + '?gr=' + kwargs['address'])
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.contex)
    
    def post(self, request, *args, **kwargs):
        left_group = request.POST.get('left_group', None)
        if left_group:
            if request.user in self.group.members.all():
                if self.group.manager == request.user:
                    self.group.delete()
                else:
                    self.group.members.remove(request.user)
                    chat = {
                        'address': self.group.address,
                        'id': self.group.id,
                        'can_send_message': self.group.can_send_message
                    }
                    channel_layer = get_channel_layer()
                    async_to_sync(send_message_group)(chat, channel_layer, 'left', sender=request.user.username)
                    GroupMessage.objects.create(message_type='left', sender=request.user, chat=self.group)
        return redirect("chat:main")


class JoinView(LoginRequiredMixin, View):
    template_name = 'chat/join_chat.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            group_address = request.GET.get('gr', None)
            if group_address:
                self.group = get_object_or_404(GroupChat.objects.prefetch_related('members'), address=group_address)
                if request.user not in self.group.members.all():
                    self.context = {
                        'group': self.group,
                    }
                else:
                    return redirect('chat:group-chat', address = self.group.address)
            else:
                self.context = {}
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *arg, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        request_joined_group = request.POST.get('group_join', None)

        if request_joined_group:
            if request.user not in self.group.members.all():
                self.group.members.add(request.user)
                channel_layer = get_channel_layer()
                chat = {
                    'address': self.group.address,
                    'id': self.group.id,
                    'can_send_message': self.group.can_send_message
                }
                async_to_sync(send_message_group)(chat, channel_layer,'join', sender=request.user.username )
                GroupMessage.objects.create(message_type='join', sender=request.user, chat=self.group)
            return redirect('chat:group-chat', address=self.group.address)
        return render(request, self.template_name, {})