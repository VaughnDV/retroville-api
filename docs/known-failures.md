# Known failures and preserved behaviour

Characterisation before the 2026 migration. Items marked **preserved** stay in
the modernised code unless a later ADR records a deliberate change. Items marked
**fixed with justification** were security or crash bugs, not product behaviour.

## Matching algorithm (preserved)

- Jaccard coefficient over liked story IDs; the first strictly greater score wins.
- Tied scores keep the earlier candidate.
- The shared story is `random.sample(intersection, 1)[0]`, so story choice is
  not deterministic when several stories overlap.
- Coefficient starts at `0`, so a coefficient of `0.0` never produces a match.
- `find_match` built dict literals for “no other users” / “no stories read by
  other users” and did not `return` them. Callers therefore fell through to the
  algorithm and typically received “no users to match with”.
- Division by empty union raises `ZeroDivisionError` in the 2019 code. The
  extracted domain function returns `0.0` instead of crashing; see ADR 0002.

## HTTP and permissions (fixed with justification)

- `list_room` returned every waiting-room row to any authenticated caller.
- `UserViewSet` queryset was `User.objects.all()` with no object-level check.
- `check_match` accepted any `match_id` without verifying participation.
- `send_sms` combined query filters with Python `and` on `Q` objects, so the
  country-code clause was discarded.
- Chat consumer accepted any WebSocket client and had no message size limit.
- Production `ALLOWED_HOSTS = ["*"]` and a missing secret key did not fail closed.

## Platform (recorded, then replaced)

- `python_2_unicode_compatible` and `ugettext_lazy` are Django 2 / Python 2 relics.
- `django-suit` was installed from an unpinned GitHub tarball.
- `generate_token` did `str(token.to_jwt()).split("'")[1]` for Py2/Py3 bytes.
- AppConfig `name = "matching"` / `"voice"` did not match `retroville.*` labels.
- `UserAdmin.search_fields` contained a corrupted string that searched a literal
  field name `'last_name, "phone_number", "country_code"'`.

## Tests (recorded)

- `test_user_model.py` is fully commented out.
- Matching tests call view functions with `RequestFactory` and therefore skip
  URL/auth middleware.
- Matching tests call Twilio token generation and fail without credentials.
- `StoryFactory.live_date` passes a format string to `factory.Sequence` incorrectly.
