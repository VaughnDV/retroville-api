from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from retroville.matching_room.consumers import MatchingRoomConsumer
from djangochannelsrestframework.consumers import view_as_consumer


application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^matching/$", view_as_consumer(MatchingRoomConsumer)),
        ])
    ),
 })
