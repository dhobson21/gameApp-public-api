"""
   Author: Dustin Hobson
   Purpose: To convert game category data to json
   Methods: GET, POST
"""

"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from capstone.models import Category, Game
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from datetime import date
from datetime import time
from datetime import datetime


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    class Meta:
        model = Category
        url = serializers.HyperlinkedIdentityField(
            view_name='categories',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name')


class Categories(ViewSet):
    """Game categories for game app Park"""
    permission_classes = (IsAuthenticatedOrReadOnly,)



    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to game Categories resource

        Returns:
            Response -- JSON serialized list of park ProductCategorys
        """
        now = date.today()
        # This only returns game categories that have games that fill that category
        category = Category.objects.all()
        games = Game.objects.all()
        cat_set = set()
        for game in games:
            for id in game.category_ids:
                cat_set.add(id)
        new_cat = category.filter(pk__in=cat_set)

        serializer = CategorySerializer(
            new_cat, many=True, context={'request': request})
        return Response(serializer.data)