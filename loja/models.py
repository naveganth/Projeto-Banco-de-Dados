from django.db import models
from django.contrib.auth.models import User

class Acesso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, unique=False)
    data = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    endereco_ip = models.CharField(max_length=255, blank=False, null=False)
    pagina = models.CharField(max_length=255, blank=False, null=False)
    
    def __str__(self):
        return f"Acesso: {self.usuario if self.usuario else 'Anônimo'} - {self.pagina} ({self.endereco_ip})"

class Produto(models.Model):
    nome = models.CharField(max_length=255, blank=False, null=False, default="Produto sem nome")
    descricao = models.CharField(max_length=2048, blank=False, null=False, default="")
    mini_descricao = models.CharField(max_length=255, blank=False, null=False, default="")
    preco = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0.0)
    estoque = models.IntegerField(blank=False, null=False, default=0)
    peso = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0.0)
    cod_barras = models.CharField(max_length=255, blank=False, null=False, default="000000000")
    # desconto = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False, default=0.0)
    avaliacao = models.IntegerField(blank=False, null=False, default=0)
    url_imagem = models.CharField(max_length=255, blank=False, null=False, default="")

    def range_avaliacao(self):
        return range(0, self.avaliacao)
    
    def __str__(self):
        return f"Produto: {self.nome}"

class Cliente(models.Model):
    nome = models.CharField(max_length=255, blank=False, null=False)
    usuario = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, blank=False, null=False)
    nome = models.CharField(max_length=255, blank=False, null=False)
    endereco = models.CharField(max_length=255, blank=False, null=False)
    cpf = models.CharField(max_length=15, blank=False, null=False)
    nascimento = models.DateField(blank=False, null=False)
    idade = models.IntegerField(blank=False, null=False)
    sexo = models.CharField(max_length=1, blank=False, null=False, default="m")
    aceitou_cookies = models.BooleanField(blank=False, null=False, default=False)
    
    def __str__(self):
        return f"Cliente: {self.nome}"

class Compra(models.Model):
    data = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=False, null=False)
    
    def __str__(self):
        return f"Compra: {self.cliente}"
    
class CompraProduto(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, blank=False, null=False)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, blank=False, null=False)
    quantidade = models.IntegerField(default=1, blank=False, null=False)
    
    def __str__(self):
        return f"Produto de {self.compra} {str(self.produto)[:30]}... (qtd: {self.quantidade})"

# Não tamo usando
# class NFE(models.Model):
#     servico = models.CharField(max_length=255, blank=False, null=False)
#     cnpj_empresa = models.CharField(max_length=255, blank=False, null=False)
#     cod_municipio = models.CharField(max_length=255, blank=False, null=False)
#     valor_liquido = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0.0)
#     pis = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0.0)
#     cofins = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0.0)
#     ir = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0.0)
#     csll = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0.0)
#     iss = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0.0)
#     desconto = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0.0)
#     compra = models.ForeignKey(Compra, on_delete=models.CASCADE, blank=False, null=False)
    
#     def __str__(self):
#         return f"Nota fiscal: Compra: {self.compra}"

class Rastreio(models.Model):
    codigo = models.CharField(max_length=255, blank=False, null=False)
    transportadora = models.CharField(max_length=255, blank=False, null=False)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, blank=False, null=False)

class Carrinho(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=False, null=False)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, blank=False, null=False)
    quantidade = models.IntegerField(default=1, blank=False, null=False)
