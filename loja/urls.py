from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("shop", views.shop, name="shop"),
    path("produto/<int:id_produto>", views.produto, name="produto"),
    path("login", views.logar, name="login"),
    path("logout", views.deslogar, name="deslogar"),
    path("signin", views.signin, name="signin"),
    path("profile", views.profile, name="profile"),
    path("cart", views.cart, name="cart"),
    path("admin/", views.chart, name="admin"),
    path("termos/", views.termos, name="termos"),
    path("apagar_usuario_1234567890", views.apagar_usuario, name="apagar usuário"),
    path("admin/geral", views.admin_geral, name="admin geral"),
    path("admin/produtos", views.admin_produtos, name="admin produto"),
    path("admin/clientes", views.admin_clientes, name="admin clientes"),
    path("admin/kpis", views.admin_kpis, name="admin kpis"),
    path("admin/importacao", views.admin_importacao, name="admin importação"),
]