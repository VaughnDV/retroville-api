"""Structured logging with request/job correlation and redaction."""

from __future__ import annotations

import json
import logging
import re
import uuid
from contextvars import ContextVar

from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin

correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="-")

_SECRET_KEYS = re.compile(
    r"(password|secret|token|authorization|api[_-]?key|account_sid)", re.I
)
_REDACTED = "***REDACTED***"


def get_correlation_id() -> str:
    return correlation_id_var.get()


class RequestContextMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest) -> None:
        incoming = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        correlation_id_var.set(incoming)
        request.correlation_id = incoming  # type: ignore[attr-defined]

    def process_response(self, request: HttpRequest, response: HttpResponse) -> HttpResponse:
        response["X-Request-ID"] = getattr(request, "correlation_id", get_correlation_id())
        return response


class RedactingJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": get_correlation_id(),
            "time": self.formatTime(record, self.datefmt),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(_redact(payload), default=str)


def _redact(value: object) -> object:
    if isinstance(value, dict):
        return {
            key: _REDACTED if _SECRET_KEYS.search(str(key)) else _redact(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_redact(item) for item in value]
    if isinstance(value, str) and "Bearer " in value:
        return _REDACTED
    return value
