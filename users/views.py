from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.exceptions import NotFound
from users.api.serializers import UserRegistrationSerializer, ProfileSerializer
from users.models import Profile

# Create your views here.


class RegistrationView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
                "username": user.username,
            }
        )


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
                "username": user.username,
            }
        )


class ProfileRetrieveUpdateView(RetrieveUpdateAPIView):
    """
    View to retrieve and update user profile.
    """

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        user_id = self.kwargs.get("id")
        profile = get_object_or_404(self.queryset, user__id=user_id)
        return profile
