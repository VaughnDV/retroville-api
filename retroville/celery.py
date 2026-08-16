import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "retroville.settings.local")

app = Celery("retroville")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
