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
from capstone.models import Category
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    class Meta:
        model = Category
        url = serializers.HyperlinkedIdentityField(
            view_name='category',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name')


class Categories(ViewSet):
    """Game categories for game app Park"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # def create(self, request):
    #     """Handle POST operations

    #     Returns:
    #         Response -- JSON serialized product category instance
    #     """
    #     new_product_category = Category()
    #     new_product_category.name = request.data["name"]
    #     new_product_category.save()

    #     serializer = CategorySerializer(new_product_category, context={'request': request})

    #     return Response(serializer.data)

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
        category = Category.objects.all()

        serializer = CategorySerializer(
            category, many=True, context={'request': request})
        return Response(serializer.data)