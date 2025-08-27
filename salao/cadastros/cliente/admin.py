from django.contrib import admin

from .models import *
from core.utils.filtragem import PrecoRangeFilter


# Register your models here.
@admin.register(Cliente)
class CadastroAdmin(admin.ModelAdmin):
    list_filter=('ativo',)


@admin.register(Servico)
class CadastroAdmin(admin.ModelAdmin):
    list_display=('nome', 'preco')
    list_filter = (PrecoRangeFilter,)


@admin.register(Profissional)
class CadastroAdmin(admin.ModelAdmin):
    list_filter=('ativo',)
