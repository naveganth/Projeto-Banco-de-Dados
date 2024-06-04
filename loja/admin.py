from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Produto)
admin.site.register(Cliente)
admin.site.register(Endereco)
admin.site.register(Compra)
admin.site.register(CompraProduto)
admin.site.register(NFE)
admin.site.register(Rastreio)
admin.site.register(Carrinho)