class Partido:
    """
    Representa a un partido político dentro de una circunscripción específica.
    Almacena sus resultados oficiales y permite compararlos con los calculados.
    """
    
    def __init__(self, nombre: str, votos: int, escanos_oficiales: int = 0):
        self.nombre = nombre
        self.votos = votos
        
        # Escaños oficiales (leídos del Excel)
        self.escanos_oficiales = escanos_oficiales
        
        # Escaños calculados (generados por nuestro algoritmo D'Hondt)
        self.escanos_calculados = 0 

    # ==========================================
    # ✨ MÉTODOS MÁGICOS (DUNDER METHODS)
    # ==========================================

    def __str__(self) -> str:
        """
        Define cómo se imprime el objeto cuando usamos print(partido).
        Ejemplo: "PARTIDO POPULAR (150000 votos, 3 escaños)"
        """
        return f"{self.nombre} ({self.votos} votos, {self.escanos_calculados} escaños)"

    def __eq__(self, otro_partido: object) -> bool:
        """
        Define cómo se comparan dos partidos para saber si son el mismo (operador ==).
        Dos objetos Partido son iguales si tienen el mismo nombre.
        """
        if isinstance(otro_partido, Partido):
            return self.nombre == otro_partido.nombre
        return False

    def __lt__(self, otro_partido: object) -> bool:
        """
        Define cómo se ordenan los partidos (operador <).
        Prioridad 1: Más escaños calculados.
        Prioridad 2: En caso de empate a escaños, más votos.
        (Esto permite usar lista_partidos.sort(reverse=True) directamente sin lambdas).
        """
        if not isinstance(otro_partido, Partido):
            return NotImplemented
            
        if self.escanos_calculados == otro_partido.escanos_calculados:
            return self.votos < otro_partido.votos
            
        return self.escanos_calculados < otro_partido.escanos_calculados
    
    def __hash__(self) -> int:
        """Permite que el objeto Partido se use como clave en un diccionario."""
        return hash(self.nombre)
