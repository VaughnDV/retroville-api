from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .users.views import UserViewSet, UserCreateViewSet
from .stories.views import StoryViewSet, UserReadStoryViewSet
from .voice.views import token
from .voice.views import incoming
from .voice.views import makeCall
from .voice.views import placeCall
from .voice.views import ping


router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"users", UserCreateViewSet)
router.register(r"stories", StoryViewSet)
router.register(r"stories/read", UserReadStoryViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api-token-auth/", views.obtain_auth_token),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("api-root"), permanent=False)),
    path("accessToken/", token, name="token"),
    path("placeCall/", placeCall, name="placeCall"),
    path("incoming/", incoming, name="incoming"),
    path("makeCall/", makeCall, name="makeCall"),
    path("ping/", ping, name="ping"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
