from __future__ import absolute_import, unicode_literals
# from celery import shared_task
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Match, MatchActivity , Room
from retroville.stories.models import UserReadStory, Story
from retroville.voice.tasks import generate_token
from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist
import json
from datetime import date


User = get_user_model()
NON_RETURN_FIELDS = ["password", "is_superuser", "is_staff", "groups", "user_permissions"]


def serialise_data(data):
    serialized_data = serialize('json', [data, ])
    json_data = json.loads(serialized_data)[0]
    data = {"id": json_data['pk']}
    for field in json_data["fields"].items():
        if field[0] not in NON_RETURN_FIELDS:
            data.update({field[0]: field[1]})
    return data


def fetch_detail(match):
    match["matched_story"] = serialise_data(Story.objects.get(id=match["matched_story"]))
    match["caller"] = serialise_data(User.objects.get(id=match["caller"]))
    match["receiver"] = serialise_data(User.objects.get(id=match["receiver"]))
    return match


# @shared_task
def match_maker(user_id):
    # Get user
    user = User.objects.get(pk=user_id)

    # Check to see if user is in the matched table
    if Match.objects.filter(Q(caller=user) | Q(receiver=user)).exists():
        match = Match.objects.filter(Q(caller=user) | Q(receiver=user)).first()
        return fetch_detail(serialise_data(match))

    try:
        user_in_room = Room.objects.get(user=user)
    except ObjectDoesNotExist:
        return {"Message": "Current user not in room!"}

    user_stories = Story.objects.filter(
        userreadstory__user=user,
        userreadstory__interested=True,
        live_date=date.today().strftime("%Y-%m-%d")
    )

    if not user_stories:
        return {"Message": "There are no user read stories for today! add some?"}

    matched_story = None
    matched_user = None

    # Get all users in room

    other_users_in_room = Room.objects.exclude(user=user)
    if not other_users_in_room:
        {"Message": "No other users in room!"}

    for other in other_users_in_room:
        for story in user_stories:
            try:
                other_interested = UserReadStory.objects.get(
                    user_id=str(other.user.id),
                    story=story,
                    interested=True
                )
                if other_interested:
                    matched_story = story
                    matched_user = User.objects.get(pk=other.user.id)
            except ObjectDoesNotExist:
                continue

    if not matched_user or not matched_story:
        return {"Message": "Currently no one is interested in the same stories"}

    # Create match with current user
    match = Match.objects.create(
        caller=user,
        caller_access_token=generate_token(str(user.id)),
        receiver=matched_user,
        receiver_access_token=generate_token(str(matched_user.id)),
        matched_story=matched_story
    )

    # Record the match in the activity
    activity = MatchActivity.objects.create(
        caller=user,
        caller_access_token=generate_token(str(user.id)),
        receiver=matched_user,
        receiver_access_token=generate_token(str(matched_user.id)),
        matched_story=matched_story
    )

    if not Match.objects.filter(id=match.id).exists():
        return {"Message": "Match not created"}

    if not MatchActivity.objects.filter(id=activity.id).exists():
        return {"Message": "Match Activity not created"}

    data = fetch_detail(serialise_data(match))
    user_in_room.delete()
    if not Room.objects.filter(user=user).exists():
        Room.objects.filter(user_id=str(user.id)).delete()

    matched_user_in_room = Room.objects.filter(user=matched_user)
    matched_user_in_room.delete()
    if Room.objects.filter(user=matched_user.id).exists():
        Room.objects.filter(user=matched_user.id).delete()

    return data
