from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import MatchingRoom
from .serializers import MatchingRoomSerializer
from django.utils import timezone
from datetime import timedelta, datetime


@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        sapien = MatchingRoom.objects.get(pk=pk, modified_attimezone.now()-timedelta)
    except MatchingRoom.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = MatchingRoomSerializer(sapien)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = MatchingRoomSerializer(sapien, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        sapien.delete()
        return HttpResponse(status=204)
