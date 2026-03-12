class Temporada:
    def __init__(self, identificador):
        """
        Inicializa una temporada.
        :param identificador: Cadena de texto con el formato 'XXXX-YY' (ej. '2017-18')
        """
        self.identificador = str(identificador).strip()
        # Diccionario con clave = nombre del equipo, valor = objeto Equipo
        self.equipos = {} 

    def agregar_equipo(self, equipo):
        """Añade un objeto Equipo al diccionario de la temporada."""
        self.equipos[equipo.nombre] = equipo


    @property
    def num_equipos(self):
        """Devuelve la cantidad de equipos que participan en esta temporada."""
        return len(self.equipos)

    @property
    def num_partidos(self):
        """
        Calcula el número total de partidos de la temporada.
        En una liga de todos contra todos a ida y vuelta, la fórmula es N * (N - 1).
        """
        n = self.num_equipos
        return n * (n - 1)

    @property
    def goles_totales(self):
        """Suma los goles de todos los equipos que conforman la temporada."""
        return sum(equipo.goles_marcados for equipo in self.equipos.values())

    @property
    def media_goles_por_partido(self):
        """Calcula el promedio de goles por partido en la temporada."""
        partidos = self.num_partidos
        if partidos > 0:
            return self.goles_totales / partidos
        return 0.0

    @property
    def año_inicio(self):
        """Extrae el año en el que comienza la temporada (convierte '2017-18' a 2017)."""
        try:
            return int(self.identificador.split('-')[0])
        except (ValueError, AttributeError, IndexError):
            return 0