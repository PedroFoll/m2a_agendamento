from django.urls import path
from . import views


app_name='servico' 
urlpatterns =[
    path(
        'cadastrar_servico/',
        views.cadastrar_servico,
        name='cdt_serv'
        ),
    path(
        'criar_servico/',
        views.criar_servico,
        name='criar_serv'
        ),
    path('editar_servico/<int:id>/', views.editar_servico, name='editar_servico'),
    path('deletar_servico/<int:id>/', views.deletar_servico, name='deletar_servico'),

]