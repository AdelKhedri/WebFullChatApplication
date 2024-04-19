from django.urls import path
from . import views


app_name = 'chat'

urlpatterns = [
    path('', views.ChatView.as_view(), name='main'),
    path('u/<username>/', views.PrivateChateView.as_view(), name='private-chat'),
    path('group/<address>/', views.GroupChatView.as_view(), name='group-chat'),
    path('join/', views.JoinView.as_view(), name='request-join'),
]