from django.shortcuts import render, redirect, get_object_or_404
from django.views import View, generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PrivateChat, PrivateMessage
from user.models import User


class ChatView(LoginRequiredMixin, View):
    template_name = 'chat/base.html'

    def setup(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.context = {
                'private_chats': PrivateChat.objects.filter(user1=request.user),
            }
        else:
            self.context = {}
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
                pass
        else:
            self.context.update({'msg': 'user not found'})
        return render(request, self.template_name, self.context)