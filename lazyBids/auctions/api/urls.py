from django.urls import path
from .views import *

urlpatterns = [
    path('test/',AuctionView.as_view()),
    path('', AuctionListView.as_view()),
    path('create', AuctionCreateView.as_view()),
    path('<int:pk>', AuctionRemoveView.as_view())

]