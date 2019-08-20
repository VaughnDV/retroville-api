from django.db import models
from django.utils import timezone
from django.conf import settings


class Room(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    access_token = models.CharField(max_length=1024)
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(Room, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} {self.user} {self.access_token}"

    class Meta:
        verbose_name_plural = "room"


class Match(models.Model):

    caller = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    caller_access_token = models.CharField(max_length=1024)
    receiver = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    receiver_access_token = models.CharField(max_length=1024)
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(Match, self).save(*args, **kwargs)

    def __str__(self):
        return f"Caller: {self.receiver}, Receiver: {self.caller}"

    class Meta:
        verbose_name_plural = "matches"


class RoomActivity(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=1024)
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(RoomActivity, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "room_activity"


class MatchActivity(models.Model):

    caller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    caller_access_token = models.CharField(max_length=1024)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    receiver_access_token = models.CharField(max_length=1024)
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(MatchActivity, self).save(*args, **kwargs)

    def __str__(self):
        return f"Caller: {self.receiver.id}, Receiver: {self.caller.id}"

    class Meta:
        verbose_name_plural = "match_activity"
