from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """
    TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('business', 'Business'),
    )

    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='customer',
        help_text='Type of user, either customer or business.'
    )
