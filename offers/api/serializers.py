from offers.models import Offer, OfferDetail
from rest_framework import serializers
from users.api.serializers import UserDetailsSerializer


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'offer', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferSerializer(serializers.ModelSerializer):
    user_details = UserDetailsSerializer(source='user', read_only=True)
    offer_details = OfferDetailSerializer(many=True, read_only=True, source='details')

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'min_price', 'min_delivery_time', 'user_details', 'offer_details']
        read_only_fields = ('created_at', 'updated_at')
