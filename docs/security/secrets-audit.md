# Secrets and sensitive-data audit

Scanned after a local `git-filter-repo` rewrite on 2026-08-16.

## History rewrite

`dump.rdb` and `.travis.yml` were removed from every revision. The News API key
and mailbox password were replaced with placeholders. Author names and commit
dates were preserved. The local backup bundle was destroyed after the rewritten
history was on GitHub.

GitHub may still serve pre-rewrite objects by SHA until Support runs garbage
collection. Keep the repository private until that request is resolved.

## Current tree

| Finding | Action |
| --- | --- |
| Redis dump | Gone from tree and history |
| Travis encrypted Heroku token | `.travis.yml` gone from tree and history |
| News API key | Replaced with `NEWSAPI_KEY_REDACTED` throughout history |
| Mailbox password | Replaced with `REDACTED` throughout history |
| Personal emails in old seed scripts | Still present in history (not tokens; not rewritten) |

## Rotation checklist

History rewrite does not un-leak a credential. These were revoked at the
provider on 2026-08-16.

- [x] Revoke/rotate any Heroku auth token that may have been encrypted for Travis
- [x] Rotate the News API key that used to be hard-coded in `scripts/fetch_stories_for_today.py`
- [x] Rotate the mailbox password that used to appear in `retroville/config/local.py`
- [x] Confirm Twilio, AWS and Authy credentials from 2019 are revoked
- [x] Force-push rewritten `master` (and delete unre-written leftover branches)
- [ ] GitHub Support purge of cached pre-rewrite objects
- [ ] Keep the GitHub repository private until the Support purge is done
