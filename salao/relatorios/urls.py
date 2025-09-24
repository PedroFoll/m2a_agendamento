from django.urls import path, include
from .clientes import views as cliente_views
from .agendamentos import views as agend_views
from .geral import views as geral_views
from pydf import generate_pdf

app_name ='relatorios'
urlpatterns =[
    path(
        'clientes/', 
        cliente_views.relatorio_clientes, 
        name='relatorio_clientes'
        ),

    path(
        'agendamentos/',
        agend_views.relatorio_agendamentos,
        name='relatorio_agendamentos'
        ),

    path(
        'ver_cliente/<int:id>',
        cliente_views.ver_cliente,
        name='ver_cliente'
        ),

    path(
        'ver_agendamento/<int:id>',
        agend_views.ver_agendamento,
        name='ver_agendamento'
        ),
    
    path(
        'deletar_cliente/<int:id>',
        cliente_views.deletar_cliente,
        name='deletar_cliente'
        ),
    
    path(
        'deletar_agendamento/<int:id>',
        agend_views.deletar_agendamento,
        name='deletar_agendamento'
        ),

    path(
        'editar_agendamento/<int:id>',
        agend_views.editar_agendamento,
        name='editar_agendamento'
        ),

    #path('cadastro_gestor_cliente/', views.cadastro_gestor_cliente, name='cadastro_gestor_cliente')
    
    path(
        'relatorio_geral/',
        geral_views.relatorio_geral,
        name='relatorio_geral'
        ),

    path(
        'imprimir/',
        agend_views.imprimir_relatorio_pdf,
        name='imprimir_relatorio'
        ),

    path('imprimir_layout/', 
         agend_views.imprimir_layout, 
         name='imprimir_layout'
         ),
]