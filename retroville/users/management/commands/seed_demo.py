from datetime import date

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from retroville.matching.models import Room
from retroville.providers.news import FakeNewsProvider
from retroville.stories.models import Story, UserReadStory

User = get_user_model()


class Command(BaseCommand):
    help = "Load synthetic demo users, stories and a waiting room. No paid APIs."

    def handle(self, *args, **options):
        owner, _ = User.objects.get_or_create(
            email="owner@example.com",
            defaults={"country_code": "44", "phone_number": "7700000001"},
        )
        if not owner.has_usable_password():
            owner.set_password("password123")
            owner.is_staff = True
            owner.is_superuser = True
            owner.save()

        peer, created = User.objects.get_or_create(
            email="peer@example.com",
            defaults={"country_code": "44", "phone_number": "7700000002"},
        )
        if created:
            peer.set_password("password123")
            peer.save()

        today = date.today()
        for headline in FakeNewsProvider().fetch_headlines(today):
            story, _ = Story.objects.get_or_create(
                title=headline.title,
                live_date=headline.live_date,
                defaults={"content": headline.content, "picture_url": headline.picture_url},
            )
            UserReadStory.objects.get_or_create(user=owner, story=story, defaults={"interested": True})
            UserReadStory.objects.get_or_create(user=peer, story=story, defaults={"interested": True})

        Room.objects.get_or_create(user=owner)
        Room.objects.get_or_create(user=peer)
        self.stdout.write(self.style.SUCCESS("Demo data ready. Log in as owner@example.com / password123"))
