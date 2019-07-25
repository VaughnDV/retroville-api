from django.db import models
from django.utils import timezone
from django.conf import settings


class MatchingRoom(models.Model):

    STATES = [
        ('ONLINE', 'online'),
        ('LOOKING', 'looking_for_match'),
        ('WAITING', 'waiting_for_match'),
        ('MATCHED', 'matched'),
        ('OFFLINE', 'offline'),
    ]
    ROLES = [
        ('UNASSIGNED', 'unassigned'),
        ('CALLER', 'caller'),
        ('RECEIVER', 'receiver'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=256)
    state = models.CharField(max_length=24, choices=STATES, default="OFFLINE")
    role = models.CharField(max_length=24, choices=ROLES, default=None)
    created_at = models.DateTimeField(editable=False)
    modified_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        """On save, update timestamps"""
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()
        return super(MatchingRoom, self).save(*args, **kwargs)

    def __str__(self):
        return self.state
