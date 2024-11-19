from django.urls import path, include
from .views import *

app_name = "accounts"

urlpatterns = [
    path("api/v1/", include("accounts.api.v1.urls"), name="api-v1"),
    path("login/", SignInView.as_view(), name="sign_in"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("sign_up/", SignUpView.as_view(), name="sign_up"),
]
