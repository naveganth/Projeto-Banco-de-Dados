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


meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "dezembro"]

def pega_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def tentar_rastrear(view):
    def _decorated(request: HttpRequest, *args, **kwargs):
        user = request.user
        print(f"View acessada: '{view.__qualname__}' Usuário do acesso: '{user}'")
        
        print(f"user: {user}, booleano: {bool(user)}")
        cookie = request.COOKIES.get("cookies")
        if cookie:            
            print("Usuário aceitou os termos")
            acesso = Acesso.objects.create(
                usuario=user if user.is_authenticated else None,
                endereco_ip=f"{pega_ip(request)}",
                pagina=f"{view.__qualname__}"
            )
            print(f"Acesso criado: {acesso}")
            acesso.save()
        else:
            print("Usuário não aceitou os termos. Fazer oq né")
        
        # Retorna a view que foi requisitada
        return view(request,*args, **kwargs)
    
    return _decorated

@tentar_rastrear
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

@tentar_rastrear
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

@tentar_rastrear
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

@tentar_rastrear
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

@tentar_rastrear
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
                login(request, novo_usuario)
                return redirect("/")
            except Exception as e:
                return render(request, "loja/signin.html", {"erro": f"Erro criando usuário: {e}"})
            
        
    elif request.method == "GET":
        return render(request, "loja/signin.html", {"erro": ""})

@tentar_rastrear
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
            
            if nome is None or email is None or senha is None or endereco is None or user.username == "admin":
                compras = Compra.objects.filter(cliente=cliente)
                dados["pedidos"] = []
                for compra in compras:
                    produtos = CompraProduto.objects.filter(compra=compra)
                    dados["cliente"] = cliente
                    dados["pedidos"].append({"compra": compra, "produtos": produtos, "soma": sum([p.produto.preco for p in produtos]) + 20})
                    dados["erro"] = "formulario inválido"
                return render(request, "loja/profile.html", dados)
            
            cliente.endereco = endereco
            cliente.nome = nome
            
            user.set_password(senha)
            user.username = email
        
            cliente.save()
            user.save()
            
            return redirect("/profile")
        
        dados["cliente"] = Cliente.objects.get(usuario=user)
        cliente = Cliente.objects.get(usuario=user)
        compras = Compra.objects.filter(cliente=cliente)
        dados["pedidos"] = []
        for compra in compras:
            produtos = CompraProduto.objects.filter(compra=compra)
            dados["pedidos"].append({"compra": compra, "produtos": produtos, "soma": sum([p.produto.preco for p in produtos]) + 20})
        
        return render(request, "loja/profile.html", dados)
    else:
        return redirect("/login")

@xframe_options_exempt
@csrf_exempt
def cart(request: HttpRequest):
    user = request.user
    if user.is_authenticated:
        dados = {}
        
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
                    id_carrinho = request.POST.get("carrinho")
                    nova_qtd = request.POST.get("nova-qtd")
                    print(f"Alterando carrinho carrinho: {id_carrinho}, nova quantidade: {nova_qtd}")
                    carrinho = Carrinho.objects.get(id=id_carrinho)
                    try:
                        carrinho.quantidade = int(nova_qtd)
                        carrinho.save()
                    except ValueError:
                        print(f"Erro ao converter nova quantidade ({nova_qtd}) para int")
                case "2":
                    cliente = Cliente.objects.get(usuario=user)
                    carrinhos = Carrinho.objects.filter(cliente=cliente)
                    for carrinho in carrinhos:
                        carrinho.delete()
                case "3":
                    cliente = Cliente.objects.get(usuario=user)
                    carrinhos = Carrinho.objects.filter(cliente=cliente)
                    
                    if len(carrinhos) > 0:
                        compra = Compra.objects.create(
                            cliente=cliente
                        )
                        compra.save()
                        
                        for carrinho in carrinhos:
                            CompraProduto.objects.create(
                                compra=compra,
                                produto=carrinho.produto,
                                quantidade=carrinho.quantidade
                            ).save()
                            carrinho.delete()
                case _:
                    pass
                    
        
        cliente = Cliente.objects.get(usuario=user)
        dados["carrinhos"] = Carrinho.objects.filter(cliente=cliente)
        return render(request, "loja/cart.html", dados)
    else:
        return redirect("/login")

def apagar_usuario(request: HttpRequest):
    user = request.user
    
    if user.username == "admin":
        return HttpResponse("Tu tá ficando doido??")
    else:
        if user.is_authenticated:
            user.delete()
    
    return redirect("/")

@tentar_rastrear
def termos(request: HttpRequest):
    return render(request, "loja/terms.html", {})

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

@xframe_options_exempt
def admin_geral(request: HttpRequest):
    dados = {}
    hoje = date.today()
    mes_atual = date.today().month
    dados["acessos_hoje"] = Acesso.objects.filter(data__date=hoje).count()
    dados["mes_atual"] = meses[mes_atual]
    dados["acessos_mes"] = Acesso.objects.filter(data__month = mes_atual).count()
    dados["compras_hoje"] = Compra.objects.filter(data__date = hoje).count()
    dados["compras_mes"] = Compra.objects.filter(data__month = mes_atual).count()
    return render(request, "loja/admin/geral.html", dados)

@xframe_options_exempt
def admin_produtos(request: HttpRequest):
    dados = {}
    dados["produtos"] = Produto.objects.all().order_by("id")
    return render(request, "loja/admin/produtos.html", dados)