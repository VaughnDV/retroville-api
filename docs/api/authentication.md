# Authentication

Clients authenticate with a DRF token in the `Authorization` header:

```
Authorization: Token <token>
```

Register with `POST /api/v1/users/` (email + password) or exchange credentials
at `POST /api-token-auth/` using the email address as `username`.

