from django.urls import path, include
from . import views


app_name ='cadastros'
urlpatterns =[
    path(
        'criar_funcionario/',
        views.criar_funcionario,
        name='cr_func'
        ),
]