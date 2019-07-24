from django.db import models
from django.utils import timezone
from django.conf import settings


class Story(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=2000)
    picture_url = models.CharField(max_length=100)
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()
    live_date = models.DateField(default=None)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="UserReadStory")

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(Story, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class UserReadStory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    created_at = models.DateField(editable=False)
    interested = models.BooleanField()
    modified_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(UserReadStory, self).save(*args, **kwargs)
