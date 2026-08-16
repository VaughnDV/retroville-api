# Users

Register with email, not username:

`POST /api/v1/users/`

```json
{
  "email": "ada@example.com",
  "password": "longenough",
  "first_name": "Ada",
  "last_name": "Lovelace"
}
```

Retrieve or update only your own record at `/api/v1/users/{id}/`. Cross-user
reads return 404. `GET /api/v1/whoami/` returns the authenticated profile.

