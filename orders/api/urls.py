from django.urls import path
from . views import OrderListCreateAPIView, OrderUpdateDestroyAPIView, OrderCountAPIView, CompletedOrderCountAPIView

urlpatterns = [
    path('orders/', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderUpdateDestroyAPIView.as_view(), name='order-update-destroy'),
    path('order-count/<int:pk>/', OrderCountAPIView.as_view(), name='order-count/'),
    path('completed-order-count/<int:pk>/', CompletedOrderCountAPIView.as_view(), name='completed-order-count'),
]
