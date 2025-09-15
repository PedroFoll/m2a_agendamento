from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Cliente
from relatorios.clientes.views import get_relatorio_clientes

# Create your views here.
def cadastro_usuario(request):
    
    if request.method == "GET":
        return render (request, "cadastros/clientes/cadastrar_login.html")
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse('Já existe um usuário com esse username')
        else:
            user = User.objects.create_user(username=username, 
                                            email=email, 
                                            password=senha, 
                                            first_name= first_name, 
                                            last_name=last_name)
            user.save()

        return HttpResponse('Deu bom')

def criar_cliente(request):
    consulta_cliente = get_relatorio_clientes(request)
    clientes = consulta_cliente['clientes']
    qntd_clientes = consulta_cliente['qntd_clientes']
    pagina = consulta_cliente['pagina']
    limit = consulta_cliente['limit']

    if request.method == "GET":
        contexto = {
        'clientes': clientes,
        'qntd_clientes': qntd_clientes,
        'pagina': pagina,
        'limit': limit,
    }
        return render(request, "cadastros/clientes/criar_cliente.html", contexto)
    else:
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        cpf = request.POST.get('cpf')


        user = Cliente(nome=nome,email=email, telefone=telefone, cpf=cpf)
        user.save()
        return redirect('/cadastros/cliente/criar_cliente/')


def perfil_usuario(request):
    cliente=User.objects.get(id=id)
    return  render(request, "cadastros/clientes/perfil.html", {'cliente': cliente})

