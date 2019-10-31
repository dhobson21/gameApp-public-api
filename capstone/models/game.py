from django.db import models
from .category import Category
from .player import Player
from boardgamegeek import BGGClient, BGGRestrictSearchResultsTo, BGGChoose



class Game(models.Model):

    game = models.IntegerField()
    name = models.CharField(max_length=50)
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING, related_name='user_games')
    host_descrip = models.CharField(max_length=300)



    @property
    def category_ids(self):
        bgg= BGGClient()
        id_list = []
        api_game = bgg.game(game_id=str(self.game))
        for category in api_game.categories:
            cat = Category.objects.get(name=category)
            id_list.append(cat.id)
        return id_list


    class Meta:
        verbose_name = ("game")
        verbose_name_plural = ("games")


