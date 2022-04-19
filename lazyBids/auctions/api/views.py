from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Auction
from .serializers import AuctionDetailSerializer, AuctionCreateSerializer
from rest_framework import generics
from rest_framework.authtoken.models import Token


class AuctionView(APIView):

    def get(self, request):

        
        return Response("Risposta")


class AuctionListView(generics.ListAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer
    permission_classes = []

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = AuctionDetailSerializer(queryset, many=True)
        
        return Response(serializer.data)


class AuctionCreateView(generics.CreateAPIView):
        queryset = Auction.objects.all()
        serializer_class = AuctionCreateSerializer
        permission_classes = []

        def perform_create(self, serializer):

               
                
                
                user = Token.objects.get(key=get_authenticated_user(self.request)).user
                serializer.save(user=user)

class AuctionRemoveView(generics.DestroyAPIView, generics.UpdateAPIView, generics.RetrieveAPIView):
        queryset = Auction.objects.all()
        serializer_class = AuctionDetailSerializer
        permission_classes = []


def get_authenticated_user(request):
        token = request.headers.get("Authorization").split()
        return token[1]


# TODO: implement pagination in auction list
# TODO: implement validators in serializers
# TODO: make only the owner to be able to update/remove his auctions
# TODO: implement uuid
# TODO: add __str__ to bid model
# TODO: add retrieve to AuctionRemoveView and rename it
# TODO: add last_updated