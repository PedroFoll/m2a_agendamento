from django.shortcuts import render, HttpResponse
from servicos.agendamento.models import Agendamento
from cadastros.cliente.models import Cliente



def relatorio(request):
    limit = 15
    pagina = int(request.GET.get('pagina', 1))
    agendamentos = Agendamento.objects.all()
    qntd_agendamentos = agendamentos.count()
    selecionar_status = request.GET.get('selecionar_status')

    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

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
    }

    return render(request, "clientes/relatorio_clientes.html", contexto)

def ver_cliente(request,id):
    cliente=Cliente.objects.get(id=id)
    return  render(request, 'clientes/ver_cliente.html', {'cliente': cliente})