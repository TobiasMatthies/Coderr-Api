from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from users.api.permissions import IsCustomerUser
from reviews.models import Review
from .serializers import ReviewSerializer

# Create your views here.
class ReviewListCreateAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAuthenticated(), IsCustomerUser()]
        return [IsAuthenticated()]
