from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_datetime
from django.contrib import messages

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

        try:
            clientes = Cliente.objects.get(pk=cliente_ID)
        except Cliente.DoesNotExist:
            messages.error(request, 'Cliente não encontrado')

        try:
            profissional = Profissional.objects.get(pk=funcionario_ID)
        except Profissional.DoesNotExist:
            messages.error(request, 'Profissional não encontrado')

        try:
            servicos = Servico.objects.get(pk=servico_ID)
        except Servico.DoesNotExist:
            messages.error(request, 'Serviço não encontrado')
        
        try:
            data_hora = parse_datetime(data_hora)
            if data_hora is None:
                raise ValueError("Formato de data/hora inválido.")
        except (ValueError, TypeError):
            messages.error(request, 'Data/Hora inválida')

        if messages:
            return redirect(request.path_info)



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
        