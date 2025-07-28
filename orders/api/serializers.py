from rest_framework import serializers
from offers.models import OfferDetail
from orders.models import Order

class OrderSerializer(serializers.ModelSerializer):
    business_user = serializers.PrimaryKeyRelatedField(source='offerdetail.offer.user', read_only=True)
    title = serializers.ReadOnlyField(source='offerdetail.title')
    revisions = serializers.ReadOnlyField(source='offerdetail.revisions')
    delivery_time_in_days = serializers.ReadOnlyField(source='offerdetail.delivery_time_in_days')
    price = serializers.ReadOnlyField(source='offerdetail.price')
    features = serializers.ReadOnlyField(source='offerdetail.features')
    offer_type = serializers.ReadOnlyField(source='offerdetail.offer_type')
    offer_detail_id = serializers.PrimaryKeyRelatedField(queryset=OfferDetail.objects.all(), write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'status', 'created_at', 'updated_at', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'offer_detail_id']
        read_only_fields = ['id', 'created_at', 'updated_at', 'customer_user']

    def create(self, validated_data):
        """
        Create a new order instance.

        Creates a new Order instance with the customer user as the request user, the given offer detail and the validated data.
        Returns the created order instance.
        """
        offer_detail = validated_data.pop('offer_detail_id')
        order = Order.objects.create(customer_user=self.context['request'].user, offerdetail = offer_detail, **validated_data)
        return order

    def get_fields(self):
        """
        Customize fields for the serializer based on the request method.

        If the request method is 'PATCH', set all fields to read-only except 'status'.
        Returns the modified fields.
        """

        fields = super().get_fields()
        request = self.context.get('request', None)

        if request and request.method == 'PATCH':
            for field_name in fields:
                if field_name != 'status':
                    fields[field_name].read_only = True

        return fields
