import sys
import os
import django
import string
import random
import time
from datetime import date


def random_date(start, end):
    stime = time.mktime(time.strptime(start, '%Y-%m-%d'))
    etime = time.mktime(time.strptime(end, '%Y-%m-%d'))
    ptime = stime + random.random() * (etime - stime)
    return time.strftime('%Y-%m-%d', time.localtime(ptime))


def random_name(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def main():

    stories = []
    users = []

    try:
        vaughn = User.objects.create_superuser(
            email="vaughndevilliers@gmail.com",
            password="password123"
        )
        erim = User.objects.create_superuser(
            email="erimfranci@gmail.com",
            password="password123"
        )
        users.append(vaughn)
        users.append(erim)
    except Exception:
        print("Super users not created")
        pass

    for i in range(10):
        name = random_name()
        email = f'{name}@jumanji-hq.com'
        password = name
        user = User.objects.create_user(
            email=email,
            password=password,
            date_of_birth=random_date("1920-01-01", "1970-01-01")
        )

        title = f"Title {random_name()}"
        content = f"Content for  {title}"
        picture_url = "https://loremflickr.com/640/480/beach,holiday,old/all"
        live_date = random_date(
            date.today().strftime("%Y-%m-%d"),
            date.today().strftime("%Y-%m-%d")
        )
        story = Story.objects.create(
            title=title,
            content=content,
            picture_url=picture_url,
            live_date=live_date
        )

        story.save()
        stories.append(story)

    for user in User.objects.all():
        for story in stories:
            UserReadStory.objects.create(
                user=user,
                story=story,
                interested=random.choice([True, False])
            )


if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault("DJANGO_CONFIGURATION", "Local")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "retroville.config")
    import configurations
    configurations.setup()
    from retroville.users.models import User
    from retroville.stories.models import Story
    from retroville.stories.models import UserReadStory
    django.setup()
    main()
