from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from offers.api.serializers import OfferListCreateSerializer, OfferRetrieveDestroySerializer, OfferUpdateSerializer, OfferDetailSerializer
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
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = OfferFilter
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['updated_at']
    search_fields = ['title', 'description']

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

    def filter_queryset(self, queryset):
        allowed_ordering_fields = set(self.ordering_fields)
        allowed_search_fields = set(self.search_fields)

        ordering = self.request.query_params.get('ordering')
        if ordering:
            invalid_ordering_fields = {
                field for field in ordering.split(',')
                if field.lstrip('-') not in allowed_ordering_fields
            }
            if invalid_ordering_fields:
                raise ValidationError({
                    'ordering': f"Invalid ordering fields: {', '.join(invalid_ordering_fields)}"
                })

        search = self.request.query_params.get('search')
        if search:
            invalid_search_fields = {
                field for field in search.split(',')
                if field not in allowed_search_fields
            }
            if invalid_search_fields:
                raise ValidationError({
                    'search': f"Invalid search fields: {', '.join(invalid_search_fields)}"
                })

        return super().filter_queryset(queryset)


class OfferRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete an offer.
    """
    queryset = Offer.objects.all()
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return OfferUpdateSerializer
        return OfferRetrieveDestroySerializer

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
