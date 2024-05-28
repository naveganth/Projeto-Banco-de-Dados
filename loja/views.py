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