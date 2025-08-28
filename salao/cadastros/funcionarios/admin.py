from django.contrib import admin
from django.utils.html import format_html


from .models import *
from core.utils.filtragem import PrecoRangeFilter


@admin.register(Profissional)
@admin.display(boolean=True)
class CadastroAdmin(admin.ModelAdmin):
    list_filter=('ativo',)