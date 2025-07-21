from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.api.permissions import IsCustomerUser
from orders.models import Order
from . permissions import IsBusinessOwner
from . serializers import OrderSerializer
# Create your views here.


class OrderListCreateAPIView(ListCreateAPIView):
    serializer_class = OrderSerializer

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


class OrderUpdateDestroyAPIView(UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ['patch', 'delete']

    def get_permissions(self):
        if self.request.method in ['PATCH']:
            return [IsBusinessOwner()]
        if self.request.method in ['DELETE']:
            return [IsAdminUser()]

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(self.queryset, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
