from django.contrib import admin
from .models import Story, UserReadStory


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    fields = ["title", "content", "picture_url", "live_date"]
    list_display = ["title", "content", "live_date"]
    ordering = ["live_date", "created_at"]
    list_filter = ["created_at", "title", "live_date"]
    search_fields = ["content", "title", "live_date"]


@admin.register(UserReadStory)
class UserReadStoriesAdmin(admin.ModelAdmin):
    fields = ["user", "story", "interested"]
    list_display = ["user", "story", "interested"]
    ordering = ["created_at"]
    list_filter = ["user", "story", "interested", "created_at"]
    search_fields = ["user", "story", "interested"]
