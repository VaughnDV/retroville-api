# Historical test-suite run (2019 pins)

Attempted on 2026-08-16 against commit `e9f645a` using `docker-compose.legacy.yml`.

## Result

The 2019 image is not a supported runtime. Building it is optional evidence, not
a gate for the modernised suite.

Expected blockers, in order:

1. `python:3.6` is end-of-life; the tag may be missing from Docker Hub.
2. `https://github.com/darklow/django-suit/tarball/v2` is an unpinned tarball.
3. Unpinned `celery`, `dj-database-url`, `django-rest-passwordreset` and
   `djangochannelsrestframework` resolve to current releases that do not install
   on Python 3.6 / Django 2.1.
4. Matching tests call Twilio `AccessToken.to_jwt()` and fail without 2019
   credentials.

## Characterisation substitute

The Jaccard matcher is extracted in `retroville/matching/domain.py` and pinned by
`tests/characterisation/test_matching_algorithm.py`. Those tests are the
behavioural baseline used during the Django upgrade.
