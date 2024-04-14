from django.contrib import admin
from .models import Profile, User
from django.contrib import admin


class UserRegistration(admin.ModelAdmin):
    list_display = ('username', 'phone_number', 'email')
    search_fields = ('username', 'phone_number', 'email')
    ordering = ['username', 'phone_number', 'email']
    # fieldsets 
    list_display_links = ['username', 'phone_number']
    list_per_page = 40

class ProfileRegistration(admin.ModelAdmin):
    list_display = ['user', 'show_phone']
    search_fields = ['user',]
    list_display_links = ['user', 'show_phone']


admin.site.register(User, UserRegistration)
admin.site.register(Profile, ProfileRegistration)