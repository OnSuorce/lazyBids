from django.urls import path
from .views import *

urlpatterns = [
    path('test/',AuctionView.as_view(), name="test endpoint"),
    path('list/', AuctionListView.as_view()),
    path('', AuctionCreateView.as_view()),
    path('<uuid:uuid>/', AuctionDetailView.as_view()),
    path('currencies/', CurrenciesView.as_view()),
    path('<uuid:uuid>/winner/', AuctionWinnerView.as_view())


]