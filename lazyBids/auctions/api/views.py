from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .pagination import AuctionsPagination
from .permissions import IsAuthorizedOrReadOnly
from ..models import Auction
from .serializers import AuctionDetailSerializer, AuctionCreateSerializer
from rest_framework import generics
from rest_framework.authtoken.models import Token

#https://www.django-rest-framework.org/api-guide/generic-views/#generic-views

class AuctionView(APIView):

    def get(self, request):

        
        return Response("Successfull")


class AuctionListView(generics.ListAPIView):
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = AuctionsPagination

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = AuctionDetailSerializer(self.paginate_queryset(queryset), many=True)
        
        return Response(self.get_paginated_response(serializer.data).data)


class AuctionCreateView(generics.CreateAPIView):
        queryset = Auction.objects.all()
        serializer_class = AuctionCreateSerializer
        permission_classes = [IsAuthenticated]

        def perform_create(self, serializer):
       
                user = Token.objects.get(key=get_authenticated_user(self.request)).user
                serializer.save(user=user)

class AuctionDetailView(generics.DestroyAPIView, generics.UpdateAPIView, generics.RetrieveAPIView):
        queryset = Auction.objects.all()
        serializer_class = AuctionDetailSerializer
        permission_classes = [IsAuthorizedOrReadOnly, IsAuthenticated]
        lookup_field = "uuid"


def get_authenticated_user(request):
        token = request.headers.get("Authorization").split()
        return token[1]


# TODO: implement pagination in auction list
# TODO: implement validators in serializers
# TODO: add view to return currencies