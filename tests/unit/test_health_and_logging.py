import json
import logging

import pytest
from django.test import RequestFactory

from retroville.health.views import liveness, readiness
from retroville.observability import RedactingJsonFormatter, RequestContextMiddleware


def test_liveness_does_not_touch_dependencies(rf):
    response = liveness(rf.get("/health/live/"))
    assert response.status_code == 200
    assert json.loads(response.content)["status"] == "ok"


@pytest.mark.django_db
def test_readiness_reports_checks(rf):
    response = readiness(rf.get("/health/ready/"))
    payload = json.loads(response.content)
    assert "database" in payload["checks"]
    assert "cache" in payload["checks"]


def test_log_formatter_redacts_secrets():
    formatter = RedactingJsonFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="ok",
        args=(),
        exc_info=None,
    )
    payload = json.loads(formatter.format(record))
    assert payload["correlation_id"]
    redacted = formatter.format  # noqa: F841
    assert "***REDACTED***" in json.dumps(
        __import__("retroville.observability", fromlist=["_redact"])._redact(
            {"password": "secret", "token": "abc", "ok": "yes"}
        )
    )


def test_request_id_header_round_trip():
    factory = RequestFactory()
    request = factory.get("/health/live/", HTTP_X_REQUEST_ID="abc-123")
    middleware = RequestContextMiddleware(lambda req: liveness(req))
    response = middleware(request)
    assert response["X-Request-ID"] == "abc-123"
