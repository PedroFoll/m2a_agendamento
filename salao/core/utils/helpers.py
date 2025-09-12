from servicos.agendamento.models import Agendamento
from cadastros.cliente.models import Cliente
from cadastros.funcionarios.models import Profissional
from cadastros.servicos.models import Servico

from django.utils import timezone
from django.db.models import Count, Sum, Prefetch
from django.db.models.functions import TruncDate
from django.shortcuts import redirect, get_object_or_404


from datetime import date, datetime, timedelta

from datetime import datetime, timedelta
from .forms import FiltroRelatorioForm

import calendar
from collections import defaultdict



class Helpers():

    def cliente_Count():
        clientes = Cliente.objects.all().order_by('nome')[:5]
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
        agendamentos = Agendamento.objects.all().order_by('data_agendada')[:5]
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
        funcionarios = Profissional.objects.all().order_by('nome')[:5]
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
        amanha = inicio_da_semana + timedelta(days=1)

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
            .order_by('-total_servicos')[:5]
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
                agendamentos = agendamentos.filter(data_agendada__gte=data_inicio)
            if data_fim:
                agendamentos = agendamentos.filter(data_agendada__lte=data_fim)
            if status:
                agendamentos = agendamentos.filter(status=status)

        # 🔹 Métricas
        total_agendamentos = agendamentos.count()
        total_arrecadado = agendamentos.aggregate(
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
    

class AgendarHelper():
    @staticmethod
    def proximos_dias_agendamentos():
        hoje = date.today()
        dias = []

        
        labels = ["Hoje", "Amanhã", "Depois de amanhã"]

        for i, label in enumerate(labels):
            dia = hoje + timedelta(days=i)
            agendamentos = Agendamento.objects.filter(data_agendada__date=dia)
            conta_agend_hoje = Agendamento.objects.filter(data_agendada__date=hoje).count()

            dias.append({
                "data": dia,
                "label": label,
                "is_today": i == 0,
                "appointments": agendamentos,
                "contagem":conta_agend_hoje
            })

        return {"proximos_dias": dias}
    

    def alterar_status(request, id, status):
        agendamento = Agendamento.objects.get(id=id)
        agendamento.status = status
        agendamento.save()

        return redirect(request.META.get("HTTP_REFERER", "relatorios:lista_agendamentos"))
        