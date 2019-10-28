"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from capstone.models import Player, Game, Event
from .game import GameSerializer
from .player import PlayerSerializer
from boardgamegeek import BGGClient, BGGRestrictSearchResultsTo, BGGChoose



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
            view_name='event',
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
            event1 = {}
            event1["id"]=event.id
            event1['name']=event.name
            event1['description']=event.description
            event1['address']=event.address
            event1['zip_code']=event.zip_code
            event1['date']=event.date
            event1['time']=event.time
            event1['recurring']=event.recurring
            event1['recurring_days']=event.recurring_days
            game1={}
            game1['name'] = event.game.name
            player = Player.objects.get(user=event.game.player.user)
            playerObj = PlayerSerializer(player, context={'request': request})
            game1['player'] = playerObj.data
            game1['host_descrip'] = event.game.host_descrip
            game1['max_players'] = BGGObj.max_players
            game1['min_players'] = BGGObj.min_players
            game1['categories'] = []
            for category in BGGObj.categories:
                game1['categories'].append(category)
            game1['image'] = BGGObj.image
            game1['thumb_nail'] = BGGObj.thumbnail
            event1['game'] = game1
            return Response(event1)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area

        Returns:
            Response -- Empty body with 204 status code
        """
        event = Event.objects.get(pk=pk)
        event.name = request.data["name"]
        # game = game.objects.get(pk=request.data["game"])
        # event.game = game
        event.description = request.data["description"]
        event.address = request.data["address"]
        event.zip_code = request.data["zip_code"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        event.recurring = request.data["recurring"]
        event.recurring_days = request.data["recurring_days"]

        event.save()



        # ordered_products = set()
        # order = Order.objects.get(pk=pk)
        # payment = Payment.objects.get(pk=request.data["payment_type"])
        # order.payment_type = payment
        # order.save()
        # if order.payment_type is not "NULL":
        #     ordered_items = order.invoiceline.all()

        #     for oi in ordered_items:
        #         ordered_products.add(oi.product)

        #     products = list(ordered_products)

        #     for p in products:
        #         num_sold = p.item.filter(order=order).count()
        #         p.quantity = p.new_inventory(num_sold)
        #         p.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single event

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            event = Event.objects.get(pk=pk)
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
        events = Event.objects.all()
        bgg = BGGClient()
        event_list = []



        for event in events:

            BGGObj = bgg.game(game_id=str(event.game.game))
            event1={}
            event1["id"]=event.id
            event1['name']=event.name
            event1['description']=event.description
            event1['address']=event.address
            event1['zip_code']=event.zip_code
            event1['date']=event.date
            event1['time']=event.time
            event1['recurring']=event.recurring
            event1['recurring_days']=event.recurring_days
            game1={}
            game1['host_name'] = event.game.name
            player = Player.objects.get(user=event.game.player.user)
            playerObj = PlayerSerializer(player, context={'request': request})
            game1['player'] = playerObj.data
            game1['host_descrip'] = event.game.host_descrip
            game1['max_players'] = BGGObj.max_players
            game1['min_players'] = BGGObj.min_players
            game1['categories'] = []
            for category in BGGObj.categories:
                game1['categories'].append(category)
            game1['image'] = BGGObj.image
            game1['thumb_nail'] = BGGObj.thumbnail
            event1['game'] = game1
            event_list.append(event1)

        # game = self.request.query_params.get('game', None)
        # zip_code = self.request.query_params.get('zip_code', None)
        # category = self.request.query_params.get('payment_id', None)
        # if customer is not None:
        #     if complete == "0":
        #         orders = orders.filter(customer__id=customer, payment_type__id__isnull=True)
        #     if complete == "1":
        #         orders = orders.filter(customer__id=customer, payment_type__id__isnull=False)

        # if payment is not None:
        #     orders = orders.filter(payment_type__id=payment)
        # if complete is not None:
        #     print("EEEEEEEEEEEEEEEEEEEEEEEEEEEE")
        #     if complete == "1":
        #         orders = orders.filter(payment_type__id__isnull=False)
        #     elif complete == "0":
        #         orders = orders.filter(payment_type__id__isnull=True)

        # serializer = EventSerializer(
        #     events, many=True, context={'request': request})
        return Response(event_list)
