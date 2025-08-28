from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


# Create your views here.
def login_user(request):
    
    if request.method == "GET":
        return render (request, 'login.html')
    else:
        username=request.POST.get('username')
        senha=request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login(request, user)

            return HttpResponse('Deu bom')
        else: 
            return HttpResponse('Usuario ou senha invalidos')