from django.urls import re_path

from retroville.chat.consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r"^ws/chat/(?P<room_name>[^/]+)/$", ChatConsumer.as_asgi()),
]
