from rest_framework import viewsets
from .models import Story
from .models import UserReadStory
from retroville.permissions import IsUserOrReadOnly, IsAdminUserOrReadOnly
from .serializers import StorySerializer
from .serializers import UserReadStorySerializer
from django_filters.rest_framework import DjangoFilterBackend


class StoryViewSet(viewsets.ModelViewSet):
    """
    List all and fetch one
    """

    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['live_date', 'users']


class UserReadStoryViewSet(viewsets.ModelViewSet):
    """
    """

    queryset = UserReadStory.objects.all()
    serializer_class = UserReadStorySerializer
    permission_classes = (IsUserOrReadOnly,)
