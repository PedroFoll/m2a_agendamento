from servicos.agendamento.models import Agendamento
from cadastros.cliente.models import Cliente
from cadastros.funcionarios.models import Profissional
from cadastros.servicos.models import Servico
from django.db.models import Count


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
            'total_func':total_func,            }
            )
        