from django.db import models
from user.models import User


class PrivateChat(models.Model):
    users = models.ManyToManyField(User, related_name='users')
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت چت')

    def users_str_list(self):
        return ' '.join([user.username for user in self.users.all()])
    
    def __str__(self):
        return f"{self.users.all().first().username} & {self.users.all().last().username}"


class PrivateMessage(models.Model):
    text = models.CharField(max_length=1000, verbose_name='متن')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sender', verbose_name='ارسال کننده')
    chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE, related_name='chat', verbose_name='چت')
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال')

    def __str__(self):
        return "{} : {}".format(self.sender.username, self.chat.pk)