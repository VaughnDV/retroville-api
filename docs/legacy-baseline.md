# 2019 legacy baseline

Recorded from the last production-era commit `e9f645a` (17 Sep 2019) before the
2026 showcase modernisation.

## Runtime

| Component | Version in 2019 tree | Notes |
| --- | --- | --- |
| Python | 3.6 (Travis + `Dockerfile`) | EOL 23 Dec 2021 |
| Django | 2.1.9 | EOL December 2019; 2.2 LTS was already the supported line |
| Django REST Framework | 3.9.1 | |
| PostgreSQL | 9.6 (`docker-compose.yml`) | EOL 11 Nov 2021 |
| Redis | unpinned `redis:latest`, commented out of Compose | Used for Channels and intended Celery broker |
| Celery | unpinned | Worker wiring is present; matching ran synchronously in-request |
| Channels | present, commented out of `INSTALLED_APPS` | WebSocket consumer exists but was not enabled |
| Gunicorn | 19.9.0 | |
| psycopg2-binary | 2.7.7 | |
| Twilio | `twilio==6.*`, `authy==2.2.3` | Voice tokens + SMS verification |
| boto3 / django-storages | 1.9.93 / 1.7.1 | S3 media in production settings |
| Test runner | pytest + pytest-django + mixer/factory-boy | `./manage.py test` via a pytest runner |

## Application shape

- Cookiecutter Django REST skeleton with `django-configurations` (`Local` / `Production`)
- Email-as-username user model with DRF token auth
- Daily “stories”, a waiting room, Jaccard-style interest matching, Twilio voice tokens
- Celery, cron/APScheduler story ingest, and Channels chat were partially wired
- Deployed to Heroku container registry from Travis on `master` and `qa`

## Historical test suite

Existing tests live under `retroville/tests/` and cover:

- URL reverse for `/ping/`
- Django mail outbox
- Match model mixer smoke test
- Matching and room view characterisation (happy path + a few empty-room cases)

They hit Twilio token generation, use `RequestFactory` without DRF authentication
context, and depend on `random` for story interest. Known failures are recorded
in `docs/known-failures.md`.

## How to re-run the 2019 suite

```bash
docker compose -f docker-compose.legacy.yml run --rm legacy-tests
```

Python 3.6 images and several 2019 indexes are themselves end-of-life. Treat
that Compose file as a museum piece: if it cannot be built, use the recorded
result in `docs/legacy-test-run.md` rather than changing historical pins.
