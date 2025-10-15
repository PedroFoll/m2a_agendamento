from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_datetime
from django.contrib import messages

from servicos.agendamento.models import Agendamento
from cadastros.cliente.models import Cliente
from cadastros.servicos.models import Servico
from cadastros.funcionarios.models import Profissional
from core.utils.helpers import AgendarHelper

from django.utils.dateparse import parse_datetime
from django.contrib import messages
from decimal import Decimal

from decimal import Decimal
from django.utils.dateparse import parse_datetime
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Agendamento, Servico, Cliente, Profissional

def agendar_servico(request):
    if request.method == 'GET':
        clientes = Cliente.objects.all().order_by('nome')
        servicos = Servico.objects.all()
        profissional = Profissional.objects.all().order_by('nome')
        helper = AgendarHelper()

        id = request.GET.get('id')

        contexto = {
            'clientes': clientes,
            'servicos': servicos,
            'profissional': profissional,
            'id': id,
        }

        contexto.update(helper.proximos_dias_agendamentos())

        return render(request, 'agendar.html', contexto)

    elif request.method == 'POST':
        cliente_ID = request.POST.get('cliente')
        funcionario_ID = request.POST.get('funcionario')
        servicos_IDs = request.POST.getlist('servico')  # pode vir vários serviços
        data_hora = request.POST.get('data_hora')

        erro_ocorrido = False

        # validações
        try:
            cliente = Cliente.objects.get(pk=cliente_ID)
        except Cliente.DoesNotExist:
            messages.error(request, 'Cliente não encontrado')
            erro_ocorrido = True

        try:
            profissional = Profissional.objects.get(pk=funcionario_ID)
        except Profissional.DoesNotExist:
            messages.error(request, 'Profissional não encontrado')
            erro_ocorrido = True

        try:
            servicos = Servico.objects.filter(pk__in=servicos_IDs)
            if not servicos.exists():
                raise Servico.DoesNotExist
        except Servico.DoesNotExist:
            messages.error(request, 'Serviço não encontrado')
            erro_ocorrido = True

        try:
            data_hora = parse_datetime(data_hora)
            if data_hora is None:
                raise ValueError("Formato de data/hora inválido.")
        except (ValueError, TypeError):
            messages.error(request, 'Data/Hora inválida')
            erro_ocorrido = True

        if erro_ocorrido:
            return redirect(request.path_info)

        # 🧮 Calcula o valor total com base nas quantidades enviadas
        total_servicos = Decimal('0.00')
        servico_quantidades = {}

        for servico in servicos:
            qtd = int(request.POST.get(f'quantidade_{servico.id}', 1))
            total_servicos += servico.preco * qtd
            servico_quantidades[servico.id] = qtd  # guarda para uso futuro, se quiser salvar

        # cria o agendamento
        agendamento = Agendamento.objects.create(
            cliente=cliente,
            profissional=profissional,
            data_agendada=data_hora,
            valor_total=total_servicos
        )

        # associa os serviços
        agendamento.servico.set(servicos)

        # se quiser salvar quantidades, precisa criar uma relação intermediária (ex: AgendamentoServico)
        # senão, apenas associa normalmente

        messages.success(request, 'Agendamento criado com sucesso!')
        return redirect('/servicos/agendamento/')
    

def alterar_status(request, agendamento_id, status):
    agendamento = get_object_or_404(Agendamento, pk=agendamento_id)
    agendamento.status = status
    agendamento.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))
        