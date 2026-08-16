# Retroville API

Spontaneous activity matching and real-time communication for people who liked the same daily stories.

Originally built in 2019, Retroville is a Django API for spontaneous activity matching and real-time communication. In 2026 it was recovered and modernised using characterisation tests, staged framework upgrades, secure configuration, retry-safe background jobs and contemporary CI while retaining its original Git history.

## Why this project is shown

This is not a greenfield demo. It is a 2019 production-style backend (DRF, PostgreSQL, Celery, Redis, Channels, Twilio) brought onto a currently supported stack without pretending it was always modern. The 2019 commits stay in history; the `modernise/showcase` branch is the maintained runtime.

What changed: Python 3.6 / Django 2.1 → Python 3.12 / Django 5.2 LTS, Poetry lockfile, provider fakes, transactional matching, health checks, GitHub Actions, and a multi-stage non-root image.

## Architecture

HTTP clients hit Django REST Framework. WebSocket clients hit Channels. PostgreSQL stores users, stories and matches. Redis is the cache, channel layer and Celery broker. Workers ingest daily stories and can create matches off the request path.

See [docs/architecture.md](docs/architecture.md) for the diagram and [docs/decisions/](docs/decisions/) for trade-offs.

## Quick start (offline demo)

No Twilio or News API keys are required.

```bash
cp .env.example .env
make compose-up
```

Then:

- API: http://127.0.0.1:8000/api/docs/
- Health: http://127.0.0.1:8000/health/live/ and `/health/ready/`
- Demo login: `owner@example.com` / `password123`

Example:

```bash
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api-token-auth/ \
  -H 'Content-Type: application/json' \
  -d '{"username":"owner@example.com","password":"password123"}' | jq -r .token)

curl -H "Authorization: Token $TOKEN" http://127.0.0.1:8000/api/v1/whoami/
curl -H "Authorization: Token $TOKEN" http://127.0.0.1:8000/api/v1/match/find/
```

OpenAPI: http://127.0.0.1:8000/api/schema/

## Quality commands

```bash
make install          # Poetry + pre-commit
make lint             # Ruff
make typecheck        # mypy on the new modules
make test             # unit + characterisation, no network
make test-integration # PostgreSQL / Redis / Channels
make audit            # pip-audit
make docs             # MkDocs
```

## Limitations and status

- Matching story selection is still sampled from the Jaccard intersection, as in 2019.
- Chat does not replay missed messages after reconnect.
- Voice calling against live Twilio is optional; the demo mints fake tokens.
- Historical Git blobs still contain old secrets until the playbook in
  `docs/security/history-rewrite.md` is run against a backup.
- Keep the GitHub repository **private** until that audit is complete.

Licence: MIT. See `SECURITY.md` for reporting.
