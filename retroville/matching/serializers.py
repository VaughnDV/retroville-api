from rest_framework import serializers

from retroville.matching.models import Match, Room, RoomActivity
from retroville.users.serializers import UserSerializer
from retroville.stories.serializers import StorySerializer


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("id", "user", "created_at")
        read_only_fields = ("id", "user", "created_at")

    def create(self, validated_data):
        user = validated_data["user"]
        room = Room.objects.create(user=user)
        RoomActivity.objects.create(user=user)
        return room


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = (
            "id",
            "caller",
            "caller_access_token",
            "receiver",
            "receiver_access_token",
            "created_at",
        )
        read_only_fields = fields


class MatchDetailSerializer(serializers.ModelSerializer):
    caller = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    story = StorySerializer(source="matched_story", read_only=True)

    class Meta:
        model = Match
        fields = (
            "id",
            "caller",
            "caller_access_token",
            "receiver",
            "receiver_access_token",
            "story",
            "created_at",
        )
        read_only_fields = fields
