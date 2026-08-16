import pytest
from django.core.exceptions import ImproperlyConfigured


def test_production_settings_fail_closed(monkeypatch):
    monkeypatch.delenv("DJANGO_SECRET_KEY", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("REDIS_URL", raising=False)
    monkeypatch.delenv("DJANGO_ALLOWED_HOSTS", raising=False)
    with pytest.raises(ImproperlyConfigured):
        from importlib import reload

        import retroville.settings.production as production

        reload(production)
