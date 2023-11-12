from django.urls import path

from .views import index, login, logout, report_create, shop

urlpatterns = [
    path("", index, name="index"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("shop/<slug:slug>/", shop, name="shop"),
    path("report-create/", report_create, name="report_create"),
]
