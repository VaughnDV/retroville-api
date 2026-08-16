# ADR 0002: Provider fakes and fail-closed production settings

## Status

Accepted

## Context

The 2019 tree mixed Twilio, Authy, News API and Gmail credentials into views
and commented settings. Tests could not run without network access.

## Decision

- Third-party systems are accessed through small protocols in
  `retroville/providers/`.
- Local and test settings set `PROVIDERS_USE_FAKES = True`.
- Production settings raise `ImproperlyConfigured` if `DJANGO_SECRET_KEY`,
  `DATABASE_URL`, `REDIS_URL` or `DJANGO_ALLOWED_HOSTS` are missing.

## Consequences

The default demo and CI never call paid APIs. A production deploy must supply
real secrets explicitly.
