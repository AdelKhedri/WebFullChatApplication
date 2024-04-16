from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PrivateChat
from user.models import User
from django.db.models import Q


class ChatView(View):
    template_name = 'chat/base.html'

    def setup(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            self.context = {
                'private_chats': PrivateChat.objects.prefetch_related('users').filter(users=request.user),
            }
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        username_receive = request.POST.get('receive', None)

        if username_receive:
            try:
                receive = User.objects.get(username=username_receive)
                private_chat = PrivateChat.objects.prefetch_related('users').filter(users=receive).filter(users=request.user).exists()
                if not private_chat:
                    private_chat = PrivateChat.objects.create()
                    private_chat.users.set([receive, request.user])
                    private_chat.save()
                return redirect('chat:main', username=username_receive)
            except:
                pass
        else:
            self.context.update({'msg': 'user not found'})
        return render(request, self.template_name, self.context)