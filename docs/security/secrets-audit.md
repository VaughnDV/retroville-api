# Secrets and sensitive-data audit

Scanned after a local `git-filter-repo` rewrite on 2026-08-16.

## History rewrite (local)

`dump.rdb` and `.travis.yml` were removed from every revision. The News API key
and mailbox password were replaced with placeholders. Author names and commit
dates were preserved.

A recoverable backup is at:

`/Users/vaughn/Projects/retroville-api-backup-20260816.bundle`

GitHub still has the pre-rewrite objects until every rewritten branch is
force-pushed. Do not change repository visibility before that.

## Current tree

| Finding | Action |
| --- | --- |
| Redis dump | Gone from tree and history |
| Travis encrypted Heroku token | `.travis.yml` gone from tree and history |
| News API key | Replaced with `NEWSAPI_KEY_REDACTED` throughout history |
| Mailbox password | Replaced with `REDACTED` throughout history |
| Personal emails in old seed scripts | Still present in history (not tokens; not rewritten) |

## Rotation checklist

History rewrite does not un-leak a credential. Rotate at the provider even
though the Git objects are now clean locally.

- [ ] Revoke/rotate any Heroku auth token that may have been encrypted for Travis
- [ ] Rotate the News API key that used to be hard-coded in `scripts/fetch_stories_for_today.py`
- [ ] Rotate the mailbox password that used to appear in `retroville/config/local.py`
- [ ] Confirm Twilio, AWS and Authy credentials from 2019 are revoked
- [ ] Force-push rewritten branches only after reviewing this backup
- [ ] Keep the GitHub repository private until this list is complete
