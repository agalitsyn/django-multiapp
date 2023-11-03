from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include(("public_app.index.urls", "public"))),
    path("seller/", include(("seller_app.index.urls", "seller"))),
    path("admin/", admin.site.urls),
]
