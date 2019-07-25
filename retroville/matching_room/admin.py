from django.contrib import admin
from .models import MatchingRoom


@admin.register(MatchingRoom)
class MatchingRoomAdmin(admin.ModelAdmin):
    fields = ["user", "state", "role", "access_token"]
    list_display = ["state", "role"]
    ordering = ["modified_at", "created_at"]
    list_filter = ["user", "created_at", "modified_at", "state", "role"]
    search_fields = ["user", "modified_at", "state", "role"]
