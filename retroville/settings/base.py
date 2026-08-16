"""Shared Django settings. Environment-specific modules import from here."""

from __future__ import annotations

import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def env_bool(name: str, default: str = "false") -> bool:
    value = os.getenv(name, default).strip().lower()
    if value in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if value in {"0", "false", "f", "no", "n", "off"}:
        return False
    raise ValueError(f"Invalid boolean for {name}: {value!r}")


def env_list(name: str, default: str = "") -> list[str]:
    raw = os.getenv(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "")
DEBUG = env_bool("DJANGO_DEBUG", "false")
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "django_filters",
    "django_rest_passwordreset",
    "drf_spectacular",
    "channels",
    "retroville.users.apps.UsersConfig",
    "retroville.stories",
    "retroville.voice",
    "retroville.matching",
    "retroville.chat",
    "retroville.health",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "retroville.observability.RequestContextMiddleware",
]

ROOT_URLCONF = "retroville.urls"
WSGI_APPLICATION = "retroville.wsgi.application"
ASGI_APPLICATION = "retroville.asgi.application"
AUTH_USER_MODEL = "users.User"
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
APPEND_SLASH = False
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"
USE_I18N = False
USE_TZ = True
LOGIN_REDIRECT_URL = "/"

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL", "postgres://postgres:@127.0.0.1:5432/postgres"),
        conn_max_age=int(os.getenv("POSTGRES_CONN_MAX_AGE", "600")),
        conn_health_checks=True,
    )
}

REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [REDIS_URL], "capacity": 100, "expiry": 60},
    }
}

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", REDIS_URL)
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", REDIS_URL)
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_TIME_LIMIT = 60
CELERY_TASK_SOFT_TIME_LIMIT = 50
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_ALWAYS_EAGER = env_bool("CELERY_TASK_ALWAYS_EAGER", "false")

EMAIL_BACKEND = os.getenv(
    "DJANGO_EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = os.getenv("DJANGO_EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.getenv("DJANGO_EMAIL_PORT", "25"))
DEFAULT_FROM_EMAIL = os.getenv("DJANGO_DEFAULT_FROM_EMAIL", "noreply@example.com")
ADMINS = [("Author", os.getenv("DJANGO_ADMIN_EMAIL", "owner@example.com"))]

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS: list[Path] = []
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": int(os.getenv("DJANGO_PAGINATION_LIMIT", "10")),
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z",
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "30/minute", "user": "120/minute"},
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Retroville API",
    "DESCRIPTION": "Spontaneous activity matching and real-time communication.",
    "VERSION": "2.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

PASSWORD_RESET_CONFIRM_URL = os.getenv(
    "PASSWORD_RESET_CONFIRM_URL", "http://localhost:8000/reset-password?token={token}"
)

TWILIO_ACCOUNT_SID = os.getenv("ACCOUNT_SID", "")
TWILIO_API_KEY = os.getenv("API_KEY", "")
TWILIO_API_KEY_SECRET = os.getenv("API_KEY_SECRET", "")
TWILIO_APP_SID = os.getenv("APP_SID", "")
TWILIO_PUSH_CREDENTIAL_SID = os.getenv("PUSH_CREDENTIAL_SID", "")
TWILIO_VERIFY_SERVICE_SID = os.getenv("TWILIO_VERIFY_SERVICE_SID", "")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
NEWS_COUNTRY = os.getenv("COUNTRY", "gb")
NEWS_LANGUAGE = os.getenv("LANGUAGE", "en")
PROVIDERS_USE_FAKES = env_bool("PROVIDERS_USE_FAKES", "false")

WEBSOCKET_ALLOWED_ORIGINS = env_list("WEBSOCKET_ALLOWED_ORIGINS", "http://localhost:8000")
WEBSOCKET_MAX_MESSAGE_BYTES = int(os.getenv("WEBSOCKET_MAX_MESSAGE_BYTES", "4096"))

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "retroville.observability.RedactingJsonFormatter",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        }
    },
    "root": {"handlers": ["console"], "level": os.getenv("LOG_LEVEL", "INFO")},
    "loggers": {
        "django.security": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "celery": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}
