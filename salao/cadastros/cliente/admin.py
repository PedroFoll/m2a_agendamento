from django.contrib import admin

from .models import *

# Register your models here.
@admin.register(Cliente)
class CadastroAdmin(admin.ModelAdmin):
    list_filter=('ativo',)

@admin.register(Servico)
class CadastroAdmin(admin.ModelAdmin):
    list_filter=('nome',)

@admin.register(Profissional)
class CadastroAdmin(admin.ModelAdmin):
    list_filter=('nome',)