from django.contrib import admin
from django.utils.html import format_html


from .models import *
from core.utils.filtragem import PrecoRangeFilter


@admin.register(Servico)
class CadastroAdmin(admin.ModelAdmin):
    list_display=('nome', 'preco')
    list_filter = (PrecoRangeFilter,)
