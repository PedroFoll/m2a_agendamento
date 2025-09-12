from django import forms

class FiltroRelatorioForm(forms.Form):
    data_inicio = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    data_fim = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    status = forms.ChoiceField(
        choices=[
            ('', 'Todos'),
            ('pendente', 'Pendente'),
            ('concluido', 'Concluído'),
            ('cancelado', 'Cancelado')
        ],
        required=False
    )
