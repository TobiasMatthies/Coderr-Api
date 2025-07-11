from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from offers.api.serializers import OfferSerializer
from offers.models import Offer
from users.api.permissions import IsBusinessUser

class OfferViewSet(ModelViewSet):
    """
    API view to list and create offers.
    """
    queryset = Offer.objects.all().prefetch_related('details')
    serializer_class = OfferSerializer
    pagination_class = PageNumberPagination

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method in ['POST']:
            return [IsBusinessUser()]
        return super().get_permissions()
