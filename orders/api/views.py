from django.db.models import Q
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from users.api.permissions import IsCustomerUser
from orders.models import Order
from . serializers import OrderListCreateSerializer
# Create your views here.


class OrderListCreateAPIView(ListCreateAPIView):
    serializer_class = OrderListCreateSerializer

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsCustomerUser()]
        if self.request.method in ['GET']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = Order.objects.all()
        user = self.request.user

        queryset = queryset.filter(Q(customer_user=user) | Q(offerdetail__offer__user=user))
        return queryset
