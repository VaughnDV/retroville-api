"""Celery wrappers. Domain work lives in services/providers; these tasks are retry-safe."""

from __future__ import annotations

import logging
from datetime import date

from django.utils import timezone

from celery import shared_task
from retroville.matching.services import MatchServiceError, request_match
from retroville.providers.news import get_news_provider
from retroville.stories.models import Story

logger = logging.getLogger(__name__)


class TransientProviderError(Exception):
    """Retryable provider/network failure."""


@shared_task(
    bind=True,
    acks_late=True,
    autoretry_for=(TransientProviderError,),
    retry_backoff=True,
    retry_backoff_max=300,
    retry_kwargs={"max_retries": 5},
)
def ingest_daily_stories(self, live_on: str | None = None) -> dict:
    """Create today's stories once. Duplicate deliveries are no-ops."""
    target = date.fromisoformat(live_on) if live_on else timezone.now().date()
    existing = Story.objects.filter(live_date=target).count()
    if existing >= 10:
        logger.info("stories.ingest.skipped", extra={"live_on": target.isoformat(), "count": existing})
        return {"created": 0, "skipped": existing, "live_on": target.isoformat()}

    try:
        headlines = get_news_provider().fetch_headlines(target)
    except Exception as exc:
        raise TransientProviderError(str(exc)) from exc

    created = 0
    for headline in headlines:
        _, was_created = Story.objects.get_or_create(
            title=headline.title,
            live_date=headline.live_date,
            defaults={"content": headline.content, "picture_url": headline.picture_url},
        )
        created += int(was_created)
    return {"created": created, "skipped": existing, "live_on": target.isoformat()}


@shared_task(
    bind=True,
    acks_late=True,
    autoretry_for=(TransientProviderError,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
)
def create_match_for_user(self, user_id: str) -> dict:
    """Idempotent match creation. A second delivery returns the existing match."""
    from django.contrib.auth import get_user_model

    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
        match = request_match(user)
    except User.DoesNotExist:
        return {"status": "missing_user", "user_id": user_id}
    except MatchServiceError as exc:
        return {"status": "unmatched", "message": exc.message, "user_id": user_id}
    return {"status": "matched", "match_id": match.pk, "user_id": user_id}
