from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from offers.api.serializers import OfferListCreateSerializer, OfferRetrieveUpdateDestroySerializer
from offers.models import Offer
from users.api.permissions import IsBusinessUser, IsOwner

class OfferListCreateAPIView(ListCreateAPIView):
    """
    API view to list and create offers.
    """
    queryset = Offer.objects.all().prefetch_related('details')
    serializer_class = OfferListCreateSerializer
    pagination_class = PageNumberPagination

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

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsOwner()]
        return super().get_permissions()
