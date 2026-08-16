# Retry and failure semantics

Matching and story ingest are safe to run more than once.

## `ingest_daily_stories`

- Late ack, exponential backoff, five retries, 5 minute cap.
- Retries on `TransientProviderError` only (provider/network).
- Idempotent key: `(title, live_date)`. A second worker seeing ten stories
  already present for that date returns without inserting.
- Terminal failure after max retries leaves the previous day's stories in place.
  Operators re-run `make seed` or the task with an explicit `live_on`.

## `create_match_for_user`

- Late ack, three retries on transient errors.
- Idempotent key: a `Match` row for the caller or receiver. `select_for_update`
  serialises two users matching each other at the same moment.
- Domain misses (`MatchServiceError`) are not retried; the task returns
  `unmatched` so the client can poll `GET /api/v1/match/find/`.

## Voice tokens

Token minting is delegated to `VoiceProvider`. The fake provider is used in
tests and the offline demo. Twilio failures raise `TransientProviderError` when
called from a task.
