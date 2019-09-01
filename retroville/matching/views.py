from .models import Room, Match
from .serializers import RoomSerializer
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from .tasks import match_maker
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q


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
        # data = JSONParser().parse(request)
        data={"user": str(request.user)}
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
            room = Room.objects.filter(user=request.user).first()
        except ObjectDoesNotExist:
            return JsonResponse({"message": "User not in room yet, try POST instead"}, status=400)

        data = JSONParser().parse(request)
        data["user"] = str(request.user)
        serializer = RoomSerializer(room, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['DELETE'])
def exit_room(request):
    if request.method == 'DELETE':
        room = Room.objects.filter(user=request.user).first()
        if room:
            room.delete()
            return JsonResponse({"message": "User has exited room!"}, status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({"message": "User not found in room!"}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
def find_match(request):
    if request.method == 'GET':
        match = match_maker(user_id=request.user.pk)
        if "Message" not in match:
            return JsonResponse(match, status=status.HTTP_201_CREATED, safe=False)
        return JsonResponse(match, status=status.HTTP_204_NO_CONTENT)



@csrf_exempt
@api_view(['DELETE'])
def delete_match(request):
    if request.method == 'DELETE':
        match = Match.objects.filter(Q(caller=request.user) | Q(receiver=request.user)).first()
        if match:
            match.delete()
            return JsonResponse({"message": "Match deleted"}, status=status.HTTP_204_NO_CONTENT)
        return JsonResponse({"message": "Match not found!"}, status=status.HTTP_400_BAD_REQUEST)


