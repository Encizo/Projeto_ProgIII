# aminoapp/admin.py

from django.contrib import admin
from .models import Grupo, Mensagem

# Registra o modelo Grupo no admin
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'criador', 'criado_em')
    search_fields = ('nome', 'descricao')
    list_filter = ('criador',)
    ordering = ('-criado_em',)

admin.site.register(Grupo, GrupoAdmin)

# Registra o modelo Mensagem no admin
class MensagemAdmin(admin.ModelAdmin):
    list_display = ('grupo', 'usuario', 'texto', 'criado_em')
    search_fields = ('texto',)
    list_filter = ('grupo', 'usuario')

admin.site.register(Mensagem, MensagemAdmin)
