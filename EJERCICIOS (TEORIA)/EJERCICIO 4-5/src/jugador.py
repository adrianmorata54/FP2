class Jugador:
    def __init__(self, nombre, partidos, pcompletos, ptitular, psuplente, 
                 minutos, lesiones, tarjetas, expulsiones, goles, penalties):
        self.nombre = str(nombre).strip()
        self.partidos = int(partidos)
        self.pcompletos = int(pcompletos)
        self.ptitular = int(ptitular)
        self.psuplente = int(psuplente)
        self.minutos = float(minutos)
        self.lesiones = float(lesiones)
        self.tarjetas = int(tarjetas)
        self.expulsiones = int(expulsiones)
        self.goles = int(goles)
        self.penalties = int(penalties)

    
    @property
    def tarjetas_totales(self):
        """Devuelve la suma de tarjetas amarillas y expulsiones."""
        return self.tarjetas + self.expulsiones

    @property
    def veces_sustituido(self):
        """Calcula cuántas veces fue cambiado (titular pero no completo)."""
        return self.ptitular - self.pcompletos

    @property
    def goles_por_minuto(self):
        """Ratio de goles por minuto. Protegido contra división por cero."""
        if self.minutos > 0:
            return self.goles / self.minutos
        return 0.0

    @property
    def es_revulsivo(self):
        """Devuelve True si ha jugado más partidos de suplente que de titular."""
        return self.psuplente > self.ptitular

    def __str__(self):
        return f"{self.nombre} | PJ: {self.partidos} | Mins: {self.minutos} | Goles: {self.goles}"