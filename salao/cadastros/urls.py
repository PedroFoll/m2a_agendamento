from django.urls import path, include

urlpatterns =[
   path(
       'cliente/', 
       include('cadastros.cliente.urls'),
        ),

   path(
       'funcionarios/', 
        include('cadastros.funcionarios.urls'),
        ),
        
   path(
       'servicos/', 
       include('cadastros.servicos.urls'),
       ),
]