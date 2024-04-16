from django.urls import path
from . import views


app_name = 'chat'

urlpatterns = [
    path('', views.ChatView.as_view(), name='main'),
    path('u/<username>/', views.PrivateChateView.as_view(), name='private-chat'),
]