from dataclasses import fields
from rest_framework import serializers
from ..models import Auction
from django.conf import settings
from users.models import CustomUser

class AuctionUserSerializer(serializers.ModelSerializer):
    #Custom serializer field to display a field of a relationship other than the pk
    #by default django in this cases will show the user's pk
    #StringRelatedField() could be used but that would return the user's email (or whatever the __str__ returns)
    #see https://www.django-rest-framework.org/api-guide/relations/ or https://stackoverflow.com/questions/15329301/django-rest-framework-define-fields-in-nested-object(solution used)
    class Meta:
        model = CustomUser
        fields = ["email", "username"]
        read_only_fields = ["email", "username"]

class AuctionDetailSerializer(serializers.ModelSerializer):
    user = AuctionUserSerializer()

    class Meta:
        model = Auction
        exclude = ['id']
        read_only_fields = ['publish_date','last_updated']

class AuctionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model= Auction
        exclude = ['id','publish_date', 'user', 'last_updated']