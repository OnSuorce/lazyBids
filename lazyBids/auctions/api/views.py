from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Auction

class AuctionView(APIView):

    def get(self, request):

        return Response("Risposta")