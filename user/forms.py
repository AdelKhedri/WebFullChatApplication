from typing import Any
from django import forms
from . import validators
from .models import User, Profile
from django.utils.translation import gettext_lazy as _

def_atter = { 'class': 'form-control background text-white' }


class UserLoginForm(forms.Form):
    phone_number = forms.CharField(help_text='9123456789', widget=forms.NumberInput(attrs=def_atter), validators=[validators.phone_number_exist, ])
    password = forms.CharField(help_text="*******", widget=forms.PasswordInput(attrs=def_atter), validators=[validators.password_validator])


class UserCreateForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=def_atter), validators=[validators.password_validator])

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'password', 'password2']

        widgets = {
            'username': forms.TextInput(attrs=def_atter),
            'phone_number': forms.NumberInput(attrs=def_atter),
            'password': forms.PasswordInput(attrs=def_atter),
        }

        error_messages = {
            'username': {
                'required': 'این فیلد اجباری است',
                'unique': 'این یوزرنیم تکراری است',
            },
            'phone_number': {
                'required': 'این فیلد اجباری است',
                'unique': 'این شماره تکراری است',
            }
        }


    def clean(self):
        cleaned_data = super().clean()
        password2 = cleaned_data.get('password2', None)
        password1 = cleaned_data['password']
        if password1 != password2:
            raise forms.ValidationError(_('رمز عبور نباید با هم تفاوت داشته باشند'))
        return cleaned_data


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'phone_number', 'email', 'last_name', 'first_name']
    
        widgets = {
            'username': forms.TextInput(attrs=def_atter),
            'phone_number': forms.NumberInput(attrs=def_atter),
            'email': forms.EmailInput(attrs=def_atter),
            'last_name': forms.TextInput(attrs=def_atter),
            'first_name': forms.TextInput(attrs=def_atter)
        }


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['description', 'show_phone', 'image']

        widgets = {
            'description': forms.Textarea(attrs=def_atter),
            'show_phone': forms.CheckboxInput(attrs=def_atter),
            # 'image': forms.FileInput(attrs=def_atter)
        }