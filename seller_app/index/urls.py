from django.contrib.auth.views import LoginView
from django.urls import path

from .forms import UserLoginForm
from .views import index

urlpatterns = [
    path("", index, name="index"),
    path(
        "login/",
        LoginView.as_view(authentication_form=UserLoginForm, template_name="seller/login.html"),
        name="login",
    ),
]
