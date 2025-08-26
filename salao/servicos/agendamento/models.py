from django.db import models

from core.models import Base

from cadastros.cliente.models import *

#2.2.1 - Eu como reepcionista, quero poder agendar:
#1- Um serviço para um cliente, com um profissional e um serviço, em uma data e horário específicos.
#1.1- Preciso do nome do cliente, nome do profissionla, o serviço que será realizado, a data e o horário do agendamento.
#2- O status do agendamento (Agendado, Concluído, Cancelado)

# Create your models here.

class Agendamento(Base):
    #Nome do cliente
    cliente=models.ForeignKey(
        Cliente,
        verbose_name='Cliente',
        to_field='id', 
        on_delete=models.CASCADE
    )
    #Serviço
    servico=models.ForeignKey(
        Servico,
        verbose_name='Serviço',
        to_field='id',
        on_delete=models.CASCADE
    )
    #Profissional Especifico
    profissional=models.ForeignKey(
        Profissional,
        verbose_name='Profissionais',
        to_field='id',
        on_delete=models.CASCADE
    )
    #Estado do serviço, marcado como padrão em: Agendado dentro do banco
    status = models.CharField(
        verbose_name='Estado do agendamento',
        max_length=20, 
        default='Agendado'
    )
    #Data e hora especificada
    data_agendada = models.DateTimeField(
        verbose_name="Dia agendado"
    )

    def __str__(self):
        return f'{self.cliente} - {self.data_agendada}'