from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from users.api.permissions import IsCustomerUser
from reviews.models import Review
from . filters import ReviewFilter
from .serializers import ReviewSerializer

class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = ReviewFilter
    ordering_fields = ['updated_at', 'rating']

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]
