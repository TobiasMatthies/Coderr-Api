from .views import OfferListCreateAPIView
from django.urls import path

urlpatterns = [
    path('offers/', OfferListCreateAPIView.as_view(), name='offer-list-create'),
]
