class Asignatura:
    def __init__(self, nombre: str, creditos: int, curso: int, cuatrimestre: int):
        self.nombre = nombre
        self.creditos = creditos
        self.curso = curso if 1 <= curso <= 4 else 1
        self.cuatrimestre = cuatrimestre if 1 <= cuatrimestre <= 2 else 1

    def set_curso(self, nuevo_curso: int):
        if 1 <= nuevo_curso <= 4:
            self.curso = nuevo_curso

    def set_cuatrimestre(self, nuevo_cuatrimestre: int):
        if 1 <= nuevo_cuatrimestre <= 2:
            self.cuatrimestre = nuevo_cuatrimestre

    def __str__(self):
        return f"{self.nombre} ({self.creditos} cr.)"