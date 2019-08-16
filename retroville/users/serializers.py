from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model
from django.core.serializers import serialize
import json


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "date_of_birth")
        # read_only_fields = ("email",)


class CreateUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "date_of_birth",
            "auth_token",
        )
        read_only_fields = ("auth_token",)
        extra_kwargs = {"password": {"write_only": True}}


User = get_user_model()
NON_RETURN_FIELDS = ["password", "is_superuser", "is_staff", "groups", "user_permissions"]


def serialise_data(data):
    serialized_data = serialize('json', [data, ])
    json_data = json.loads(serialized_data)[0]
    data = {"id": json_data['pk']}
    for field in json_data["fields"].items():
        if field[0] not in NON_RETURN_FIELDS:
            data.update({field[0]: field[1]})
    return data


def get_user(user_id):
    user = User.objects.get(id=user_id)
    return serialise_data(user)
