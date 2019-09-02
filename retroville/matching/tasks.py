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
import uuid


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


def find_match(user, user_stories):

    matched_story = None
    matched_user = None

    other_users_in_room = Room.objects.exclude(user=user)
    if not other_users_in_room:
        {"Message": "No other users in room!"}

    comparison_data = []

    for other in other_users_in_room:
        others_stories = []
        for story in user_stories:
            try:
                s = serialise_data(story)
                s["interested"] = UserReadStory.objects.filter(user_id=other.user.id, story=story.id).last().interested

                others_stories.append(s)

            except ObjectDoesNotExist:
                continue
            except AttributeError:
                continue

        comparison_data.append({
            "user": {
                "detail": serialise_data(User.objects.get(pk=other.user.id)),
                "stories": others_stories
                }
            }
        )

    serialised_user_stories = []
    for i in user_stories:
        s = serialise_data(i)
        s["interested"] = UserReadStory.objects.filter(user=user, story=i.id).last().interested
        serialised_user_stories.append(s)

    user_data = {
        "user": {
            "detail": serialise_data(user),
            "stories": serialised_user_stories
        }
    }

    # print("#" * 50)
    # print("#" * 50)
    # print("#" * 50)
    # from pprint import pprint
    # pprint(comparison_data)
    # print("#" * 50)
    # pprint(user_data)
    # print("#" * 50)
    # print("#" * 50)
    # print("#" * 50)

    try:
        matched_story = Story.objects.get(id=user_stories[0].id)
        matched_user = User.objects.get(pk=other_users_in_room[0].user_id)
    except IndexError:
        matched_story, matched_user = None, None

    return matched_story, matched_user


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
        live_date=date.today().strftime("%Y-%m-%d")
    )
    if not user_stories:

        return {"Message": "There are no user read stories for today! add some?"}

    matched_story,  matched_user = find_match(user, user_stories)

    if not matched_user or not matched_story:
        return {"Message": "There are no users to match with at the moment!"}

    # Create match with current user
    print("#" * 50)
    print("#" * 50)
    print("#" * 50)
    print(type(matched_story))
    print(matched_story)
    print(matched_story.pk)
    print("#" * 50)
    print(type(matched_user))
    print(matched_user)
    print(matched_user.pk)
    print("#" * 50)
    print("#" * 50)

    match = Match.objects.create(
        caller_id=user.id,
        caller_access_token=generate_token(str(user.id)),
        receiver_id=matched_user.id,
        receiver_access_token=generate_token(str(matched_user.id)),
        matched_story_id=matched_story.id
    )

    activity = MatchActivity.objects.create(
        caller_id=user.id,
        caller_access_token=generate_token(str(user.id)),
        receiver_id=matched_user.id,
        receiver_access_token=generate_token(str(matched_user.id)),
        matched_story_id=matched_story.id
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
