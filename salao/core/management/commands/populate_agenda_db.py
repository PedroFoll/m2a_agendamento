from datetime import datetime, timedelta
import random

from django.core.management.base import BaseCommand

from cadastros.cliente.models import Cliente
from cadastros.funcionarios.models import Profissional
from cadastros.servicos.models import Servico

from servicos.agendamento.models import Agendamento

class Command(BaseCommand):
    help = "Cria dados falsos no banco de dados"

    def handle(self, *args, **kwargs):
        nome = random.choice(list(Cliente.objects.all()))
        profissional=random.choice(list(Profissional.objects.all()))
        espec=random.choice(list(Servico.objects.all()))
        days=random.randint(1,10)
        data_hoje = datetime.now()
        data = data_hoje + timedelta(days=days)

        #cria manualmente objetos de model empresa
        agendamentos = [
            Agendamento(
                cliente_id=nome.id,
                profissional_id=profissional.id,
                servico_id=espec.id,
                data_agendada=data,
            ),           
        ]
        #insere no banco
        for agendamento in agendamentos:
          try:
            agendamento.save()
          except Exception as erro:
            pass
        #redireciona para pegar do banco de dados
        agendamento = Agendamento.objects.all()