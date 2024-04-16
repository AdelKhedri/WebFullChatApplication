from django.contrib import admin
from .models import PrivateChat, PrivateMessage
from django.contrib import admin


class PrivateChatRegistration(admin.ModelAdmin):
    list_display = ['date_time', 'users_str_list']
    search_fields = ['users']
    list_per_page = 40


class PrivateMessageRegistration(admin.ModelAdmin):
    list_display = ['date_time', 'sender', 'chat']
    search_fields = ['sender', 'chat']
    list_per_page = 40
    ordering = ['date_time', 'chat', 'sender']


admin.site.register(PrivateChat, PrivateChatRegistration)
admin.site.register(PrivateMessage, PrivateMessageRegistration)