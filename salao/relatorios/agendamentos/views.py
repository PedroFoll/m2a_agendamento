from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

import tempfile
import fitz  # PyMuPDF
import os
import io
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from servicos.agendamento.models import Agendamento
from cadastros.cliente.models import Cliente
from cadastros.servicos.models import Servico
from cadastros.funcionarios.models import Profissional
from core.utils.helpers import Helpers, PDFHelper


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
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1920")
    options.add_argument("--hide-scrollbars")

    driver = webdriver.Chrome(options=options)
    # Defina o caminho correto para o arquivo HTML
    try:
        url= request.build_absolute_uri('/relatorios/layout/')
        url += f'?data_inicio={request.GET.get("data_inicio","")}&data_fim={request.GET.get("data_fim","")}&selecionar_status={request.GET.get("selecionar_status","")}'
        driver.get(url)
    except Exception as e:
        return HttpResponse(f"Erro ao carregar a página: {e}", status=500)
    # Tira o screenshot
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img:
        screenshot_path = tmp_img.name
        driver.save_screenshot(screenshot_path)
    driver.quit()

    # Cria o documento PDF em memória
    pdf_bytes = io.BytesIO()
    pdf = fitz.open()

    # Abre a imagem e insere no PDF
    img = fitz.Pixmap(screenshot_path)
    rect = fitz.Rect(0, 0, img.width, img.height)
    pdf_page = pdf.new_page(width=rect.width, height=rect.height)
    pdf_page.insert_image(rect, pixmap=img)

    # Salva o PDF em memória
    pdf.save(pdf_bytes)
    pdf.close()

    # Deleta o arquivo temporário da imagem
    os.remove(screenshot_path)

    # Retorna o PDF como resposta HTTP
    pdf_bytes.seek(0)  # Volta o ponteiro do arquivo para o começo
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'
    return response


def layout(request):
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

    }

    return render(request, "imprimir/layout.html", contexto)