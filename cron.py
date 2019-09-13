from apscheduler.schedulers.blocking import BlockingScheduler
import sys
import os
import django
from datetime import date
import requests
import json
from pprint import pprint


sched = BlockingScheduler()


# @sched.scheduled_job('cron', day_of_week='mon-sun', hour=00)
@sched.scheduled_job('interval', minutes=0.5)
def fetch_stories():
    url = "https://newsapi.org/v2/top-headlines"
    checked = []
    catagories = ["business", "business", "health", "health", "technology", "science", "sports", "entertainment", "general", "general"]

    for catagory in catagories:

        request_url = f"{url}?country={COUNTRY}&category={catagory}&sortBy=popularity&language={LANGUAGE}&apiKey={NEWS_API_KEY}"
        pprint(request_url)

        title = None
        content = None
        index = checked.count(f"{catagory}")

        while not content and not title:
            response = requests.get(request_url)
            articles = json.loads(response.content)["articles"]
            title = articles[index][f"title"]
            content = articles[index]["description"]
            picture_url = articles[index]["urlToImage"]
            live_date = date.today().strftime("%Y-%m-%d")

        Story.objects.create(
            title=title,
            content=content,
            picture_url=picture_url,
            live_date=live_date
        )
        checked.append(catagory)


if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault("DJANGO_CONFIGURATION", "Local")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "retroville.config")
    COUNTRY = os.environ.get("COUNTRY", "gb")
    LANGUAGE = os.environ.get("LANGUAGE", "en")
    NEWS_API_KEY = os.environ.get("NEWS_API_KETY", "c5c5322336d54e079ba396b59d850e52")
    import configurations
    configurations.setup()
    from retroville.stories.models import Story
    django.setup()
    fetch_stories()
