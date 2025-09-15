from django.shortcuts import render, redirect, get_object_or_404

from servicos.agendamento.models import Agendamento
from cadastros.cliente.models import Cliente
from cadastros.servicos.models import Servico
from cadastros.funcionarios.models import Profissional
from core.utils.helpers import AgendarHelper

def agendar_servico(request):
    if request.method == 'GET':
        clientes = Cliente.objects.all().order_by('nome')
        servicos = Servico.objects.all()
        profissional = Profissional.objects.all().order_by('nome')
        helper = AgendarHelper()

        id = request.GET.get('id')

        # Primeiro monta o contexto básico com os dados fixos
        contexto = {
            'clientes': clientes,
            'servicos': servicos,
            'profissional': profissional,
            'id': id,
        }

        # Atualiza com os dados que vêm do helper (ex: proximos_dias_agendamentos)
        contexto.update(helper.proximos_dias_agendamentos())

        return render(request, 'agendar.html', contexto)
    
    elif request.method == 'POST':
        cliente_ID = request.POST.get('cliente')
        funcionario_ID = request.POST.get('funcionario')
        servico_ID = request.POST.get('servico')
        data_hora = request.POST.get('data_hora')

        clientes = Cliente.objects.get(pk=cliente_ID)
        profissional = Profissional.objects.get(pk=funcionario_ID)
        servicos = Servico.objects.get(pk=servico_ID)

        agendamento = Agendamento(
            cliente=clientes, 
            profissional=profissional, 
            servico=servicos, 
            data_agendada=data_hora
            )
        agendamento.save()        

        return redirect('/servicos/agendamento/')
    

def alterar_status(request, agendamento_id, status):
    agendamento = get_object_or_404(Agendamento, pk=agendamento_id)
    agendamento.status = status
    agendamento.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))
        