from django.urls import path, include
from . import views


app_name='servico' 
urlpatterns =[
    path('cadastrar_servico/', views.cadastrar_servico, name='cdt_serv'),
]