from django.db import models
from .event import Event
from .player import Player


class PlayerEvent(models.Model):

    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, related_name="player_event")
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    has_played = models.BooleanField()
    is_approved = models.BooleanField(default = False)


    class Meta:
        verbose_name = ("player_event")
        verbose_name_plural = ("player_events")


