from django.shortcuts import render, HttpResponse, redirect

from cadastros.servicos.models import Servico

def cadastrar_servico(request):
    pagina = int(request.GET.get('pagina', 1))
    limit = 10  # define o limite por página

    servicos = Servico.objects.all()
    qtd_serv = servicos.count()

    offset = (pagina - 1) * limit
    servicos = servicos.order_by('nome')[offset:offset + limit]

    context = {
        'servicos': servicos,
        'qtd_serv': qtd_serv,
        'limit': limit,
        'pagina': pagina,
    }

    if request.method == 'GET':
        return render(request, 'cadastros/servicos/cadastro_Servico.html', context)
    else:
        nome_servico = request.POST.get('nome_servico')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        duracao = request.POST.get('duracao')

        serv = Servico(
            nome=nome_servico,
            descricao=descricao,
            preco=preco,
        )
        serv.save()


def criar_servico(request):
    if request.method == 'GET':
        return render(request, 'cadastros/servicos/criar_servico.html')
    else:
        nome_servico = request.POST.get('nome_servico')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')

        serv = Servico(
            nome=nome_servico,
            descricao=descricao,
            preco=preco,
        )
        serv.save()
        return redirect('/cadastros/servicos/cadastrar_servico/')