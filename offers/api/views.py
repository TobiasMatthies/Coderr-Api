from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from offers.api.serializers import OfferSerializer
from offers.models import Offer

class OfferViewSet(ModelViewSet):
    """
    API view to list and create offers.
    """
    queryset = Offer.objects.all().prefetch_related('details')
    serializer_class = OfferSerializer
    pagination_class = PageNumberPagination
