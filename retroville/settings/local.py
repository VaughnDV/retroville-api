from .base import *  # noqa: F403

DEBUG = True
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
CELERY_TASK_ALWAYS_EAGER = True
CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
STORAGES["staticfiles"] = {  # noqa: F405
    "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
}
