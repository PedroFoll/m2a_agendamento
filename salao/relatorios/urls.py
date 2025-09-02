from django.urls import path, include
from .clientes import views


app_name ='relatorios'
urlpatterns =[
    path('', views.relatorio, name='relatorio'),
    path('ver_cliente/<int:id>',views.ver_cliente, name='ver_cliente'),

    #path('cadastro_gestor_cliente/', views.cadastro_gestor_cliente, name='cadastro_gestor_cliente')
]