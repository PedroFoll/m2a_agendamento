from django.contrib import admin
from django.utils.html import format_html


from .models import *


# Register your models here.
@admin.register(Cliente)
@admin.display(boolean=True)
class CadastroAdmin(admin.ModelAdmin):
    list_filter=('ativo',)
    list_display=(
        'cpf',
        'nome',
        'email',
        'ativo'
    )
    list_per_page=15


    def get_fields(self, request, obj = ...):
        return super().get_fields(request, obj)
    fieldsets=[
        (
            'Informações do Agendamento',
            {
                "fields": (
                    'cpf',
                    'nome',
                    'email',
                    'data_nascimento',
                    'ativo',
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


