"""
   Author: Dustin Hobson
   Purpose: To convert player events data to json
   Methods: GET, DELETE, POST
"""

"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from capstone.models import PlayerEvent, Player, Event
from .player import PlayerSerializer
import datetime


class PlayerEventSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    player = PlayerSerializer(many=False)
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
        # FIGURE THIS OUT
        # try:
        #     neworder = Order.objects.get(customer=customer, payment_type__isnull=True)
        # except Order.DoesNotExist:
        #     neworder = Order()
        #     neworder.created_date = datetime.date.today()
        #     neworder.customer = customer
        #     neworder.save()



        new_player_event.event.save()
        # if order.payment_type is not "NULL":
        #     ordered_items = order.invoiceline.all()

        #     for oi in ordered_items:
        #         ordered_products.add(oi.product)

        #     products = list(ordered_products)

        #     for p in products:
        #         num_sold = p.item.filter(order=order).count()
        #         p.quantity = p.new_inventory(num_sold)
        #         p.save()

        serializer = PlayerEventSerializer(new_player_event, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single player event instance

        Returns:
            Response -- JSON serialized player event instance
        """
        try:
            player_event = PlayerEvent.objects.get(pk=pk)
            serializer = PlayerEvent(player_event, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area ItineraryItem

        Returns:
            Response -- Empty body with 204 status code
        """
        new_player_event = PlayerEvent.objects.get(pk=pk)
        new_player_event.is_approved = request.data["is_approved"]
        new_player_event.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single player event

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            player_event = PlayerEvent.objects.get(pk=pk)
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
        # ordered_products = set()

        # Support filtering OrderProducts by area id
        # area = self.request.query_params.get('area', None)
        # if area is not None:
        #     OrderProducts = OrderProducts.filter(area__id=area)
        # productId = self.request.query_params.get('product_id', None)
        # order = self.request.query_params.get('order_id', None)
        # if order is not None:
        #     OrderProducts = OrderProducts.filter(order__id=order)
        #     # if productId is None:
            #     for op in OrderProducts:
            #         ordered_products.add(op.product)

            #     product_items = list(ordered_products)

            #     for p in product_items:
            #         num = p.item.filter(order__id=order).count()
            #         p.new_cart(num)
            #         p.save()

        # if productId is not None:
        #     OrderProducts = OrderProducts.filter(product__id=productId)

        serializer = PlayerEventSerializer(
            playerEvents, many=True, context={'request': request})
        return Response(serializer.data)
