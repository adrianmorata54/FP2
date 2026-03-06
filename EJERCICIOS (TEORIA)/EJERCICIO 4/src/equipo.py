class Equipo:
    def __init__(self, nombre):
        self.nombre = str(nombre)
        self.jugadores = [] # Lista que contendrá objetos de tipo Jugador

    def agregar_jugador(self, jugador):
        self.jugadores.append(jugador)

    def obtener_jugador(self, nombre_buscado):
        """Busca un jugador por nombre dentro del equipo"""
        for jugador in self.jugadores:
            if nombre_buscado.upper() in jugador.nombre.upper():
                return jugador
        return None
    