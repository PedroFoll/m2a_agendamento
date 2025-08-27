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
        'ativo'
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


    def get_fields(self, request, obj = ...):
        return super().get_fields(request, obj)
    fieldsets=[
        (
            'Informações do Agendamento',
            {
                "fields": (
                    "cliente",
                    "data_agendada",
                    "servico", 
                    "profissional", 
                    "status", 
                    "ativo",
                )
            }
        ),
        (
            'Imagem',
            {
                "fields":(
                    "foto",
                    "preview_image"
                )
            }
        )
    ]
    readonly_fields = ("preview_image",) 

    def preview_image(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="max-height: 200px; border-radius: 8px;" />', obj.foto.url)
        return "Nenhuma imagem"
    preview_image.short_description = "Pré-visualização"