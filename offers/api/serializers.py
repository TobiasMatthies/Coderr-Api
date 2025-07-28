from django.db.models import Min
from offers.models import Offer, OfferDetail
from rest_framework import serializers
from users.api.serializers import UserDetailsSerializer


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ["id", "title", "revisions", "delivery_time_in_days", "price", "features", "offer_type"]
        read_only_fields = ("id", "offer")

    def validate(self, data):
        """
        Validate the given data.
        Checks that the data contains a valid offer type.
        """
        if 'offer_type' not in data or data['offer_type'] not in ["basic", "standard", "premium"]:
            raise serializers.ValidationError("Invalid offer type. Must be one of 'basic', 'standard', 'premium'.")
        return data


class OfferDetailLinkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ["id", "url"]
        extra_kwargs = {
            "url": {"view_name": "offerdetail", "lookup_field": "pk"}
        }


class OfferBaseSerializer(serializers.ModelSerializer):
    user_details = UserDetailsSerializer(source="user", read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ["id", "user", "title", "image", "description", "created_at", "updated_at", "min_price", "min_delivery_time", "user_details", "details"]
        read_only_fields = ("created_at", "updated_at", "min_price", "min_delivery_time", "user")

    def get_min_price(self, instance):
        """
        Return the minimum price of the offer's details.

        If the instance has a min_price attribute, return it. Otherwise, calculate the minimum price of the offer's details using an aggregate query.
        """
        if hasattr(instance, "min_price"):
            return instance.min_price
        return instance.details.aggregate(min_price=Min('price'))['min_price']

    def get_min_delivery_time(self, instance):
        """
        Return the minimum delivery time of the offer's details.

        If the instance has a min_delivery_time attribute, return it.
        Otherwise, calculate the minimum delivery time of the offer's details
        using an aggregate query.
        """

        if hasattr(instance, "min_delivery_time"):
            return instance.min_delivery_time
        return instance.details.aggregate(min_delivery_time=Min('delivery_time_in_days'))['min_delivery_time']


class OfferListSerializer(OfferBaseSerializer):
    details = OfferDetailLinkSerializer(many=True, read_only=True)


class OfferCreateSerializer(OfferBaseSerializer):
    details = OfferDetailSerializer(many=True)

    def create(self, validated_data):
        """
        Create an offer and its details.

        Pop the details from the validated data and create an Offer with the remaining data.
        Then, create each of the details from the popped data and assign them to the offer.
        Finally, return the created offer.
        """
        detail_data = validated_data.pop("details")
        user = self.context["request"].user

        offer = Offer.objects.create(user=user, **validated_data)
        for detail in detail_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer


    def validate(self, data):
        """
        Validate the given data.

        Checks that the data contains exactly 3 details with distinct types.
        Also validates each detail using the OfferDetailSerializer.
        """
        offerdetails = data.get("details", [])

        if len(offerdetails) != 3:
            raise serializers.ValidationError("An offer must have exactly 3 details.")

        for type in ["basic", "standard", "premium"]:
            for detail in offerdetails:
                offerdetail_serializer = OfferDetailSerializer(data=detail)
                if not offerdetail_serializer.is_valid():
                    raise serializers.ValidationError(f"Detail for {type} type is invalid: {offerdetail_serializer.errors}")
                if not any(detail["offer_type"] == type for detail in offerdetails):
                    raise serializers.ValidationError(f"Offer must have a detail of type {type}.")

        return data



class OfferUpdateSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]
        read_only_fields = ("id", "created_at", "updated_at", "user",)

    def update(self, instance, validated_data):
        """
        Update the given offer instance with the validated data.

        Updates the offer with the given title, image, and description.
        Then, updates each of the offer's details with the given data.
        Returns the updated offer instance.
        """

        for attr, value in validated_data.items():
            if attr != "details":
                setattr(instance, attr, value)
        instance.save()

        details_data = validated_data.get("details", [])
        for detail_data in details_data:
            offer_detail = instance.details.get(offer_type=detail_data["offer_type"])
            for attr, value in detail_data.items():
                setattr(offer_detail, attr, value)
            offer_detail.save()

        return instance


class OfferRetrieveDestroySerializer(OfferBaseSerializer):
    details = OfferDetailLinkSerializer(many=True, read_only=True)

    class Meta(OfferBaseSerializer.Meta):
        fields = ["id", "user", "title", "image", "description", "created_at", "updated_at", "min_price", "min_delivery_time", "details"]
