from django.shortcuts import render, redirect

from servicos.agendamento.models import Agendamento
from cadastros.cliente.models import Cliente
from cadastros.servicos.models import Servico


def relatorio_agendamentos(request):
    limit = 5
    pagina = int(request.GET.get('pagina', 1))
    agendamentos = Agendamento.objects.all()
    servico = Servico.objects.all()
    qntd_agendamentos = agendamentos.count()
    selecionar_status = request.GET.get('selecionar_status')
    selecionar_servico = request.GET.get('selecionar_servico')
    selecionar_funcionario = request.GET.get('selecionar_funcionario')



    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    if selecionar_funcionario:
        agendamentos = agendamentos.filter(status__iexact=selecionar_funcionario.lower())

    if selecionar_servico:
        agendamentos = agendamentos.filter(servico__iexact=selecionar_servico.lower())

    if selecionar_status:
        agendamentos = agendamentos.filter(status__iexact=selecionar_status.lower())

    if data_inicio and data_fim:
        agendamentos = agendamentos.filter(data_agendada__range=[data_inicio, data_fim])

    offset = (pagina - 1) * limit
    agendamentos = agendamentos.order_by('data_agendada')[offset:offset + limit]

    contexto = {
        'agendamentos': agendamentos,
        'qntd_agendamentos': qntd_agendamentos,
        'pagina': pagina,
        'limit': limit,
        'servico': servico,

    }

    return render(request, "agendamentos/relatorio_agendamentos.html", contexto)


def ver_agendamento(request, id):
    agendamento=Agendamento.objects.get(id=id)
    return  render(request, "agendamentos/ver_agendamento.html", {'agendamento': agendamento})


def deletar_agendamento(request, id):
    agendamento = Agendamento.objects.get(id=id)
    agendamento.delete()
    return redirect('/relatorios/agendamentos/')
