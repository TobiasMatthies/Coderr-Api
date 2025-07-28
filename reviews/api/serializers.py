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
        """
        Validate the given data.

        Checks that the business user is of type 'business' and that the reviewer has not already reviewed this business user.
        """
        reviewer = self.context['request'].user
        business_user = data['business_user']

        if business_user.type != 'business':
            raise serializers.ValidationError("The business user must be of type 'business'.")

        if Review.objects.filter(business_user=business_user, reviewer=reviewer).exists():
            raise serializers.ValidationError("You have already reviewed this business user.")

        return data

    def create(self, validated_data):
        """
        Create a new review instance.

        Automatically assigns the current user as the reviewer of the review.
        Returns the created review instance.
        """

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
