from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Cliente

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

@login_required(login_url='/admin/')
def criar_cliente(request):
    if request.method == "GET":
        return render(request, "cadastros/clientes/criar_cliente.html")
    else:
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        cpf = request.POST.get('cpf')


        user = Cliente(nome=nome,email=email, telefone=telefone, cpf=cpf)
        user.save()
        return redirect('/cadastros/cliente/criar_cliente/')


@login_required(login_url='/cadastros/cliente/cliente')
def perfil_usuario(request):
    cliente=User.objects.get(id=id)
    return  render(request, "cadastros/clientes/perfil.html", {'cliente': cliente})

