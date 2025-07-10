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

class Profile(models.Model):
    """
    Profile model that extends the User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    description = models.TextField(blank=True, null=True, help_text='Short biography of the user.')
    location = models.CharField(max_length=50, blank=True, null=True, help_text='Location of the user.')
    tel = models.CharField(max_length=15, blank=True, null=True, help_text='Telephone number of the user.')
    working_hours = models.CharField(max_length=50, blank=True, null=True, help_text='Working hours of the user.')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Date and time when the profile was created.')
    file = models.FileField(upload_to='profile-picture/', blank=True, null=True)

    def __str__(self):
        return self.user.username
