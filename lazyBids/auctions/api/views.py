import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from bids.models import Bid
from .pagination import AuctionsPagination
from .permissions import IsAuthorizedOrReadOnly
from ..models import Auction
from .serializers import AuctionDetailSerializer, AuctionCreateSerializer, AuctionWinnerSerializer
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from django.conf import settings

#https://www.django-rest-framework.org/api-guide/generic-views/#generic-views

class AuctionView(APIView):

    def get(self, request):

        
        return Response("Successfull")

class CurrenciesView(APIView):
        def get(self, request):
                response = []
                for element in settings.CURRENCIES:
                        response.append({'currency_name':element[1], 'ISO':element[0]})

                return Response(response)



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

class AuctionWinnerView(generics.RetrieveUpdateAPIView):
        
        queryset = Auction.objects.filter(is_open=True)
        serializer_class = AuctionWinnerSerializer
        lookup_field = "uuid"

        def update(self, request, *args, **kwargs):

            try:
                bid = Bid.objects.get(uuid=request.data.get('bid_uuid'))
            except ObjectDoesNotExist:
                return Response({'bid_uuid': 'No matching bid has been found with this uuid'},
                            status=status.HTTP_404_NOT_FOUND)

            bid.has_won = True
            bid.save(update_fields=['has_won'])
            return super().update(request, *args, **kwargs)

        def perform_update(self, serializer):
            serializer.save(is_open=False)

        def retrieve(self, request, *args, **kwargs):
                auction = self.get_object()

                bid = Bid.objects.get(uuid=request.data.get('bid_uuid'))
                
                return Response({'auction_uuid': auction.uuid, 'winner_uuid':bid.uuid})
                

        

def get_authenticated_user(request):
        token = request.headers.get("Authorization").split()
        return token[1]


# TODO: implement validators in serializers