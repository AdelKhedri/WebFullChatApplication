from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PrivateChat, PrivateMessage, GroupChat, GroupMessage
from user.models import User
from django.db.models import Q


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
            redirect('chat:main')
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


class GroupChatView(LoginRequiredMixin, generic.ListView):
    template_name = 'chat/group_chat.html'
    context_object_name = 'messages'

    def get_queryset(self):
        self.all_groups = GroupChat.objects.prefetch_related('members').filter(members=self.request.user)
        self.group = get_object_or_404(self.all_groups, Q(address=self.kwargs['address']) & Q(members=self.request.user))
        return GroupMessage.objects.filter(chat=self.group)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['private_chats'] = PrivateChat.objects.select_related('user1', 'user2').filter(Q(user1=self.request.user) | Q(user2=self.request.user))
        context['group_chats'] = self.all_groups
        context['group'] = self.group
        return context