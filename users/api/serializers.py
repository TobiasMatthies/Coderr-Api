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
    type = serializers.CharField(source="user.type", read_only=True)
    firstname = serializers.CharField(source="user.first_name", read_only=True)
    lastname = serializers.CharField(source="user.last_name", read_only=True)
    # Writeable user fields for update
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(source="user.email", required=False)

    class Meta:
        model = Profile
        fields = [
            "description",
            "location",
            "tel",
            "working_hours",
            "user",
            "username",
            "type",
            "firstname",
            "lastname",
            "created_at",
            "first_name",
            "last_name",
            "email",
        ]

    def update(self, instance, validated_data):
        user_data = {}
        user_fields = ["first_name", "last_name"]
        for field in user_fields:
            if field in validated_data:
                user_data[field] = validated_data.pop(field)

        # Handle email update separately
        user_dict = validated_data.pop("user", None)
        if user_dict and "email" in user_dict:
            user_data["email"] = user_dict["email"]
        # Update Profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # Update User fields
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        return instance
