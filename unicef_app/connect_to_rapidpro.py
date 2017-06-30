from temba_client.v2 import TembaClient

def connect_to_client():
    client = TembaClient("https://app.rapidpro.io","1a831bd482fd57b89ed731895e5a80ebf3539225")    
    return client

def obtener_token_brigadistas():
    return "d46f492c-abe0-4b11-a51f-1f173d014405"

def obtener_token_embarazadas():
    return "de7b3080-5f5c-4534-a20f-0a4d5cbd2e82"