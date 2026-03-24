from partido import Partido

class Circunscripcion:
    def __init__(self, nombre, codigo, poblacion, num_mesas, 
                 censo_ine, censo_cera, censo_total, 
                 votantes_ine, votantes_cera, votantes_totales, 
                 votos_validos, votos_candidaturas, votos_blancos, votos_nulos):
        
        # Identificación
        self.nombre = nombre
        self.codigo = codigo
        
        # Demografía y Mesas
        self.poblacion = poblacion
        self.num_mesas = num_mesas
        
        # Censo
        self.censo_ine = censo_ine          # Residentes en España
        self.censo_cera = censo_cera        # Residentes en el extranjero
        self.censo_total = censo_total      # Censo Total
        
        # Participación
        self.votantes_ine = votantes_ine    # Votantes desde España
        self.votantes_cera = votantes_cera  # Votantes desde el extranjero (P3)
        self.votantes_totales = votantes_totales # Participación total
        
        # Escrutinio
        self.votos_validos = votos_validos
        self.votos_candidaturas = votos_candidaturas
        self.votos_blancos = votos_blancos
        self.votos_nulos = votos_nulos
        
        # Relaciones y D'Hondt
        self.partidos = [] 
        self.ultimo_escano = None
        self.subcampeon = None
        self.votos_faltantes = 0

    @property
    def total_escanos(self):
        """Calcula cuántos escaños en total reparte la provincia."""
        return sum(p.escanos_oficiales for p in self.partidos)

    @property
    def porcentaje_nulos_blancos(self):
        """Devuelve el % de votos nulos y blancos sobre los válidos."""
        if self.votos_validos > 0:
            return ((self.votos_nulos + self.votos_blancos) / self.votos_validos) * 100
        return 0
       
    def agregar_partido(self, partido: Partido):
        if partido.votos > 0 or partido.escanos_oficiales > 0:
            self.partidos.append(partido)
            
    def chequear_sumas(self):
        """Comprueba que la suma de votos de los partidos cuadra con los votos a candidaturas."""
        suma_votos_partidos = sum(p.votos for p in self.partidos)
        return suma_votos_partidos == self.votos_candidaturas

    def aplicar_ley_dhondt(self):
        total_escanos = sum(p.escanos_oficiales for p in self.partidos)
        self.ultimo_escano = None
        self.subcampeon = None
        self.votos_faltantes = 0
        
        if total_escanos == 0:
            return

        for p in self.partidos:
            p.escanos_calculados = 0
            
        barrera = self.votos_validos * 0.03
        cocientes = {p: p.votos for p in self.partidos if p.votos >= barrera}
        
        for i in range(total_escanos):
            if not cocientes:
                break
            partido_ganador = max(cocientes, key=cocientes.get)
            partido_ganador.escanos_calculados += 1
            
            if i == total_escanos - 1:
                self.ultimo_escano = partido_ganador
                cociente_ganador = cocientes[partido_ganador]
                
                cocientes[partido_ganador] = partido_ganador.votos / (partido_ganador.escanos_calculados + 1)
                partido_subcampeon = max(cocientes, key=cocientes.get)
                self.subcampeon = partido_subcampeon
                
                votos_necesarios = cociente_ganador * (partido_subcampeon.escanos_calculados + 1)
                self.votos_faltantes = int(votos_necesarios - partido_subcampeon.votos) + 1

            cocientes[partido_ganador] = partido_ganador.votos / (partido_ganador.escanos_calculados + 1)