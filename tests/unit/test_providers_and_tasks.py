from datetime import date

import pytest
from retroville.matching.tasks import TransientProviderError, create_match_for_user, ingest_daily_stories
from retroville.providers.news import FakeNewsProvider
from retroville.providers.sms import FakeSmsProvider
from retroville.providers.voice import FakeVoiceProvider
from retroville.stories.models import Story


def test_fake_sms_accepts_demo_code():
    provider = FakeSmsProvider()
    assert provider.start_verification("7700000001", "44").ok
    assert provider.check_verification("7700000001", "44", "1234").ok
    assert not provider.check_verification("7700000001", "44", "0000").ok


def test_fake_voice_token_is_stable():
    token = FakeVoiceProvider().access_token("abc-def")
    assert token == "demo-token:abc_def"


def test_fake_news_returns_ten_headlines():
    headlines = FakeNewsProvider().fetch_headlines(date(2019, 9, 1))
    assert len(headlines) == 10
    assert all(item.live_date.isoformat() == "2019-09-01" for item in headlines)


@pytest.mark.django_db
def test_ingest_is_idempotent():
    first = ingest_daily_stories.run(live_on="2019-09-01")
    second = ingest_daily_stories.run(live_on="2019-09-01")
    assert first["created"] == 10
    assert second["created"] == 0
    assert Story.objects.filter(live_date="2019-09-01").count() == 10


@pytest.mark.django_db
def test_ingest_retries_on_provider_failure(monkeypatch):
    def boom(_live_on):
        raise RuntimeError("news down")

    provider = type("P", (), {"fetch_headlines": boom})()
    monkeypatch.setattr("retroville.matching.tasks.get_news_provider", lambda: provider)
    with pytest.raises(TransientProviderError):
        ingest_daily_stories.run(live_on="2019-09-02")


@pytest.mark.django_db
def test_create_match_task_duplicate_delivery(two_users_in_room):
    left, _right, _story = two_users_in_room
    first = create_match_for_user.run(str(left.pk))
    second = create_match_for_user.run(str(left.pk))
    assert first["status"] == "matched"
    assert second["match_id"] == first["match_id"]


@pytest.mark.django_db
def test_create_match_task_missing_user():
    result = create_match_for_user.run("00000000-0000-0000-0000-000000000000")
    assert result["status"] == "missing_user"


@pytest.mark.django_db
def test_send_sms_uses_fake_provider(api_client):
    response = api_client.post("/sendSMS/?country_code=44&phone_number=7700000099")
    assert response.status_code == 200
    assert response.json()["success"] is True
