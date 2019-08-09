from .models import Room, Match
from .serializers import RoomSerializer, MatchSerializer
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from .tasks import match_maker
from rest_framework.decorators import api_view
from django.db.models import Q
import json

User = get_user_model()


@csrf_exempt
@api_view(['GET'])
def list_room(request):
    if request.method == 'GET':
        room = Room.objects.all()
        serializer = RoomSerializer(room, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
@api_view(['GET'])
def check_room(request):
    if request.method == 'GET':
        room = Room.objects.filter(user=request.user)
        serializer = RoomSerializer(room, many=True)
        return JsonResponse(serializer.data, safe=False)
        # In order to serialize objects, we must set 'safe=False'


@csrf_exempt
@api_view(['POST'])
def enter_room(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        data["user"] = str(request.user)
        serializer = RoomSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['PUT'])
def update_token(request):
    if request.method == 'PUT':
        try:
            room = Room.objects.filter(user=request.user)[0]
        except Exception:
            return JsonResponse({"error": "User not in room yet, try POST instead"}, status=400)
        data = JSONParser().parse(request)
        data["user"] = str(request.user)
        serializer = RoomSerializer(room, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['DELETE'])
def exit_room(request):
    if request.method == 'DELETE':
        room = Room.objects.filter(user=request.user)[0]
        room.delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['GET'])
def find_match(request):
    if request.method == 'GET':
        match = match_maker(user_id=request.user.pk)
        if not match:
            return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

        return JsonResponse(match, status=status.HTTP_201_CREATED, safe=False)


@csrf_exempt
@api_view(['DELETE'])
def delete_match(request):
    if request.method == 'DELETE':
        match = Match.objects.filter(Q(caller=request.user) | Q(receiver=request.user))
        match.delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
