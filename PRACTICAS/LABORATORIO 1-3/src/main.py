# ==============================================================================
# MÓDULO: main.py
# Propósito: Punto de entrada principal (Entry Point) del programa.
# Orquesta todas las clases creadas para ejecutar los Laboratorios 1 y 2.
# ==============================================================================

import os
import random

# Importamos las herramientas que hemos fabricado en nuestros otros archivos
from registro import Registro 
from factoria import FactoriaUniversal
from modelos import Clasificador_kNN

def evaluar_modelo(modelo, dataset, nombre_dataset):
    """
    Función auxiliar (Helper) para calcular el porcentaje de acierto del modelo.
    Aplicamos el principio DRY (Don't Repeat Yourself) para no escribir este 
    bucle for tres veces (una por cada dataset).
    """
    aciertos = 0
    total = len(dataset.registros)
    
    # Recorremos a todos los pacientes/flores/vinos del dataset
    for registro in dataset.registros:
        # Le pedimos al modelo que adivine la etiqueta
        prediccion = modelo.predecir(registro)
        
        # Comparamos su adivinanza con la realidad
        if prediccion == registro.objetivo:
            aciertos += 1
            
    # Calculamos el porcentaje sobre 100
    precision = (aciertos / total) * 100
    print(f"[{nombre_dataset}] k={modelo.k} | Distancia: {modelo.distancia} -> Precisión: {precision:.2f}%")
    return precision


