from datetime import date

import factory
from django.contrib.auth import get_user_model

from retroville.matching.models import Room
from retroville.stories.models import Story, UserReadStory

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    date_of_birth = date(1950, 1, 1)
    country_code = "44"
    phone_number = factory.Sequence(lambda n: f"77000000{n:02d}")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop("password", "password123")
        user = model_class.objects.create_user(password=password, **kwargs)
        return user


class StoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Story

    title = factory.Sequence(lambda n: f"Story {n}")
    content = factory.Sequence(lambda n: f"Content {n}")
    picture_url = "/static/demo/story-1.svg"
    live_date = factory.LazyFunction(date.today)


class UserReadStoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserReadStory

    user = factory.SubFactory(UserFactory)
    story = factory.SubFactory(StoryFactory)
    interested = True


class WaitingRoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Room

    user = factory.SubFactory(UserFactory)
