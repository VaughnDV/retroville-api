from __future__ import absolute_import, unicode_literals
# from celery import shared_task
import random

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
    match["story"] = serialise_data(Story.objects.get(id=match["matched_story"]))
    match["caller"] = serialise_data(User.objects.get(id=match["caller"]))
    match["receiver"] = serialise_data(User.objects.get(id=match["receiver"]))
    return match


def structure_user_data(user, user_stories):
    serialised_user_stories = []
    for i in user_stories:
        s = serialise_data(i)
        s["interested"] = UserReadStory.objects.filter(user=user, story=i.id).last().interested
        serialised_user_stories.append(s)

    return {
        "user": {
            "detail": serialise_data(user),
            "stories": serialised_user_stories
        }
    }


def structure_other_users_data(user_stories, other_users_in_room):
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
    return comparison_data


def structure_user_likes(user_data):
    user_likes = list()
    for j in range(len(user_data['user']['stories'])):

        if user_data['user']['stories'][j]['interested']:
            user_likes.append(user_data['user']['stories'][j]['id'])
        else:
            continue
    return user_likes


def match_algorythim(comparison_data, user_likes):
    coeff = 0
    matched_user = None
    matched_story = None

    for i in range(len(comparison_data)):

        temp_likes = list()
        for j in range(len(comparison_data[i]['user']['stories'])):
            if comparison_data[i]['user']['stories'][j]['interested']:
                temp_likes.append(comparison_data[i]['user']['stories'][j]['id'])
            else:
                continue

        intersection = list(set(temp_likes) & set(user_likes))
        union = list(set(temp_likes + user_likes))

        coeff_new = len(intersection) / len(union)
        if (coeff_new > coeff):
            matched_user = comparison_data[i]['user']['detail']['id']
            matched_story = random.sample(intersection, 1)
            coeff = coeff_new
            user_no = i

    return matched_story[0] if matched_story else None, \
        matched_user if matched_story else None


def find_match(user, user_stories):

    user_data = structure_user_data(user, user_stories)

    user_likes = structure_user_likes(user_data)

    other_users_in_room = Room.objects.exclude(user=user)

    if not other_users_in_room:
        {"Message": "No other users in room!"}

    comparison_data = structure_other_users_data(user_stories, other_users_in_room)

    if not comparison_data:
        {"Message": "No stories read by other users!"}

    return match_algorythim(comparison_data, user_likes)


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

    match = Match.objects.create(
        caller_id=matched_user,
        caller_access_token=generate_token(matched_user),
        receiver_id=user.id,
        receiver_access_token=generate_token(str(user.id)),
        matched_story_id=matched_story
    )

    activity = MatchActivity.objects.create(
        caller_id=matched_user,
        caller_access_token=generate_token(matched_user),
        receiver_id=user.id,
        receiver_access_token=generate_token(str(user.id)),
        matched_story_id=matched_story
    )

    if not Match.objects.filter(id=match.id).exists():
        return {"Message": "Match not created"}

    if not MatchActivity.objects.filter(id=activity.id).exists():

        return {"Message": "Match Activity not created"}

    data = fetch_detail(serialise_data(match))
    user_in_room.delete()
    if not Room.objects.filter(user_id=str(user.id)).exists():
        Room.objects.filter(user_id=str(user.id)).delete()

    matched_user_in_room = Room.objects.filter(user_id=matched_user)
    matched_user_in_room.delete()
    if Room.objects.filter(user_id=matched_user).exists():
        Room.objects.filter(user_id=matched_user).delete()

    return data
