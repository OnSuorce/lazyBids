from rest_framework import serializers
from ..models import Bid
from users.models import CustomUser

class BidderSerializer(serializers.ModelSerializer):
    #Custom serializer field to display a field of a relationship other than the pk
    #by default django in this cases will show the user's pk
    #StringRelatedField() could be used but that would return the user's email (or whatever the __str__ returns)
    #see https://www.django-rest-framework.org/api-guide/relations/ or https://stackoverflow.com/questions/15329301/django-rest-framework-define-fields-in-nested-object(solution used)
    class Meta:
        model = CustomUser
        fields = ["email", "username"]
        read_only_fields = ["email", "username"]

class BidDetailSerializer(serializers.ModelSerializer):
    bidder = BidderSerializer()

    class Meta:
        model = Bid
        exclude = ['id']
        read_only_fields = ['publish_date']

class BidCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model= Bid
        fields = ['amount']