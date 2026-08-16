"""
WebSocket chat.

- Authentication: DRF token in `Authorization: Token ...` or `?token=`.
- Origin: `AllowedHostsOriginValidator` using `ALLOWED_HOSTS`.
- Message size: `WEBSOCKET_MAX_MESSAGE_BYTES` (default 4096). Oversize closes 4408.
- Reconnect: clients should reconnect to the same `ws/chat/<room>/` URL with a
  fresh token; membership is re-joined on `connect`. There is no server-side
  backlog; missed messages are not replayed.
"""

import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.contrib.auth.models import AnonymousUser


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if user is None or isinstance(user, AnonymousUser) or not user.is_authenticated:
            await self.close(code=4401)
            return

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        payload = text_data or ""
        if len(payload.encode()) > settings.WEBSOCKET_MAX_MESSAGE_BYTES:
            await self.close(code=4408)
            return
        try:
            message = json.loads(payload)["message"]
        except (json.JSONDecodeError, KeyError, TypeError):
            await self.send(text_data=json.dumps({"error": "invalid_payload"}))
            return
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))
