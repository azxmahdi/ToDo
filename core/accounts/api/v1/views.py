from rest_framework_simplejwt.tokens import RefreshToken
from mail_templated import EmailMessage 
from rest_framework import generics, status, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.urls import reverse
from django.conf import settings
from rest_framework.views import APIView
import jwt
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token 
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView
from ..utils import EmailThread
from .serializers import (
    RegistrationSerializer,
    ResendEmailConfirmSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    LoginSerializer,
    CustomTokenObtainPairSerializer,
)
from accounts.models import Profile


class RegistrationView(generics.GenericAPIView):
    """
    This API endpoint allows users to register a new account. Upon successful registration, an email confirmation link is sent to the user's email address.

    Args:
        request (HttpRequest): The HTTP request object containing the user's registration data.

    Returns:
        Response: A JSON response containing a message indicating whether the registration was successful or if there were any errors.

    Raises:
        ValidationError: If the provided registration data is invalid.
    """

    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            email = serializer.validated_data["email"]
            data = {
                "details": f"account {email} created. pleas check your email for verify account"
            }

            token = self.get_tokens_for_user(user)

            from_email = "your_email@example.com"
            recipient_list = [email]
            url = request.build_absolute_uri(
                reverse("accounts:api-v1:email-confirm", args=[token])
            )

            email_obj = EmailMessage(
                "email/send-mail-confirm.tpl",
                {"url": url},
                from_email,
                to=recipient_list,
            )

            EmailThread(email_obj).start()

            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


User = get_user_model()


class EmailConfirmView(APIView):
    """
    This API endpoint allows users to confirm their email address by providing the email confirmation token.

    Args:
        request (HttpRequest): The HTTP request object containing the user's email confirmation token.

    Returns:
        Response: A JSON response containing a message indicating whether the email address was successfully confirmed or if there were any errors.

    Raises:
        ValidationError: If the provided email confirmation token is invalid.
    """

    def get(self, request, token, *args, **kwargs):
        try:
            decoded = jwt.decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return Response(
                {"detail": "This token is expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.InvalidTokenError:

            return Response(
                {"detail": "This token is invalid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_id = decoded.get("user_id")

        try:
            user = User.objects.get(id=user_id)
            user.is_verified = True
            user.save()
            return Response(
                {"detail": "Account verified."}, status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )


class EmailResendConfirmView(generics.GenericAPIView):
    """
    This API endpoint allows users to resend the email confirmation link.

    Args:
        request (HttpRequest): The HTTP request object containing the user's email address and token.

    Returns:
        Response: A JSON response containing a message indicating whether the email confirmation link was successfully resend or if there were any errors.

    Raises:
        ValidationError: If the provided email address or token is invalid.
    """

    serializer_class = ResendEmailConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = serializer.validated_data["user"]

        token = self.get_tokens_for_user(user)
        from_email = "your_email@example.com"
        recipient_list = [email]
        url = request.build_absolute_uri(
            reverse("accounts:api-v1:email-confirm", args=[token])
        )

        email_obj = EmailMessage(
            "email/resend-mail-confirm.tpl",
            {"url": url},
            from_email,
            to=recipient_list,
        )

        EmailThread(email_obj).start()

        return Response({"detail": "Pleas check your email"})

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ChangePasswordView(generics.UpdateAPIView):
    """
    This API endpoint allows users to change their password.

    Args:
        request (HttpRequest): The HTTP request object containing the user's new password.

    Returns:
        Response: A JSON response containing a message indicating whether the password was successfully changed or if there were any errors.

    Raises:
        AuthenticationFailed: If the provided credentials are invalid.
    """

    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(self.object, data=request.data)

        serializer.is_valid(raise_exception=True)

        self.object.set_password(serializer.validated_data["new_password"])
        self.object.save()

        return Response(
            {"detail": "Password updated successfully!"},
            status=status.HTTP_200_OK,
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    This API endpoint allows users to retrieve and update their profile information.

    Args:
        request (HttpRequest): The HTTP request object containing the user's profile data.

    Returns:
        Response: A JSON response containing the user's profile information or a message indicating whether the profile was successfully updated or if there were any errors.

    Raises:
        AuthenticationFailed: If the provided credentials are invalid.
    """

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.queryset.get(user=self.request.user.id)


class LoginView(generics.GenericAPIView):
    """
    Allows users to log in by providing their username and password.

    Upon successful validation, the view returns a JSON response containing the user's authentication token and email.

    Args:
        request (HttpRequest): The HTTP request object containing the user's login credentials.

    Returns:
        Response: A JSON response containing the user's authentication token and email.

    Raises:
        AuthenticationFailed: If the provided credentials are invalid.
    """

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "email": user.email})


class LogoutView(APIView):
    """
    Logs out the user by deleting their authentication token.

    Args:
        request (HttpRequest): The HTTP request object containing the user's authentication token.

    Returns:
        Response: A JSON response containing a message indicating whether the logout was successful or if the token does not exist.

    Raises:
        AttributeError: If the user does not have an 'auth_token' attribute.
        Token.DoesNotExist: If the user's authentication token does not exist.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"detail": "Successfully logged out."}, status=200)
        except (AttributeError, Token.DoesNotExist):
            return Response({"detail": "Token does not exist."}, status=400)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom implementation of TokenObtainPairView for obtaining JWT tokens.

    This view allows users to obtain a JWT token pair by providing their username and password.

    Args:
        TokenObtainPairView (class): The base class for obtaining JWT token pair.
        serializer_class (class): A custom serializer class for handling token generation.

    Returns:
        A JSON response containing the access and refresh tokens.
    """

    serializer_class = CustomTokenObtainPairSerializer
