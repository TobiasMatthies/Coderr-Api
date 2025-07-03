from django.urls import path, include
from users.views import RegistrationView, LoginView, ProfileRetrieveUpdateView

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "profile/<int:id>",
        ProfileRetrieveUpdateView.as_view(),
        name="profile_retrieve_update",
    ),
]
