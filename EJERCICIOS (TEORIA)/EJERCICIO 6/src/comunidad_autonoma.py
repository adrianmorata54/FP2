from typing import List, TYPE_CHECKING

# Esto evita errores de importación circular, pero permite el tipado
if TYPE_CHECKING:
    from circunscripcion import Circunscripcion

class ComunidadAutonoma:
    """
    Representa una Comunidad Autónoma, que actúa como un contenedor (agregación)
    de múltiples circunscripciones (provincias).
    Calcula sus propios datos demográficos y electorales de forma dinámica.
    """
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.circunscripciones: List['Circunscripcion'] = []

    # ==========================================
    # ✨ MÉTODOS MÁGICOS
    # ==========================================

    def __str__(self) -> str:
        """Devuelve una representación legible de la CCAA para depuración."""
        return f"{self.nombre.upper()} ({len(self.circunscripciones)} provincias)"

    def agregar_circunscripcion(self, circ: 'Circunscripcion') -> None:
        """Añade una provincia a la lista de la comunidad autónoma."""
        self.circunscripciones.append(circ)

    # ==========================================
    # 📈 PROPIEDADES DERIVADAS (AGREGACIÓN DINÁMICA)
    # ==========================================
    
    @property
    def censo_total(self) -> int:
        """Devuelve el censo total sumando sus provincias."""
        return sum(c.censo_total for c in self.circunscripciones)

    @property
    def censo_cera(self) -> int:
        """Devuelve el censo de extranjeros sumando sus provincias."""
        return sum(c.censo_cera for c in self.circunscripciones)
        
    @property
    def votantes_cera(self) -> int:
        """Devuelve los votantes CERA reales de la CCAA sumando sus provincias."""
        return sum(c.votantes_cera for c in self.circunscripciones)

    @property
    def votos_validos(self) -> int:
        """Suma de todos los votos válidos en la comunidad."""
        return sum(c.votos_validos for c in self.circunscripciones)

    @property
    def votos_nulos_y_blancos(self) -> int:
        """Suma de votos nulos y en blanco en la comunidad."""
        return sum(c.votos_nulos + c.votos_blancos for c in self.circunscripciones)

    # --- NUEVAS PROPIEDADES AVANZADAS (CÁLCULOS AL VUELO) ---

    @property
    def porcentaje_nulos_blancos(self) -> float:
        """Calcula el % de votos nulos y blancos sobre los válidos a nivel autonómico (Pregunta 2)."""
        total_validos = self.votos_validos
        if total_validos > 0:
            return (self.votos_nulos_y_blancos / total_validos) * 100
        return 0.0

    @property
    def participacion_cera_porcentaje(self) -> float:
        """Calcula el % de participación de residentes en el extranjero a nivel autonómico (Pregunta 3)."""
        total_censo_cera = self.censo_cera
        if total_censo_cera > 0:
            return (self.votantes_cera / total_censo_cera) * 100
        return 0.0

    @property
    def proporcion_cera_sobre_censo(self) -> float:
        """Calcula qué porcentaje del censo total representa el censo CERA a nivel autonómico (Pregunta 5)."""
        total_censo = self.censo_total
        if total_censo > 0:
            return (self.censo_cera / total_censo) * 100
        return 0.0