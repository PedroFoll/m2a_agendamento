from random import randint
from faker import Faker
import random
from os import sys

class Helpers():

    def gerador_data_hora():
    
        dia=random.randint(1,28)
        mes=random.randint(1,12)
        ano=random.randint(1970,2025)
        data=dia+"/"+mes+"/"+ano
        return data

    def gerador_telefone():
    
        prefixo = (str(85))
        inicio = (str(99999))
        final = str((randint(1000,9999)))
        numeroCelularAleatorio = (prefixo+inicio+final)
        
        return numeroCelularAleatorio
        
    def gerador_email(domain="randommail.com"):

            fake=Faker()
            nome = fake.first_name().lower()
            sobrenome=fake.last_name().lower()
            randomMail=()

            return f'{nome}.{sobrenome}@{domain}'