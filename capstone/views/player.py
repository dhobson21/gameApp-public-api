from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from capstone.models import Player
from django.contrib.auth.models import User
from .user import UserSerializer


class PlayerSerializer(serializers.HyperlinkedModelSerializer):

    # Depth of one allows user object to be seen on Customer
    class Meta:
        model = Player
        url = serializers.HyperlinkedIdentityField(
            view_name='player',
            lookup_field = 'id'

        )
        fields = ('id', 'url', 'user', 'zip_code', 'full_name')
        depth = 1


class Players(ViewSet):
    # """Players for gameApp
    # Author: Dustin Hobson
    # Purpose: Allow a user to communicate with the Bangazon database to GET PUT POST and DELETE Customers.
    # Methods: GET PUT(id) POST
    # """

    # def create(self, request):
    #     # """Handle POST operations
    #     # Author: Dustin Hobson
    #     # Purpose: Allow a user to communicate with the gameApp database to create new player
    #     # Methods:  POST
    #     # Returns:
    #     #     Response -- JSON serialized Customer instance
    #     # """
    #     new_player = Player()
    #     new_player.zip_code = request.data["zip_code"]
    #     # Grab the Player object based on the user ID
    #     # This + User view allows you to see the entire user object on the Customer instance
    #     user = Player.objects.get(user=request.auth.user)
    #     new_player.user = user

    #     new_player.save()
    #     serializer = PlayerSerializer(new_player, context={'request': request})

    #     return Response(serializer.data)

    def retrieve(self, request, pk=None):
        # """Handle GET requests for single customer
        # Author: Dustin Hobson
        # Purpose: Allow a user to communicate with the Bangazon database to retrieve  customer
        # Methods:  GET
        # Returns:
        #     Response -- JSON serialized customer instance
        # """
        try:
            player = Player.objects.get(pk=pk)
            serializer = PlayerSerializer(player, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        # """Handle PUT requests for a customer
        # Author: Dustin Hobson
        # Purpose: Allow a user to communicate with the Bangazon database to update  customer's 'is_active property
        # Methods:  PUT
        # Returns:
        #     Response -- Empty body with 204 status code
        # """
        user = User.objects.get(pk=request.auth.user.id)
        user.last_name = request.data["last_name"]
        user.save()

        player = Player.objects.get(user=user)
        player.zip_code = request.data["zip_code"]
        player.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def list(self, request):
        # """Handle GET requests to customers resource

        # Author: Dustin Hobson
        # Purpose: Allow a user to communicate with the Bangazon database to list Customers        Methods:  GET
        # Returns:
        #     Response -- JSON serialized list of park areas
        # """
        players = Player.objects.all()

        name = self.request.query_params.get('name', None)

        if name is not None:
            players = players.filter(user__first_name__iexact=name)

        serializer = PlayerSerializer(players, many=True, context={'request': request})

        return Response(serializer.data)