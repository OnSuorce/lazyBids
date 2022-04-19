from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Auction
from .serializers import AuctionSerializer
from rest_framework import generics

class AuctionView(APIView):

    def get(self, request):

        return Response("Risposta")

class AuctionListView(generics.ListAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    permission_classes = []

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = AuctionSerializer(queryset, many=True)
        return Response(serializer.data)

class AuctionCreateView(generics.CreateAPIView):
        queryset = Auction.objects.all()
        serializer_class = AuctionSerializer
        permission_classes = []

class AuctionRemoveView(generics.DestroyAPIView, generics.UpdateAPIView):
        queryset = Auction.objects.all()
        serializer_class = AuctionSerializer
        permission_classes = []



        
# TODO: implement validators in serializers
# TODO: remove "is open" from register 
# TODO: write enum for currencies
# TODO: implement uuid
# TODO: add __str__ to auction model and bid model
# TODO: add retrieve to AuctionRemoveView and rename it
# TODO: add last_updated
# TODO: add status
