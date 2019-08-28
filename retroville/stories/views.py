from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from .models import Story
from .models import UserReadStory
from .serializers import StorySerializer
from .serializers import UserReadStorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from datetime import date


@csrf_exempt
@api_view(['POST'])
def stories(request):
    if request.method == 'POST':
        stories = Story.objects.filter(live_date=request.data["live_date"])
        serializer = StorySerializer(stories, context={'request': request}, many=True)
        return JsonResponse({"results": serializer.data}, safe=False)


@csrf_exempt
@api_view(['POST'])
def read_story(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        data["user"] = str(request.user)
        serializer = UserReadStorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

