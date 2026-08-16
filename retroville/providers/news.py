from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Protocol


@dataclass(frozen=True)
class Headline:
    title: str
    content: str
    picture_url: str
    live_date: date


class NewsProvider(Protocol):
    def fetch_headlines(self, live_on: date) -> list[Headline]: ...


class FakeNewsProvider:
    def fetch_headlines(self, live_on: date) -> list[Headline]:
        return [
            Headline(
                title=f"Demo story {index} for {live_on.isoformat()}",
                content=f"Synthetic headline {index} for the offline demo.",
                picture_url=f"/static/demo/story-{index}.svg",
                live_date=live_on,
            )
            for index in range(1, 11)
        ]


class NewsApiProvider:
    def __init__(self, api_key: str, country: str = "gb", language: str = "en"):
        self.api_key = api_key
        self.country = country
        self.language = language

    def fetch_headlines(self, live_on: date) -> list[Headline]:
        import requests

        categories = [
            "business",
            "health",
            "technology",
            "science",
            "sports",
            "entertainment",
            "general",
        ]
        headlines: list[Headline] = []
        for category in categories:
            response = requests.get(
                "https://newsapi.org/v2/top-headlines",
                params={
                    "country": self.country,
                    "category": category,
                    "language": self.language,
                    "apiKey": self.api_key,
                },
                timeout=10,
            )
            response.raise_for_status()
            for article in response.json().get("articles", []):
                if article.get("title") and article.get("url"):
                    headlines.append(
                        Headline(
                            title=article["title"],
                            content=article.get("description") or article["url"],
                            picture_url=article.get("urlToImage") or "",
                            live_date=live_on,
                        )
                    )
                if len(headlines) >= 10:
                    return headlines
        return headlines


def get_news_provider() -> NewsProvider:
    from django.conf import settings

    if getattr(settings, "PROVIDERS_USE_FAKES", True) or not settings.NEWS_API_KEY:
        return FakeNewsProvider()
    return NewsApiProvider(settings.NEWS_API_KEY, settings.NEWS_COUNTRY, settings.NEWS_LANGUAGE)
