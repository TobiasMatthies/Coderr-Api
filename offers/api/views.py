from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from offers.api.serializers import OfferListCreateSerializer
from offers.models import Offer
from users.api.permissions import IsBusinessUser

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
