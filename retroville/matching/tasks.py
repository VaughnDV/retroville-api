from __future__ import absolute_import, unicode_literals
# from celery import shared_task
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Match, MatchActivity, Room
from retroville.stories.models import UserReadStory, Story
from retroville.voice.tasks import generate_token
from django.core.serializers import serialize
from django.core.exceptions import ObjectDoesNotExist
import json


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


def fetch_stories(match):
    match["caller_stories"] = []
    match["receiver_stories"] = []

    for story in Story.objects.filter(userreadstory__user_id=match["caller"]):
        s = serialise_data(story)
        interested = UserReadStory.objects.filter(user=match["caller"], story=story).first()
        s.update({"interested": interested.interested})
        match["caller_stories"].append(s)

    for story in Story.objects.filter(userreadstory__user_id=match["receiver"]):
        s = serialise_data(story)
        interested = UserReadStory.objects.filter(user=match["receiver"], story=story).first()
        s.update({"interested": interested.interested})
        match["receiver_stories"].append(s)

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
        return fetch_stories(serialise_data(match))

    try:
        user_in_room = Room.objects.get(user=user)
    except ObjectDoesNotExist:
        return {"Message": "Current user not in room!"}

    # Get all users in room
    other_users_in_room = Room.objects.exclude(user=user)

    # Check if users are in the room/
    # Get the first user in room
    try:
        other_user_in_room = other_users_in_room[0]
    except IndexError:
        return {"Message": "No other users in room!"}

    # get the other users info
    other_user = User.objects.get(id=other_user_in_room.user.id)

    # Create match with current user
    match = Match.objects.create(
        caller=user,
        caller_access_token=generate_token(str(user.id)),
        receiver=other_user,
        receiver_access_token=generate_token(str(other_user.id))
    )

    match.save()

    # Record the match in the activity
    activity = MatchActivity.objects.create(
        caller=user,
        caller_access_token=generate_token(str(user.id)),
        receiver=other_user,
        receiver_access_token=generate_token(str(other_user.id))
    )

    activity.save()

    # Delete both users from the room
    user_in_room.delete()
    other_user_in_room.delete()

    return fetch_stories(serialise_data(match))
