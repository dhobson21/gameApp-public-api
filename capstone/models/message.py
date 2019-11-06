from django.db import models
from .event import Event
from .player import Player
from .playerEvent import PlayerEvent


class Message(models.Model):

    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
    sender = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    reciever = models.ForeignKey(Player, related_name= 'reciever', on_delete=models.DO_NOTHING)
    message = models.CharField(max_length=500)
    open_time = models.DateTimeField(null=True, default=None)
    type = models.CharField(default='request', max_length=50)
    player_event = models.ForeignKey(PlayerEvent, on_delete=models.SET_NULL, null=True, default=None)


    class Meta:
        verbose_name = ("message")
        verbose_name_plural = ("messages")


