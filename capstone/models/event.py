from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .game import Game
from .player import Player
from django.contrib.auth.models import User

class Event(models.Model):

    name = models.CharField(max_length=50)
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=300)
    address = models.CharField(max_length=50)
    zip_code = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(5)])
    date = models.DateField()
    time = models.TimeField(default= "00:00")
    recurring = models.BooleanField()
    recurring_days = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)], null=True)

    @property
    def player_list(self):
        playerEvents = self.player_event.filter(is_approved=True)
        playerList = []
        for playerEvent in playerEvents:
            player = Player.objects.get(user=str(playerEvent.player_id))
            playerList.append(player)
        return playerList




    class Meta:
        verbose_name = ("event")
        verbose_name_plural = ("events")


