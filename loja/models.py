from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Produto(models.Model):
    nome = models.CharField(max_length=255, blank=False, null=False, default="Produto sem nome")
    descricao = models.CharField(max_length=2048, blank=False, null=False, default="")
    mini_descricao = models.CharField(max_length=255, blank=False, null=False, default="")
    preco = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0.0)
    estoque = models.IntegerField(blank=False, null=False, default=0)
    peso = models.DecimalField(max_digits=11, decimal_places=2, blank=False, null=False, default=0.0)
    cod_barras = models.CharField(max_length=255, blank=False, null=False, default="000000000")
    desconto = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False, default=0.0)
    avaliacao = models.IntegerField(blank=False, null=False, default=0)
    url_imagem = models.CharField(max_length=255, blank=False, null=False, default="")

    def range_avaliacao(self):
        return range(0, self.avaliacao)
    
    def __str__(self):
        return f"Produto: {self.nome}"

class Cliente(models.Model):
    nome = models.CharField(max_length=255, blank=False, null=False)
    usuario = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, blank=False, null=False)
    cpf = models.CharField(max_length=15, blank=False, null=False)
    nascimento = models.DateField(blank=False, null=False)
    idade = models.IntegerField(max_length=3, blank=False, null=False)
    sexo = models.CharField(max_length=1, blank=False, null=False, default="m")



