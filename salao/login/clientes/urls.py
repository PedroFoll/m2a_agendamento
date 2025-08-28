from django.urls import path, include
from . import views


app_name ='login'
urlpatterns =[
    path('clientes/', views.cadastro_usuario, name='clientes'),
]