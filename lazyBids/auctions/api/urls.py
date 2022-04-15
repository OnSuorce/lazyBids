from django.urls import path
from .views import *

urlpatterns = [
    path('test/',AuctionView.as_view())
]