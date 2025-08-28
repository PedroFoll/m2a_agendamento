from django.urls import path, include

urlpatterns =[
   path('cliente/', include('cadastros.cliente.urls'),),
]