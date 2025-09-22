from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User


def sidebar(request):
    if request.method == "GET":
        return render (request, 'sidebar.html')
    
    