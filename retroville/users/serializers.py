from django.contrib.auth import get_user_model
from rest_framework import serializers

from retroville.users.models import User

MAX_NAME = 150
MAX_PHONE = 32
MAX_COUNTRY = 8


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "date_of_birth",
            "phone_number",
            "country_code",
        )
        extra_kwargs = {
            "first_name": {"max_length": MAX_NAME},
            "last_name": {"max_length": MAX_NAME},
            "phone_number": {"max_length": MAX_PHONE},
            "country_code": {"max_length": MAX_COUNTRY},
        }


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, max_length=128)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

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
            "phone_number",
            "country_code",
        )
        read_only_fields = ("auth_token",)
        extra_kwargs = {
            "first_name": {"max_length": MAX_NAME},
            "last_name": {"max_length": MAX_NAME},
            "phone_number": {"max_length": MAX_PHONE},
            "country_code": {"max_length": MAX_COUNTRY},
        }


def get_user(user_id):
    user = get_user_model().objects.get(id=user_id)
    return UserSerializer(user).data
