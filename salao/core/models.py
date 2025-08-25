from django.db import models


class Base(models.Model):
    data_criacao = models.DateTimeField( #Registrar data de criação do registro
        auto_now_add=True,
        null=True,
        blank=True,
        verbose_name='Data de Criação'
    )
    data_modificacao = models.DateTimeField(    #Registrar data de modificação do registro
        auto_now=True,
        null=True,
        blank=True,
        verbose_name='Data de Modificação'
    )
    class Meta:
        abstract = True