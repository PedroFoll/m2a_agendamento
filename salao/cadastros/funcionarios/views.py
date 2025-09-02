from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Profissional


def criar_funcionario(request):
    if request.method=='GET':
        return render(request, 'cadastro/funcionarios/cadastrar_funcionario.html')
    else:
        return HttpResponse("Aqui tem nada não man")