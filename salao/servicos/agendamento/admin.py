from django.contrib import admin

from .models import *

# Register your models here.
@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_filter = ('servico', 'cliente')