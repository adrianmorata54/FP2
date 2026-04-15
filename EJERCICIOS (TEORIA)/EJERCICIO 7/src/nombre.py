from typing import Dict, Tuple

class Nombre:
    def __init__(self, nombre: str, genero: str):
        self.nombre = nombre
        self.genero = genero 
        self.datos_por_decada: Dict[int, Tuple[int, float]] = {}

    @property
    def frecuencia_acumulada(self) -> int:
        """Propiedad derivada que suma la frecuencia absoluta de todas sus décadas."""
        return sum(frecuencia for frecuencia, _ in self.datos_por_decada.values())

    @property
    def es_compuesto(self) -> bool:
        """Determina si un nombre es compuesto si contiene espacios."""
        return " " in self.nombre.strip()

    def __str__(self):
        return f"{self.nombre} ({self.genero}) - Total: {self.frecuencia_acumulada}"