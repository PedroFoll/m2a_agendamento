from django.urls import path
from . import views



urlpatterns = [
    path("sistema/", views.configuracao, name="configuracao")
]