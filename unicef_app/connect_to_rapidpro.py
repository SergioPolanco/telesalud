import os
from temba_client.v2 import TembaClient

host = os.environ.get('HOST_RAPIDPRO')
token = os.environ.get('TOKEN_RAPIDPRO')
TOKEN_BRIGADISTA = os.environ.get('TOKEN_BRIGADISTA')
TOKEN_EMBARAZADA = os.environ.get('TOKEN_EMBARAZADA')
TOKEN_PUESTOS_DE_SALUD = os.environ.get('TOKEN_PUESTOS_DE_SALUD')

def connect_to_client():
    client = TembaClient(host, token)    
    return client


    
