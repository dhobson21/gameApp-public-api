"""
   Author: Dustin Hobson
   Purpose: To convert message data to json
   Methods: GET, POST
"""

"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from capstone.models import Message
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from capstone.models import Event, Player
from .event import EventSerializer
from .player import PlayerSerializer


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    event = EventSerializer(many=False)
    sender = PlayerSerializer(many=False)
    reciever = PlayerSerializer(many=False)
    class Meta:
        model = Message
        url = serializers.HyperlinkedIdentityField(
            view_name='message',
            lookup_field='id'
        )
        fields = ('id', 'url', 'event','sender','reciever','message', 'open_time')
        depth = 2


class Messages(ViewSet):
    """Message View for game app"""
    # permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized product category instance
        """
        new_message = Message()
        new_message.event = Event.objects.get(pk=request.data["event"])
        new_message.sender = Player.objects.get(user=request.auth.user)
        # Will need to attach id of original message sender to approve/disprove btn to send back as participant
        new_message.reciever = Player.objects.get(pk=request.data["participant"])
        new_message.message = request.data["message"]

        serializer = MessageSerializer(new_message, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single message

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            message = Message.objects.get(pk=pk)
            serializer = MessageSerializer(message, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to game Categories resource

        Returns:
            Response -- JSON serialized list of park ProductCategorys
        """
        player = Player.objects.get(user=request.auth.user)
        messages = Message.objects.filter(reciever=player)

        serializer = MessageSerializer(
            messages, many=True, context={'request': request})
        return Response(serializer.data)




        # NEED TO FIGURE OUT GAMES API TO GAMES AND HOW TO GET JUST YOUR MESSAGES
        # I THINK I NEED TO POST TO REGISTER TO GET AN AUTH KEY AND USE THAT TO PULL MESSAGEES/GAMES THAT BELONG TO USER