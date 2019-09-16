from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from .users.views import UserViewSet, UserCreateViewSet
from .stories.views import stories, read_story
from .voice.views import incoming
from .voice.views import make_call
from .voice.views import place_call
from .voice.views import ping, send_sms, validate_sms
from .matching.views import (
    enter_room,
    update_token,
    check_room,
    exit_room,
    list_room,
    find_match,
    delete_match,
    check_match,
)
from .users.views import who_am_i
from django.contrib.auth import views as auth_views


admin.site.site_header = "Retroville"
admin.site.site_title = "Retroville Admin Panel"
admin.site.index_title = "Retroville"

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"users", UserCreateViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html')),
    # path('accounts/password_reset/', auth_views.LoginView.as_view(template_name='registration/password_reset.html')),
    path("api-token-auth/", views.obtain_auth_token),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # path("api/v1/password_reset/", include('django_rest_passwordreset.urls', namespace='password_reset')),
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("api-root"), permanent=False)),
    # path("accessToken/", token, name="token"),
    path("placeCall/", place_call, name="placeCall"),
    path("incoming/", incoming, name="incoming"),
    path("makeCall/", make_call, name="makeCall"),
    path("sendSMS/", send_sms, name="sendSMS"),
    path("validateSMS/", validate_sms, name="validateSMS"),
    path("ping/", ping, name="ping"),
    path("api/v1/", include(router.urls)),
    path("api/v1/room/check/", check_room, name="check_room"),
    path("api/v1/room/enter/", enter_room, name="enter_room"),
    path("api/v1/room/update/", update_token, name="update_token"),
    path("api/v1/room/exit/", exit_room, name="exit_room"),
    path("api/v1/room/list/", list_room, name="list_room"),
    path("api/v1/match/find/", find_match, name="find_match"),
    path("api/v1/match/check/", check_match, name="check_match"),
    path("api/v1/match/delete/", delete_match, name="delete_match"),
    path("api/v1/whoami/", who_am_i, name="who_am_i"),
    path("api/v1/stories/read/", read_story, name="read_story"),
    path("api/v1/stories/", stories, name="stories"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
