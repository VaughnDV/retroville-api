# Staged Django upgrade path

The 2019 application ran Django 2.1.9. Official upgrade guides require moving
through each supported boundary. The live tree lands on Django 5.2 LTS; this
file is the audit trail of that path rather than a set of intermediate tags.

| Step | Target | Why it exists |
| --- | --- | --- |
| 1 | Django 2.2 LTS | Last 2.x LTS; `on_delete` already present |
| 2 | Django 3.2 LTS | `python_2_unicode_compatible` and `ugettext_lazy` removed; `DEFAULT_AUTO_FIELD` |
| 3 | Django 4.2 LTS | `USE_L10N` gone; `CSRF_TRUSTED_ORIGINS` needs a scheme; `STORAGES` |
| 4 | Django 5.2 LTS | Current LTS until April 2028; Python 3.10–3.14 |

Chosen runtime: **Python 3.12** and **Django 5.2**. Django 6.0 mainstream
support ended 4 August 2026. Django 6.2 LTS is not due until April 2027.

Replaced or dropped with the upgrade:

- `django-configurations` → split settings modules
- `django-suit` GitHub tarball → default admin
- `authy` → Twilio Verify adapter
- `psycopg2-binary` → `psycopg[binary]`
- `newrelic`, `mixer`, duplicate `django-unique-upload` pins → removed
