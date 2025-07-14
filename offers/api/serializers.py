from offers.models import Offer, OfferDetail
from rest_framework import serializers
from users.api.serializers import UserDetailsSerializer


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'offer', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']
        read_only_fields = ('id', 'offer')


class OfferDetailLinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'url']
        extra_kwargs = {
            'url': {'view_name': 'offerdetail', 'lookup_field': 'pk'}
        }


class OfferListCreateSerializer(serializers.ModelSerializer):
    user_details = UserDetailsSerializer(source='user', read_only=True)
    details = OfferDetailSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'min_price', 'min_delivery_time', 'user_details', 'details']
        read_only_fields = ('created_at', 'updated_at', 'min_price', 'min_delivery_time', 'user')


    def create(self, validated_data):
        detail_data = validated_data.pop('details')
        user = self.context['request'].user

        offer = Offer.objects.create(user=user, **validated_data)
        for detail in detail_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer


    def get_min_price(self, instance):
        detail_data = instance.details.all()
        return  min(detail.price for detail in detail_data)


    def get_min_delivery_time(self, instance):
        detail_data = instance.details.all()
        return min(detail.delivery_time_in_days for detail in detail_data)


    def validate(self, data):
        offerdetails = data.get('details', [])

        if len(offerdetails) != 3:
            raise serializers.ValidationError("An offer must have exactly 3 details.")

        for type in ['basic', 'standard', 'premium']:
            for detail in offerdetails:
                offer_serializer = OfferDetailSerializer(data=detail)
                if not offer_serializer.is_valid():
                    raise serializers.ValidationError(f"Detail for {type} type is invalid: {offer_serializer.errors}")
                if not any(detail['offer_type'] == type for detail in offerdetails):
                    raise serializers.ValidationError(f"Offer must have a detail of type {type}.")

        return data


class OfferRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    details = OfferDetailLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details']
        read_only_fields = ('created_at', 'updated_at', 'min_delivery_time', 'user')
