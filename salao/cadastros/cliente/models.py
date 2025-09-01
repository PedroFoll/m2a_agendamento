from django.db import models

from core.models import Base
# Create your models here.

#2.1.1 - Eu como recepcionista, quero cadastrar :
#clientes - nome, telefone, email, data de nascimento, cpf
#serviços - nome, descrição, preço
#profissionais - nome, telefone, email, especialidade


class Cliente(Base):
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
    cpf = models.CharField(
        max_length=11, 
        verbose_name='CPF', 
        unique=True
        )
    foto = models.ImageField(
        upload_to='clientes/', 
        blank=True, 
        null=True
    )
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'cliente_cliente'
    
    def __str__(self):
        return f'{self.nome} - {self.cpf} - {self.data_nascimento} - {self.foto}'
