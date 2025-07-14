from .views import OfferListCreateAPIView, OfferRetrieveUpdateDestroyAPIView
from django.urls import path

urlpatterns = [
    path('offers/', OfferListCreateAPIView.as_view(), name='offer-list-create'),
    path('offers/<int:pk>/', OfferRetrieveUpdateDestroyAPIView.as_view(), name='offer-detail'),
]
