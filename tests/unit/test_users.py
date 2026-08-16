import pytest
from django.core import mail
from rest_framework.authtoken.models import Token

from tests.factories import UserFactory


@pytest.mark.django_db
def test_create_user_hashes_password_and_issues_token(api_client):
    response = api_client.post(
        "/api/v1/users/",
        {
            "email": "new@example.com",
            "password": "longenough",
            "first_name": "Ada",
            "last_name": "Lovelace",
            "country_code": "44",
            "phone_number": "7700000001",
        },
        format="json",
    )
    assert response.status_code == 201
    body = response.json()
    assert "password" not in body
    assert body["auth_token"]
    user_id = body["id"]
    from django.contrib.auth import get_user_model

    user = get_user_model().objects.get(pk=user_id)
    assert user.check_password("longenough")
    assert not user.check_password("plaintext-should-fail")


@pytest.mark.django_db
def test_create_user_rejects_short_password(api_client):
    response = api_client.post(
        "/api/v1/users/",
        {"email": "new@example.com", "password": "short"},
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_user_rejects_oversized_name(api_client):
    response = api_client.post(
        "/api/v1/users/",
        {
            "email": "new@example.com",
            "password": "longenough",
            "first_name": "x" * 200,
        },
        format="json",
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_user_cannot_retrieve_another_user(auth_client, other_user):
    response = auth_client.get(f"/api/v1/users/{other_user.pk}/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_user_can_retrieve_self(auth_client, user):
    response = auth_client.get(f"/api/v1/users/{user.pk}/")
    assert response.status_code == 200
    assert response.json()["email"] == user.email


@pytest.mark.django_db
def test_whoami_requires_auth(api_client, auth_client):
    assert api_client.get("/api/v1/whoami/").status_code == 401
    assert auth_client.get("/api/v1/whoami/").status_code == 200


@pytest.mark.django_db
def test_token_auth_with_email(api_client, user):
    user.set_password("password123")
    user.save()
    response = api_client.post(
        "/api-token-auth/",
        {"username": user.email, "password": "password123"},
        format="json",
    )
    assert response.status_code == 200
    assert response.json()["token"] == Token.objects.get(user=user).key


@pytest.mark.django_db
def test_password_reset_sends_mail(api_client, user):
    response = api_client.post("/api/v1/password_reset/", {"email": user.email}, format="json")
    assert response.status_code in {200, 201}
    assert len(mail.outbox) == 1
    assert user.email in mail.outbox[0].to
