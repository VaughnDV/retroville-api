from rest_framework import serializers
from .models import Story, UserReadStory


class StorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Story
        fields = ("id", "url", "users", "title", "content", "picture_url")


class UserReadStorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserReadStory
        fields = ("id", "url", "user", "story", "interested")

