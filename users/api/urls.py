from django.urls import path, include
from users.views import RegistrationView, LoginView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
]
