from rest_framework import serializers
from users.models import User, Profile


class UserRegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "repeated_password", "type"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        if attrs["type"] not in dict(User.TYPE_CHOICES):
            raise serializers.ValidationError({"type": "Invalid user type."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            type=validated_data["type"],
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    firstname = serializers.CharField(source="user.first_name", read_only=True)
    lastname = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "description",
            "location",
            "tel",
            "working_hours",
            "user",
            "username",
            "email",
            "type",
            "firstname",
            "lastname",
            "created_at",
        ]
