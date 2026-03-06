class Departamento:
    def __init__(self, nombre, num_etc, tc, tp, experimentalidad):
        self.nombre = nombre
        self.num_etc = float(num_etc)
        self.tc = int(tc)
        self.tp = int(tp)
        self.experimentalidad = float(experimentalidad)
        self.sede = None

    @property
    def total_profesores(self):
        # El enunciado dice: TC + 1/2 * TP
        return self.tc + (0.5 * self.tp)

    @property
    def carga_docente_real(self):
        # Fórmula: (ETC * Exp) / Total
        total = self.total_profesores
        if total == 0:
            return 0.0
        return (self.num_etc * self.experimentalidad) / total

    def __str__(self):
        return (f"{self.nombre} (Exp: {self.experimentalidad}) | "
                f"Carga: {self.carga_docente_real:.4f}")
    
    def __repr__(self):
        return self.__str__()