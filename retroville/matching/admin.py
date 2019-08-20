from django.contrib import admin
from .models import Room, Match, RoomActivity, MatchActivity


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    fields = ["user"]
    list_display = ["user"]
    search_fields = ["user"]


@admin.register(RoomActivity)
class RoomActivityAdmin(admin.ModelAdmin):
    fields = ["user"]
    list_display = ["user", "created_at", "modified_at"]
    search_fields = ["user"]


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    fields = ["caller", "receiver", "caller_access_token", "receiver_access_token"]
    list_display = ["caller", "receiver"]
    ordering = ["modified_at", "created_at"]
    list_filter = ["caller", "receiver"]
    search_fields = ["caller", "receiver"]


@admin.register(MatchActivity)
class MatchActivityAdmin(admin.ModelAdmin):
    fields = ["caller", "receiver", "caller_access_token", "receiver_access_token"]
    list_display = ["caller", "receiver"]
    ordering = ["modified_at", "created_at"]
    list_filter = ["caller", "receiver"]
    search_fields = ["caller", "receiver"]
