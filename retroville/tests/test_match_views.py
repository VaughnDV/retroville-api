from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.test import RequestFactory, Client
# from retroville.users.models import User
from retroville.stories.models import Story, UserReadStory
from retroville.matching.models import Match, MatchActivity, Room, RoomActivity
from retroville.matching.views import check_room, exit_room, list_room, enter_room, find_match, delete_match
from mixer.backend.django import mixer
import pytest
from django.db.models import Q
import json
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
import string
import random
import time

User = get_user_model()


def random_date(start, end):
    stime = time.mktime(time.strptime(start, '%Y-%m-%d'))
    etime = time.mktime(time.strptime(end, '%Y-%m-%d'))
    ptime = stime + random.random() * (etime - stime)
    return time.strftime('%Y-%m-%d', time.localtime(ptime))


def random_name(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class TestMatchAlgorithm(APITestCase):

    def setUp(self) -> None:
        self.client =Client()

        self.caller = User.objects.create_user(
            email="caller@jumanji.com",
            password="password123",
            date_of_birth=random_date("1920-01-01", "1970-01-01")
        )
        self.receiver = User.objects.create_user(
            email="receiver@jumanji.com",
            password="password123",
            date_of_birth=random_date("1920-01-01", "1970-01-01")
        )

        for n in range(10):
            name = random_name()
            email = f'{name}@jumanji-hq.com'
            password = name
            User.objects.create_user(
                email=email,
                password=password,
                date_of_birth=random_date("1920-01-01", "1970-01-01")
            )

            picture_url = "https://loremflickr.com/640/480/beach,holiday,old/all"
            live_date = random_date(
                date.today().strftime("%Y-%m-%d"),
                date.today().strftime("%Y-%m-%d")
            )

            live_date = random_date(
                date.today().strftime("%Y-%m-%d"),
                date.today().strftime("%Y-%m-%d")
            )

            random_string = random_name()
            Story.objects.create(
                title=f"Title {random_string}",
                content=f"Content for  {random_string}",
                picture_url=picture_url,
                live_date=live_date
            )

        stories = Story.objects.all()

        for u in User.objects.all():
            for s in Story.objects.all():
                UserReadStory.objects.create(
                    user=u,
                    story=s,
                    interested=random.choice([True, False])
                )
            Room.objects.create(
                user=u
            )

    def test_matching_algorithm_works(self):
        request = RequestFactory().get(reverse("find_match"))
        request.user = User.objects.all().first()
        response = find_match(request)
        assert response.status_code == 201


class TestMatchView(APITestCase):

    def setUp(self) -> None:
        self.client = Client()

        self.caller = User.objects.create_user(
            email="caller@jumanji.com",
            password="password123",
            date_of_birth=random_date("1920-01-01", "1970-01-01")
        )
        self.receiver = User.objects.create_user(
            email="receiver@jumanji.com",
            password="password123",
            date_of_birth=random_date("1920-01-01", "1970-01-01")
        )

        picture_url = "https://loremflickr.com/640/480/beach,holiday,old/all"
        live_date = random_date(
            date.today().strftime("%Y-%m-%d"),
            date.today().strftime("%Y-%m-%d")
        )

        random_string = random_name()
        self.story1 = Story.objects.create(
            title=f"Title {random_string}",
            content=f"Content for  {random_string}",
            picture_url=picture_url,
            live_date=live_date
        )

        random_string = random_name()
        self.story2 = Story.objects.create(
            title=f"Title {random_string}",
            content=f"Content for  {random_string}",
            picture_url=picture_url,
            live_date=live_date
        )
        random_string = random_name()
        self.story3 = Story.objects.create(
            title=f"Title {random_string}",
            content=f"Content for  {random_string}",
            picture_url=picture_url,
            live_date=live_date
        )
        for i, v in enumerate([True, False, False]):
            UserReadStory.objects.create(
                user=self.caller,
                story=eval(f"self.story{i + 1}"),
                interested=v
            )

        for i, v in enumerate([True, True, True]):
            UserReadStory.objects.create(
                user=self.receiver,
                story=eval(f"self.story{i + 1}"),
                interested=v
            )

    def test_match_is_created(self):
        Room.objects.create(
            user=self.caller
        )
        Room.objects.create(
            user=self.receiver
        )
        request = RequestFactory().get(reverse("find_match"))
        request.user = self.caller
        response = find_match(request)
        assert response.status_code == 204

    def test_no_user_users_to_match_with_no_other_user_in_room(self):
        Room.objects.create(
            user=self.caller
        )
        request = RequestFactory().get(reverse("find_match"))
        request.user = self.caller
        response = find_match(request)
        assert json.loads(response.content)["Message"] == 'There are no users to match with at the moment!'
        assert response.status_code == 204

    def test_user_not_in_room(self):
        Room.objects.create(
            user=self.receiver
        )
        request = RequestFactory().get(reverse("find_match"))
        request.user = self.caller
        response = find_match(request)
        assert json.loads(response.content)["Message"] == "Current user not in room!"
        assert response.status_code == 204

    def test_no_user_users_to_match_with_no_stories_read(self):
        Room.objects.create(
            user=self.caller
        )
        Room.objects.create(
            user=self.receiver
        )
        for item in UserReadStory.objects.filter(user=self.receiver):
            item.delete()

        request = RequestFactory().get(reverse("find_match"))
        request.user = self.caller
        response = find_match(request)
        assert json.loads(response.content)["Message"] == "There are no users to match with at the moment!"
        assert response.status_code == 204

    def test_match_is_created(self):
        Room.objects.create(
            user=self.caller
        )
        Room.objects.create(
            user=self.receiver
        )
        request = RequestFactory().get(reverse("find_match"))
        request.user = self.caller
        response = find_match(request)

        assert Match.objects.filter(caller=self.caller, receiver=self.receiver).exists()

    # def test_match_activity_is_created(self):
    #     Room.objects.create(
    #         user=self.caller
    #     )
    #     Room.objects.create(
    #         user=self.receiver
    #     )
    #     request = RequestFactory().get(reverse("find_match"))
    #     request.user = self.caller
    #     response = find_match(request)
    #
    #     assert MatchActivity.objects.filter(caller=self.caller, receiver=self.receiver).exists()
