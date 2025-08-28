from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User


# Create your views here.
def sidebar(request):
    if request.method == "GET":
        return render (request, 'sidebar.html')
    
    