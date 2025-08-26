
from faker import Faker

from django.core.management.base import BaseCommand

from core.utils.gerador_cpf import cpf_validado
from core.utils.geradores import Helpers

from cadastros.cliente.models import Cliente

fake = Faker('pt_BR')
nome = fake.name()
email = Helpers.gerador_email()
random_number = Helpers.gerador_telefone()
cpf = cpf_validado
data = Helpers.gerador_data_hora()


class Command(BaseCommand):
    help = "Cria dados falsos no banco de dados"

    def handle(self, *args, **kwargs):

        #cria manualmente objetos de model empresa
        clientes = [
            Cliente(
                nome=nome,
                email=email,
                telefone=random_number,
                data_nascimento=data,
                cpf=cpf_validado
            ),           
        ]
        #insere no banco
        for cliente in clientes:
          try:
            print("salvando "+cliente.nome)
            print(data)
            cliente.save()
          except Exception as erro:
            print(erro)
            pass
        #redireciona para pegar do banco de dados
        cliente = Cliente.objects.all()