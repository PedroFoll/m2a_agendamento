from django.urls import path, include
from . import views


app_name ='cadastros'
urlpatterns =[
    path(
        'criar_funcionario/',
        views.criar_funcionario,
        name='cr_func'
        ),

    path(
        'listar_funcionarios/',
        views.listar_funcionario,
        name='lst_func'
    ),

    path(
        'editar_funcionarios/<int:id>',
        views.editar_funcionario,
        name='edt_func'
    ),
    
    path(
        'deletar_funcionario/<int:id>',
        views.deletar_funcionario,
        name='del_func'
    )
]