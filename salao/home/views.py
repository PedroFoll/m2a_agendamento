from django.shortcuts import render, HttpResponse


def HomePage(request):
    if request.method =='GET':
        return HttpResponse('Pagina Home')
        return render(request,'home.html')