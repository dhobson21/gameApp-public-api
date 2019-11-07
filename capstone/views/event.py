"""View module for handling requests about park areas"""
import json
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from capstone.models import Player, Game, Event, PlayerEvent, Message
from .game import GameSerializer
from .player import PlayerSerializer
# from .playerEvent import PlayerEventSerializer
from boardgamegeek import BGGClient, BGGRestrictSearchResultsTo, BGGChoose
import datetime
from datetime import date
import pytz





'''
auther: Dustin Hobson
purpose: Allow a user to communicate with the gameApp database to GET PUT POST and DELETE event entries.
methods: all
'''

class EventSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for order

    Arguments:
        serializers
    """



    class Meta:
        model = Event
        url = serializers.HyperlinkedIdentityField(
            view_name='events',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'game', 'description', 'address', 'zip_code', 'date', 'time', 'recurring', 'recurring_days')
        depth = 3


class Events(ViewSet):
    """Create Event for gameApp"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Event instance
        """
        new_event = Event()
        new_event.name = request.data['name']
        new_event.description = request.data['description']
        new_event.address = request.data['address']
        new_event.zip_code = request.data['zip_code']
        new_event.date = request.data['date']
        new_event.time = request.data['time']
        new_event.recurring = request.data['recurring']
        new_event.recurring_days = request.data['recurring_days']

        game = Game.objects.get(pk=request.data["game"])
        new_event.game = game
        new_event.save()





        # When event created, also create PlayerEvent for event host

        new_player_event = PlayerEvent()
        player = Player.objects.get(user=request.auth.user)
        new_player_event.player = player
        event = Event.objects.get(pk= int(json.dumps(new_event.id)))
        new_player_event.has_played = request.data['has_played']
        new_player_event.is_approved = "True"
        new_player_event.event = event

        new_player_event.save()

        serializer = EventSerializer(new_event, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for order

        Returns:
            Response -- JSON serialized order
        """
        try:

            event = Event.objects.get(pk=pk)


            bgg = BGGClient()


            BGGObj = bgg.game(game_id=str(event.game.game))
            event1={}
            event1["id"]=event.id
            event1['name']=event.name
            event1['description']=event.description
            event1['address']=event.address
            event1['zip_code']=event.zip_code
            # event1['date']=event.date
            event1['date']=event.date.strftime("%a %b %d, %Y")
            event1['real_date']=event.date
            event1['time']=event.time
            event1['recurring']=event.recurring
            event1['recurring_days']=event.recurring_days

            # Creating custom game object out of BGG API and game info from user
            game1={}
            game1['name'] = event.game.name
            player = Player.objects.get(user= event.game.owner.user.id)
            playerObj = PlayerSerializer(player, context={'request': request})
            game1['owner'] = playerObj
            game1['owner_descrip'] = event.game.host_descrip
            game1['min_players'] = BGGObj.min_players
            game1['max_players'] = BGGObj.max_players
            game1['categories'] = []
            for category in BGGObj.categories:
                game1['categories'].append(category)
            game1['image'] = BGGObj.image
            game1['thumb_nail'] = BGGObj.thumbnail
            event1['game'] = game1

            event1['need_players'] = event.need_players

            # Event model method compairing game max_players against player_list and returning a boolean of True if player_list >= max_players
            event1['is_full'] = event.is_full

            # sending request into event .user_player method to obtain info about logged in user to determine if they are a player on the player_list
            event.user_player = request
            event1['user_player'] = event.user_player

            event1['player_list'] = []

                # serializing each player in the event method that gathers a list of approved players----NOT SURE I TO DO THIS
            for player in event.player_list:
                playerObj = PlayerSerializer(player, context={'request': request})
                event1['player_list'].append(playerObj.data)


            return Response(event1)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area

        Returns:
            Response -- Empty body with 204 status code
        """
        event = Event.objects.get(pk=pk)
        for player in event.player_list:
            if  player.id is not request.auth.user_id:
                new_message = Message()
                reciever = Player.objects.get(user=player.user)
                new_message.reciever = reciever
                sender = Player.objects.get(user=request.auth.user)
                new_message.event = event
                new_message.sender = sender
                new_message.open_time = None
                new_message.message = f'{sender.user.username} has updated {event.name}. Please see new details of event below.'
                new_message.type = 'change'
                new_message.save()
        event.name = request.data["name"]
        # game = game.objects.get(pk=request.data["game"])
        # event.game = game
        event.description = request.data["description"]
        event.address = request.data["address"]
        event.zip_code = request.data["zip_code"]
        event.date = request.data["date"]
        event.time = request.data["time"]

        event.save()
        # Event Change Message Creation




        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single event

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            event = Event.objects.get(pk=pk)
            ep_list = PlayerEvent.objects.filter(event=event)
            for player in ep_list:
                if  player.id is not request.auth.user_id:
                    delete_message = Message()
                    delete_message.event = event
                    sender = Player.objects.get(user=event.game.player_id)
                    delete_message.sender = sender
                    reciever = Player.objects.get(user=player.player_id)
                    delete_message.reciever = reciever
                    delete_message.message = f'{event.game.player.user.username} has cancelled the {event.name} event scheduled for {event.date}. It has been removed from your events calendar'
                    delete_message.type = 'cancel'
                    delete_message.open_time = None
                    delete_message.save()
                player.delete()

            event.delete()







            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to events resource

        Returns:
            Response -- JSON serialized list of park areas
        """
        events = Event.objects.all().order_by("date")
        bgg = BGGClient()
        event_list = []
        new_list = []

        # Building my own event dictionary using BGG API and Event object created by user
        for event in events:

            BGGObj = bgg.game(game_id=str(event.game.game))
            event1={}
            event1["id"]=event.id
            event1['name']=event.name
            event1['description']=event.description
            event1['address']=event.address
            event1['zip_code']=event.zip_code
            event1['date']=event.date.strftime("%a %b %d, %Y")
            event1['real_date']=event.date
            event1['time']=event.time.strftime("%I:%M %p")
            event1['real_time']=event.time
            event1['recurring']=event.recurring
            event1['recurring_days']=event.recurring_days

            # Creating custom game object out of BGG API and game info from user
            game1={}
            game1['name'] = event.game.name
            player = Player.objects.get(user=event.game.player.user)
            playerObj = PlayerSerializer(player, context={'request': request})
            game1['owner'] = playerObj.data
            game1['owner_descrip'] = event.game.host_descrip
            game1['min_players'] = BGGObj.min_players
            game1['max_players'] = BGGObj.max_players
            game1['categories'] = []
            for category in BGGObj.categories:
                game1['categories'].append(category)
            game1['image'] = BGGObj.image
            game1['thumb_nail'] = BGGObj.thumbnail
            event1['game'] = game1

            event1['need_players'] = event.need_players

            # Event model method compairing game max_players against player_list and returning a boolean of True if player_list >= max_players
            event1['is_full'] = event.is_full
            event.pending_request = request
            event1['pending_request'] = event.pending_request

            # sending request into event .user_player method to obtain info about logged in user to determine if they are a player on the player_list
            event.user_player = request
            event1['user_player'] = event.user_player

            event1['player_list'] = []


            # serializing each player in the event method that gathers a list of approved players----NOT SURE I TO DO THIS
            for player in event.player_list:
                playerObj = PlayerSerializer(player, context={'request': request})
                event1['player_list'].append(playerObj.data)




            # comparing date of event to today's date. If event has happened--it is not added to event_list and sent back to user
            today = datetime.datetime.now(pytz.utc)
            compare = event1['date']
            if event.date >=today:
                event_list.append(event1)
        # query params for:
        #  getting events a user is participating in
        user_player = self.request.query_params.get('user_player', None)
        # getting events that have a game with a category query
        category = self.request.query_params.get('category', None)
        # getting events that are taking place in a zip code query
        zip_code = self.request.query_params.get('zip_code', None)
        # getting events that are playing a certain game
        game = self.request.query_params.get('game', None)
        # getting events that are not full
        is_full= self.request.query_params.get('is_full', None)


        user= self.request.query_params.get('user', None)

        # if there is any query_param then  query param fills up new_list and event_list becomes new list--if not, event_list stays event_list
        if self.request.query_params:


            if user_player is not None:
                for event in event_list:
                    if (str(event['user_player'])  == user_player) & (event not in new_list):
                        new_list.append(event)


            if category is not None:
                if user_player:
                    for event in new_list:
                        if category in event['game']['categories']:
                            pass
                        else:
                            new_list.remove(event)
                else:
                    for event in event_list:
                        for cat in event['game']['categories']:
                            if (str(cat) == str(category)) & (event not in new_list):
                                new_list.append(event)


            if zip_code is not None:
                if user_player:
                    for event in new_list:
                        if (str(event['zip_code']) == str(zip_code)):
                            pass
                        else:
                            new_list.remove(event)
                else:
                    for event in event_list:
                        if (str(event['zip_code']) == zip_code) & (event not in new_list):
                            new_list.append(event)

            if game is not None:
                if user_player:
                    for event in new_list :
                        if (event['game']['name'].lower() == game.lower()):
                            pass
                        else:
                            new_list.remove(event)
                else:
                    for event in event_list:
                        if (event['game']['name'].lower() == game.lower()) & (event not in new_list):
                            new_list.append(event)

            if user is not None:
                if user_player:
                    for event in new_list:
                        if (event['game']['owner']['user']['username'].lower() == user.lower()):
                            pass
                        else:
                            new_list.remove(event)
                else:
                    for event in event_list:
                        if (event['game']['owner']['user']['username'].lower() == user.lower()) & (event not in new_list):
                            new_list.append(event)

            if is_full is not None:
                if user_player:
                    for event in event_list:
                        if(str(event['is_full']) == is_full):
                            pass
                    else:
                        new_list.remove(event)
                else:

                    for event in event_list:
                        if(str(event['is_full']) == is_full) & (event not in new_list):
                            new_list.append(event)

            event_list = new_list

        else:
            pass
        return Response(event_list)
