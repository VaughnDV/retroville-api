from django.conf import settings
from django.db import models
from django.utils import timezone


class Story(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=512)
    content = models.CharField(max_length=2048)
    picture_url = models.CharField(max_length=512)
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()
    live_date = models.DateField(default=None)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="UserReadStory")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["title", "live_date"], name="unique_story_title_per_day")
        ]

    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.id:
            self.created_at = now
        self.modified_at = now
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class UserReadStory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    created_at = models.DateField(editable=False)
    interested = models.BooleanField()
    modified_at = models.DateTimeField()

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "story"], name="unique_user_read_story")]

    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.id:
            self.created_at = now.date()
        self.modified_at = now
        return super().save(*args, **kwargs)
