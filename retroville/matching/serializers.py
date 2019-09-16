from rest_framework import serializers
from .models import Room, Match, MatchActivity, RoomActivity
from django.contrib.auth import get_user_model

User = get_user_model()


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("id", "user", "created_at")
        read_only_fields = ("created_at",)

    def create(self, validated_data):
        user = User.objects.get(id=validated_data["user"])
        room = Room.objects.create(user=user)
        RoomActivity.objects.create(user=user)
        return room


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = (
            "caller",
            "caller_access_token",
            "receiver",
            "receiver_access_token",
            "created_at",
        )
