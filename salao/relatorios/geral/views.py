from django.shortcuts import render
from django import forms
from core.utils.helpers import Helpers


def relatorio_geral(request):
   if request.method =='GET':
        
        geral = Helpers.relatorio_geral(request)
        rank_func = Helpers.rank_funcionarios()
        rank_cli = Helpers.rank_clientes()
        rank_serv = Helpers.rank_servicos()
        
        return render(request,'geral/geral.html',{
            'form': geral['form'],
            'agendamentos': geral['agendamentos'][:25],
            'total_agendamentos': geral['total_agendamentos'],
            'total_arrecadado': geral['total_arrecadado'],
            'rank_func':rank_func,
            'rank_cli':rank_cli,
            'rank_serv':rank_serv,
            }
            )
   

