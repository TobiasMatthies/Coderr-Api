import django_filters
from django.db.models import Count, Q
from offers.models import Offer

class OfferFilter(django_filters.FilterSet):
    creator_id = django_filters.NumberFilter(field_name='user', lookup_expr='exact')
    min_price = django_filters.NumberFilter(method='filter_min_price')
    max_delivery_time = django_filters.NumberFilter(method='filter_max_delivery_time')

    class Meta:
        model = Offer
        fields = ['creator_id', 'min_price', 'max_delivery_time']


    def filter_min_price(self, queryset, name, value):
        """
        Filter offers that have all 3 details with a price greater or
        equal to the given value.
        """
        return queryset.annotate(
            matching_details_count=Count(
                'details',
                filter=Q(details__price__gte=value)
            )
        ).filter(
            matching_details_count=3
        )

    def filter_max_delivery_time(self, queryset, name, value):
        """
        Filter offers that have all 3 details with a delivery time less than
        or equal to the given value.
        """
        return queryset.annotate(
            matching_details_count=Count(
                'details',
                filter=Q(details__delivery_time_in_days__lte=value)
            )
        ).filter(
            matching_details_count=3
        )
