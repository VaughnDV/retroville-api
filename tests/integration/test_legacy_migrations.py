"""Apply historical migrations then the 2026 unique constraints on a clean schema."""

import pytest
from django.core.management import call_command
from django.db import connection


@pytest.mark.integration
@pytest.mark.django_db
def test_legacy_schema_migrates_forward():
    call_command("migrate", "stories", "0002", verbosity=0)
    call_command("migrate", "stories", "0003", verbosity=0)
    constraints = connection.introspection.get_constraints("stories_story")
    names = set(constraints)
    assert any("unique_story_title_per_day" in name for name in names)
