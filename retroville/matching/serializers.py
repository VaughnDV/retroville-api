import json

from django.core.serializers import serialize
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


# def serialise_data(data):
#     print("#" * 50)
#     print("#" * 50)
#     print("#" * 50)
#     print("#" * 50)
#     print(data)
#     print("#" * 50)
#     print("#" * 50)
#     print("#" * 50)
#     serialized_data = serialize('json', [data, ])
#     json_data = json.loads(serialized_data)[0]
#     data = {"id": json_data['pk']}
#     for field in json_data["fields"].items():
#         if field[0] not in NON_RETURN_FIELDS:
#             data.update({field[0]: field[1]})
#     return data

# def enter_or_update_room(user_id):
#     user = User.objects.get(id=user_id)
#     room = Room.objects.get_or_create(user=user)
#     RoomActivity.objects.create(user=user)
#     return serialise_data(room)
# NON_RETURN_FIELDS = ["password", "is_superuser", "is_staff", "groups", "user_permissions"]
