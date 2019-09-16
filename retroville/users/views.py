from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from .serializers import CreateUserSerializer, UserSerializer, get_user


class UserViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    """
    Updates and retrieves user accounts
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class UserCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Creates user accounts
    """

    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


@csrf_exempt
@api_view(["GET"])
def who_am_i(request):
    if request.method == "GET":
        user = get_user(user_id=request.user.pk)
        return JsonResponse(user, status=status.HTTP_200_OK, safe=False)
