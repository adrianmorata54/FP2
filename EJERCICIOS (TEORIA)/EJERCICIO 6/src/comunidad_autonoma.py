class ComunidadAutonoma:
    def __init__(self, nombre):
        self.nombre = nombre
        self.circunscripciones = []

    def agregar_circunscripcion(self, circ):
        self.circunscripciones.append(circ)

    # --- PROPIEDADES DERIVADAS ---
    
    @property
    def censo_total(self):
        """Devuelve el censo total sumando sus provincias."""
        return sum(c.censo_total for c in self.circunscripciones)

    @property
    def censo_cera(self):
        """Devuelve el censo de extranjeros sumando sus provincias."""
        return sum(c.censo_cera for c in self.circunscripciones)
        
    @property
    def votantes_cera(self):
        """Devuelve los votantes CERA reales de la CCAA."""
        return sum(c.votantes_cera for c in self.circunscripciones)

    @property
    def votos_validos(self):
        return sum(c.votos_validos for c in self.circunscripciones)

    @property
    def votos_nulos_y_blancos(self):
        return sum(c.votos_nulos + c.votos_blancos for c in self.circunscripciones)