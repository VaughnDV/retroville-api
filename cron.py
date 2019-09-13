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
# @sched.scheduled_job('interval', minutes=1)
def fetch_stories():
    print("#" * 50)
    print(date.today())
    print("#" * 50)
    url = "https://newsapi.org/v2/top-headlines"
    checked = []
    checked_titles = []
    catagories = ["business", "business", "health", "health", "technology", "science", "sports", "entertainment", "general", "general"]

    for catagory in catagories:

        request_url = f"{url}?country={COUNTRY}&category={catagory}&sortBy=popularity&language={LANGUAGE}&apiKey={NEWS_API_KEY}"
        print(request_url)
        print("#" * 50)

        title = None
        content = None
        # index = checked.count(f"{catagory}")

        response = requests.get(request_url)
        pprint(response.content)

        articles = json.loads(response.content)["articles"]

        for artitle in articles:
            if artitle["title"] and artitle["title"] not in checked_titles:
                title = artitle["title"]
            else:
                continue
            if artitle["content"]:
                content = artitle["content"].rstrip()
            else:
                continue
            picture_url = artitle["urlToImage"]
            live_date = date.today().strftime("%Y-%m-%d")
    #
    #     Story.objects.create(
    #         title=title,
    #         content=content,
    #         picture_url=picture_url,
    #         live_date=live_date
    #     )
    #     checked.append(catagory)


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
