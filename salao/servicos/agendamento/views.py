from django.shortcuts import render, HttpResponse, redirect

from servicos.agendamento.models import Agendamento
from cadastros.cliente.models import Cliente
from cadastros.servicos.models import Servico

def agendar_servico(request):
    if request.method == 'GET':
         return render(request, 'agendar.html', {})

    """ else:
        cliente_ID = request.POST.get('cliente')
        funcionario_ID = request.POST.get('funcionario')
        servico_ID = request.POST.get('servico')
        status = request.POST.get('status_filtrar')
        data_hora = request.POST.get('data_hora')

        clientes = Cliente.objects.get(pk=cliente_ID)
        servicos = Servico.objects.get(pk=servico_ID)
        funcionarios = Cliente.objects.get(pk=funcionario_ID)

        agendamento = Agendamento(cliente=clientes, funcionario=funcionarios, servico=servicos, status=status, data_hora=data_hora)
        agendamento.save()        

        return redirect('/agendamento/') """