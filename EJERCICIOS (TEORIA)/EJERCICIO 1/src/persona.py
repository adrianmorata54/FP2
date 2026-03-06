from datetime import date
class Persona:
    def __init__(self, apellidos: str, nombre: str, dni: str, fechaNac: date):
        self.apellidos = apellidos
        self.nombre = nombre
        self.dni = dni
        self.fechaNac = fechaNac

    def getEdad(self) -> int:
        hoy = date.today()
        return hoy.year - self.fechaNac.year - (
            (hoy.month, hoy.day) < (self.fechaNac.month, self.fechaNac.day)
        )