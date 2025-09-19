from django.urls import path
from . import views


app_name ='cadastros'
urlpatterns =[
    path('cliente/', views.cadastro_usuario, name='cliente'),
    path('criar_cliente/', views.criar_cliente, name='criar_cliente')
]