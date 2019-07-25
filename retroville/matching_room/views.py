from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import MatchingRoom
from .serializers import MatchingRoomSerializer
from django.utils import timezone
from datetime import timedelta, datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@csrf_exempt
def room_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        sapien = MatchingRoom.objects.get(pk=pk, modified_at__gt=timezone.now()-timedelta(hours=24))
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


@login_required
def room(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    sapiens = MatchingRoom.objects.filter(modified_at__gt=timezone.now()-timedelta(hours=24))

    # Render that in the index template
    return render(request, "index.html", {
        "sapiens": sapiens,
    })
