from django.contrib import admin
from django.utils.html import format_html

from .models import Agendamento

# Register your models here.
@admin.register(Agendamento)
@admin.display(boolean=True)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display=(
        'cliente__nome',
        'cliente__cpf',
        'servico',
        'profissional',
        'data_agendada',
        'status',
        'ativo',
        )
    list_filter = (
        "data_agendada",
        "servico",
        'ativo',
        'status'
        )
    list_per_page=15
    ordering=(
        'data_agendada',
        )
    raw_id_fields = "cliente", 
    date_hierarchy = "data_agendada"
