from __future__ import annotations

import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403
from .base import env_list

required = [
    "DJANGO_SECRET_KEY",
    "DATABASE_URL",
    "REDIS_URL",
    "DJANGO_ALLOWED_HOSTS",
]
missing = [name for name in required if not os.getenv(name)]
if missing:
    raise ImproperlyConfigured(
        "Production settings refuse to start without: " + ", ".join(missing)
    )

DEBUG = False
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")

if os.getenv("DJANGO_AWS_STORAGE_BUCKET_NAME"):
    STORAGES["default"] = {  # noqa: F405
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "access_key": os.getenv("DJANGO_AWS_ACCESS_KEY_ID"),
            "secret_key": os.getenv("DJANGO_AWS_SECRET_ACCESS_KEY"),
            "bucket_name": os.getenv("DJANGO_AWS_STORAGE_BUCKET_NAME"),
            "default_acl": "private",
            "querystring_auth": True,
        },
    }
