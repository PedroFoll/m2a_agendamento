from django.urls import path, include
from .agendamento import views


app_name='servico'
urlpatterns =[
    path(
        'agendamento/',
        views.agendar_servico,
        name='agendar_servico'
        ),
    
    path(
        'alterar_status/<int:agendamento_id>/<str:status>/', 
        views.alterar_status, 
        name='alterar_status'
        ),

    #path('calendario/', views.calendario_agendamentos, name='calendario_agendamentos')
]