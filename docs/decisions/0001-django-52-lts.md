# ADR 0001: Django 5.2 LTS and Python 3.12

## Status

Accepted

## Context

The 2019 application ran Django 2.1.9 and Python 3.6, both long past end of
life. Django 6.0 mainstream support ended 4 August 2026. Django 6.2 LTS is not
due until April 2027.

## Decision

Land the recovered runtime on Django 5.2 LTS (security fixes until April 2028)
and Python 3.12, with 3.13 in CI. Record the 2.2 → 3.2 → 4.2 → 5.2 path in
`docs/migration-path.md` rather than shipping intermediate tags.

## Consequences

Compatibility shims (`python_2_unicode_compatible`, Authy, django-suit) are
removed. The Git history still shows the 2019 code.
