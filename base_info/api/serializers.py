from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Review
from users.models import Profile
from offers.models import Offer

class BaseInfoSerializer(serializers.Serializer):
    review_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    business_profile_count = serializers.SerializerMethodField()
    offer_count = serializers.SerializerMethodField()

    def get_review_count(self, obj):
        """
        Return the total count of reviews.
        """
        return Review.objects.count()

    def get_average_rating(self, obj):
        """
        Return the average rating of all reviews.
        If no reviews exist, return 0.
        """
        average = Review.objects.aggregate(Avg('rating'))['rating__avg']
        return average if average is not None else 0

    def get_business_profile_count(self, obj):
        """
        Return the total count of business profiles.
        """

        return Profile.objects.filter(user__type='business').count()

    def get_offer_count(self, obj):
        """
        Return the total count of offers.
        """
        return Offer.objects.count()
