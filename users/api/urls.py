from django.urls import path, include
from users.views import RegistrationView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
]
