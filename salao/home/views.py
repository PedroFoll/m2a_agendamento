from django.shortcuts import render
from core.utils.helpers import Helpers
from django.core.paginator import Paginator


def HomePage(request):
    if request.method =='GET':
        dados_clt = Helpers.cliente_Count()
        dados_age=Helpers.agenda_Count()
        dados_func=Helpers.func_count()
        agrp=Helpers.agrup_agen()
        data_range=Helpers.data_range_semana()

        
        paginator= Paginator(agrp, 5)
        numero_pagina = request.GET.get('pagina',1)
        pagina_atual = paginator.get_page(numero_pagina)

        
        
        return render(request,'home.html',{
            'qntd_clientes': dados_clt['qntd_clientes'],
            'total_clientes':dados_clt['total_clientes'],

            'qntd_agendamentos':dados_age['qntd_agendamentos'],
            'total_agendamentos_serv': dados_age['total_agendamentos_serv'],

            'qntd_funcionarios':dados_func['qntd_funcionarios'],
            'total_func':dados_func['total_func'],
            'agrp':pagina_atual,
            'data_range':data_range,

            }
            )
