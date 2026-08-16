# Third-party licence and asset review

The project is MIT-licensed (`LICENSE`, copyright 2019 Vaughn de Villiers).

## Runtime and tooling licences

| Component | Licence | Compatible with MIT publication |
| --- | --- | --- |
| Django | BSD-3-Clause | Yes |
| Django REST Framework | BSD-3-Clause | Yes |
| Celery | BSD-3-Clause | Yes |
| Channels | BSD-3-Clause | Yes |
| Redis / redis-py | BSD-3-Clause / MIT | Yes |
| psycopg | LGPL-3.0 | Yes, dynamically linked |
| boto3 / botocore | Apache-2.0 | Yes |
| Twilio SDK | MIT | Yes |
| Gunicorn | MIT | Yes |
| pytest / factory-boy / ruff | MIT | Yes |
| MkDocs | BSD-2-Clause | Yes |

## Removed or replaced

| Component | Issue | Replacement |
| --- | --- | --- |
| `django-suit` GitHub tarball `v2` | Unpinned third-party admin skin, no licence vendored in-tree | Default Django admin |
| `authy` Python package | Twilio Authy API sunset | Twilio Verify adapter |
| `newrelic` agent | Optional SaaS agent, not required for the showcase | Omitted from the production image |
| `mixer` | Duplicate of factory-boy | factory-boy only |
| Duplicate `django-unique-upload` / `django_unique_upload` | Abandoned duplicate pins | Removed |

## Assets and copy

- Dummy image URLs historically pointed at `loremflickr.com`. Demo seed now uses
  local placeholder paths under `docs/assets/`.
- Postman examples contain no customer payloads.
- No copied proprietary UI kits or fonts were found in the tree.
- Cookiecutter Django REST was the original project skeleton; remaining
  boilerplate is used under its MIT licence.
