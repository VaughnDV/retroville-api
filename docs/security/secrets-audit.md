# Secrets and sensitive-data audit

Scanned: working tree on `modernise/showcase` and every Git revision reachable
from `master` as of 2026-08-16.

## Findings removed from the current tree

| Finding | Location | Action |
| --- | --- | --- |
| Redis dump | `dump.rdb` | Deleted from the working tree and ignored. File is 92 bytes; treated as production-adjacent data. |
| Travis encrypted Heroku deploy token | `.travis.yml` `env.global.secure` | File removed. Treat the ciphertext as a secret until the underlying Heroku token is rotated/revoked. |
| Hard-coded News API key | `scripts/fetch_stories_for_today.py` | Key removed. **Rotate the News API key** `NEWSAPI_KEY_REDACTED` if it was ever valid. |
| Commented Gmail password | `retroville/config/local.py` | Credential removed. **Rotate that mailbox password** if it was ever used. |
| Personal emails in seed/admin config | dummy-data script, `ADMINS` | Replaced with synthetic `@example.com` addresses. |
| Heroku app names and deploy flow | `.travis.yml`, README, `docs/index.md` | Obsolete deploy config removed from the current tree. |

## Postman collection

`retroville.postman_collection.json` used `{{token}}` placeholders and dummy
`access_token` values (`FRIENDLY`, `DFGDFGDFG`). No live credentials were found.
Payloads were rewritten to explicit placeholders.

## Still present in Git history

History rewrite was **not** applied in this commit. The 2019 author dates are
part of the portfolio value. A recoverable backup is required before rewriting.

Known historical remnants:

- `dump.rdb` blob from commit `ebb999f`
- Travis encrypted deploy value
- News API key default
- Commented mailbox password
- Personal emails in seed scripts

See `docs/security/history-rewrite.md` for the backup-and-filter procedure.

## Rotation checklist

- [ ] Revoke/rotate any Heroku auth token that may have been encrypted for Travis
- [ ] Rotate the News API key that appeared in `scripts/fetch_stories_for_today.py`
- [ ] Rotate the mailbox password that appeared in `retroville/config/local.py`
- [ ] Confirm Twilio, AWS and Authy credentials from 2019 are revoked
- [ ] Keep the GitHub repository private until this list is complete
