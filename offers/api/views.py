from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from offers.api.serializers import OfferListCreateSerializer, OfferRetrieveUpdateDestroySerializer, OfferDetailSerializer
from offers.models import Offer, OfferDetail
from users.api.permissions import IsBusinessUser, IsOwner
from offers.api.filters import OfferFilter

class OfferListCreateAPIView(ListCreateAPIView):
    """
    API view to list and create offers.
    """
    queryset = Offer.objects.all().prefetch_related('details')
    serializer_class = OfferListCreateSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = OfferFilter

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
