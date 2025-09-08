from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User


# Create your views here.
def configuracao(request):
    if request.method == "GET":
        return render (request, 'config.html')
    
    