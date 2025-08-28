from django.db import models

from core.models import Base


class Servico(Base):
    nome = models.CharField(
        max_length=100, 
        verbose_name='Serviço'
        )
    descricao = models.TextField(
        verbose_name='Descrição'
        )
    preco = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Valor'
        )

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        db_table = 'cliente_servico'
    
    def __str__(self):
        return f'{self.nome}'