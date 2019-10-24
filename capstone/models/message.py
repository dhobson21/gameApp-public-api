from django.db import models
from .event import Event
from.player import Player


class Message(models.Model):

    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
    sender = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    reciever = models.ForeignKey(Player, related_name= 'reciever', on_delete=models.DO_NOTHING)
    message = models.CharField(max_length=500)
    open_time = models.DateTimeField(null=True, default=None)


    class Meta:
        verbose_name = ("message")
        verbose_name_plural = ("messages")


