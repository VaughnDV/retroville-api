from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from retroville.stories.models import Story
from retroville.stories.serializers import StorySerializer, UserReadStorySerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def stories(request):
    live_date = request.data.get("live_date")
    if not live_date:
        return Response({"live_date": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
    queryset = Story.objects.filter(live_date=live_date)
    serializer = StorySerializer(queryset, context={"request": request}, many=True)
    return Response({"results": serializer.data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def read_story(request):
    serializer = UserReadStorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
