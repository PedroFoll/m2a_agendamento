from django.shortcuts import render, HttpResponse
from servicos.agendamento.models import Agendamento
from cadastros.cliente.models import Cliente
from cadastros.funcionarios.models import Profissional
from cadastros.servicos.models import Servico



def HomePage(request):
    if request.method =='GET':
        clientes = Cliente.objects.all()
        qntd_clientes = clientes.count()
        agendamentos = Agendamento.objects.all()
        qntd_agendamentos = agendamentos.count()
        funcionarios = Profissional.objects.all()
        qntd_funcionarios = funcionarios.count()
        servicos = Servico.objects.all()
        qntd_servicos = servicos.count()

        return render(request,'home.html', {
            'qntd_clientes': qntd_clientes,
            'qntd_agendamentos':qntd_agendamentos,
            'qntd_funcionarios':qntd_funcionarios,
            'qntd_servicos':qntd_servicos
            }
            )