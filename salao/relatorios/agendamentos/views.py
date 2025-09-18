from math import ceil

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string

import pdfkit

from servicos.agendamento.models import Agendamento
from cadastros.cliente.models import Cliente
from cadastros.servicos.models import Servico
from cadastros.funcionarios.models import Profissional
from core.utils.helpers import Helpers


def relatorio_agendamentos(request):
    geral = Helpers.relatorio_geral(request)
    rank_func = Helpers.rank_funcionarios()
    rank_cli = Helpers.rank_clientes()
    rank_serv = Helpers.rank_servicos()
    limit = 25
    pagina = int(request.GET.get('pagina', 1))
    agendamentos = Agendamento.objects.all()
    servico = Servico.objects.all()
    qntd_agendamentos = agendamentos.count()
    selecionar_status = request.GET.get('selecionar_status')
    

    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    if selecionar_status:
        agendamentos = agendamentos.filter(status__iexact=selecionar_status.lower())

    if data_inicio and data_fim:
        agendamentos = agendamentos.filter(data_agendada__range=[data_inicio, data_fim])

    total_paginas = ceil(qntd_agendamentos / limit)
    paginas = list(range(1, total_paginas + 1))

    offset = (pagina - 1) * limit
    agendamentos = agendamentos.order_by('data_agendada')[offset:offset + limit]

    contexto = {
        'form': geral['form'],
        'agendamentos': geral['agendamentos'][:25],
        'total_agendamentos': geral['total_agendamentos'],
        'total_arrecadado': geral['total_arrecadado'],
        'rank_func':rank_func,
        'rank_cli':rank_cli,
        'rank_serv':rank_serv,
        'agendamentos': agendamentos,
        'qntd_agendamentos': qntd_agendamentos,
        'pagina': pagina,
        'limit': limit,
        'servico': servico,
        'total_paginas': total_paginas,
        'paginas': paginas

    }

    return render(request, "agendamentos/relatorio_agendamentos.html", contexto)


def ver_agendamento(request, id):
    agendamento = Agendamento.objects.get(pk=id)
    contexto = {
        "agendamento": agendamento
    }
    return  render(request, "agendamentos/ver_agendamento.html", contexto)
    


def deletar_agendamento(request, id):
    agendamento = Agendamento.objects.get(id=id)
    agendamento.delete()
    return redirect('/relatorios/agendamentos/')



def editar_agendamento(request, id):
    agendamento = get_object_or_404(Agendamento, id=id)

    clientes = Cliente.objects.all()
    servicos = Servico.objects.all()
    profissionais = Profissional.objects.all()

    if request.method == 'POST':
        agendamento.cliente_id = request.POST.get('cliente') or agendamento.cliente_id
        agendamento.servico_id = request.POST.get('servico') or agendamento.servico_id
        agendamento.profissional_id = request.POST.get('profissional') or agendamento.profissional_id
        agendamento.status = request.POST.get('status') or agendamento.status
        agendamento.data_agendada = request.POST.get('data_agendada') or agendamento.data_agendada

        agendamento.save()
        return redirect('/relatorios/agendamentos/')
    
    context = {
        'agendamento': agendamento,
        'clientes': clientes,
        'servicos': servicos,
        'profissionais': profissionais,
    }
    return render(request, "agendamentos/editar_agendamento.html", context)


def imprimir_relatorio(request):
    # Configurações do Selenium para rodar headless
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    selecionar_status = request.GET.get('selecionar_status', '')
    contexto = {
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'selecionar_status': selecionar_status,
    }

    html_str = render_to_string('imprimir/layout.html', contexto)
    
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf') 

    pdf_file = pdfkit.from_string(html_str, False, configuration=config)
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_agendamentos.pdf'
    return response

