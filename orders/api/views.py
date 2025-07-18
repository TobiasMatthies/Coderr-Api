from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from orders.models import Order
from . serializers import OrderListCreateSerializer
# Create your views here.


class OrderListCreateAPIView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer_user=self.request.user)
