from __future__ import annotations

import socket

import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from tests.factories import StoryFactory, UserFactory, UserReadStoryFactory, WaitingRoomFactory


@pytest.fixture(autouse=True)
def _block_network(monkeypatch, request):
    if request.node.get_closest_marker("integration"):
        return

    def _guard(*_args, **_kwargs):
        raise RuntimeError("Network access is disabled in the default test suite")

    monkeypatch.setattr(socket.socket, "connect", _guard)


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def other_user(db):
    return UserFactory()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client(user):
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=user)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    client.user = user
    return client


@pytest.fixture
def staff_client(db):
    staff = UserFactory(is_staff=True, is_superuser=True)
    client = APIClient()
    token, _ = Token.objects.get_or_create(user=staff)
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    client.user = staff
    return client


@pytest.fixture
def two_users_in_room(db):
    left = UserFactory()
    right = UserFactory()
    story = StoryFactory()
    UserReadStoryFactory(user=left, story=story, interested=True)
    UserReadStoryFactory(user=right, story=story, interested=True)
    WaitingRoomFactory(user=left)
    WaitingRoomFactory(user=right)
    return left, right, story
