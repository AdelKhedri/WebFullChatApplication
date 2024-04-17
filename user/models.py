from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    phone_number = models.IntegerField(verbose_name='شماره تلفن', unique=True)
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'phone_number'
    
    class Meta:
        ordering = ['phone_number']
    
    def has_email(self):
        return True if self.email else False
    
    def __str__(self):
        if self.last_name or self.first_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return str(self.username)


class Profile(models.Model):
    description = models.CharField(max_length=100, blank=True, verbose_name='درباره من')
    show_phone = models.BooleanField(default=0, verbose_name='نمایش شماره تلفن')
    image = models.ImageField(upload_to='images/profiles/', blank=True, null=True, verbose_name='عکس کاربر')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['user']
    
    def has_image(self):
        return True if self.image else False

    def __str__(self):
        return self.user.__str__()