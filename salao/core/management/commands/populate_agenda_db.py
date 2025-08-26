from faker import Faker
from datetime import datetime
import random

from django.core.management.base import BaseCommand

from core.utils.geradores import Helpers

from cadastros.cliente.models import Profissional, Servico, Cliente

class Command(BaseCommand):
    help = "Cria dados falsos no banco de dados"

    def handle(self, *args, **kwargs):

        nome = random.choice(list(Cliente.objects.all()))
        profissional=random.choice(list(Profissional.objects.all()))
        email = Helpers.gerador_email()
        random_number = Helpers.gerador_telefone()
        espec=random.choice(list(Servico.objects.all()))
        data = datetime.now()

        #cria manualmente objetos de model empresa
        profissionais = [
            Profissional(
                nome=nome,
                profissional=profissional,
                telefone=random_number,
                especialidade=espec,
                data_contratacao=data,
            ),           
        ]
        #insere no banco
        for profissional in profissionais:
          try:
            print("salvando "+profissional.nome)
            print(data)
            profissional.save()
          except Exception as erro:
            print(erro)
            pass
        #redireciona para pegar do banco de dados
        profissional = Profissional.objects.all()