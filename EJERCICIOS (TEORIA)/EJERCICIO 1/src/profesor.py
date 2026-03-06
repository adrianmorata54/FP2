from datetime import date
from persona import Persona
from alumno import Alumno

class Profesor(Persona):
    def __init__(self, apellidos: str, nombre: str, dni: str, fechaNac: date, nombreAsignatura: str):
        super().__init__(apellidos, nombre, dni, fechaNac)
        self.nombreAsignatura = nombreAsignatura
        self.alumnos = []

    def agregar_alumno(self, alumno: Alumno):
        """Añade un alumno a la lista del profesor."""
        self.alumnos.append(alumno)

    def set_nota_alumno(self, dni_alumno: str, nueva_nota: float):
        """Busca al alumno y cambia la nota de la asignatura que imparte este profesor."""
        for alumno in self.alumnos:
            if alumno.dni == dni_alumno:
                for i, (asig, _) in enumerate(alumno.asignaturas):
                    if asig.nombre == self.nombreAsignatura:
                        alumno.asignaturas[i] = (asig, nueva_nota)
                        print(f"--> Nota actualizada para {alumno.nombre} en {self.nombreAsignatura}: {nueva_nota}")
                        return
        print(f"No se pudo actualizar la nota. Verifique DNI o asignatura.")

    # ---------------------------------------------------------
    # NUEVAS FUNCIONES
    # ---------------------------------------------------------

    def get_top_n_mejores_alumnos(self, n: int) -> list[Alumno]:
        """
        Devuelve una lista con los 'n' alumnos que tienen mejor nota media.
        """
        # Ordenamos la lista de alumnos basándonos en su nota media (descendente)
        alumnos_ordenados = sorted(self.alumnos, key=lambda a: a.getNotaMedia(), reverse=True)
        
        return alumnos_ordenados[:n]

    def get_diccionario_medias_asignaturas(self) -> dict[str, float]:
        """
        Devuelve un diccionario donde la clave es el nombre de la asignatura
        y el valor es la nota media global de todos los alumnos en esa asignatura.
        """
        datos_asignaturas = {} # Formato: {'Matemáticas': [suma_notas, cantidad_alumnos]}

        # Recorremos todos los alumnos y sus asignaturas
        for alumno in self.alumnos:
            for asig, nota in alumno.asignaturas:
                nombre = asig.nombre
                
                if nombre not in datos_asignaturas:
                    datos_asignaturas[nombre] = [0.0, 0] # [suma, contador]
                
                datos_asignaturas[nombre][0] += nota
                datos_asignaturas[nombre][1] += 1

        resultado = {}
        for nombre, datos in datos_asignaturas.items():
            suma, cantidad = datos
            resultado[nombre] = suma / cantidad if cantidad > 0 else 0.0
            
        return resultado

    def get_edad_media_curso(self, n_curso: int) -> float:
        """
        Calcula la edad media de los alumnos que tienen al menos una asignatura
        del curso 'n_curso'.
        """
        edades = []
        
        for alumno in self.alumnos:
            pertenece_al_curso = False
            for asig, _ in alumno.asignaturas:
                if asig.curso == n_curso:
                    pertenece_al_curso = True
                    break
            
            if pertenece_al_curso:
                edades.append(alumno.getEdad())

        if not edades:
            return 0.0
            
        return sum(edades) / len(edades)

    def subir_punto_aprobados(self):
            """
            Suma un punto a las notas de los alumnos SOLO en la asignatura 
            que imparte este profesor, y solo si la nota original es >= 5.
            La nota final no puede superar el 10.
            """
            print(f"\n--- Subiendo notas a los aprobados en '{self.nombreAsignatura}' ---")
            contador_cambios = 0
            
            for alumno in self.alumnos:
                # Recorremos las asignaturas del alumno
                for i, (asig, nota) in enumerate(alumno.asignaturas):
                    
                    if asig.nombre == self.nombreAsignatura:
                        
                        if nota >= 5.0:
                            nueva_nota = min(10.0, nota + 1.0)
                            
                            if nueva_nota != nota: 
                                alumno.asignaturas[i] = (asig, nueva_nota)
                                contador_cambios += 1
                                print(f"   -> {alumno.nombre}: sube de {nota} a {nueva_nota}")
                        
                        # Rompemos el bucle interno porque ya encontramos la asignatura de este profesor
                        break 
                            
            print(f"Se han bonificado {contador_cambios} alumnos.")