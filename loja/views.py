from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth.models import User, UserManager
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.clickjacking import xframe_options_exempt
from datetime import date, timedelta
from dateutils import relativedelta
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from .models import *
import pandas as pd
import json
import uuid
import time
import ast


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
        endereco = request.POST.get("endereco")
        
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
                    endereco=endereco
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
    user = request.user
    print("Tentando acessar menu admin")
    print("Usuário:", user)
    print("Grupos", user.groups.all())
    print("Admin lá dentro:", user.groups.filter(name = "admin").exists() )
    if user.is_authenticated and user.groups.filter(name = "admin").exists():
        
        if request.method == "POST":
            marketing = request.POST.get("marketing")
            despesas = request.POST.get("despesas")
            config = Configuracoes.objects.get()
            
            try:
                config.orcamento_marketing = float(marketing)
                config.custo_geral = float(despesas)
                config.save()
            except ValueError:
                print("Valor deu ruim aqui")
            
        dados = {}
        return render(request, "loja/chart.html", {"dados": dados})
    else:
        return redirect("/")

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
    
    dias_grafico = 30
    data_grafico_inicio = date.today() - timedelta(days=dias_grafico)
    
    grafico_labels = []
    grafico_acessos = []
    grafico_compras = []
    
    for i in range(dias_grafico + 1):
        data = data_grafico_inicio + timedelta(days=i)
        grafico_acessos.append(Acesso.objects.filter(data__date=data).count())
        grafico_compras.append(Compra.objects.filter(data__date=data).count())
        grafico_labels.append(str(data))
    
    dados["labels"] = json.dumps(list(grafico_labels), cls=DjangoJSONEncoder)
    dados["grafico_acessos"] = json.dumps(grafico_acessos, cls=DjangoJSONEncoder)
    dados["grafico_compras"] = json.dumps(grafico_compras, cls=DjangoJSONEncoder)
    return render(request, "loja/admin/geral.html", dados)

@xframe_options_exempt
def admin_produtos(request: HttpRequest):
    dados = {}
    dados["produtos"] = Produto.objects.all().order_by("id")
    return render(request, "loja/admin/produtos.html", dados)

@xframe_options_exempt
def admin_clientes(request: HttpRequest):
    dados = {}
    dados["clientes"] = Cliente.objects.all().order_by("usuario__id")
    return render(request, "loja/admin/clientes.html", dados)

@xframe_options_exempt
def admin_kpis(request: HttpRequest):
    dados = {}
    mes_atual = date.today().month
    dados["mes_atual"] = meses[mes_atual]
    dados["visitantes_hoje"] = Acesso.objects.filter(data__date=date.today()).count()
    dados["visitantes_mes"] = Acesso.objects.filter(data__month=date.today().month).count()
    dados["vendas_hoje"] = Compra.objects.filter(data__date=date.today()).count()
    dados["vendas_mes"] = Compra.objects.filter(data__month=date.today().month).count()
    dados["conversao_hoje"] = ((dados["vendas_hoje"] / dados["visitantes_hoje"]) * 100) if dados["vendas_hoje"] else 0.0
    dados["conversao_mes"] = ((dados["vendas_mes"] / dados["visitantes_mes"]) * 100) if dados["vendas_mes"] else 0.0
    
    total_mes = float(sum(x.produto.preco for x in CompraProduto.objects.filter(compra__data__month=date.today().month)))
    total_hoje = float(sum(x.produto.preco for x in CompraProduto.objects.filter(compra__data__date=date.today())))
    config = Configuracoes.objects.get()
    
    dados["roi_mes"] = (total_mes - float(config.custo_geral)) / float(config.custo_geral) * 100
    dados["cac_mes"] = (float(config.custo_geral) + float(config.orcamento_marketing)) / Cliente.objects.filter(criacao__month=date.today().month).count()
    dados["ticket_medio_hoje"] = (total_hoje / dados["vendas_hoje"]) if dados["vendas_hoje"] else 0.0
    dados["ticket_medio_mes"] = (total_mes / dados["vendas_mes"]) if dados["vendas_mes"] else 0.0
    
    dias_grafico = 30
    data_grafico_inicio = date.today() - timedelta(days=dias_grafico)
    
    grafico_labels = []
    grafico_visitantes = []
    grafico_vendas = []
    grafico_conversao = []
    grafico_ticket = []
    
    config = Configuracoes.objects.get()
    
    for i in range(dias_grafico + 1):
        data = data_grafico_inicio + timedelta(days=i)
        grafico_labels.append(str(data))
        
        visitantes = Acesso.objects.filter(data__date=data).count()
        grafico_visitantes.append(visitantes)
        
        vendas = Compra.objects.filter(data__date=data).count()
        grafico_vendas.append(vendas)
        
        grafico_conversao.append(((vendas / visitantes) * 100) if vendas else 0.0)
        
        receita = float(sum(x.produto.preco for x in CompraProduto.objects.filter(compra__data__date=data)))
        grafico_ticket.append((receita / vendas) if vendas else 0.0)
        
    dados["labels"] = json.dumps(list(grafico_labels), cls=DjangoJSONEncoder)
    dados["grafico_visitantes"] = json.dumps(list(grafico_visitantes), cls=DjangoJSONEncoder)
    dados["grafico_vendas"] = json.dumps(list(grafico_vendas), cls=DjangoJSONEncoder)
    dados["grafico_conversao"] = json.dumps(list(grafico_conversao), cls=DjangoJSONEncoder)
    dados["grafico_ticket"] = json.dumps(list(grafico_ticket), cls=DjangoJSONEncoder)
    
    return render(request, "loja/admin/kpis.html", dados)

