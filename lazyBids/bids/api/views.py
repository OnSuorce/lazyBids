import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Bid
from auctions.models import Auction
from .serializers import *
from rest_framework import generics
from rest_framework.authtoken.models import Token

class BidTestView(APIView):

    def get(self, request):

        
        return Response("Successfull")


class BidListView(generics.ListAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidDetailSerializer
    permission_classes = []

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = BidDetailSerializer(queryset, many=True)
        
        return Response(serializer.data)


class BidCreateView(generics.CreateAPIView):

    queryset = Bid.objects.all()
    serializer_class = BidCreateSerializer
    permission_classes = []

    def perform_create(self, serializer):

        user = Token.objects.get(key=get_authenticated_user(self.request)).user
        print(self.request.data)
        auction = Auction.objects.get(uuid=self.request.data.get('uuid'))
        serializer.save(bidder=user,auction=auction)


def get_authenticated_user(request):
        token = request.headers.get("Authorization").split()
        return token[1]


# TODO: Add remove bid
# TODO: validate if bidding amount is higher than last bid or starting bid
# TODO: retrive list of bids based on the uuid parameter set in the body request
