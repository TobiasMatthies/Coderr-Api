from rest_framework import serializers
from reviews.models import Review


class ReviewListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'reviewer']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate(self, data):
        reviewer = self.context['request'].user
        business_user = data['business_user']

        if business_user.type != 'business':
            raise serializers.ValidationError("The business user must be of type 'business'.")

        if Review.objects.filter(business_user=business_user, reviewer=reviewer).exists():
            raise serializers.ValidationError("You have already reviewed this business user.")

        return data

    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)


class ReviewUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'business_user', 'reviewer', 'created_at', 'updated_at']

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
