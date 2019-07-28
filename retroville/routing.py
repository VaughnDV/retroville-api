from django.conf.urls import url
from django.urls import path
from retroville.chat import consumers
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from retroville.matching_room.consumers import MatchingRoomConsumer
from djangochannelsrestframework.consumers import view_as_consumer


application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^matching/$", view_as_consumer(MatchingRoomConsumer)),
            url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
        ])
    ),
 })
