from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=1000)


class Message(models.Model):
    message = models.CharField(max_length=1000)
    date = models.DateTimeField(default=timezone.now)
    sender = models.ForeignKey(
        settings.AUTH_USER,
        verbose_name=_("User"),
        on_delete=models.CASCADE
    )
    room = models.ForeignKey(
        "chat.Room", verbose_name=_("Room"), on_delete=models.CASCADE)
