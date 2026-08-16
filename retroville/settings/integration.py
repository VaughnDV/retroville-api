import os

import dj_database_url

from .test import *  # noqa: F403

if os.getenv("DATABASE_URL"):
    DATABASES = {  # noqa: F405
        "default": dj_database_url.config(conn_max_age=0, conn_health_checks=True)
    }

if os.getenv("REDIS_URL"):
    REDIS_URL = os.environ["REDIS_URL"]
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
            "CONFIG": {"hosts": [REDIS_URL]},
        }
    }
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    CELERY_TASK_ALWAYS_EAGER = False
