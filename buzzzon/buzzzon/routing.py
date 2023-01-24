from django.core.asgi import get_asgi_application
from django.urls import path, re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import django_eventstream

from chat import consumers, auth


application = ProtocolTypeRouter({
    "http": URLRouter([
        path('events/', AuthMiddlewareStack(URLRouter(django_eventstream.routing.urlpatterns))),
        re_path(r'', get_asgi_application()),
    ]),
    # WebSocket chat handler
    "websocket": auth.TokenAuthMiddleware(
        URLRouter([
            path('ws/chat/<int:contact_id>/', consumers.ChatConsumer.as_asgi()),
            path('ws/chat/group/<str:share_code>/', consumers.GroupChatConsumer.as_asgi()),
        ])
    ),
})
