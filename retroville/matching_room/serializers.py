
from rest_framework import serializers
from .models import MatchingRoom

class MatchingRoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MatchingRoom
        fields = ("id", "url", "user", "access_token", "state", "role",)
