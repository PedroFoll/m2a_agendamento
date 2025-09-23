from django.shortcuts import render, HttpResponse, redirect
from .models import Cliente
from relatorios.clientes.views import get_relatorio_clientes

# Create your views here.
def cadastro_usuario(request):
    if request.method == "GET":
        return render (request, "cadastros/clientes/cadastrar_login.html")
    else:
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        cpf = request.POST.get('cpf')

        user = Cliente(
            nome=nome,
            email=email,
            telefone=telefone,
            cpf=cpf)
        
        user.save()

        return redirect('/cadastros/cliente/criar_cliente/')

def criar_cliente(request):
    # Inicia a consulta de clientes
    clientes = Cliente.objects.all()

    # Captura filtros do GET
    nome_filtrar = request.GET.get('nome_filtrar')
    email_filtrar = request.GET.get('email_filtrar')
    cpf_filtrar = request.GET.get('cpf_filtrar')

    # Aplica filtros
    if nome_filtrar:
        clientes = clientes.filter(nome__icontains=nome_filtrar)
    if email_filtrar:
        clientes = clientes.filter(email__icontains=email_filtrar)
    if cpf_filtrar:
        clientes = clientes.filter(cpf__icontains=cpf_filtrar)


    # Prepara o contexto com os dados filtrados e a quantidade de agendamentos
    consulta_cliente = get_relatorio_clientes(request)
    if request.method == "GET":
        contexto = {
            'clientes': consulta_cliente['clientes'],
            'qntd_clientes': consulta_cliente['qntd_clientes'],
            'pagina': consulta_cliente['pagina'],
            'limit': consulta_cliente['limit'],
        }
        return render(request, "cadastros/clientes/criar_cliente.html", contexto)
