from rest_framework import serializers
from .models import Story, UserReadStory


class StorySerializer(serializers.HyperlinkedModelSerializer):
    is_read = serializers.SerializerMethodField('user_read_story')

    class Meta:
        model = Story
        fields = ("id", "is_read", "url", "title", "content", "picture_url", "live_date",)

    def user_read_story(self, obj):
        return True if self.context['request'].user in obj.users.all() else False


class UserReadStorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserReadStory
        fields = ("id", "url", "user", "story", "interested")
