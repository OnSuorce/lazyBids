from django.urls import path
from .views import *

urlpatterns = [
    path('test/',BidTestView.as_view()),
    path('list/', BidListView.as_view()),
    path('', BidCreateView.as_view()),


]