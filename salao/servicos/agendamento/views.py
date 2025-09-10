from django.shortcuts import render, redirect

from servicos.agendamento.models import Agendamento
from cadastros.cliente.models import Cliente
from cadastros.servicos.models import Servico
from cadastros.funcionarios.models import Profissional

def agendar_servico(request):
    if request.method == 'GET':
        clientes = Cliente.objects.all().order_by('nome')
        servicos = Servico.objects.all()
        profissional = Profissional.objects.all().order_by('nome')

        contexto = {
            'clientes': clientes,
            'servicos': servicos,
            'profissional': profissional
        }

        return render(request, 'agendar.html', contexto)

    else:
        cliente_ID = request.POST.get('cliente')
        funcionario_ID = request.POST.get('funcionario')
        servico_ID = request.POST.get('servico')
        data_hora = request.POST.get('data_hora')

        clientes = Cliente.objects.get(pk=cliente_ID)
        funcionarios = Profissional.objects.get(pk=funcionario_ID)
        servicos = Servico.objects.get(pk=servico_ID)

        agendamento = Agendamento(
            cliente=clientes, 
            profissional=funcionarios, 
            servico=servicos, 
            data_agendada=data_hora
            )
        agendamento.save()        

        return redirect('/servicos/agendamento/')