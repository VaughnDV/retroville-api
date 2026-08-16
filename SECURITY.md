# Security policy

If you find a vulnerability in this showcase repository, email the maintainer
at the address in `docs/ownership.md`. Do not open a public issue for
credential leaks or remote-code-execution reports.

## Supported versions

Only the `modernise/showcase` branch is maintained. The 2019 `master` history
is kept for provenance and is not a supported runtime.

## Reporting

Include the affected path, a reproduction against the local Compose stack, and
whether production-like secrets were involved. We will acknowledge reports
within a week.

## Secrets

Never commit `.env` files, Redis dumps, or provider keys. Use `.env.example`.
Historical secrets are listed in `docs/security/secrets-audit.md` and must be
rotated at the provider.
