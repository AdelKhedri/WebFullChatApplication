from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from websocket import routing as wsrouting

django_asgi_aplication = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_aplication,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            wsrouting.websocket_urlpatterns
        )
    )
})