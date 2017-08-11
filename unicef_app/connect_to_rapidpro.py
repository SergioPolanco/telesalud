from temba_client.v2 import TembaClient

def connect_to_client():
    client = TembaClient("https://app.rapidpro.io","1a831bd482fd57b89ed731895e5a80ebf3539225")    
    return client

def obtener_token_brigadistas():
    return "d46f492c-abe0-4b11-a51f-1f173d014405"

def obtener_token_embarazadas():
    return "de7b3080-5f5c-4534-a20f-0a4d5cbd2e82"
    
class Node(object):
    def __init__(self, name, parent=None, telefono=None):
        self.name = name
        self.parent = parent
        self.telefono = telefono
        
    def get_parents(self):
        parents = [self.name]
        if self.parent:
            parent = self.parent
            
            while parent:
                parents.append(parent.name)
                parent = parent.parent
        parents.reverse()
        
        return parents


RACCS = Node("RACCS")

CENTRO_DE_SALUD_1 = Node("CENTRO_DE_SALUD_1", parent=RACCS)

CENTRO_DE_SALUD_KUKRA_HILL = Node("CENTRO_DE_SALUD_KUKRA_HILL", parent=RACCS)

MUNICIPIO_GISI_HOULOVER = Node("MUNICIPIO_GISI_HOULOVER", parent=CENTRO_DE_SALUD_1)

MUNICIPIO_GISI_PEDREGAL = Node("MUNICIPIO_GISI_PEDREGAL", parent=CENTRO_DE_SALUD_1)

MUNICIPIO_GISI_ORINOCO = Node("MUNICIPIO_GISI_ORINOCO", parent=CENTRO_DE_SALUD_1)

MUNICIPIO_GISI_TASBAPAUNI = Node("MUNICIPIO_GISI_TASBAPAUNI", parent=CENTRO_DE_SALUD_1)

COMUNIDADES = {
    "manhatam": Node("Manhatam", parent=MUNICIPIO_GISI_HOULOVER, telefono="51616565")
}