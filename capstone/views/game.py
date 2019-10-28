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
from boardgamegeek import BGGClient, BGGRestrictSearchResultsTo, BGGChoose


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
        player = Player.objects.get(user= request.auth.user)
        new_game.player = player
        new_game.game = request.data["game"]
        new_game.host_descrip= request.data["host_descrip"]
        new_game.save()


        serializer = GameSerializer(new_game, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        try:
            game = Game.objects.get(pk=pk)
            bgg = BGGClient()
            player = Player.objects.get(user=game.player.user)

            BGGObj = bgg.game(game_id=str(game.game))
            game1={}
            game1['name'] = game.name
            game1["api_id"] = game.game
            game1["api_game_name"]= BGGObj.name
            playerObj = PlayerSerializer(player, context={'request': request})
            game1['player'] = playerObj.data
            game1['host_descrip'] = game.host_descrip
            game1['max_players'] = BGGObj.max_players
            game1['min_players'] = BGGObj.min_players
            game1['categories'] = []
            for category in BGGObj.categories:
                game1['categories'].append(category)
            game1['image'] = BGGObj.image
            game1['thumb_nail'] = BGGObj.thumbnail
            return Response(game1)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """
        game = Game.objects.get(pk=pk)
        game.game = request.data["game"]
        game.name = request.data["name"]
        # game = game.objects.get(pk=request.data["game"])
        # event.game = game
        game.host_descrip = request.data["host_descrip"]


        game.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single game

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            game = Game.objects.get(pk=pk)
            game.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request):
        """Handle GET requests to game Categories resource

        Returns:
            Response -- JSON serialized list of park ProductCategorys
        """
        # Creating game dictionary of custom info from game object and API boardgame object so user can see info from both
        bgg = BGGClient()
        player = Player.objects.get(user=request.auth.user)
        games = Game.objects.filter(player=player)
        game_list = []
        for game in games:
            BGGObj = bgg.game(game_id=str(game.game))
            game1={}
            game1['name'] = game.name
            game1["api_id"] = game.game
            owner = Player.objects.get(user=game.player.user)
            playerObj = PlayerSerializer(owner, context={'request': request})
            game1['player'] = playerObj.data
            game1['host_descrip'] = game.host_descrip
            game1['max_players'] = BGGObj.max_players
            game1['min_players'] = BGGObj.min_players
            game1['categories'] = []
            for category in BGGObj.categories:
                game1['categories'].append(category)
            game1['image'] = BGGObj.image
            game1['thumb_nail'] = BGGObj.thumbnail
            game_list.append(game1)



        # serializer = GameSerializer(
        #     games, many=True, context={'request': request})
        return Response(game_list)