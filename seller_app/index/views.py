from crispy_forms.utils import render_crispy_form
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.context_processors import csrf
from django.urls import reverse

from .forms import UserLoginForm


@login_required(login_url="seller:login")
def index(request):
    return render(request, "seller/index.html")


def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect("seller:index")
        form = UserLoginForm()
        return render(request, "seller/login.html", {"form": form})
    elif request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user is not None:
                auth_login(request, user)
                template = render(request, "seller/index.html")
                template["HX-Push-Url"] = reverse("seller:index")
                template["HX-Reswap"] = "innerHTML"
                template["HX-Retarget"] = "closest body"
                return template
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return HttpResponse(form_html)


def logout(request):
    auth_logout(request)
    return redirect("seller:login")
