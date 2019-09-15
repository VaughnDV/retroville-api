from apscheduler.schedulers.blocking import BlockingScheduler
import sys
import os
import django
from datetime import date
import requests
import json

sched = BlockingScheduler()

def fetch_stories():
    url = "https://newsapi.org/v2/top-headlines"
    checked = []
    checked_titles = []
    categories = ["business", "business", "health", "health", "technology", "science", "sports", "entertainment", "general", "general"]
    count = 0
    while count <= 10:
        for category in categories:
            try:
                request_url = f"{url}?country={COUNTRY}&category={category}&sortBy=popularity&language={LANGUAGE}&apiKey={NEWS_API_KEY}"
                title = None
                content = None
                limit = 10
                index = checked.count(f"{category}")

                response = requests.get(request_url)

                if not response.ok:
                    print(response.reason)
                    print(response.status_code)
                    continue

                articles = json.loads(response.content).get("articles", "")

                if not articles:
                    print(json.loads(response.content)["message"])
                    continue

                while not title and not content and limit > 0:
                    if articles[index]["title"] and articles[index]["title"] not in checked_titles:
                        if articles[index]["url"]:
                            title = articles[index]["title"]
                            checked_titles.append(title)
                            content = articles[index]["url"]
                            limit -= 1

                picture_url = articles[index]["urlToImage"]
                live_date = date.today().strftime("%Y-%m-%d")

                Story.objects.create(
                    title=title,
                    content=content,
                    picture_url=picture_url,
                    live_date=live_date
                )
                checked.append(category)
                count += 1

            except Exception as e:
                print(e)
                continue


if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault("DJANGO_CONFIGURATION", "Local")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "retroville.config")
    COUNTRY = os.environ.get("COUNTRY", "gb")
    LANGUAGE = os.environ.get("LANGUAGE", "en")
    NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
    import configurations
    configurations.setup()
    from retroville.stories.models import Story
    django.setup()
    fetch_stories()
