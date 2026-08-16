from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from retroville.matching.models import Match, Room
from retroville.matching.serializers import MatchDetailSerializer, RoomSerializer
from retroville.matching.services import (
    MatchServiceError,
    delete_match_for,
    enter_waiting_room,
    leave_waiting_room,
    request_match,
    user_can_see_match,
)


@api_view(["GET"])
@permission_classes([IsAdminUser])
def list_room(request):
    serializer = RoomSerializer(Room.objects.select_related("user"), many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_room(request):
    serializer = RoomSerializer(Room.objects.filter(user=request.user), many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def enter_room(request):
    room, created = enter_waiting_room(request.user)
    serializer = RoomSerializer(room)
    return JsonResponse(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_token(request):
    try:
        room = Room.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return JsonResponse({"message": "User not in room yet, try POST instead"}, status=400)
    data = JSONParser().parse(request)
    data["user"] = str(request.user.pk)
    serializer = RoomSerializer(room, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def exit_room(request):
    if leave_waiting_room(request.user):
        return JsonResponse({"message": "User has exited room!"}, status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({"message": "User not found in room!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def find_match(request):
    try:
        match = request_match(request.user)
    except MatchServiceError as exc:
        return JsonResponse({"Message": exc.message}, status=status.HTTP_204_NO_CONTENT)
    return JsonResponse(
        MatchDetailSerializer(match, context={"request": request}).data,
        status=status.HTTP_201_CREATED,
        safe=False,
    )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_match(request):
    if delete_match_for(request.user):
        return JsonResponse({"message": "Match deleted"}, status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({"message": "Match not found!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_match(request):
    match_id = request.GET.get("match_id", "")
    match = Match.objects.filter(id=match_id).first()
    if match and user_can_see_match(request.user, match):
        return JsonResponse({"message": "Match exists!"}, status=status.HTTP_200_OK)
    return JsonResponse({"message": "Match not found!"}, status=status.HTTP_404_NOT_FOUND)
