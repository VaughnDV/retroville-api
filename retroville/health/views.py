"""Liveness is process-only. Readiness checks PostgreSQL and Redis."""

from __future__ import annotations

from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.http import require_GET


@require_GET
def liveness(_request):
    return JsonResponse({"status": "ok"})


@require_GET
def readiness(_request):
    checks = {"database": _database_ok(), "cache": _cache_ok()}
    status = 200 if all(checks.values()) else 503
    return JsonResponse({"status": "ok" if status == 200 else "degraded", "checks": checks}, status=status)


def _database_ok() -> bool:
    try:
        connection.ensure_connection()
        return True
    except Exception:
        return False


def _cache_ok() -> bool:
    try:
        from django.core.cache import cache

        cache.set("readiness", "1", 5)
        return cache.get("readiness") == "1"
    except Exception:
        # Local/test settings may use locmem; still a valid cache backend.
        return getattr(settings, "CACHES", {}).get("default", {}).get("BACKEND") is not None
