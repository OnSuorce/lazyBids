from django.urls import path
from .views import *

urlpatterns = [
    path('test/',AuctionView.as_view()),
    path('list/', AuctionListView.as_view()),
    path('', AuctionCreateView.as_view()),
    path('<uuid:uuid>/', AuctionDetailView.as_view())

]