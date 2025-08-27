from django.contrib import admin

from .models import Agendamento

# Register your models here.
@admin.register(Agendamento)
@admin.display(boolean=True)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display=(
        'cliente',
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


    def get_fields(self, request, obj = ...):
        return super().get_fields(request, obj)
    fieldsets=[
        (
            'Informações do Cliente',
            {
                'fields':[
                    "cliente",
                    ]
            }

        ),

        (
            'Informações do Agendamento',
            {
                "fields": [
                    "data_agendada",
                    "servico", 
                    "profissional", 
                    "status", 
                    "ativo"
                        ]
            }
        ),
      ]
    date_hierarchy = "data_agendada"