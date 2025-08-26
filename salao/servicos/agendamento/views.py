#Imports Nativos

#Imports de Terceiros
from django.shortcuts import render

#imports core/common

#imports da aplicação

# Create your views here.

def home(request):


    return render(request, 'home.html')


def cadastro_cliente(request):
    

    return render(request, 'cadastro_cliente.html')
#2.1.1 - Eu como recepcionista, quero cadastrar :
#clientes - nome, telefone, email, data de nascimento
#serviços - nome, descrição, preço
#profissionais - nome, telefone, email, especialidade