from math import ceil

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import HttpResponse
from django.template.loader import render_to_string

import pdfkit

from core.utils.helpers import Helpers

from servicos.agendamento.models import Agendamento
from cadastros.cliente.models import Cliente
from cadastros.servicos.models import Servico
from cadastros.funcionarios.models import Profissional

def relatorio_agendamentos(request):
    geral = Helpers.relatorio_geral(request)
    limit = 25
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

    total_paginas = ceil(qntd_agendamentos / limit)
    paginas = list(range(1, total_paginas + 1))

     # Cálculo do número total de páginas
    total_paginas = ceil(qntd_agendamentos / limit)
    
    # Garantir sempre exibir 4 páginas consecutivas
    if total_paginas <= 4:
        paginas_exibidas = list(range(1, total_paginas + 1))
    else:
        # Lógica para garantir 4 páginas consecutivas
        if pagina <= 2:
            paginas_exibidas = [1, 2, 3, 4]
        elif pagina == total_paginas - 1:
            paginas_exibidas = [total_paginas - 3, total_paginas - 2, total_paginas - 1, total_paginas]
        elif pagina == total_paginas:
            paginas_exibidas = [total_paginas - 3, total_paginas - 2, total_paginas - 1, total_paginas]
        else:
            paginas_exibidas = [pagina - 1, pagina, pagina + 1, pagina + 2]

    offset = (pagina - 1) * limit
    agendamentos = agendamentos.order_by('data_agendada')[offset:offset + limit]

    contexto = {
        'total_agendamentos': geral['total_agendamentos'],
        'agendamentos': agendamentos,
        'qntd_agendamentos': qntd_agendamentos,
        'pagina': pagina,
        'limit': limit,
        'total_paginas': total_paginas,
        'paginas': paginas_exibidas  # Passa apenas as páginas que queremos exibir
    }
    return render(
        request, "agendamentos/relatorio_agendamentos.html", contexto
        )


def ver_agendamento(request, id):
    agendamento = Agendamento.objects.get(pk=id)
    contexto = {
        "agendamento": agendamento
    }
    return  render(
        request, "agendamentos/ver_agendamento.html", contexto
        )
    
def deletar_agendamento(request, id):
    agendamento = Agendamento.objects.get(id=id)
    agendamento.delete()
    return redirect(
        '/relatorios/agendamentos/'
        )

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
        return redirect(
            '/servicos/agendamento/'
            )
    
    context = {
        'agendamento': agendamento,
        'clientes': clientes,
        'servicos': servicos,
        'profissionais': profissionais,
    }
    return render(
        request,
        "agendamentos/editar_agendamento.html",
        context
        )


def imprimir_relatorio(request):
    # Configurações do Selenium para rodar headless
    """ data_inicio = request.GET.get('data_inicio', '')
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
 """
    return HttpResponse("Em desenvolvimento")