def main():
    print("==================================================")
    print("   PARTE 1: TEST DE LA CLASE BASE (LABORATORIO 1) ")
    print("==================================================\n")
    
    # 1. Creación de 10 registros aleatorios de dimensión 4
    lista_registros = []
    for _ in range(10):
        # random.uniform genera números con decimales entre 0 y 100
        atributos_aleatorios = [random.uniform(0, 100) for _ in range(4)]
        nuevo_registro = Registro(atributos_aleatorios)
        lista_registros.append(nuevo_registro)

    print("--- REGISTROS GENERADOS ---")
    for i, r in enumerate(lista_registros):
        atributos_str = [f"{val:.2f}" for val in r.atributos]
        print(f"Registro {i}: {atributos_str}")

    # 2. Pruebas de las matemáticas geométricas de la clase Registro
    reg_base = lista_registros[0]
    reg_destino = lista_registros[1]

    print("\n--- PRUEBAS DE DISTANCIA ---")
    d_euclidea = reg_base.calcula_distancia(reg_destino, tipo="euclídea")
    print(f"Distancia Euclídea (Reg 0 a Reg 1): {d_euclidea:.2f}")

    d_manhattan = reg_base.calcula_distancia(reg_destino, tipo="manhattan")
    print(f"Distancia Manhattan (Reg 0 a Reg 1): {d_manhattan:.2f}")

    pesos_prueba = [0.4, 0.3, 0.2, 0.1] 
    d_ponderada = reg_base.calcula_distancia(reg_destino, tipo="ponderada", pesos=pesos_prueba)
    print(f"Distancia Ponderada (Reg 0 a Reg 1): {d_ponderada:.2f} con pesos {pesos_prueba}")

    print("\n--- PRUEBA DE NORMALIZACIÓN ---")
    minimos = [0.0, 0.0, 0.0, 0.0]
    maximos = [100.0, 100.0, 100.0, 100.0]
    
    reg_normalizado = reg_base.normalizar(minimos, maximos)
    atributos_norm_str = [f"{val:.4f}" for val in reg_normalizado.atributos]
    print(f"Registro 0 original: {[f'{val:.2f}' for val in reg_base.atributos]}")
    print(f"Registro 0 normalizado: {atributos_norm_str}")

    print("\n--- PRUEBA DE K-VECINOS ---")
    k = 3
    vecinos = reg_base.k_vecinos(lista_registros, k, tipo_distancia="euclídea")
    print(f"Buscando los {k} vecinos más cercanos al Registro 0...")
    print(f"Los índices resultantes son: {vecinos}")
    print("(Nota: El índice 0 NO aparece porque el algoritmo evita compararse consigo mismo).")


    print("\n\n==================================================")
    print("   PARTE 2: TEST DE MODELOS KNN (LABORATORIO 2)   ")
    print("==================================================\n")

    # 1. CARGA DE DATOS CON RUTAS DINÁMICAS (A PRUEBA DE ERRORES)
    try:
        print("Calculando rutas a la carpeta 'datos'...")
        # os.path.abspath(__file__) averigua dónde está guardado este main.py exactamente.
        # Esto permite que el programa funcione igual en Windows, Mac o Linux, sin importar
        # en qué carpeta lo haya descomprimido el profesor.
        directorio_src = os.path.dirname(os.path.abspath(__file__))
        
        # Subimos una carpeta ("..") y entramos en "datos"
        directorio_datos = os.path.join(directorio_src, "..", "datos")
        
        # Construimos las rutas finales uniendo el directorio con el nombre del archivo
        ruta_iris = os.path.join(directorio_datos, "iris.xlsx") 
        ruta_diabetes = os.path.join(directorio_datos, "diabetes.csv")
        ruta_wine = os.path.join(directorio_datos, "wine.data")

        print("Cargando datasets reales con la Factoría Universal...")
        # Delegamos toda la complejidad de lectura a la Factoría
        ds_iris = FactoriaUniversal.crear_dataset_clasificacion(ruta_iris, indice_objetivo=-1)
        ds_diabetes = FactoriaUniversal.crear_dataset_clasificacion(ruta_diabetes, indice_objetivo=-1)
        ds_wine = FactoriaUniversal.crear_dataset_clasificacion(ruta_wine, indice_objetivo=0)
        print("¡Datasets cargados con éxito!\n")
        
    except Exception as e:
        print(f"Error cargando los archivos: {e}")
        return

    # 2. PRUEBAS CON IRIS (Búsqueda de Hiperparámetros básica)
    print("--- 🌸 DATASET IRIS ---")
    # Los bucles anidados nos permiten probar múltiples combinaciones de k y distancias rápidamente.
    for k_val in [1, 3, 5]:
        for dist in ["euclídea", "manhattan"]:
            modelo = Clasificador_kNN(k=k_val, distancia=dist)
            modelo.entrenar(ds_iris)
            evaluar_modelo(modelo, ds_iris, "IRIS")

    # 3. PRUEBAS CON DIABETES
    print("\n--- 🩸 DATASET DIABETES ---")
    # En problemas médicos, suelen usarse k más grandes para evitar el ruido de casos aislados
    for k_val in [3, 7, 11]: 
        modelo = Clasificador_kNN(k=k_val, distancia="euclídea")
        modelo.entrenar(ds_diabetes)
        evaluar_modelo(modelo, ds_diabetes, "DIABETES")

    # 4. PRUEBAS CON WINE (Demostración de Distancia Ponderada)
    print("\n--- 🍷 DATASET WINE ---")
    # Inicializamos todos los pesos a 1.0 (peso normal)
    pesos_wine = [1.0] * 13 
    # El profesor nos pidió dar más importancia a características clave:
    pesos_wine[0] = 5.0  # Multiplicamos x5 la importancia del Alcohol
    pesos_wine[9] = 3.0  # Multiplicamos x3 la importancia de la Intensidad de color

    # Comparamos el modelo normal vs el modelo con "enchufes" (pesos)
    mod_wine_eu = Clasificador_kNN(k=5, distancia="euclídea")
    mod_wine_eu.entrenar(ds_wine)
    evaluar_modelo(mod_wine_eu, ds_wine, "WINE")

    mod_wine_pond = Clasificador_kNN(k=5, distancia="ponderada", pesos=pesos_wine)
    mod_wine_pond.entrenar(ds_wine)
    evaluar_modelo(mod_wine_pond, ds_wine, "WINE")
    
    print("\n==============================================")
    print("Fin de la ejecución. Fíjate en los resultados de k=1 (Overfitting).")



# ==============================================================================
# BLOQUE DE EJECUCIÓN
# ==============================================================================
# Esta línea mágica le dice a Python: "Solo ejecuta la función main() si el 
# usuario le ha dado a ejecutar directamente a este archivo".
# Si otro programa importa este archivo, el main() no se ejecutará por accidente.
if __name__ == "__main__":
    main()