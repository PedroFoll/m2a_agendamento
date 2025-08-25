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
        verbose_name='Nome')
    telefone = models.CharField(
        max_length=20, 
        verbose_name='Telefone')
    email = models.EmailField(
        max_length=100, 
        verbose_name='Email')
    data_nascimento = models.DateField(
        verbose_name='Data de Nascimento')
    cpf = models.CharField(
        max_length=11, 
        verbose_name='CPF', 
        unique=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


class Servico(Base):
    nome = models.CharField(
        max_length=100, 
        verbose_name='Nome')
    descricao = models.TextField(
        verbose_name='Descrição')
    preco = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Preço')

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'


class Profissional(Base):
    nome = models.CharField(
        max_length=100, 
        verbose_name='Nome')
    telefone = models.CharField(
        max_length=20, 
        verbose_name='Telefone')
    email = models.EmailField(
        max_length=100, 
        verbose_name='Email')
    especialidade = models.CharField(
        max_length=100, 
        verbose_name='Especialidade')
    data_contratacao = models.DateField(
        verbose_name='Data de Contratação')

    class Meta:
        verbose_name = 'Profissional'
        verbose_name_plural = 'Profissionais'
