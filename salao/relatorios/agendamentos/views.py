from math import ceil
from time import sleep

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import HttpResponse
from django.urls import reverse
from urllib.parse import urlencode

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import fitz

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

    total_paginas = ceil(qntd_agendamentos / limit)
    
    if total_paginas <= 4:
        paginas_exibidas = list(range(1, total_paginas + 1))
    else:
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
        'paginas': paginas_exibidas 
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


def imprimir_layout(request):
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    selecionar_status = request.GET.get('selecionar_status', '')

    qs = Agendamento.objects.all()
    if data_inicio and data_fim:
        qs = qs.filter(data_agendada__date__range=[data_inicio, data_fim])
    if selecionar_status:
        qs = qs.filter(status=selecionar_status)

    contexto = {
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'selecionar_status': selecionar_status,
        'agendamentos': qs,
    }
    return render(request, 'imprimir/layout.html', contexto)


def imprimir_relatorio_pdf(request):
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')
    selecionar_status = request.GET.get('selecionar_status', '')

    base_path = reverse('relatorios:imprimir_layout') 
    query = urlencode({
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'selecionar_status': selecionar_status
    })
    url = request.build_absolute_uri(f"{base_path}?{query}")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "print-ready"))
        )

        width = driver.execute_script("return Math.max(document.body.scrollWidth, document.documentElement.scrollWidth);")
        height = driver.execute_script("return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);")

        driver.set_window_size(width, height)
        sleep(0.5)
        png = driver.get_screenshot_as_png()

    finally:
        driver.quit()

    img_doc = fitz.open("png", png)
    rect = img_doc[0].rect
    pdf_doc = fitz.open()
    page = pdf_doc.new_page(width=rect.width, height=rect.height)
    page.insert_image(rect, stream=png)
    pdf_bytes = pdf_doc.write()
    pdf_doc.close()
    img_doc.close()

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_agendamentos.pdf"'
    return response