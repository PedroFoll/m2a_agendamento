from math import ceil
import fitz 

from servicos.agendamento.models import Agendamento
from cadastros.cliente.models import Cliente
from cadastros.funcionarios.models import Profissional
from cadastros.servicos.models import Servico

from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.shortcuts import redirect, get_object_or_404, HttpResponse

from datetime import date, datetime, timedelta

from datetime import datetime, timedelta
from .forms import FiltroRelatorioForm

from collections import defaultdict



class Helpers():

    def cliente_Count():
        clientes = Cliente.objects.all().order_by('nome')
        qntd_clientes = clientes.count()

        total_clientes = (
            Cliente.objects.values('ativo')
            .annotate(total=Count('id'))
            .order_by('ativo')
        )
        
        return ({
            'qntd_clientes': qntd_clientes,
            'total_clientes':total_clientes,
            'clientes':clientes 
            })
    
    def agenda_Count():
        agendamentos = Agendamento.objects.all().order_by('data_agendada')
        qntd_agendamentos = agendamentos.count()

        total_agendamentos_serv = (
            Agendamento.objects.values('servico__nome')
            .annotate(total=Count('id')) 
            .order_by('servico__nome')
        )

        for agend in total_agendamentos_serv:
            agend['percentual']= round((agend['total'] / qntd_agendamentos)*100,2)

        return({
            'qntd_agendamentos':qntd_agendamentos,
            'total_agendamentos_serv': total_agendamentos_serv,
            'agendamentos':agendamentos}
            )
    
    def func_count():
        funcionarios = Profissional.objects.all().order_by('nome')
        qntd_funcionarios = funcionarios.count()

        total_func = (
            Profissional.objects.values('ativo')
            .annotate(total=Count('id'))
            .order_by('ativo')
        )
        
        return ({
            'qntd_funcionarios':qntd_funcionarios,
            'total_func':total_func,
            'funcionarios':funcionarios,
            }
            )
    

    def agrup_agen():    
        
        hoje = datetime.now().date()
        
        # Calcule o dia do início da semana (segunda-feira)
        # hoje.weekday() retorna 0 para segunda, 1 para terça, ..., 6 para domingo
        dias_para_subtrair = hoje.weekday()
        inicio_da_semana = hoje - timedelta(days=dias_para_subtrair)
        
        # Calcule o fim da semana (domingo)
        fim_da_semana = inicio_da_semana + timedelta(days=6)
        
        # 2. Modifique a query para filtrar os agendamentos da semana atual
        agrp_data = Agendamento.objects.filter(
            data_agendada__date__range=[inicio_da_semana, fim_da_semana]
        ).annotate(
            dia=TruncDate('data_agendada')
        ).values('dia').annotate(
            total_agendamentos=Count('dia')
        ).order_by('dia')
        
        agrp_ajustado = []
        
        dias_semana = [
                'Segunda-feira',
                'Terça-feira',
                'Quarta-feira',
                'Quinta-feira',
                'Sexta-feira',
                'Sábado',
                'Domingo'
                ]
        
        for data in agrp_data:
            data_objeto = data['dia']
            nome_dia_semana = dias_semana[data_objeto.weekday()]
            data_formatada = data_objeto.strftime("%d/%m/%Y")
            conta_agendamentos = data['total_agendamentos']

            agrp_ajustado.append({
                'dia_nome': f"{data_formatada}: {nome_dia_semana}",
                'total_agendamentos': conta_agendamentos
            })
        return agrp_ajustado


    def data_range_semana():
        hoje = datetime.now().date()
        agendamentos_hoje = Agendamento.objects.filter(
            data_agendada__date=hoje).count()

        dia_da_semana = hoje.weekday()
        inicio_da_semana = hoje - timedelta(days=dia_da_semana)

        fim_da_semana = inicio_da_semana + timedelta(days=6)
        amanha = hoje + timedelta(days=1)

        agendamentos_semana = Agendamento.objects.filter(
            data_agendada__date__range=[
                inicio_da_semana, 
                fim_da_semana]).count()

        context={
            'agendamentos_hoje': agendamentos_hoje,
            'agendamentos_semana': agendamentos_semana,
            'inicio_da_semana': inicio_da_semana.strftime('%Y-%m-%d'),
            'fim_da_semana': fim_da_semana.strftime('%Y-%m-%d'),
            'amanha': amanha.strftime('%Y-%m-%d'),
            'hoje': hoje.strftime('%Y-%m-%d'),
        }

        return context
    
    def serv_count():
        servicos= Servico.objects.all()
        qntd_servicos = servicos.count()

        return qntd_servicos
    

    def rank_funcionarios():
        ranking = (
            Agendamento.objects.values('profissional__nome')
            .annotate(total_servicos=Count('id'))
            .order_by('-total_servicos')[:5]
        )
        return ranking
    
    def rank_servicos():
        ranking = (
            Agendamento.objects.values('servico__nome')
            .annotate(total_servicos=Count('id'))
            .order_by('-total_servicos')[:5]
        )
        return ranking
    
    def rank_clientes():
        ranking = (
            Agendamento.objects.values('cliente__nome')
            .annotate(total_servicos=Count('id'))
            .order_by('-total_servicos')
        )
        return ranking
    
    def agendamento_concluido():

        agendamentos_concluidos = Agendamento.objects.filter(status='Concluído').count()
        return agendamentos_concluidos
    
    def agendamento_cancelado():

        agendamentos_cancelados = Agendamento.objects.filter(status='Cancelado').count()
        return agendamentos_cancelados
    
    def agendamento_agendado():

        agendamentos_agendados = Agendamento.objects.filter(status='Agendado').count()
        return agendamentos_agendados
    
    @staticmethod
    def valor_total_servicos():
        total_valor_servicos = (
            Agendamento.objects
            .filter(status="Concluído")  # só pega concluídos
            .aggregate(total_valor=Sum('servico__preco'))['total_valor'] or 0
        )
        return total_valor_servicos
    

    def relatorio_geral(request):
        form = FiltroRelatorioForm(request.GET or None)

        agendamentos = Agendamento.objects.all()

        # 🔹 Se o form for válido, pega os dados filtrados
        if form.is_valid():
            periodo = form.cleaned_data.get('periodo')
            data_inicio = form.cleaned_data.get('data_inicio')
            data_fim = form.cleaned_data.get('data_fim')
            status = form.cleaned_data.get('status')

            # 🔹 Ajusta período automático
            if periodo == 'semanal':
                data_inicio = datetime.today() - timedelta(days=7)
                data_fim = datetime.today()
            elif periodo == 'mensal':
                data_inicio = datetime.today().replace(day=1)
                data_fim = datetime.today()

            # 🔹 Aplica filtros
            if data_inicio:
                agendamentos = agendamentos.filter(data_agendada__gte=data_inicio).order_by('data_agendada')
            if data_fim:
                agendamentos = agendamentos.filter(data_agendada__lte=data_fim)
            if status:
                agendamentos = agendamentos.filter(status=status)

        # 🔹 Métricas
        total_agendamentos = agendamentos.count()
        total_arrecadado = agendamentos.filter(status='Concluído').aggregate(
            total=Sum('servico__preco')
        )['total'] or 0

        cliente_top = (
            agendamentos.values('cliente__nome')
            .annotate(total=Count('id'))
            .order_by('-total')
            .first()
        )

        funcionario_top = (
            agendamentos.filter(status='concluido')
            .values('profissional__nome')
            .annotate(total=Count('id'))
            .order_by('-total')
            .first()
        )

        return {
            'form': form,  # 🔹 manda o form para o template também
            'total_agendamentos': total_agendamentos,
            'total_arrecadado': total_arrecadado,
            'cliente_top': cliente_top,
            'funcionario_top': funcionario_top,
            'agendamentos': agendamentos,
        }
    

    def agenda_cliente():
        agenda_cliente = (
            Agendamento.objects.values('cliente__nome')  # agrupar por nome do cliente
            .annotate(total_servicos=Count('id'))  # contar quantos agendamentos o cliente tem
            .order_by('-total_servicos')  # ordena pela quantidade de serviços
        )
        return agenda_cliente
    
    def get_funcionarios(request):
        limit = 10  # Limitar a quantidade de registros por página
        pagina = int(request.GET.get('pagina', 1))  # Página atual
        letra = request.GET.get("letra")  # Filtro pela primeira letra do nome

        # Consultar todos os profissionais
        profissionais = Profissional.objects.all()

        # Filtros de pesquisa
        nome_filtrar = request.GET.get('nome_filtrar')
        email_filtrar = request.GET.get('email_filtrar')
        cpf_filtrar = request.GET.get('cpf_filtrar')
        phone_filtrar = request.GET.get('phone_filtrar')

        # Aplicar filtros de acordo com o que foi passado no formulário
        if nome_filtrar:
            profissionais = profissionais.filter(nome__contains=nome_filtrar)
        
        if email_filtrar:
            profissionais = profissionais.filter(email__contains=email_filtrar)

        if cpf_filtrar:
            profissionais = profissionais.filter(cpf__contains=cpf_filtrar)
        
        if phone_filtrar:
            profissionais = profissionais.filter(telefone__contains=phone_filtrar)
        
        # Filtro pela letra inicial do nome
        if letra:
            profissionais = Profissional.objects.filter(nome__istartswith=letra)

        # Contagem do total de profissionais
        qntd_profissionais = profissionais.count()

        # Cálculo de páginas
        total_paginas = ceil(qntd_profissionais / limit)
        paginas = list(range(1, total_paginas + 1))

        # Paginação
        offset = (pagina - 1) * limit
        profissionais = profissionais.order_by('nome')[offset:offset + limit]

        contexto = {
            'profissionais': profissionais,  # Lista de profissionais
            'qntd_profissionais': qntd_profissionais,  # Quantidade total de profissionais
            'pagina': pagina,  # Página atual
            'limit': limit,  # Limite de profissionais por página
            'total_paginas': total_paginas,  # Total de páginas
            'paginas': paginas,  # Páginas para navegação
            'letra': letra  # Letra para filtro
        }

        return contexto
    

