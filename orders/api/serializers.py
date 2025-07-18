from rest_framework import serializers
from orders.models import Order

class OrderListCreateSerializer(serializers.ModelSerializer):
    business_user = serializers.ReadOnlyField(source='offerdetail.offer.user)')
    title = serializers.ReadOnlyField(source='offerdetail.title')
    revisions = serializers.ReadOnlyField(source='offerdetail.revisions')
    delivery_time_in_days = serializers.ReadOnlyField(source='offerdetail.delivery_time_in_days')
    price = serializers.ReadOnlyField(source='offerdetail.price')
    features = serializers.ReadOnlyField(source='offerdetail.features')
    offer_type = serializers.ReadOnlyField(source='offerdetail.offer_type')

    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'status', 'created_at', 'updated_at', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']
        read_only_fields = ['id', 'created_at', 'updated_at', 'customer_user']

    def create(self, validated_data):
        user = self.context['request'].user
        order = Order.objects.create(customer_user=user, **validated_data)
        return order
