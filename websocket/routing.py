from django.urls import path
from .consumers import PrivateChatsConsumer, GroupChatConsumer, NotificationConsumer

app_name = 'websocket'
websocket_urlpatterns = [
    path('ws/privatechat/', PrivateChatsConsumer.as_asgi(), name='private-chat-websocket'),
    path('ws/groupchat/', GroupChatConsumer.as_asgi(), name='group-chat-websocket'),
    path('ws/notification/', NotificationConsumer.as_asgi(), name='notification'),
]