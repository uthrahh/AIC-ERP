from django.urls import path
from accounts.views import (
    UserLoginView,
    UserLogoutView,
    ChangePasswordView,
)
from accounts.views import applicant_register

app_name = "accounts"

urlpatterns = [
    path(
        "login/",
        UserLoginView.as_view(),
        name="login",
    ),

    path(
        "logout/",
        UserLogoutView.as_view(),
        name="logout",
    ),

    path(
        "password/change/",
        ChangePasswordView.as_view(),
        name="change_password",
    ),
    path(
        "register/",
        applicant_register,
        name="register"
    ),
]