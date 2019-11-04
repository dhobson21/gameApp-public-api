from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from .game import Game
from .player import Player
from django.contrib.auth.models import User
from boardgamegeek import BGGClient, BGGRestrictSearchResultsTo, BGGChoose
from django.http import HttpRequest


class Event(models.Model):

    name = models.CharField(max_length=50)
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=300)
    address = models.CharField(max_length=50)
    zip_code = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(5)])
    date = models.DateTimeField()
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
    @property
    def waiting_list(self):

        reqEvents = self.player_event.filter(is_approved=False)
        wait_list = []
        for playerEvent in reqEvents:
            player = Player.objects.get(user=str(playerEvent.player_id))
            wait_list.append(player)
        return wait_list


    @property
    def is_full(self):
        gameObj = Game.objects.get(pk=self.game_id)
        bgg= BGGClient()
        game = bgg.game(game_id=str(gameObj.game))

        if len(self.player_list) >= int(game.max_players):
            return True
        else:
            return False
    @property
    def need_players(self):
        gameObj = Game.objects.get(pk=self.game_id)
        bgg= BGGClient()
        game = bgg.game(game_id=str(gameObj.game))

        if len(self.player_list) < int(game.min_players):
            players_needed = int(game.min_players)- len(self.player_list)
            return players_needed
        else:
            return 0

    @property
    def user_player(self):
        try:
            return self.__user_player
        except AttributeError:
            return "error somewhere"

    @user_player.setter
    def user_player(self, request):
        id = request.auth.user_id
        self.__user_player = False
        for player in self.player_list:
            if player.id == id:
                self.__user_player = True









    class Meta:
        verbose_name = ("event")
        verbose_name_plural = ("events")


