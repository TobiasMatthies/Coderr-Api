from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from users.api.permissions import IsCustomerUser
from orders.models import Order
from . serializers import OrderListCreateSerializer
# Create your views here.


class OrderListCreateAPIView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListCreateSerializer

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsCustomerUser()]
        if self.request.method in ['GET']:
            return [IsAuthenticated()]
        return super().get_permissions()
