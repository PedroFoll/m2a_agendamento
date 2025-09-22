#criar uma side bar

from django.urls import path, include
from . import views


app_name ='core'
urlpatterns =[
    path(
        'home/'
        , views.sidebar, 
        name='home'
        ),
    #path('cadastro_gestor_cliente/', views.cadastro_gestor_cliente, name='cadastro_gestor_cliente')
]