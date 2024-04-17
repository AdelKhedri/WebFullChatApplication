from django.db import models
from user.models import User


class PrivateChat(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user2')
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت چت')
    
    def __str__(self):
        return f"{self.user1.username} & {self.user2.username}"


class PrivateMessage(models.Model):
    text = models.CharField(max_length=1000, verbose_name='متن')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sender', verbose_name='ارسال کننده')
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='receiver', verbose_name='دریافت کننده')
    chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE, related_name='chat', verbose_name='چت')
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال')

    def __str__(self):
        return "{} : {}".format(self.sender.username, self.chat.pk)


class GroupChat(models.Model):
    name = models.CharField(max_length=50, help_text='نام گروه', verbose_name='نام گروه')
    description = models.TextField(max_length=100, blank=True, verbose_name='درباره گروه')
    image = models.ImageField(upload_to='images/groups/', blank=True, null=True, verbose_name='عکس گروه')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='manager_group', verbose_name='مدیر')
    members = models.ManyToManyField(User, related_name='members', verbose_name='اعضا')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت')
    can_send_message = models.BooleanField(default=True, verbose_name='امکان ارسال پیام')
    can_see_members = models.BooleanField(default=True, verbose_name='امکان دیدن اعضا')
    address = models.CharField(unique=True, max_length=20, verbose_name='ادرس گروه')

    class Meta:
        ordering = ['created_time', 'name']
    
    def __str__(self):
        return self.name


class GroupMessage(models.Model):
    class ChoiceMessageType(models.TextChoices):
        type_1 = 'join', 'join'
        type_2 = 'left', 'left'
        type_3 = 'msg', 'msg'
        type_4 = 'delete', 'delete'
        type_5 = 'private_msg', 'private_msg'
    
    message_type = models.TextField(choices=ChoiceMessageType.choices, verbose_name='نوع پیام')
    text = models.CharField(blank=True, max_length=500, verbose_name='متن پیام')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sender_group', verbose_name='ارسال کننده')
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='receiver_group', verbose_name='ارسال کننده')
    send_time = models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال پیام')
    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, related_name='groupchat', verbose_name='گروه')
    
    class Meta:
        ordering = ['send_time']
    
    def __str__(self):
        return f'{self.send_time}'