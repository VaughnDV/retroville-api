from django.http.response import JsonResponse
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated

from retroville.permissions import IsSelf
from retroville.users.models import User
from retroville.users.serializers import CreateUserSerializer, UserSerializer, get_user


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateUserSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated(), IsSelf()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        if self.request.user.is_authenticated:
            return User.objects.filter(pk=self.request.user.pk)
        return User.objects.none()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def who_am_i(request):
    return JsonResponse(get_user(user_id=request.user.pk), status=status.HTTP_200_OK, safe=False)
