from django.urls import path
from .views import register

app_name = "applicants"

urlpatterns = [
    path(
        "register/",
        register,
        name="register"
    ),
]