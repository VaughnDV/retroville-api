"""Matching use-cases. Views and Celery tasks call this module, not models directly."""

from __future__ import annotations

import logging
from datetime import date

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from retroville.matching.domain import Candidate, liked_story_ids, select_match
from retroville.matching.models import Match, MatchActivity, Room, RoomActivity
from retroville.providers.voice import get_voice_provider
from retroville.stories.models import Story, UserReadStory

logger = logging.getLogger(__name__)
User = get_user_model()


class MatchServiceError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


def enter_waiting_room(user) -> tuple[Room, bool]:
    with transaction.atomic():
        room, created = Room.objects.select_for_update().get_or_create(user=user)
        RoomActivity.objects.create(user=user)
        return room, created


def leave_waiting_room(user) -> bool:
    deleted, _ = Room.objects.filter(user=user).delete()
    return deleted > 0


def request_match(user, *, today: date | None = None, rng=None) -> Match:
    """Idempotent: an existing match for the user is returned without creating another."""
    today = today or timezone.now().date()
    with transaction.atomic():
        existing = (
            Match.objects.select_for_update()
            .filter(Q(caller=user) | Q(receiver=user))
            .select_related("caller", "receiver", "matched_story")
            .first()
        )
        if existing:
            logger.info("match.idempotent_hit", extra={"user_id": str(user.pk), "match_id": existing.pk})
            return existing

        if not Room.objects.select_for_update().filter(user=user).exists():
            raise MatchServiceError("Current user not in room!")

        user_stories = list(Story.objects.filter(userreadstory__user=user, live_date=today).distinct())
        if not user_stories:
            raise MatchServiceError("There are no user read stories for today! add some?")

        user_likes = liked_story_ids(
            [
                {
                    "id": story.id,
                    "interested": UserReadStory.objects.filter(user=user, story=story)
                    .values_list("interested", flat=True)
                    .last(),
                }
                for story in user_stories
            ]
        )

        other_rooms = list(Room.objects.select_for_update().exclude(user=user).select_related("user"))
        candidates = []
        for room in other_rooms:
            likes = liked_story_ids(
                [
                    {
                        "id": story.id,
                        "interested": UserReadStory.objects.filter(user=room.user, story=story)
                        .values_list("interested", flat=True)
                        .last(),
                    }
                    for story in user_stories
                ]
            )
            if likes:
                candidates.append(
                    Candidate(str(room.user_id), frozenset(int(i) for i in likes if i is not None))
                )

        story_id, matched_user_id = select_match(user_likes, candidates, rng=rng)
        if not matched_user_id or not story_id:
            raise MatchServiceError("There are no users to match with at the moment!")

        matched_user = User.objects.select_for_update().get(pk=matched_user_id)
        voice = get_voice_provider()
        match = Match.objects.create(
            caller=matched_user,
            caller_access_token=voice.access_token(str(matched_user.pk)),
            receiver=user,
            receiver_access_token=voice.access_token(str(user.pk)),
            matched_story_id=story_id,
        )
        MatchActivity.objects.create(
            caller=matched_user,
            caller_access_token=match.caller_access_token,
            receiver=user,
            receiver_access_token=match.receiver_access_token,
            matched_story_id=story_id,
        )
        Room.objects.filter(user__in=[user, matched_user]).delete()
        logger.info(
            "match.created",
            extra={"user_id": str(user.pk), "match_id": match.pk, "peer_id": str(matched_user.pk)},
        )
        return match


def delete_match_for(user) -> bool:
    deleted, _ = Match.objects.filter(Q(caller=user) | Q(receiver=user)).delete()
    return deleted > 0


def user_can_see_match(user, match: Match) -> bool:
    return match.caller_id == user.pk or match.receiver_id == user.pk
