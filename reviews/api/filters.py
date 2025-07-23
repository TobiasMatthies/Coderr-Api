import django_filters
from reviews.models import Review

class ReviewFilter(django_filters.FilterSet):
    reviewer_id = django_filters.NumberFilter(field_name='reviewer', lookup_expr='exact')
    business_user_id = django_filters.NumberFilter(field_name='business_user', lookup_expr='exact')

    class Meta:
        model = Review
        fields = ['reviewer_id', 'business_user_id']
