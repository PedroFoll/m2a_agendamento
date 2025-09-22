from math import ceil

from django.shortcuts import render, redirect

from servicos.agendamento.models import Agendamento
from cadastros.cliente.models import Cliente


def relatorio_clientes(request):
    limit = 25
    pagina = int(request.GET.get('pagina', 1))

    clientes = Cliente.objects.all()
    qntd_clientes = clientes.count()
    nome_filtrar=request.GET.get('nome_filtrar')
    email_filtrar=request.GET.get('email_filtrar')
    tipo_usuario_filtrar= request.GET.get('tipo_usuario_filtrar')

    if nome_filtrar:
        clientes = clientes.filter(nome__contains=nome_filtrar)
    
    if email_filtrar:
        clientes = clientes.filter(email__contains=email_filtrar)
    
    if tipo_usuario_filtrar:
        clientes = clientes.filter(tipo_usuario__iexact=tipo_usuario_filtrar.lower())

    total_paginas = ceil(qntd_clientes / limit)
    paginas = list(range(1, total_paginas + 1))

    offset = (pagina - 1) * limit
    clientes = clientes.order_by('nome')[offset:offset + limit]

    contexto = {
        'clientes': clientes,
        'qntd_clientes': qntd_clientes,
        'pagina': pagina,
        'limit': limit,
        'total_paginas': total_paginas,
        'paginas': paginas,
    }

    return render(
        request,
        "clientes/relatorio_clientes.html",
        contexto
        )


def ver_cliente(request,id):
    cliente=Cliente.objects.get(id=id)
    return  render(
        request,
        "clientes/ver_clientes.html",
        {'cliente': cliente}
        )


def ver_agendamento(request, id):
    agendamento=Agendamento.objects.get(id=id)
    return  render(
        request,
        "agendamentos/ver_agendamento.html",
        {'agendamento': agendamento}
    )


def deletar_cliente(request,id):
    cliente=Cliente.objects.get(id=id)
    cliente.delete()
    return redirect(
        '/cadastros/cliente/criar_cliente/'
        )

def deletar_agendamento(request, id):
    agendamento = Agendamento.objects.get(id=id)
    agendamento.delete()
    return redirect(
        '/relatorios/agendamentos/'
        )


def get_relatorio_clientes(request):
    limit = 10
    pagina = int(request.GET.get('pagina', 1))
    letra = request.GET.get("letra")  

    clientes = Cliente.objects.all()
    nome_filtrar=request.GET.get('nome_filtrar')
    email_filtrar=request.GET.get('email_filtrar')
    cpf_filtrar = request.GET.get('cpf_filtrar')
    phone_filtrar = request.GET.get('phone_filtrar')

    clientes = Cliente.objects.all()

    if nome_filtrar:
        clientes = clientes.filter(nome__contains=nome_filtrar)
    
    if email_filtrar:
        clientes = clientes.filter(email__contains=email_filtrar)

    if cpf_filtrar:
        clientes = clientes.filter(cpf__contains=cpf_filtrar)
    
    if phone_filtrar:
        clientes = clientes.filter(telefone__contains=phone_filtrar)
    
    if letra:
        clientes = Cliente.objects.filter(nome__istartswith=letra)
    

    qntd_clientes = clientes.count()

    total_paginas = ceil(qntd_clientes / limit)
    paginas = list(range(1, total_paginas + 1))

    offset = (pagina - 1) * limit
    clientes = clientes.order_by('nome')[offset:offset + limit]

    contexto = {
        'clientes': clientes,
        'qntd_clientes': qntd_clientes,
        'pagina': pagina,
        'limit': limit,
        'total_paginas': total_paginas,
        'paginas': paginas,
        'letra': letra
    }

    return (contexto)