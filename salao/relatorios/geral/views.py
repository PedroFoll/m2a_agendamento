from django.shortcuts import render
from django import forms
from core.utils.helpers import Helpers


def relatorio_geral(request):
   if request.method =='GET':
        
        geral = Helpers.relatorio_geral(request)
        
        return render(request,'geral/geral.html',{
            'form': geral['form'],
            'cliente_top': geral['cliente_top'],
            'agendamentos': geral['agendamentos'],
            'funcionario_top': geral['funcionario_top'],
            'total_agendamentos': geral['total_agendamentos'],
            'total_arrecadado': geral['total_arrecadado'],
            }
            )
   

   class FiltroRelatorioForm(forms.Form):
        PERIODO_CHOICES = [
            ('hoje', 'Hoje'),
            ('ontem', 'Ontem'),
            ('semana_atual', 'Semana Atual'),
            ('mes_atual', 'Mês Atual'),
            ('ano_atual', 'Ano Atual'),
            ('personalizado', 'Personalizado'),
        ]

        periodo = forms.ChoiceField(choices=PERIODO_CHOICES, required=False, label='Período')
        data_inicio = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Data Início')
        data_fim = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}), label='Data Fim')

        STATUS_CHOICES = [
            ('todos', 'Todos'),
            ('concluido', 'Concluído'),
            ('cancelado', 'Cancelado'),
            ('pendente', 'Pendente'),
        ]

        status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label='Status')
        funcionario = forms.CharField(max_length=100, required=False, label='Funcionário')
        cliente = forms.CharField(max_length=100, required=False, label='Cliente')

    