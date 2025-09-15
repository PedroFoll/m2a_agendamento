from django.shortcuts import render, redirect

from servicos.agendamento.models import Agendamento
from cadastros.cliente.models import Cliente


def relatorio_agendamentos(request):
    limit = 5
    pagina = int(request.GET.get('pagina', 1))

    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')

    agendamentos = Agendamento.objects.all()
    qntd_agendamentos = agendamentos.count()
    selecionar_status = request.GET.get('selecionar_status')


    if selecionar_status:
        agendamentos = agendamentos.filter(
            status__iexact=selecionar_status.lower())

    if data_inicio and data_fim:
        agendamentos = agendamentos.filter(
            data_agendada__range=[data_inicio, data_fim])

    offset = (pagina - 1) * limit
    agendamentos = agendamentos.order_by('data_agendada')[offset:offset + limit]

    contexto = {
        'agendamentos': agendamentos,
        'qntd_agendamentos': qntd_agendamentos,
        'pagina': pagina,
        'limit': limit,
    }

    return render(request, "agendamentos/relatorio_agendamentos.html", contexto)

def relatorio_clientes(request):
    limit = 5
    pagina = int(request.GET.get('pagina', 1))
    clientes = Cliente.objects.all()
    qntd_clientes = clientes.count()
    nome_filtrar=request.GET.get('nome_filtrar')
    email_filtrar=request.GET.get('email_filtrar')
    tipo_usuario_filtrar= request.GET.get('tipo_usuario_filtrar')

    clientes = Cliente.objects.all()

    if nome_filtrar:
        clientes = clientes.filter(nome__contains=nome_filtrar)
    
    if email_filtrar:
        clientes = clientes.filter(email__contains=email_filtrar)
    
    if tipo_usuario_filtrar:
        clientes = clientes.filter(tipo_usuario__iexact=tipo_usuario_filtrar.lower())

    offset = (pagina - 1) * limit
    clientes = clientes.order_by('nome')[offset:offset + limit]

    contexto = {
        'clientes': clientes,
        'qntd_clientes': qntd_clientes,
        'pagina': pagina,
        'limit': limit,
    }


    return render(request, "clientes/relatorio_clientes.html", contexto)



def ver_cliente(request,id):
    cliente=Cliente.objects.get(id=id)
    return  render(request, "clientes/ver_clientes.html", {'cliente': cliente})


def ver_agendamento(request, id):
    agendamento=Agendamento.objects.get(id=id)
    return  render(request, "agendamentos/ver_agendamento.html", {'agendamento': agendamento})



def deletar_cliente(request,id):
    cliente=Cliente.objects.get(id=id)
    cliente.delete()
    return redirect('/relatorios/clientes/')

def deletar_agendamento(request, id):
    agendamento = Agendamento.objects.get(id=id)
    agendamento.delete()
    return redirect('/relatorios/agendamentos/')



def get_relatorio_clientes(request):
    limit = 5
    pagina = int(request.GET.get('pagina', 1))
    clientes = Cliente.objects.all()
    qntd_clientes = clientes.count()
    nome_filtrar=request.GET.get('nome_filtrar')
    email_filtrar=request.GET.get('email_filtrar')
    tipo_usuario_filtrar= request.GET.get('tipo_usuario_filtrar')

    clientes = Cliente.objects.all()

    if nome_filtrar:
        clientes = clientes.filter(nome__contains=nome_filtrar)
    
    if email_filtrar:
        clientes = clientes.filter(email__contains=email_filtrar)
    
    if tipo_usuario_filtrar:
        clientes = clientes.filter(tipo_usuario__iexact=tipo_usuario_filtrar.lower())

    offset = (pagina - 1) * limit
    clientes = clientes.order_by('nome')[offset:offset + limit]

    contexto = {
        'clientes': clientes,
        'qntd_clientes': qntd_clientes,
        'pagina': pagina,
        'limit': limit,
    }


    return (contexto)