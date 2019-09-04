
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
        print("#" * 50)
        print("#" * 50)
        print(validated_data["user"])
        print("#" * 50)
        print("#" * 50)
        room = RoomActivity.objects.create_or_update(user=validated_data["user"])
        RoomActivity.objects.create(**validated_data)
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

