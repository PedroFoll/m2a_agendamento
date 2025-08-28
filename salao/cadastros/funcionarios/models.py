from django.db import models

from core.models import Base

from cadastros.servicos.models import *


class Profissional(Base):
    nome = models.CharField(
        max_length=100, 
        verbose_name='Nome'
        )
    telefone = models.CharField(
        max_length=20, 
        verbose_name='Telefone'
        )
    email = models.EmailField(
        max_length=100, 
        verbose_name='Email'
        )
    especialidade = models.ForeignKey(
        Servico,
        to_field='id',
        on_delete=models.CASCADE,
        verbose_name="especialidade"
        )
    data_contratacao = models.DateField(
        verbose_name='Data de Contratação'
        )
    
    

    class Meta:
        verbose_name = 'Profissional'
        verbose_name_plural = 'Profissionais'
        db_table ='cliente_profissional'

    def __str__(self):
        return f'{self.nome}'
