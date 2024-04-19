from django.contrib import admin
from .models import PrivateChat, PrivateMessage, GroupChat, GroupMessage
from django.contrib import admin


class PrivateChatRegistration(admin.ModelAdmin):
    list_display = ['date_time', 'user1', 'user2']
    search_fields = ['users']
    list_per_page = 40


class PrivateMessageRegistration(admin.ModelAdmin):
    list_display = ['date_time', 'sender', 'chat']
    search_fields = ['sender', 'chat']
    list_per_page = 40
    ordering = ['date_time', 'chat', 'sender']


class GroupChatRegistration(admin.ModelAdmin):
    list_display = ['name', 'has_image', 'can_send_message', 'can_see_members', 'created_time']
    search_fields = ['name', 'address', 'description']
    list_filter = ['can_send_message', 'can_see_members']
    

class GroupMessageRegistration(admin.ModelAdmin):
    list_display = ['message_type', 'sender', 'receiver', 'chat', 'send_time']
    search_fields = ['sender', 'receiver']
    list_filter = ['message_type']


admin.site.register(PrivateChat, PrivateChatRegistration)
admin.site.register(PrivateMessage, PrivateMessageRegistration)
admin.site.register(GroupChat, GroupChatRegistration)
admin.site.register(GroupMessage, GroupMessageRegistration)