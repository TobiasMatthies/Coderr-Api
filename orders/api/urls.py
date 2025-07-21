from django.urls import path
from . views import OrderListCreateAPIView, OrderUpdateDestroyAPIView

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderUpdateDestroyAPIView.as_view(), name='order-update-destroy'),
]
