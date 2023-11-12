from crispy_forms.utils import render_crispy_form
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.context_processors import csrf
from django.urls import reverse

from retail.models import Shop

from .forms import ReportForm, UserLoginForm


@login_required(login_url="seller:login")
def index(request):
    qs = request.user.shops.order_by("pk").values("slug").first()
    return shop(request, qs["slug"])


@login_required(login_url="seller:login")
def shop(request, slug):
    shop = get_object_or_404(Shop.objects.prefetch_related("reports"), slug=slug)
    ctx = {
        "shops": request.user.shops.order_by("pk").all(),
        "shop": shop,
    }
    return render(request, "seller/index.html", context=ctx)


@login_required(login_url="seller:login")
def report_create(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponse(status=204, headers={"HX-Trigger": "reportListChanged"})
    else:
        form = ReportForm()

    return render(request, "seller/partials/report_form.html", {"form": form})


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
                resp = render(request, "seller/index.html")
                resp["HX-Retarget"] = "body"
                resp["HX-Reswap"] = "innerHTML"
                resp["HX-Push-Url"] = reverse("seller:index")
                return resp
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return HttpResponse(form_html)


def logout(request):
    auth_logout(request)
    return redirect("seller:login")
