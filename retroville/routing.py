# from django.conf.urls import url
# from retroville.chat import consumers as chat
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
#
#
# application = ProtocolTypeRouter({
#     "websocket": AuthMiddlewareStack(
#         URLRouter([
#             url(r'^ws/chat/(?P<room_name>[^/]+)/$', chat.ChatConsumer),
#         ])
#     ),
#  })
