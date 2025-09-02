from django.urls import path, include
from . import views


app_name ='cadastros'
urlpatterns =[
    path('cliente/', views.cadastro_usuario, name='cliente'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('criar_cliente/', views.criar_cliente, name='criar_cliente')
]