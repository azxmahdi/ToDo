from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import django.contrib.auth.password_validation as validators
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import Profile

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Validates the password and ensures it matches the confirmation password.
    """

    password = serializers.CharField(max_length=300, write_only=True)
    password1 = serializers.CharField(max_length=300, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password1"]

    def create(self, validated_data):
        """
        Create a new user with the provided email and password.

        Args:
            validated_data (dict): A dictionary containing the validated data.

        Returns:
            User: A newly created user object.
        """
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data)

    def validate(self, attrs):
        """
        Validate the password and ensure it matches the confirmation password.

        Args:
            attrs (dict): A dictionary containing the provided data.

        Raises:
            serializers.ValidationError: If the passwords do not match or if the password is invalid.

        Returns:
            dict: A dictionary containing the validated data.
        """
        password = attrs["password"]
        password1 = attrs["password1"]

        if password != password1:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )

        try:
            validate_password(password=password)
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return super().validate(attrs)


class ResendEmailConfirmSerializer(serializers.Serializer):
    """
    Serializer for resending email confirmation.

    Validates the provided email and ensures the user exists and is not verified.
    """

    email = serializers.EmailField()

    def validate(self, attrs):
        """
        Validate the provided email and ensure the user exists and is not verified.

        Args:
            attrs (dict): A dictionary containing the provided data.

        Raises:
            serializers.ValidationError: If the user does not exist or if the user is already verified.

        Returns:
            dict: A dictionary containing the validated data.
        """
        try:
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "This account is not exist."}
            )

        if user.is_verified:
            raise serializers.ValidationError(
                {"detail": "This account is already verified."}
            )

        attrs["user"] = user
        return super().validate(attrs)


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing the user's password.

    Validates the old password, new password, and new password confirmation.
    """

    old_password = serializers.CharField(max_length=300, write_only=True)
    new_password = serializers.CharField(max_length=300, write_only=True)
    new_password1 = serializers.CharField(max_length=300, write_only=True)

    def validate(self, attrs):
        """
        Validate the old password, new password, and new password confirmation.

        Args:
            attrs (dict): A dictionary containing the provided data.

        Raises:
            serializers.ValidationError: If the new passwords do not match or if the old password is invalid.

        Returns:
            dict: A dictionary containing the validated data.
        """
        new_password = attrs["new_password"]
        new_password1 = attrs["new_password1"]
        old_password = attrs["old_password"]

        if new_password != new_password1:
            raise serializers.ValidationError(
                {"new_password": "New passwords do not match."}
            )

        user = self.get_user()
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                {"old_password": "The old password is not correct."}
            )

        try:
            validators.validate_password(password=new_password)
        except ValidationError as e:
            raise serializers.ValidationError(
                {"new_password": list(e.messages)}
            )

        return super().validate(attrs)

    def get_user(self):
        """
        Get the user object based on the authenticated user.

        Returns:
            User: A user object.
        """
        return get_user_model().objects.get(pk=self.context["request"].user.id)


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the user's profile.

    Includes the user's email as a read-only field.
    """

    user = serializers.CharField(label="email", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "image",
            "description",
        ]


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    Validates the provided email and password and returns the user object and token pair.
    """

    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        max_length=300, write_only=True, required=True
    )

    def validate(self, attrs):
        """
        Validate the provided email and password and return the user object and token pair.

        Args:
            attrs (dict): A dictionary containing the provided data.

        Raises:
            serializers.ValidationError: If the user does not exist or if the user cannot be authenticated.

        Returns:
            dict: A dictionary containing the validated data and the user object.
        """
        email = attrs["email"]
        password = attrs["password"]

        user = authenticate(email=email, password=password)
        if not user:
            msg = _("Unable to log in with provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return super().validate(attrs)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for obtaining a token pair.

    Includes the user's email in the token response.
    """

    def validate(self, attrs):
        """
        Validate the provided email and password and return the user object and token pair.

        Args:
            attrs (dict): A dictionary containing the provided data.

        Raises:
            serializers.ValidationError: If the user does not exist or if the user cannot be authenticated.

        Returns:
            dict: A dictionary containing the validated data, the user object, and the token pair.
        """
        validated_data = super().validate(attrs)
        validated_data["email"] = self.user.email

        return validated_data
