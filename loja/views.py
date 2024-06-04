from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User, UserManager
from django.contrib.auth import authenticate, login, logout
from datetime import date
from dateutils import relativedelta
from .models import *
import uuid

def index(request: HttpRequest):
    #Pega primeiros quatros produtos
    produtos = Produto.objects.all()
    produtos = produtos[:4]
    
    user = request.user
    dados = {"produtos": produtos}
    
    if user.is_authenticated:
        try:
            dados["cliente"] = Cliente.objects.get(usuario=user)
        except Exception as e:
            pass
        
    print("Produtos encontrados:", produtos)
    return render(request, "loja/index.html", dados)
    

def shop(request: HttpRequest):
    produtos = Produto.objects.all().order_by("nome")
    
    user = request.user
    dados = {"produtos": produtos}
    
    if user.is_authenticated:
        try:
            dados["cliente"] = Cliente.objects.get(usuario=user)
        except Exception as e:
            pass
    
    print("Produtos encontrados:", produtos)
    return render(request, "loja/shop.html", dados)

def produto(request: HttpRequest, id_produto: int):
    produto = Produto.objects.filter(id = id_produto).first()
    user = request.user
    dados = {"produto": produto}
    
    if user.is_authenticated:
        try:
            dados["cliente"] = Cliente.objects.get(usuario=user)
        except Exception as e:
            pass
    
    print("Produto encontrados:", produto)
    return render(request, "loja/sprodutct.html", dados)

def logar(request: HttpRequest):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        user = authenticate(username=email, password=senha)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "loja/login.html", {"erro": "Login incorreto"})
    elif request.method == "GET":
        return render(request, "loja/login.html", {})

def signin(request: HttpRequest):
    if request.method == "POST":
        nome = request.POST.get("nome")
        nascimento = request.POST.get("nascimento")
        sexo = request.POST.get("sexo")
        cpf = request.POST.get("cpf")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        
        print("dados do POST:", request.POST)
        
        if nome and nascimento and sexo and cpf and email and senha:
            try:
                novo_usuario = User.objects.create_user(
                    username=email, 
                    email=email, 
                    password=senha
                )
                data_nascimento = date.fromisoformat(nascimento)
                idade = relativedelta(date.today(), data_nascimento)
                novo_cliente = Cliente.objects.create(
                    usuario=novo_usuario,
                    cpf=cpf,
                    nascimento=nascimento,
                    sexo=sexo,
                    idade=idade.years,
                    nome=nome,
                )
                novo_cliente.save()
                return redirect("/")
            except Exception as e:
                return render(request, "loja/signin.html", {"erro": f"Erro criando usuário: {e}"})
            
        
    elif request.method == "GET":
        return render(request, "loja/signin.html", {"erro": ""})

def profile(request: HttpRequest):
    user = request.user
    if user.is_authenticated:
        cliente = Cliente.objects.get(usuario=user)
        pedidos = Compra.objects.filter(cliente=cliente)
        return render(request, "loja/profile.html", {pedidos: pedidos})
    else:
        return redirect("/login")

def cart(request: HttpRequest):
    user = request.user
    if user.is_authenticated:
        cliente = Cliente.objects.get(usuario=user)
        produtos = Carrinho.objects.get(cliente=cliente).produto
        return render(request, "loja/cart.html", {produtos: produtos})
    else:
        return redirect("/login")
    