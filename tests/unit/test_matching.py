from datetime import date
from unittest.mock import patch

import pytest
from rest_framework.authtoken.models import Token

from retroville.matching.models import Match, Room
from retroville.matching.services import MatchServiceError, request_match
from tests.factories import StoryFactory, UserFactory, UserReadStoryFactory, WaitingRoomFactory


@pytest.mark.django_db
def test_request_match_creates_match_and_clears_room(two_users_in_room):
    left, right, story = two_users_in_room
    match = request_match(left, today=date.today())
    assert {match.caller_id, match.receiver_id} == {left.pk, right.pk}
    assert match.matched_story_id == story.id
    assert not Room.objects.filter(user__in=[left, right]).exists()


@pytest.mark.django_db
def test_request_match_is_idempotent(two_users_in_room):
    left, right, _story = two_users_in_room
    first = request_match(left, today=date.today())
    second = request_match(left, today=date.today())
    assert first.pk == second.pk
    assert Match.objects.count() == 1


@pytest.mark.django_db
def test_user_not_in_room_raises():
    user = UserFactory()
    with pytest.raises(MatchServiceError, match="not in room"):
        request_match(user, today=date.today())


@pytest.mark.django_db
def test_no_stories_today_raises():
    user = UserFactory()
    WaitingRoomFactory(user=user)
    with pytest.raises(MatchServiceError, match="no user read stories"):
        request_match(user, today=date.today())


@pytest.mark.django_db
def test_no_overlap_raises():
    left = UserFactory()
    right = UserFactory()
    liked = StoryFactory()
    ignored = StoryFactory()
    UserReadStoryFactory(user=left, story=liked, interested=True)
    UserReadStoryFactory(user=right, story=ignored, interested=True)
    WaitingRoomFactory(user=left)
    WaitingRoomFactory(user=right)
    with pytest.raises(MatchServiceError, match="no users to match"):
        request_match(left, today=date.today())


@pytest.mark.django_db
def test_find_match_endpoint_returns_201(auth_client, two_users_in_room):
    left, right, _story = two_users_in_room
    token = Token.objects.get(user=left)
    auth_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = auth_client.get("/api/v1/match/find/")
    assert response.status_code == 201
    assert response.json()["story"]["id"] == _story.id


@pytest.mark.django_db
def test_check_match_hides_other_users_matches(auth_client, two_users_in_room):
    left, right, _story = two_users_in_room
    match = request_match(left, today=date.today())
    outsider = UserFactory()
    token = Token.objects.get(user=outsider)
    auth_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = auth_client.get(f"/api/v1/match/check/?match_id={match.pk}")
    assert response.status_code == 404


@pytest.mark.django_db
def test_list_room_is_staff_only(auth_client, staff_client, user):
    WaitingRoomFactory(user=user)
    assert auth_client.get("/api/v1/room/list/").status_code == 403
    assert staff_client.get("/api/v1/room/list/").status_code == 200
