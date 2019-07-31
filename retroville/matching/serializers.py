
from rest_framework import serializers
from .models import Room, Match, MatchActivity, RoomActivity


class RoomSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Room
        fields = ("user", "access_token", "created_at")
        read_only_fields = ("created_at",)

    def create(self, validated_data):
        room = Room.objects.create(**validated_data)
        RoomActivity.objects.create(**validated_data)
        return room


class MatchSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Match
        fields = (
            "caller",
            "caller_access_token",
            "receiver",
            "receiver_access_token",
            "created_at",
        )
        read_only_fields = ("created_at",)

    def create(self, validated_data):
        match = Match.objects.create(**validated_data)
        MatchActivity.objects.create(**validated_data)
        return match
