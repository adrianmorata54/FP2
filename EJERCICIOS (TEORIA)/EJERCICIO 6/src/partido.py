class Partido:
    def __init__(self, nombre, votos, escanos_oficiales=0):
        self.nombre = nombre
        self.votos = votos
        self.escanos_oficiales = escanos_oficiales
        self.escanos_calculados = 0 # Para cuando apliquemos D'Hondt