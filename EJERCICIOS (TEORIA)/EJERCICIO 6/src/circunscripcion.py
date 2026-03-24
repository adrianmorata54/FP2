from partido import Partido
from typing import List, Optional

class Circunscripcion:
    """
    Representa una provincia o ciudad autónoma en las elecciones.
    Almacena datos demográficos, censales y de escrutinio, y gestiona
    la lista de partidos que se presentan en ella.
    """
    def __init__(self, nombre: str, codigo: str, poblacion: int, num_mesas: int, 
                 censo_ine: int, censo_cera: int, censo_total: int, 
                 votantes_ine: int, votantes_cera: int, votantes_totales: int, 
                 votos_validos: int, votos_candidaturas: int, votos_blancos: int, votos_nulos: int):
        
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
        self.votantes_cera = votantes_cera  # Votantes desde el extranjero
        self.votantes_totales = votantes_totales # Participación total
        
        # Escrutinio
        self.votos_validos = votos_validos
        self.votos_candidaturas = votos_candidaturas
        self.votos_blancos = votos_blancos
        self.votos_nulos = votos_nulos
        
        # Relaciones y D'Hondt
        self.partidos: List[Partido] = [] 
        self.ultimo_escano: Optional[Partido] = None
        self.subcampeon: Optional[Partido] = None
        self.votos_faltantes: int = 0

    # ==========================================
    # ✨ MÉTODOS MÁGICOS
    # ==========================================
    
    def __str__(self) -> str:
        """Devuelve una representación legible de la circunscripción."""
        return f"{self.nombre.upper()} ({self.total_escanos} escaños) - {len(self.partidos)} candidaturas"

    # ==========================================
    # 📈 PROPIEDADES DERIVADAS
    # ==========================================
    
    @property
    def total_escanos(self) -> int:
        """Calcula cuántos escaños en total reparte la provincia."""
        return sum(p.escanos_oficiales for p in self.partidos)

    @property
    def porcentaje_nulos_blancos(self) -> float:
        """Devuelve el % de votos nulos y blancos sobre los válidos."""
        if self.votos_validos > 0:
            return ((self.votos_nulos + self.votos_blancos) / self.votos_validos) * 100
        return 0.0
        
    @property
    def participacion_cera_porcentaje(self) -> float:
        """Calcula el porcentaje de participación del censo CERA (Pregunta 3)."""
        if self.censo_cera > 0:
            return (self.votantes_cera / self.censo_cera) * 100
        return 0.0

    # ==========================================
    # ⚙️ MÉTODOS DE LÓGICA DE NEGOCIO
    # ==========================================
    
    def agregar_partido(self, partido: Partido) -> None:
        """Añade un partido a la circunscripción si tuvo votos o escaños."""
        if partido.votos > 0 or partido.escanos_oficiales > 0:
            self.partidos.append(partido)
            
    def chequear_sumas(self) -> bool:
        """Comprueba que la suma de votos de los partidos cuadra con los votos a candidaturas."""
        suma_votos_partidos = sum(p.votos for p in self.partidos)
        return suma_votos_partidos == self.votos_candidaturas

    def aplicar_ley_dhondt(self) -> None:
        """
        Aplica el algoritmo D'Hondt con barrera electoral del 3%.
        Calcula también el ganador del último escaño y el subcampeón.
        """
        total_escanos = self.total_escanos
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
            
            # Análisis del último escaño (solo se ejecuta en la iteración final)
            if i == total_escanos - 1:
                self.ultimo_escano = partido_ganador
                cociente_ganador = cocientes[partido_ganador]
                
                # Bajamos el cociente del ganador para ver quién se quedó a las puertas
                cocientes[partido_ganador] = partido_ganador.votos / (partido_ganador.escanos_calculados + 1)
                partido_subcampeon = max(cocientes, key=cocientes.get)
                self.subcampeon = partido_subcampeon
                
                # Fórmula de votos faltantes
                votos_necesarios = cociente_ganador * (partido_subcampeon.escanos_calculados + 1)
                self.votos_faltantes = int(votos_necesarios - partido_subcampeon.votos) + 1
                
                # Salimos para no actualizar el cociente dos veces
                continue 

            # Actualizamos el cociente para las rondas intermedias
            cocientes[partido_ganador] = partido_ganador.votos / (partido_ganador.escanos_calculados + 1)