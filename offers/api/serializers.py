from offers.models import Offer, OfferDetail
from rest_framework import serializers


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
