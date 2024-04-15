from .models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def phone_number_exist(value):
    if not User.objects.filter(phone_number=value).exists():
        raise ValidationError(_('شماره تلفن وجود ندارد'))
    return value

def password_validator(value):
    if len(value) < 8:
        raise ValidationError(_('پسورد نباید کمتر از 8 کاراکتر باشد'))
    elif value.isnumeric() or value.isalpha():
        raise ValidationError(_('پسورد نباید عدد یا متن باشد.باید ترکیبی از انها باشد'))
    
def phone_validator(value):
    if User.objects.filter(phone_number=value).exists():
        raise ValidationError(_('کاربر با این شماره رجود داره'))

def username_validator(value):
    if User.objects.filter(phone_number=value).exists():
        raise ValidationError(_('کاربر با این شماره رجود داره'))
