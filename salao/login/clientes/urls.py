from django.urls import path, include
from . import views


app_name ='login_cliente'
urlpatterns =[
    path('clientes/', views.login_user, name='clientes'),
]