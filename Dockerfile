FROM python:3.12.11-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

WORKDIR /build

RUN pip install --no-cache-dir poetry==2.1.3

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root

COPY retroville ./retroville
COPY manage.py ./
RUN poetry install --only main


FROM python:3.12.11-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=retroville.settings.production \
    PORT=8000

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system retroville \
    && useradd --system --gid retroville --home-dir /app --create-home retroville

WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY --chown=retroville:retroville manage.py wait_for_postgres.py ./
COPY --chown=retroville:retroville retroville ./retroville
COPY --chown=retroville:retroville templates ./templates

USER retroville
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health/live/')"

STOPSIGNAL SIGTERM

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "retroville.asgi:application"]
