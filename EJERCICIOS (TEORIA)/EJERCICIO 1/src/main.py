import csv
import os
from datetime import date, datetime

from asignatura import Asignatura
from alumno import Alumno
from profesor import Profesor

# --- Configuración de rutas ---
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_ASIGNATURAS = os.path.join(DIRECTORIO_ACTUAL, "..", "datos", "asignaturas.csv")
RUTA_ALUMNOS     = os.path.join(DIRECTORIO_ACTUAL, "..", "datos", "alumnos.csv")
RUTA_NOTAS       = os.path.join(DIRECTORIO_ACTUAL, "..", "datos", "notas.csv")


def cargar_datos():
    dict_asignaturas = {} 
    dict_alumnos = {}     

    print(f"--- Cargando datos desde: {os.path.abspath(os.path.join(DIRECTORIO_ACTUAL, '..', 'datos'))} ---")

    # 1. Leer Asignaturas
    try:
        with open(RUTA_ASIGNATURAS, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) < 4: continue
                nombre, creditos, curso, cuatrimestre = row
                dict_asignaturas[nombre] = Asignatura(
                    nombre, 
                    int(float(creditos)), 
                    int(float(curso)), 
                    int(float(cuatrimestre))
                )
    except FileNotFoundError:
        print(f"Error: No se encontró {RUTA_ASIGNATURAS}")
        return [], []

    # 2. Leer Alumnos
    try:
        with open(RUTA_ALUMNOS, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) < 5: continue
                apellidos, nombre, dni, fecha_str, grupo = row
                fecha_nac = datetime.strptime(fecha_str, '%Y-%m-%d').date()
                dict_alumnos[dni] = Alumno(apellidos, nombre, dni, fecha_nac, int(float(grupo)))
    except FileNotFoundError:
        print(f"Error: No se encontró {RUTA_ALUMNOS}")
        return [], []

    # 3. Leer Notas
    try:
        with open(RUTA_NOTAS, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) < 3: continue
                dni_alumno, nombre_asig, nota_str = row
                
                alumno = dict_alumnos.get(dni_alumno)
                asignatura = dict_asignaturas.get(nombre_asig)
                
                if alumno and asignatura:
                    alumno.asignaturas.append((asignatura, float(nota_str)))
    except FileNotFoundError:
        print(f"Error: No se encontró {RUTA_NOTAS}")

    return list(dict_alumnos.values()), list(dict_asignaturas.values())


if __name__ == "__main__":
    
    # 1. Cargar datos
    lista_alumnos, _ = cargar_datos()

    if not lista_alumnos:
        print("No se cargaron alumnos.")
    else:
        # 2. Crear Profesor (Asignatura: Programacion) y asignar alumnos
        mi_profesor = Profesor("Turing", "Alan", "99887766X", date(1912, 6, 23), "Programación I")
        
        for alumno in lista_alumnos:
            mi_profesor.agregar_alumno(alumno)

        print("\n" + "="*60)
        print(f" LISTADO DE ALUMNOS DEL PROFESOR: {mi_profesor.nombre} {mi_profesor.apellidos}")
        print("="*60)
        
        for alum in mi_profesor.alumnos:
            nombre_completo = f"{alum.apellidos}, {alum.nombre}"
            media = alum.getNotaMedia()
            creditos = alum.getNúmeroCreditosSuperados()
            
            print(f"Alumno: {nombre_completo}")
            print(f"  > DNI:             {alum.dni}")
            print(f"  > Nota Media:      {media:.2f}")
            print(f"  > Créditos Aprob.: {creditos}")
            print("-" * 30)
        # ---------------------------------------------------------
        # PRUEBAS DE LAS FUNCIONES NUEVAS
        # ---------------------------------------------------------
        print("\n" + "="*50)
        print(" PRUEBAS DE FUNCIONES NUEVAS")
        print("="*50)

        # A) Top N mejores alumnos
        n = 3
        print(f"\n[A] Top {n} mejores alumnos:")
        top = mi_profesor.get_top_n_mejores_alumnos(n)
        for i, alum in enumerate(top, 1):
            print(f"   {i}. {alum.nombre} {alum.apellidos} - Media: {alum.getNotaMedia():.2f}")

        # B) Medias por asignatura
        print("\n[B] Nota media global por asignatura:")
        medias_asig = mi_profesor.get_diccionario_medias_asignaturas()
        for asig, media in medias_asig.items():
            print(f"   - {asig}: {media:.2f}")

        # C) Edad media de un curso
        curso = 1
        print(f"\n[C] Edad media de alumnos del curso {curso}:")
        edad_media = mi_profesor.get_edad_media_curso(curso)
        print(f"   - {edad_media:.2f} años")

        # D) Subir nota a aprobados (PRUEBA DETALLADA)
        print("\n" + "="*50)
        print(f" [D] PRUEBA DE CONTROL: SUBIDA DE NOTAS EN '{mi_profesor.nombreAsignatura}'")
        print("="*50)

        # Tomamos una muestra de los 3 primeros alumnos para ver el antes/después
        muestra_alumnos = mi_profesor.alumnos[:3] 

        print("\n--- [ANTES DE LA SUBIDA] ---")
        for alum in muestra_alumnos:
            print(f"Alumno: {alum.nombre}")
            for asig, nota in alum.asignaturas:
                # Marcamos visualmente si debería subir
                aviso = " <--- (Debe subir)" if asig.nombre == mi_profesor.nombreAsignatura and nota >= 5 else ""
                print(f"   - {asig.nombre}: {nota}{aviso}")
            print("-" * 20)

        # EJECUTAMOS LA FUNCIÓN
        print("\n... Aplicando subida de puntos (Solo en Programacion y si nota >= 5) ...")
        mi_profesor.subir_punto_aprobados()

        print("\n--- [DESPUÉS DE LA SUBIDA] ---")
        for alum in muestra_alumnos:
            print(f"Alumno: {alum.nombre}")
            for asig, nota in alum.asignaturas:
                # Marcamos visualmente si es la asignatura del profe
                if asig.nombre == mi_profesor.nombreAsignatura:
                    print(f"   - {asig.nombre}: {nota} (VERIFICAR CAMBIO)")
                else:
                    print(f"   - {asig.nombre}: {nota}")
            print("-" * 20)