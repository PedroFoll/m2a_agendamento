from django.urls import path, include
from . import views


app_name ='cadastros'
urlpatterns =[
    path('cliente/', views.cadastro_usuario, name='cliente'),
    #path('cadastro_gestor_cliente/', views.cadastro_gestor_cliente, name='cadastro_gestor_cliente')
]