from django.shortcuts import render

from core.utils.helpers import Helpers


def relatorio_geral(request):
   if request.method =='GET':
        
        agend_concluidos = Helpers.agendamento_concluido()
        agend_cancelados = Helpers.agendamento_cancelado()
        agend_pendentes = Helpers.agendamento_agendado()

        dados_clt = Helpers.cliente_Count()
        dados_age = Helpers.agenda_Count()
        dados_func = Helpers.func_count()

        servicos = Helpers.serv_count()
        valor_total_serv = Helpers.valor_total_servicos()
        
        rank_func = Helpers.rank_funcionarios()
        rank_cli = Helpers.rank_clientes()
        rank_serv = Helpers.rank_servicos()

        data_range=Helpers.data_range_semana()
        
        return render(request,'geral/geral.html',{
            'qntd_clientes': dados_clt['qntd_clientes'],
            'total_clientes':dados_clt['total_clientes'],
            'clientes':dados_clt['clientes'],

            'qntd_agendamentos':dados_age['qntd_agendamentos'],
            'total_agendamentos_serv': dados_age['total_agendamentos_serv'],
            'agendamentos':dados_age['agendamentos'],

            'qntd_funcionarios':dados_func['qntd_funcionarios'],
            'total_func':dados_func['total_func'],
            'funcionarios':dados_func['funcionarios'],

            'data_range':data_range,
            'servicos':servicos,
            'rank_func':rank_func,
            'rank_cli':rank_cli,
            'rank_serv':rank_serv,

            'agend_concluidos': agend_concluidos,
            'agend_cancelados': agend_cancelados,
            'agend_pendentes': agend_pendentes,
            'valor_total_serv': valor_total_serv,

            }
            )