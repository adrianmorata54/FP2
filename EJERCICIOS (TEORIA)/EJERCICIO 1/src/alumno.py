from persona import Persona
from datetime import date

class Alumno(Persona):
    def __init__(self, apellidos: str, nombre: str, dni: str, fechaNac: date, grupo: int):
        super().__init__(apellidos, nombre, dni, fechaNac)
        self.grupo = grupo
        self.asignaturas = [] 

    def set_grupo(self, nuevo_grupo: int):
        self.grupo = nuevo_grupo

    def getNúmeroCreditosSuperados(self) -> int:
        return sum(asig.creditos for asig, nota in self.asignaturas if nota >= 5.0)

    def getNotaMedia(self) -> float:
        if not self.asignaturas:
            return 0.0
        suma_notas = sum(nota for _, nota in self.asignaturas)
        return suma_notas / len(self.asignaturas)
    
    def __str__(self):
        return f"{self.nombre} {self.apellidos} (DNI: {self.dni})"