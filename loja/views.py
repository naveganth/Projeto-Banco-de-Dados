from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User, UserManager
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.clickjacking import xframe_options_exempt
from datetime import date
from dateutils import relativedelta
from django.views.decorators.csrf import csrf_exempt
from .models import *
import uuid
import time

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
        
        # Guardar algo no carrinho
        if request.method == "POST":
            cliente = Cliente.objects.get(usuario=user)
            produto = Produto.objects.get(id=request.POST.get("id"))
            quantidade = request.POST.get("quantidade")
            
            # se já tiver esse item no carrinho, só adicionar mais uma na quantidade
            consulta_previa = Carrinho.objects.filter(cliente=cliente, produto=produto).first()
            if consulta_previa:
                try: # só no caso de um dos int() dar erro
                    consulta_previa.quantidade += int(quantidade)
                    # se a quantidade for maior doq tem, limita
                    if consulta_previa.quantidade > produto.estoque:
                        consulta_previa.quantidade = produto.estoque
                    consulta_previa.save()
                except ValueError as e:
                    print("De algum jeito alguem conseguiu colocar uma quantide que não seja um número")
            else:
                Carrinho.objects.create(cliente=cliente, produto=produto, quantidade=quantidade)
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

def deslogar(request: HttpRequest):
    print("Logour chamado")
    usuario = request.user
    print("Usuário:", usuario)
    if usuario.is_authenticated:
        logout(request)
    return redirect("/")

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
        dados = {}
         
        # Se o usuário apertou o botão de salvar pra lá
        if request.method == "POST":
            nome = request.POST.get("nome")
            email = request.POST.get("email")
            senha = request.POST.get("senha")
            endereco = request.POST.get("endereco")
            
            cliente = Cliente.objects.get(usuario=user)
            
            if nome is None or email is None or senha is None or endereco is None:
                dados["pedidos"] = Compra.objects.filter(cliente=cliente)
                dados["erro"] = "Preencha o formulário"
                return render(request, "loja/profile.html", dados)
            
            cliente.endereco = endereco
            cliente.nome = nome
            
            user.set_password(senha)
            user.username = email
        
            cliente.save()
            user.save()
            
            return redirect("/profile")
        
        try:
            dados["cliente"] = Cliente.objects.get(usuario=user)
        except Exception as e:
            pass
        
        cliente = Cliente.objects.get(usuario=user)
        dados["pedidos"] = Compra.objects.filter(cliente=cliente)
        return render(request, "loja/profile.html", dados)
    else:
        return redirect("/login")

@xframe_options_exempt
@csrf_exempt
def cart(request: HttpRequest):
    user = request.user
    if user.is_authenticated:
        dados = {}
        
        if user.is_authenticated:
            try:
                dados["cliente"] = Cliente.objects.get(usuario=user)
            except Exception as e:
                pass
            
            # Alterar o carrinho
            if request.method == "POST":
                print("Post no carrinho")
                operacao = request.POST.get("operacao")
                print(f"Operacao: {operacao}")
                match operacao:
                    case "0":
                        id_carrinho = request.POST.get("carrinho")
                        print(f"Apagando carrinho: {id_carrinho}")
                        carrinho = Carrinho.objects.get(id=id_carrinho)
                        carrinho.delete()
                    case "1":
                        pass
                    case _:
                        pass
                    
        
        cliente = Cliente.objects.get(usuario=user)
        dados["carrinhos"] = Carrinho.objects.filter(cliente=cliente)
        return render(request, "loja/cart.html", dados)
    else:
        return redirect("/login")

def chart(request: HttpRequest):
    dados = {}
    dados["compras_por_mes_totais"] = None
    dados["compras_por_estado"] = None
    dados["lucros_totais_por_mes"] = None
    dados["lucro_por_estado"] = None
    dados["compras_por_sexo"] = None
    dados["compras_por_nascimento"] = None
    dados["compras_por_idade"] = None
    dados["lucro_por_signo"] = None
    
    return render(request, "loja/chart.html", {"dados": dados})
    