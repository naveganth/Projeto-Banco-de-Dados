from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("loja.urls")),
    path("adminn/", admin.site.urls),
]