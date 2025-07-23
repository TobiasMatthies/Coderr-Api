from django.urls import path
from . views import ReviewListCreateAPIView, ReviewUpdateDestroyAPIView

urlpatterns = [
    path('reviews/', ReviewListCreateAPIView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewUpdateDestroyAPIView.as_view(), name='review-update-destroy'),
]
