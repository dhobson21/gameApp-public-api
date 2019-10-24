from django.db import models
from .player import Player

class Game(models.Model):

    game = models.IntegerField()
    name = models.CharField(max_length=50)
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    host_descrip = models.CharField(max_length=300)


    class Meta:
        verbose_name = ("game")
        verbose_name_plural = ("games")


