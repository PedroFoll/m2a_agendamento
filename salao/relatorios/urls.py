from django.urls import path, include
from .clientes import views


app_name ='relatorios'
urlpatterns =[
    path('clientes/', views.relatorio_clientes, name='relatorio_clientes'),
    path('agendamentos/', views.relatorio_agendamentos, name='relatorio_agendamentos'),
    path('ver_cliente/<int:id>',views.ver_cliente, name='ver_cliente'),
    path('ver_agendamento/<int:id>', views.ver_agendamento, name='ver_agendamento'),
    
    path('deletar_cliente/<int:id>',views.deletar_cliente, name='deletar_cliente'),
    path('deletar_agendamento/<int:id>', views.deletar_agendamento, name='deletar_agendamento'),

    #path('cadastro_gestor_cliente/', views.cadastro_gestor_cliente, name='cadastro_gestor_cliente')
]