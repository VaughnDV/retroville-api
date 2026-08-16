from datetime import date

import pytest
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestMatchingModels:
    def test_story_in_match_table(self):
        story = mixer.blend("stories.Story", live_date=str(date.today()))
        match = mixer.blend("matching.Match", matched_story=story)
        assert match.matched_story == story
