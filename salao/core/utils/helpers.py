from servicos.agendamento.models import Agendamento
from cadastros.cliente.models import Cliente
from cadastros.funcionarios.models import Profissional
from cadastros.servicos.models import Servico
from django.db.models import Count
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta



class Helpers():

    def cliente_Count():
        clientes = Cliente.objects.all()
        qntd_clientes = clientes.count()

        total_clientes = (
            Cliente.objects.values('ativo')
            .annotate(total=Count('id'))
            .order_by('ativo')
        )
        
        return ({
            'qntd_clientes': qntd_clientes,
            'total_clientes':total_clientes})
    
    def agenda_Count():
        agendamentos = Agendamento.objects.all()
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
            }
            )
    
    def func_count():
        funcionarios = Profissional.objects.all()
        qntd_funcionarios = funcionarios.count()

        total_func = (
            Profissional.objects.values('ativo')
            .annotate(total=Count('id'))
            .order_by('ativo')
        )
        
        return ({
            'qntd_funcionarios':qntd_funcionarios,
            'total_func':total_func,
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