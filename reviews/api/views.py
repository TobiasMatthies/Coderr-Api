from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, GenericAPIView
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from users.api.permissions import IsCustomerUser
from reviews.models import Review
from . filters import ReviewFilter
from .serializers import ReviewListCreateSerializer, ReviewUpdateDestroySerializer
from . permissions import IsReviewOwner

class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListCreateSerializer
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_class = ReviewFilter
    ordering_fields = ['updated_at', 'rating']

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]


class ReviewUpdateDestroyAPIView(UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewUpdateDestroySerializer
    http_method_names = ['patch', 'delete']
    permission_classes = [IsReviewOwner, IsAuthenticated]

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
