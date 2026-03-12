class Equipo:
    def __init__(self, nombre, temporada):
        self.nombre = str(nombre)
        self.temporada = str(temporada)  # Añadimos el atributo temporada según el Boletín 5
        self.jugadores = [] # Lista que contendrá objetos de tipo Jugador

    def agregar_jugador(self, jugador):
        self.jugadores.append(jugador)

    def obtener_jugador(self, nombre_buscado):
        """Busca un jugador por nombre dentro del equipo"""
        for jugador in self.jugadores:
            if nombre_buscado.upper() in jugador.nombre.upper():
                return jugador
        return None


    @property
    def goles_marcados(self):
        """Suma de todos los goles anotados por los jugadores de la plantilla."""
        return sum(jugador.goles for jugador in self.jugadores)

    @property
    def num_jugadores(self):
        """Devuelve la cantidad de jugadores que conforman la plantilla."""
        return len(self.jugadores)

    @property
    def partidos_jugados(self):
        """
        Calcula los partidos jugados por el equipo en esa temporada. 
        Lo obtenemos buscando el máximo de partidos disputados por algún jugador de la plantilla.
        """
        if not self.jugadores:
            return 0
        return max(jugador.partidos for jugador in self.jugadores)

    @property
    def total_tarjetas(self):
        """Suma total de todas las tarjetas (amarillas + rojas) recibidas por el equipo."""
        return sum(jugador.tarjetas_totales for jugador in self.jugadores)