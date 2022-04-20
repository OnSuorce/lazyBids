from email import message
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Bid
from auctions.models import Auction
from .serializers import *
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from .permissions import IsAuthorizedOrReadOnly
from  django.core.exceptions import ObjectDoesNotExist

class BidTestView(APIView):

    def get(self, request):

        
        return Response("Successfull")


class BidListView(generics.ListAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidDetailSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        auction_uuid = request.query_params.get('auction_uuid')
        if(auction_uuid is None):
            message = {'auction_uuid':'auction_uuid parameter is mandatory'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        try:
            auction = Auction.objects.get(uuid=auction_uuid)
        except ObjectDoesNotExist:
            return Response({'auction_uuid':'No matching auction has been found with this uuid'},
             status=status.HTTP_404_NOT_FOUND)
        queryset = self.get_queryset().filter(auction=auction)
        serializer = BidDetailSerializer(queryset, many=True)
        
        return Response(serializer.data)


class BidCreateView(generics.CreateAPIView):

    queryset = Bid.objects.all()
    serializer_class = BidCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        user = Token.objects.get(key=get_authenticated_user(self.request)).user
        
        auction = Auction.objects.get(uuid=self.request.data.get('auction_uuid'))
        serializer.save(bidder=user,auction=auction)

class BidDetailView(generics.DestroyAPIView, generics.RetrieveAPIView):
        queryset = Bid.objects.all()
        serializer_class = BidDetailSerializer
        permission_classes = [IsAuthorizedOrReadOnly, IsAuthenticated ]
        lookup_field = "uuid"


def get_authenticated_user(request):
        token = request.headers.get("Authorization").split()
        return token[1]


# TODO: Add remove bid
# TODO: validate if bidding amount is higher than last bid or starting bid
# TODO: retrive list of bids based on the uuid parameter set in the body request
