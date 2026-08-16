from rest_framework import serializers

from retroville.stories.models import Story, UserReadStory


class StorySerializer(serializers.ModelSerializer):
    is_read = serializers.SerializerMethodField("user_read_story")

    class Meta:
        model = Story
        fields = ("id", "is_read", "title", "content", "picture_url", "live_date")
        extra_kwargs = {
            "title": {"max_length": 512},
            "content": {"max_length": 2048},
            "picture_url": {"max_length": 512},
        }

    def user_read_story(self, obj) -> bool:
        request = self.context.get("request")
        if request is None or not getattr(request.user, "is_authenticated", False):
            return False
        return obj.users.filter(pk=request.user.pk).exists()


class UserReadStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReadStory
        fields = ("id", "user", "story", "interested")
        read_only_fields = ("id", "user")
