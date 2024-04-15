from django.urls import path
from .views import LoginView, SinUpView

app_name = 'user'

urlpatterns = [
    path('login/' , LoginView.as_view(), name='login'),
    path('sinup/' , SinUpView.as_view(), name='sinup'),
]