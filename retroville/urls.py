from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic.base import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from retroville.matching.views import (
    check_match,
    check_room,
    delete_match,
    enter_room,
    exit_room,
    find_match,
    list_room,
    update_token,
)
from retroville.stories.views import read_story, stories
from retroville.users.views import UserViewSet, who_am_i
from retroville.voice.views import incoming, make_call, ping, place_call, send_sms, validate_sms

admin.site.site_header = "Retroville"
admin.site.site_title = "Retroville Admin Panel"
admin.site.index_title = "Retroville"

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-token-auth/", views.obtain_auth_token),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("health/", include("retroville.health.urls")),
    path("", RedirectView.as_view(url=reverse_lazy("api-root"), permanent=False)),
    path("placeCall/", place_call, name="placeCall"),
    path("incoming/", incoming, name="incoming"),
    path("makeCall/", make_call, name="makeCall"),
    path("sendSMS/", send_sms, name="sendSMS"),
    path("validateSMS/", validate_sms, name="validateSMS"),
    path("ping/", ping, name="ping"),
    path("api/v1/", include(router.urls)),
    path("api/v1/password_reset/", include("django_rest_passwordreset.urls", namespace="password_reset")),
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
