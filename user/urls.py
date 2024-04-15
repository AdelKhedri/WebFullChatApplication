from django.urls import path
from .views import LoginView, SinUpView, ChangeProfileView

app_name = 'user'

urlpatterns = [
    path('login/' , LoginView.as_view(), name='login'),
    path('sinup/' , SinUpView.as_view(), name='sinup'),
    path('profile/', ChangeProfileView.as_view(), name='profile')
]