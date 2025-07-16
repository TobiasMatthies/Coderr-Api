from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import OrderingFilter
from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from offers.api.serializers import OfferListCreateSerializer, OfferRetrieveUpdateDestroySerializer, OfferDetailSerializer
from offers.models import Offer, OfferDetail
from users.api.permissions import IsBusinessUser, IsOwner
from offers.api.filters import OfferFilter
from . pagination import StandardResultsSetPagination

class OfferListCreateAPIView(ListCreateAPIView):
    """
    API view to list and create offers.
    """
    serializer_class = OfferListCreateSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = OfferFilter
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['updated_at']

    def get_queryset(self):
        queryset =  Offer.objects.all().prefetch_related('details')
        queryset = queryset.annotate(min_price=Min('details__price'), min_delivery_time=Min('details__delivery_time_in_days'))
        return queryset

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method in ['POST']:
            return [IsBusinessUser()]
        return super().get_permissions()

class OfferRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete an offer.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferRetrieveUpdateDestroySerializer
    lookup_field = 'pk'

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [IsAuthenticated()]
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsOwner()]
        return super().get_permissions()


class OfferDetailRetrieveAPIView(RetrieveAPIView):
    """
    API view to retrieve offer details.
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
