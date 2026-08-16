"""Authenticate WebSocket connections with a DRF token query param or header."""

from __future__ import annotations

from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        scope = dict(scope)
        scope["user"] = await _user_from_scope(scope)
        return await super().__call__(scope, receive, send)


@database_sync_to_async
def _user_from_scope(scope):
    headers = {key.decode().lower(): value.decode() for key, value in scope.get("headers", [])}
    token_key = None
    auth = headers.get("authorization", "")
    if auth.lower().startswith("token "):
        token_key = auth.split(" ", 1)[1].strip()
    if not token_key:
        query = parse_qs(scope.get("query_string", b"").decode())
        token_key = (query.get("token") or [None])[0]
    if not token_key:
        return AnonymousUser()
    try:
        return Token.objects.select_related("user").get(key=token_key).user
    except Token.DoesNotExist:
        return AnonymousUser()
