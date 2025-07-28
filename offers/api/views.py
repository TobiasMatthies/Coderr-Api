from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.exceptions import ValidationError
from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from offers.api.serializers import OfferListSerializer, OfferCreateSerializer, OfferRetrieveDestroySerializer, OfferUpdateSerializer, OfferDetailSerializer
from offers.models import Offer, OfferDetail
from users.api.permissions import IsBusinessUser, IsOwner
from offers.api.filters import OfferFilter
from . pagination import StandardResultsSetPagination

class OfferListCreateAPIView(ListCreateAPIView):
    """
    API view to list and create offers.
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = OfferFilter
    ordering_fields = ['updated_at', 'min_price']
    ordering = ['updated_at']
    search_fields = ['title', 'description']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferListSerializer

    def get_queryset(self):
        """
        Return a queryset of offers that are visible to the current user.
        """
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
        """
        Filter the queryset based on the given request query parameters.

        If the "ordering" query parameter is given, check that the given
        fields are valid ordering fields. If not, raise a ValidationError.

        Return the filtered queryset.
        """
        allowed_ordering_fields = set(self.ordering_fields)

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

        return super().filter_queryset(queryset)


class OfferRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete an offer.
    """
    queryset = Offer.objects.all()
    lookup_field = 'pk'

    def get_queryset(self):
        """
        Return a queryset of all offers, prefetched with their details,
        and annotated with the minimum price and delivery time of the
        offer's details.
        """
        queryset = Offer.objects.all().prefetch_related('details')
        queryset = queryset.annotate(min_price=Min('details__price'), min_delivery_time=Min('details__delivery_time_in_days'))
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return OfferUpdateSerializer
        return OfferRetrieveDestroySerializer

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [IsAuthenticated()]
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsBusinessUser(), IsOwner()]
        return super().get_permissions()


class OfferDetailRetrieveAPIView(RetrieveAPIView):
    """
    API view to retrieve offer details.
    """
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [IsAuthenticated]
