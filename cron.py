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
    errors = []
    created_count = 0
    api_calls = 0
    response_statuses = []

    categories = ["business", "business", "health", "health", "technology", "science", "sports", "entertainment", "general", "general",]

    for category in categories:
        title = None
        content = None
        picture_url = None

        while created_count < 10:
            try:
                request_url = f"{url}?country={COUNTRY}&category={category}&sortBy=popularity&language={LANGUAGE}&apiKey={NEWS_API_KEY}"

                index = checked.count(f"{category}")
                checked.append(category)
                response = requests.get(request_url)
                api_calls += 1

                response_statuses.append(response.status_code)
                if not response.ok:
                    print(response.reason)
                    print(response.status_code)
                    continue

                articles = json.loads(response.content).get("articles", "")

                if not articles:
                    print(json.loads(response.content)["message"])
                    continue

                if articles[index]["title"] not in checked_titles:
                    if articles[index]["url"]:
                        title = articles[index]["title"]
                        content = articles[index]["url"]
                        picture_url = articles[index]["urlToImage"]

                if title and content and picture_url:
                    Story.objects.create(
                        title=title,
                        content=content,
                        picture_url=picture_url,
                        live_date=date.today().strftime("%Y-%m-%d")
                    )
                    created_count += 1
                    checked_titles.append(title)

            except Exception as e:
                errors.append(e)
                continue

    print(f"Total requests to News API: {api_calls}:")
    print(f"created_count: {created_count}")
    print(f"response_statuses: {response_statuses}")
    print("Created Titles:")
    for title in checked_titles:
        print(title)
    print("Errors:")
    for error in errors:
        print(error)



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
