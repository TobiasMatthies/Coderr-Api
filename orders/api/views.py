from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.api.permissions import IsCustomerUser
from orders.models import Order
from users.models import User
from . permissions import IsBusinessOwner
from . serializers import OrderSerializer


class OrderListCreateAPIView(ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsCustomerUser()]
        if self.request.method in ['GET']:
            return [IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        """
        Return a queryset of all orders that are associated with the current user either as the customer or as the business owner.

        :return: A queryset of Order objects
        :rtype: QuerySet
        """
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


class BaseOrderCountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    count_key_name = 'count'  # Default key name

    def get_queryset(self, pk=None, status=None):
        """
        Get the queryset of orders for the given user and status.
        """
        if pk is not None:
            get_object_or_404(User, pk=pk, type='business')
            queryset = Order.objects.filter(offerdetail__offer__user=pk)
            if status:
                queryset = queryset.filter(status=status)
            return queryset
        return Order.objects.all()

    def get(self, request, *args, **kwargs):
        """
        Return the count of orders for the given user and status.
        """
        queryset = self.get_queryset(*args, **kwargs)
        count = queryset.count()
        return Response({self.count_key_name: count})


class OrderCountAPIView(BaseOrderCountAPIView):
    count_key_name = 'order_count'

    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        return super().get_queryset(pk=pk, status='in_progress')


class CompletedOrderCountAPIView(BaseOrderCountAPIView):
    count_key_name = 'completed_order_count'

    def get_queryset(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        return super().get_queryset(pk=pk, status='completed')
