from django.urls import path
from .consumers import PrivateChatsConsumer

app_name = 'websocket'
websocket_urlpatterns = [
    path('ws/chat/', PrivateChatsConsumer.as_asgi(), name='allchats'),
]