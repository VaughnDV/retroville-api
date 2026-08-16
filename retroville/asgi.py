import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "retroville.settings.local")

django_asgi_app = get_asgi_application()

from retroville.chat.routing import websocket_urlpatterns  # noqa: E402
from retroville.chat.token_auth import TokenAuthMiddleware  # noqa: E402

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddleware(AuthMiddlewareStack(URLRouter(websocket_urlpatterns)))
        ),
    }
)
