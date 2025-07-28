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
        """
        Validate the given data.

        Checks that the given password and repeated password match.
        Also, checks that the given user type is valid.
        """
        if attrs["password"] != attrs["repeated_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        if attrs["type"] not in dict(User.TYPE_CHOICES):
            raise serializers.ValidationError({"type": "Invalid user type."})

        return attrs

    def create(self, validated_data):
        """
        Create a new user instance.

        Creates a new User instance with the given data.
        Returns the created user instance.
        """
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            type=validated_data["type"],
        )
        return user



class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    username = serializers.CharField(source="user.username", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
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
            "created_at",
            "first_name",
            "last_name",
            "email",
            "file",
        ]

    def update(self, instance, validated_data):
        """
        Update a Profile instance with the given validated data.

        Pops the user data from the validated data and updates the User instance with the given data.
        Then, updates the Profile fields with the remaining data.
        Finally, saves the Profile instance and returns it.
        """
        user_data = validated_data.pop("user", {})
        user = instance.user

        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.email = user_data.get("email", user.email)
        user.save()

        # Update Profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Customize the representation of the Profile instance.

        If any of the fields of the instance are empty, replace them with an empty string.
        This is to prevent the API from returning None for empty fields.
        """
        my_fields = self.fields.keys()
        data = super().to_representation(instance)
        for field in my_fields:
            try:
                if not data[field]:
                    data[field] = ""
            except KeyError:
                pass
        return data


class ProfileListSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    username = serializers.CharField(source="user.username", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

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
            "first_name",
            "last_name",
            "file",
        ]

    def to_representation(self, instance):
        """
        Customize the representation of the Profile instance.

        If any of the fields of the instance are empty, replace them with an empty string.
        This is to prevent the API from returning None for empty fields.
        """
        my_fields = self.fields.keys()
        data = super().to_representation(instance)
        for field in my_fields:
            try:
                if not data[field]:
                    data[field] = ""
            except KeyError:
                pass
        return data
