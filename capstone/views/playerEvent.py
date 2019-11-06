"""
   Author: Dustin Hobson
   Purpose: To convert player events data to json
   Methods: GET, DELETE, POST
"""

"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
import json
from rest_framework import serializers
from rest_framework import status
from capstone.models import PlayerEvent, Player, Event, Message
from .player import PlayerSerializer
from .event import EventSerializer
import datetime


class PlayerEventSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    player = PlayerSerializer(many=False)
    event=EventSerializer(many=False)
    class Meta:
        model = PlayerEvent
        url = serializers.HyperlinkedIdentityField(
            view_name='playerevents',
            lookup_field='id'
        )
        fields = ('id', 'url', 'player', 'event', 'has_played', 'is_approved')
        depth = 2

class PlayerEvents(ViewSet):
    """Player Event for gameApp"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized product category instance
        """

        new_player_event = PlayerEvent()
        player = Player.objects.get(user=request.auth.user)
        new_player_event.player = player
        event = Event.objects.get(pk=request.data['event'])
        new_player_event.event = event

        new_player_event.has_played = request.data["has_played"]

        new_message = Message()
        new_message.event = event
        new_message.sender = player
        reciever = Player.objects.get(user=event.game.player_id)
        new_message.reciever = reciever
        new_message.open_time = None
        new_message.message = f'{player.user.username} has requested to join {event.name}. What would you like to do?'
        new_message.type='request'

        new_player_event.save()
        id=int(json.dumps(new_player_event.id))
        player_E= PlayerEvent.objects.get(pk=id)
        new_message.player_event =player_E


        new_message.save()


        serializer = PlayerEventSerializer(new_player_event, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single player event instance

        Returns:
            Response -- JSON serialized player event instance
        """
        try:
            player_event = PlayerEvent.objects.get(pk=pk)
            serializer = PlayerEventSerializer(player_event, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area ItineraryItem

        Returns:
            Response -- Empty body with 204 status code
        """
        new_player_event = PlayerEvent.objects.get(pk=pk)
        if request.data["is_approved"] == 'true':
            new_player_event.is_approved = True
            new_message = Message()
            event = Event.objects.get(pk=new_player_event.event.id)

            new_message.event = event
            sender = Player.objects.get(user=request.auth.user_id)
            reciever = Player.objects.get(user=new_player_event.player_id)
            new_message.reciever = reciever
            new_message.sender = sender
            new_message.open_time = None
            new_message.message = f'{sender.user.username} has approved you to join {event.name}. Event Has Been added to your calendar.'
            new_message.type = 'approve'

            new_player_event.save()
            new_message.save()
        else:
            new_message = Message()
            event = Event.objects.get(pk=new_player_event.event.id)
            new_message.event = event
            sender = Player.objects.get(user=request.auth.user_id)
            reciever = Player.objects.get(user=new_player_event.player_id)
            new_message.reciever = reciever
            new_message.sender = sender
            new_message.open_time = None
            new_message.message = f'{sender.user.username} has rejected your request to join {event.name}. Please explore other events!.'
            new_message.type = 'reject'
            new_message.save()
            new_player_event.save()
            new_player_event.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single player event

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            player_event = PlayerEvent.objects.get(pk=pk)
            if player_event.is_approved is True:
                host = Player.objects.get(user=player_event.event.game.player)
                event = Event.objects.get(pk=player_event.event.id)
                new_message = Message()
                new_message.reciever = host
                sender = Player.objects.get(user=request.auth.user)
                new_message.sender = sender
                new_message.event = event
                new_message.open_time = None
                new_message.message = f'{sender.user.username} dropped out of {player_event.event.name} and has been removed from the active player list.'
                new_message.type = 'leave'
                new_message.save()

            message_delete_list = Message.objects.filter(event=event)
            for message in message_delete_list:
                message.delete()
            player_event.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except player_event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to player event resource

        Returns:
            Response -- JSON serialized list of playerEvents
        """

        playerEvents = PlayerEvent.objects.all()


        unapproved = self.request.query_params.get('unapproved', None)
        if unapproved is not None:
            for player in playerEvents:
                playerEvents = playerEvents.filter(is_approved= False)

        serializer = PlayerEventSerializer(
            playerEvents, many=True, context={'request': request})
        return Response(serializer.data)