class AgendarHelper():
    @staticmethod
    def proximos_dias_agendamentos():
        hoje = date.today()
        dias = []

        
        labels = ["Hoje", "Amanhã", "Depois de amanhã"]

        for i, label in enumerate(labels):
            dia = hoje + timedelta(days=i)
            agendamentos = Agendamento.objects.filter(data_agendada__date=dia).order_by('data_agendada')
            conta_agend_hoje = Agendamento.objects.filter(data_agendada__date=hoje).count()

            dias.append({
                "data": dia,
                "label": label,
                "is_today": i == 0,
                "appointments": agendamentos,
                "contagem":conta_agend_hoje
            })

        return {"proximos_dias": dias}
    
class PDFHelper():
    def gerar_pdf_relatorio(agendamentos, clientes, faturamento):
        # cria um documento em memória
        pdf = fitz.open()

        # adiciona uma página
        page = pdf.new_page()

        # título
        page.insert_text((50, 50), "Relatório de Agendamentos", fontsize=18, fontname="helv")

        # insere métricas
        page.insert_text((50, 90), f"Total de Agendamentos: {agendamentos}", fontsize=12)
        page.insert_text((50, 110), f"Clientes Cadastrados: {clientes}", fontsize=12)
        page.insert_text((50, 130), f"Faturamento do Período: R$ {faturamento}", fontsize=12)

        # insere tabela simples de agendamentos recentes (exemplo)
        y = 170
        page.insert_text((50, y), "Agendamentos Recentes:", fontsize=14)
        y += 30
        for a in agendamentos[:10]:  # lista ou queryset
            linha = f"{a.cliente.nome} - {a.servico.nome} - {a.profissional.nome} - {a.data_agendada:%d/%m/%Y %H:%M} - {a.status}"
            page.insert_text((50, y), linha, fontsize=10)
            y += 15

        # retorna o PDF como HttpResponse
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'
        response.write(pdf.tobytes())  # transforma em bytes e escreve na resposta
        pdf.close()
        return response