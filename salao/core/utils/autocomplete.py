from django.http import JsonResponse
from django.views.decorators.http import require_GET
from cadastros.cliente.models import Cliente
from cadastros.funcionarios.models import Profissional
from cadastros.servicos.models import Servico

@require_GET
def autocomplete(request):
    termo = request.GET.get("q", "").strip()
    data = {}

    if termo:
        # Busca em clientes
        clientes = list(
            Cliente.objects.filter(tipo="cliente", nome__icontains=termo)
            .values("id", "nome")[:5]
        )
        # Busca em funcionários
        funcionarios = list(
            Profissional.objects.filter(tipo="funcionario", nome__icontains=termo)
            .values("id", "nome")[:5]
        )
        # Busca em serviços
        servicos = list(
            Servico.objects.filter(nome__icontains=termo)
            .values("id", "nome")[:5]
        )

        data = {
            "clientes": clientes,
            "funcionarios": funcionarios,
            "servicos": servicos,
        }

    return JsonResponse(data)
