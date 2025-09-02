from django.shortcuts import render, HttpResponse

def cadastrar_servico(request):
    if request.method=='GET':
        return render(request, 'cadastros/servicos/cadastro_Servico.html')
    else:
        return HttpResponse("Aqui tem nada não man")
    
    