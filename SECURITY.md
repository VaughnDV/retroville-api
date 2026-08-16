# Security policy

This repository is a completed 2019-to-2026 engineering showcase and is **not
maintained**. There are no supported versions.

If you find a credential leak or a serious vulnerability, email the address in
`docs/ownership.md`. Do not open a public issue for that class of report.

## Secrets

Never commit `.env` files, Redis dumps, or provider keys. Use `.env.example`.
Historical secrets were rewritten out of Git and revoked at the original
providers; see `docs/security/secrets-audit.md`.
