from django.shortcuts import render
from core.utils.helpers import Helpers

def HomePage(request):
    if request.method =='GET':
        dados_clt = Helpers.cliente_Count()
        dados_age=Helpers.agenda_Count()
        dados_func=Helpers.func_count()
        return render(request,'home.html',{
            'qntd_clientes': dados_clt['qntd_clientes'],
            'total_clientes':dados_clt['total_clientes'],

            'qntd_agendamentos':dados_age['qntd_agendamentos'],
            'total_agendamentos_serv': dados_age['total_agendamentos_serv'],

            'qntd_funcionarios':dados_func['qntd_funcionarios'],
            'total_func':dados_func['total_func'],     
            }
            )
