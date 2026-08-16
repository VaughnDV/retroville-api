import pytest
from django.core.management import call_command
from django.db import connection

from tests.factories import UserFactory


@pytest.mark.integration
@pytest.mark.django_db
def test_api_persists_user_in_configured_database(api_client):
    response = api_client.post(
        "/api/v1/users/",
        {"email": "pg@example.com", "password": "longenough"},
        format="json",
    )
    assert response.status_code == 201
    assert UserFactory._meta.model.objects.filter(email="pg@example.com").exists()


@pytest.mark.integration
@pytest.mark.django_db
def test_migrations_apply_on_empty_database():
    call_command("migrate", run_syncdb=True, verbosity=0)
    tables = connection.introspection.table_names()
    assert "users_user" in tables
    assert "matching_room" in tables
    assert "stories_story" in tables
