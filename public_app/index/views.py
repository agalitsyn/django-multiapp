from django.shortcuts import render


def index(request):
    return render(request, "public/index.html")


def page_not_found(request):
    return render(request, "public/404.html")
