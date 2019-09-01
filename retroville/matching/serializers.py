
from rest_framework import serializers
from .models import Room, Match, MatchActivity, RoomActivity
from django.contrib.auth import get_user_model

User = get_user_model()


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ("id", "user", "created_at",)
        read_only_fields = ("created_at",)

    def create(self, validated_data):
        print(validated_data["user"])
        if Room.objects.filter(user=validated_data["user"]).exists():
            Room.objects.get(user=validated_data["user"]).delete()
        room = Room.objects.create(**validated_data)
        activity = RoomActivity.objects.create(**validated_data)
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

