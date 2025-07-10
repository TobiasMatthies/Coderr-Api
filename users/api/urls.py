from django.urls import path, register_converter
from .views import RegistrationAPIView, LoginAPIView, ProfileRetrieveUpdateAPIView, ProfileListAPIView
from .converters import ProfileTypeConverter

register_converter(ProfileTypeConverter, 'profiletype')

urlpatterns = [
    path("registration/", RegistrationAPIView.as_view(), name="registration"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path(
        "profile/<int:id>",
        ProfileRetrieveUpdateAPIView.as_view(),
        name="profile_retrieve_update",
    ),
    path('profiles/<profiletype:profile_type>/', ProfileListAPIView.as_view(), name='profiles-list'),
]
