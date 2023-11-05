from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth import authenticate
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from core.models import User


class UserLoginForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "login-form"
        self.helper.attrs = {
            "hx-post": reverse_lazy("seller:login"),
            "hx-target": "#login-form",
            "hx-swap": "outerHTML",
        }
        self.helper.add_input(
            Submit(
                "submit",
                _("Login"),
                css_class="w-100 btn btn-lg btn-primary",
            )
        )

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError(_("Invalid credentials"))
        if user.shops.count() == 0:
            raise forms.ValidationError(_("Could not find any shops associated with user"))
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        return user

    class Meta:
        model = User
        fields = ("username", "password")
        widgets = {
            "username": forms.EmailInput(),
            "password": forms.PasswordInput(),
        }
        help_texts = {
            "username": None,
            "password": None,
        }
