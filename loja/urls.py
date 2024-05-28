from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("shop", views.shop, name="shop"),
    path("produto/<int:id_produto>", views.produto, name="produto")
]