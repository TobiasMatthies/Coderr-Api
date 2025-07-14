from .views import OfferListCreateAPIView, OfferRetrieveUpdateDestroyAPIView, OfferDetailRetrieveAPIView
from django.urls import path

urlpatterns = [
    path('offers/', OfferListCreateAPIView.as_view(), name='offer-list-create'),
    path('offers/<int:pk>/', OfferRetrieveUpdateDestroyAPIView.as_view(), name='offer-retrieve-update-destroy'),
    path('offerdetails/<int:pk>/', OfferDetailRetrieveAPIView.as_view(), name='offerdetail'),
]
