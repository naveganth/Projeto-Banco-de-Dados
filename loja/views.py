from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .models import *

# Create your views here.
def index(request: HttpRequest):
    #Pega primeiros quatros produtos
    produtos = Produto.objects.all()
    produtos = produtos[:4]
    
    print("Produtos encontrados:", produtos)
    return render(request, "loja/index.html", {"produtos": produtos})

def shop(request: HttpRequest):
    produtos = Produto.objects.all().order_by("nome")
    
    print("Produtos encontrados:", produtos)
    return render(request, "loja/shop.html", {"produtos": produtos})

def produto(request: HttpRequest, id_produto: int):
    produto = Produto.objects.filter(id = id_produto).first()
    
    print("Produto encontrados:", produto)
    return render(request, "loja/sprodutct.html", {"produto": produto})

def login(request: HttpRequest):
    if request.method == "POST":
        pass
    elif request.method == "GET":
        return render(request, "loja/login.html", {"produto": produto})

def signin(request: HttpRequest):
    if request.method == "POST":
        pass
    elif request.method == "GET":
        return render(request, "loja/signin.html", {"produto": produto})