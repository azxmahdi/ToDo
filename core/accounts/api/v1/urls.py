from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from . import views

app_name = "api-v1"

urlpatterns = [
    path(
        "registration/", views.RegistrationView.as_view(), name="registration"
    ),
    path("token/login/", views.LoginView.as_view(), name="login"),
    path("token/logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "email/confirm/<str:token>/",
        views.EmailConfirmView.as_view(),
        name="email-confirm",
    ),
    path(
        "email/resend/confirm/",
        views.EmailResendConfirmView.as_view(),
        name="email-resend-confirm",
    ),
    path(
        "change-password/",
        views.ChangePasswordView.as_view(),
        name="change-password",
    ),
    path("profile/", views.ProfileView.as_view(), name="profile"),
]
