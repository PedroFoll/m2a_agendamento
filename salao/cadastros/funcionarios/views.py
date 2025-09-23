from django.shortcuts import render, HttpResponse, redirect
from .models import Profissional
from core.utils.helpers import Helpers


def criar_funcionario(request):
    
    if request.method=='GET':
        return render(request, 'cadastro/funcionarios/cadastrar_funcionario.html')
    else:
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        cpf = request.POST.get('cpf')

        user = Profissional(
            nome=nome,
            email=email,
            telefone=telefone,
            cpf=cpf
            )
        
        user.save()

        return redirect('/servicos/agendamento/')
    

def listar_funcionario(request):
    # Inicia a consulta de profissionais
    profissionais = Profissional.objects.all()
    consulta_func = Helpers.get_funcionarios(request)

    # Captura filtros do GET
    nome_filtrar = request.GET.get('nome_filtrar')
    email_filtrar = request.GET.get('email_filtrar')
    cpf_filtrar = request.GET.get('cpf_filtrar')

    # Aplica filtros
    if nome_filtrar:
        profissionais = profissionais.filter(nome__icontains=nome_filtrar)
    if email_filtrar:
        profissionais = profissionais.filter(email__icontains=email_filtrar)
    if cpf_filtrar:
        profissionais = profissionais.filter(cpf__icontains=cpf_filtrar)


    if request.method == "GET":
        contexto = {
            'profissionais': consulta_func['profissionais'],
            'qntd_profissionais': consulta_func['qntd_profissionais'],

            'pagina': consulta_func['pagina'],
            'limit': consulta_func['limit'],
        }

        return render(request, 'cadastro/funcionarios/listar_funcionario.html', contexto)  # Ajuste para o template correto


def editar_funcionario(request, id):
    profissional = Profissional.objects.get(id=id)  # Busca o profissional pelo ID

    # Se for um GET, renderiza o formulário de edição
    if request.method == 'GET':
        return render(request, "cadastro/funcionarios/editar_funcionario.html", {'profissional': profissional})
    else:
        # Se for um POST, atualiza os dados do profissional
        profissional.nome = request.POST.get('nome')
        profissional.email = request.POST.get('email')
        profissional.telefone = request.POST.get('telefone')
        profissional.cpf = request.POST.get('cpf')
        
        profissional.save()  # Salva as alterações

        # Redireciona para a lista de profissionais
        return redirect('/cadastros/funcionarios/listar_funcionarios/')
    
def deletar_funcionario(request, id):
    profissional=Profissional.objects.get(id=id)
    profissional.delete()
    return redirect(
        '/cadastros/funcionarios/listar_funcionarios/'
        )