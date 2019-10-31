from django.db import models
from .player import Player
from boardgamegeek import BGGClient, BGGRestrictSearchResultsTo, BGGChoose



class Category(models.Model):

    name = models.CharField(max_length=50)


    class Meta:
        verbose_name = ("category")
        verbose_name_plural = ("categories")


