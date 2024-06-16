from django.contrib import admin
from .models import *

class AcessoAdmin(admin.ModelAdmin):
    readonly_fields = ('data',)
    
admin.site.register(Produto)
admin.site.register(Cliente)
admin.site.register(Compra)
admin.site.register(CompraProduto)
admin.site.register(NFE)
admin.site.register(Rastreio)
admin.site.register(Carrinho)
admin.site.register(Acesso, AcessoAdmin)
