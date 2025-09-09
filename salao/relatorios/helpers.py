from django.shortcuts import render

from cadastros.servicos.models import Servico

class Helpers():
    def pegar_Servico(request):
        if request.method == 'GET':

            servicos = Servico.objects.get(id=id)

            return (servicos)


