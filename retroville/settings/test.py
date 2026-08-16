from .base import *  # noqa: F403

SECRET_KEY = "test-secret-key-not-for-production"
DEBUG = False
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]
DATABASES = {  # noqa: F405
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "ATOMIC_REQUESTS": False,
    }
}
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
STORAGES["staticfiles"] = {  # noqa: F405
    "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
}

# Unit tests never call paid providers. Integration tests opt in with markers.
TWILIO_ACCOUNT_SID = "ACtest"
TWILIO_API_KEY = "test-key"
TWILIO_API_KEY_SECRET = "test-secret"
TWILIO_APP_SID = "APtest"
TWILIO_PUSH_CREDENTIAL_SID = "CRtest"
TWILIO_VERIFY_SERVICE_SID = "VAtest"
NEWS_API_KEY = ""
