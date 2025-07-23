from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User


class Review(models.Model):
    business_user = models.ForeignKey(
        User,
        related_name='business_reviews',
        on_delete=models.CASCADE,
    )
    reviewer = models.ForeignKey(
        User,
        related_name='customer_reviews',
        on_delete=models.CASCADE,
    )
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business_user', 'reviewer')
