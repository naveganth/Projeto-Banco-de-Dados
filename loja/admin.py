from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import *

class AcessoAdmin(admin.ModelAdmin):
    readonly_fields = ('data',)
    
admin.site.register(Produto)
admin.site.register(Cliente)
admin.site.register(Compra)
admin.site.register(CompraProduto)
admin.site.register(Rastreio)
admin.site.register(Carrinho)
admin.site.register(Acesso, AcessoAdmin)
admin.site.register(Configuracoes, SingletonModelAdmin)
