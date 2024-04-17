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


admin.site.register(PrivateChat, PrivateChatRegistration)
admin.site.register(PrivateMessage, PrivateMessageRegistration)
admin.site.register(GroupChat)
admin.site.register(GroupMessage)