from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Bid
from auctions.models import Auction
from .serializers import *
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from .permissions import IsAuthorizedOrReadOnly
from django.core.exceptions import ObjectDoesNotExist
from .pagination import BidsPagination


class BidTestView(APIView):

    def get(self, request):

        return Response("Successfull")


class BidListView(generics.ListAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidDetailSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = BidsPagination

    def list(self, request):

        auction_uuid = request.query_params.get('auction_uuid')

        if(auction_uuid is None):

            return Response({'auction_uuid': 'auction_uuid parameter is mandatory'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            auction = Auction.objects.get(uuid=auction_uuid)
        except ObjectDoesNotExist:
            return Response({'auction_uuid': 'No matching auction has been found with this uuid'},
                            status=status.HTTP_404_NOT_FOUND)

        queryset = self.get_queryset().filter(auction=auction)
        serializer = BidDetailSerializer(self.paginate_queryset(queryset), many=True)

        return Response(self.get_paginated_response(serializer.data).data)


class BidCreateView(generics.CreateAPIView):

    queryset = Bid.objects.all()
    serializer_class = BidCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        user = Token.objects.get(key=get_authenticated_user(request)).user
        auction_uuid = request.data.get('auction_uuid')

        if auction_uuid is None:
            return Response({'auction_uuid': 'required auction_uuid parameter is missing'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            auction = Auction.objects.get(uuid=auction_uuid)
        except ObjectDoesNotExist:
            return Response({'auction_uuid': 'No matching auction has been found with this uuid'},
                            status=status.HTTP_404_NOT_FOUND)

        bids = Bid.objects.filter(auction=auction).order_by("-amount")
        if len(bids) > 0:
            highest_bid = bids[0]
            if request.data.get('amount') <= highest_bid.amount:
                return Response({'amount': f'amount has to be greater than the leading bid of: {highest_bid.amount}'},
                                status=status.HTTP_400_BAD_REQUEST)

        elif auction.starting_bid > request.data.get('amount'):
            return Response({'amount': f'amount has to be greater or equal than the starting bid'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, user, auction)

        return Response({
            'amount': request.data.get('amount'),
            'auction_uuid': auction_uuid},
            status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, user, auction):

        serializer.save(bidder=user, auction=auction)


class BidDetailView(generics.DestroyAPIView, generics.RetrieveAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidDetailSerializer
    permission_classes = [IsAuthorizedOrReadOnly, IsAuthenticated]
    lookup_field = "uuid"


def get_authenticated_user(request):
    token = request.headers.get("Authorization").split()
    return token[1]

# TODO: make a bid wins (using put in detail view)
# TODO: remove auction id