@xframe_options_exempt
@csrf_exempt
def admin_importacao(request: HttpRequest):
    if request.method == "POST":
        print("POST:", request.POST)
        print("FILES:", request.FILES)
        
        arquivo_cliente = request.FILES.get("cliente")
        if arquivo_cliente:
            print("Arquivo recebido:", arquivo_cliente)
            match arquivo_cliente.name.split(".")[-1]:
                case "json":
                    print("Clientes é JSON")
                    df = pd.read_json(arquivo_cliente)
                    print("DATAFRAME RESGATADO:")
                    print(df)
                    for i in df.values:
                        nome = i[0]
                        email = i[1]
                        endereco = i[2]
                        cpf = i[4]
                        nascimento = i[5]
                        idade = i[6]
                        sexo = i[7]
                        
                        Cliente.objects.create(
                            nome=nome,
                            usuario=User.objects.create_user(email, email , "123"),
                            endereco=endereco,
                            cpf=cpf,
                            nascimento=nascimento,
                            idade=idade,
                            sexo=sexo,
                            aceitou_cookies=True,
                        )
                case "xml":
                    print("Clientes é XML")
                    df = pd.read_xml(arquivo_cliente)
                    print("DATAFRAME RESGATADO:")
                    print(df)
                    for i in df.values:
                        nome = i[1]
                        email = i[2]
                        endereco = i[3]
                        cpf = i[5]
                        nascimento = i[6]
                        idade = i[7]
                        sexo = i[8]
                        
                        Cliente.objects.create(
                            nome=nome,
                            usuario=User.objects.create_user(email, email , "123"),
                            endereco=endereco,
                            cpf=cpf,
                            nascimento=nascimento,
                            idade=idade,
                            sexo=sexo,
                            aceitou_cookies=True,
                        )
                        
                case "csv":
                    print("Clientes é CSV")
                    df = pd.read_csv(arquivo_cliente)
                    print("DATAFRAME RESGATADO:")
                    print(df)
                    for i in df.values:
                        nome = i[0]
                        email = i[1]
                        endereco = i[2]
                        cpf = i[4]
                        nascimento = i[5]
                        idade = i[6]
                        sexo = i[7]
                        
                        Cliente.objects.create(
                            nome=nome,
                            usuario=User.objects.create_user(email, email , "123"),
                            endereco=endereco,
                            cpf=cpf,
                            nascimento=nascimento,
                            idade=idade,
                            sexo=sexo,
                            aceitou_cookies=True,
                        )

        arquivo_produtos = request.FILES.get("produto")
        if arquivo_produtos:
            print("Arquivo recebido:", arquivo_produtos)
            match arquivo_produtos.name.split(".")[-1]:
                case "json":
                    print("Clientes é JSON")
                    df = pd.read_json(arquivo_produtos)
                    print("DATAFRAME RESGATADO:")
                    print(df)
                    for i in df.values:
                        nome = i[0]
                        descricao = i[1]
                        mini_descricao = i[2]
                        preco = i[3]
                        estoque = i[4]
                        peso = i[5]
                        cod_barras = i[6]
                        avaliacao = i[7]
                        url_imagem = i[8]
                        
                        Produto.objects.create(
                            nome=nome,
                            descricao=descricao,
                            mini_descricao=mini_descricao,
                            preco=preco,
                            estoque=estoque,
                            peso=peso,
                            cod_barras=cod_barras,
                            avaliacao=avaliacao,
                            url_imagem=url_imagem,
                        )
                case "xml":
                    print("Clientes é XML")
                    df = pd.read_xml(arquivo_produtos)
                    print("DATAFRAME RESGATADO:")
                    print(df)
                    for i in df.values:
                        nome = i[1]
                        descricao = i[2]
                        mini_descricao = i[3]
                        preco = i[4]
                        estoque = i[5]
                        peso = i[6]
                        cod_barras = i[7]
                        avaliacao = i[8]
                        url_imagem = i[9]
                        
                        Produto.objects.create(
                            nome=nome,
                            descricao=descricao,
                            mini_descricao=mini_descricao,
                            preco=preco,
                            estoque=estoque,
                            peso=peso,
                            cod_barras=cod_barras,
                            avaliacao=avaliacao,
                            url_imagem=url_imagem,
                        )
                case "csv":
                    print("Clientes é CSV")
                    df = pd.read_csv(arquivo_produtos)
                    print("DATAFRAME RESGATADO:")
                    print(df)
                    for i in df.values:
                        nome = i[0]
                        descricao = i[1]
                        mini_descricao = i[2]
                        preco = i[3]
                        estoque = i[4]
                        peso = i[5]
                        cod_barras = i[6]
                        avaliacao = i[7]
                        url_imagem = i[8]
                        
                        Produto.objects.create(
                            nome=nome,
                            descricao=descricao,
                            mini_descricao=mini_descricao,
                            preco=preco,
                            estoque=estoque,
                            peso=peso,
                            cod_barras=cod_barras,
                            avaliacao=avaliacao,
                            url_imagem=url_imagem,
                        )
    dados = {}
    return render(request, "loja/admin/importacao.html", dados)
        