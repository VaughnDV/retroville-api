from datetime import datetime

import factory


class StoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "stories.Story"
        django_get_or_create = ("title",)

    id = factory.Faker("uuid4")
    title = factory.Sequence(lambda n: f"Test Title {n}")
    content = factory.Sequence(lambda n: f"Test Content {n}")
    picture_url = factory.Sequence(lambda n: f"Fake picture url {n}")
    live_date = factory.Sequence(f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day}")
