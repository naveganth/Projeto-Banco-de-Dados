from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def index(request):
    #Pega primeiros quatros produtos
    produtos = Produto.objects.all()
    produtos = produtos[:4]
    
    print("Produtos encontrados:", produtos)
    return render(request, "loja/index.html", {"produtos": produtos})