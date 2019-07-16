from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import AllowAny
from .models import Story
from .models import UserReadStory
from retroville.permissions import IsUserOrReadOnly, IsAdminUserOrReadOnly
from .serializers import StorySerializer
from .serializers import UserReadStorySerializer


class StoryViewSet(viewsets.ModelViewSet):
    """
    Updates and retrieves user accounts
    """

    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)


class UserReadStoryViewSet(viewsets.ModelViewSet):
    """
    Creates user accounts
    """

    queryset = UserReadStory.objects.all()
    serializer_class = UserReadStorySerializer
    permission_classes = (IsUserOrReadOnly,)
