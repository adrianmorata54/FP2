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

    def __str__(self):
        return f"{self.nombre} | PJ: {self.partidos} | Mins: {self.minutos} | Goles: {self.goles}"