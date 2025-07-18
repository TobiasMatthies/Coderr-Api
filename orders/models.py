from django.db import models
from users.models import User
from offers.models import OfferDetail

# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    offerdetail = models.ForeignKey(OfferDetail, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='in_progress',
        help_text="Current status of the order"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
