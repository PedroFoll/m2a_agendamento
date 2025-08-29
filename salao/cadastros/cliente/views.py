from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def cadastro_usuario(request):
    
    if request.method == "GET":
        return render (request, "cadastros/clientes/cadastrar.html")
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = User.objects.filter(username=username).first()

        if user:
            return HttpResponse('Já existe um usuário com esse username')
        
        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()

        return HttpResponse('Deu bom')


@login_required(login_url='/cadastros/cliente/cliente')
def perfil_usuario(request):
    cliente=User.objects.get(id=id)
    return  render(request, "cadastros/clientes/perfil.html", {'cliente': cliente})
