from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
<<<<<<< HEAD
        fields = ('id', 'email', 'first_name', 'last_name',)
        read_only_fields = ('email', )
=======
        fields = ("id", "email", "first_name", "last_name", "date_of_birth")
        # read_only_fields = ("email",)
>>>>>>> e25ea72b8d2a1092b32ac15567d555bf17a7e6cd


class CreateUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
<<<<<<< HEAD
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'auth_token',)
        read_only_fields = ('auth_token',)
        extra_kwargs = {'password': {'write_only': True}}
=======
        fields = (
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "auth_token",
        )
        read_only_fields = ("auth_token",)
        extra_kwargs = {"password": {"write_only": True}}
>>>>>>> e25ea72b8d2a1092b32ac15567d555bf17a7e6cd
