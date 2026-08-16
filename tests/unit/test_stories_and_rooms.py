import pytest

from tests.factories import StoryFactory


@pytest.mark.django_db
def test_stories_requires_live_date(auth_client):
    response = auth_client.post("/api/v1/stories/", {}, format="json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_stories_lists_today(auth_client, user):
    story = StoryFactory()
    response = auth_client.post("/api/v1/stories/", {"live_date": str(story.live_date)}, format="json")
    assert response.status_code == 200
    assert response.json()["results"][0]["id"] == story.id


@pytest.mark.django_db
def test_read_story_records_interest(auth_client, user):
    story = StoryFactory()
    response = auth_client.post(
        "/api/v1/stories/read/",
        {"story": story.id, "interested": True},
        format="json",
    )
    assert response.status_code == 201
    assert response.json()["interested"] is True


@pytest.mark.django_db
def test_enter_and_exit_room(auth_client):
    created = auth_client.post("/api/v1/room/enter/")
    assert created.status_code == 201
    again = auth_client.post("/api/v1/room/enter/")
    assert again.status_code == 200
    check = auth_client.get("/api/v1/room/check/")
    assert check.status_code == 200
    assert check.json()
    exited = auth_client.delete("/api/v1/room/exit/")
    assert exited.status_code == 204


@pytest.mark.django_db
def test_unauthenticated_room_is_rejected(api_client):
    assert api_client.post("/api/v1/room/enter/").status_code == 401
