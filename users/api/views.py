from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView
from users.api.serializers import UserRegistrationSerializer, ProfileSerializer, ProfileListSerializer
from users.api.permissions import IsOwner
from users.models import Profile


class RegistrationAPIView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handle user registration and return an authentication token.

        Validates the registration data using the UserRegistrationSerializer.
        If the data is valid, a new user is created and a token is generated
        for the user. Returns a response containing the token and user details.
        """

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


class LoginAPIView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handle user login and return an authentication token.

        Validates the login data using the serializer.
        If the data is valid, a token is generated for the user.
        Returns a response containing the token and user details.
        """
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


class ProfileRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """
    View to retrieve and update user profile.
    """

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method in ['PUT', 'PATCH']:
            return [IsOwner()]
        return super().get_permissions()

    def get_object(self):
        user_id = self.kwargs.get("id")
        profile = get_object_or_404(self.queryset, user__id=user_id)
        self.check_object_permissions(self.request, profile)
        return profile


class ProfileListAPIView(ListAPIView):
    """
    View to list all user profiles based on the given url parameter.
    """

    serializer_class = ProfileListSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return a queryset of user profiles filtered by profile type.

        Retrieves the profile type from the URL parameters and filters the
        Profile queryset accordingly. If the profile type is 'business',
        returns profiles of business users. If the profile type is 'customer',
        returns profiles of customer users.
        """

        profile_type = self.kwargs.get("profile_type")

        if profile_type == "business":
            return Profile.objects.filter(user__type="business")
        elif profile_type == "customer":
            return Profile.objects.filter(user__type="customer")
