from offers.models import Offer, OfferDetail
from rest_framework import serializers
from users.api.serializers import UserDetailsSerializer


class OfferSerializer(serializers.ModelSerializer):
    user_details = UserDetailsSerializer(source='user', read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'min_price', 'min_delivery_time', 'user_details']
        read_only_fields = ('created_at', 'updated_at')
