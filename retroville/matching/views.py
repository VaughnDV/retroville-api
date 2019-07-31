from rest_framework import viewsets
from .models import Room
from .models import Match
from .serializers import MatchSerializer
from .serializers import RoomSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


class RoomViewSet(viewsets.ModelViewSet):
    """
    List all and fetch one
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('user',)

    def get_queryset(self):
        return Match.objects.filter(user=self.request.user)


class MatchViewSet(viewsets.ModelViewSet):
    """
    """

    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('caller', 'receiver',)

    def get_queryset(self):
        return Match.objects.filter(Q(caller=self.request.user) | Q(receiver=self.request.user))
