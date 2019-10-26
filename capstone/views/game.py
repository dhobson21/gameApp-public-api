"""
   Author: Dustin Hobson
   Purpose: To convert game data to json
   Methods: GET, POST
"""

"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from capstone.models import Game, Player
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .player import PlayerSerializer


class GameSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas
    Arguments:

        serializers
    """
    player = PlayerSerializer(many=False)
    class Meta:
        model = Game
        url = serializers.HyperlinkedIdentityField(
            view_name='game',
            lookup_field='id'
        )
        fields = ('id', 'url', 'game','name','player','host_descrip')
        depth=2


class Games(ViewSet):
    """Game for game app"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        """Handle POST operations

    #     Returns:
    #         Response -- JSON serialized product category instance
    #     """
        new_game = Game()
        new_game.name = request.data["name"]
        player = Player.objects.get(user=request.auth.user)
        new_game.player = player
        new_game.game = request.data["game"]
        new_game.host_descrip= request.data["game"]
        new_game.save()

    #     serializer = CategorySerializer(new_product_category, context={'request': request})

    #     return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to game Categories resource

        Returns:
            Response -- JSON serialized list of park ProductCategorys
        """
        player = Player.objects.get(user=request.auth.user)
        games = Game.objects.filter(player=player)

        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)