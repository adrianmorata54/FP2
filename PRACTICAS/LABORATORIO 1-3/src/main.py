# ==============================================================================
# MÓDULO: main.py
# Propósito: Punto de entrada principal (Entry Point) del programa.
# Orquesta todas las clases creadas para ejecutar los Laboratorios 1, 2 y 3.
# ==============================================================================

import os
import random

# Importamos las herramientas de Laboratorios 1 y 2
from registro import Registro 
from factoria import FactoriaUniversal
from modelos import Clasificador_kNN

# IMPORTACIONES (LABORATORIO 3 - OBLIGATORIO)
from preprocesado import NormalizadorMaxMin, NormalizadorZ_Score
from validacion import ValidacionClasificacion, ValidacionRegresion
from modelos import Clasificador_centroide, Regresor_kNN, Regresor_lineal_multiple

# IMPORTACIONES (LABORATORIO 3 - VOLUNTARIO)
from validacion import SeleccionAtributos
from preprocesado import FiltroVarianza

def evaluar_modelo(modelo, dataset, nombre_dataset):
    """(Función antigua del Lab 2)"""
    aciertos = 0
    total = len(dataset.registros)
    for registro in dataset.registros:
        prediccion = modelo.predecir(registro)
        if prediccion == registro.objetivo:
            aciertos += 1
    precision = (aciertos / total) * 100
    print(f"[{nombre_dataset}] k={modelo.k} | Distancia: {modelo.distancia} -> Precisión: {precision:.2f}%")
    return precision


def main():
    """
    Función principal que orquesta el pipeline completo de Machine Learning.
    Ejecuta secuencialmente las pruebas de los Laboratorios 1, 2 y 3, 
    incluyendo preprocesado, validación y métricas avanzadas.
    """
    print("==================================================")
    print("==================================================")
    print("   PARTE 1: TEST DE LA CLASE BASE (LABORATORIO 1) ")
    print("==================================================\n")
    
    lista_registros = []
    for _ in range(10):
        atributos_aleatorios = [random.uniform(0, 100) for _ in range(4)]
        nuevo_registro = Registro(atributos_aleatorios)
        lista_registros.append(nuevo_registro)

    print("--- REGISTROS GENERADOS ---")
    for i, r in enumerate(lista_registros):
        atributos_str = [f"{val:.2f}" for val in r.atributos]
        print(f"Registro {i}: {atributos_str}")

    reg_base = lista_registros[0]
    reg_destino = lista_registros[1]

    print("\n--- PRUEBAS DE DISTANCIA ---")
    print(f"Distancia Euclídea: {reg_base.calcula_distancia(reg_destino, tipo='euclídea'):.2f}")
    print(f"Distancia Manhattan: {reg_base.calcula_distancia(reg_destino, tipo='manhattan'):.2f}")

    print("\n--- PRUEBA DE NORMALIZACIÓN ---")
    minimos = [0.0, 0.0, 0.0, 0.0]
    maximos = [100.0, 100.0, 100.0, 100.0]
    reg_normalizado = reg_base.normalizar(minimos, maximos)
    print(f"Registro 0 normalizado: {[f'{val:.4f}' for val in reg_normalizado.atributos]}")

    print("\n--- PRUEBA DE K-VECINOS ---")
    k = 3
    vecinos = reg_base.k_vecinos(lista_registros, k, tipo_distancia="euclídea")
    print(f"Los {k} vecinos más cercanos al Registro 0 son los índices: {vecinos}")


    print("\n\n==================================================")
    print("   PARTE 2: TEST DE MODELOS KNN (LABORATORIO 2)   ")
    print("==================================================\n")

    try:
        print("Calculando rutas a la carpeta 'datos'...")
        directorio_src = os.path.dirname(os.path.abspath(__file__))
        directorio_datos = os.path.join(directorio_src, "..", "datos")
        
        ruta_iris = os.path.join(directorio_datos, "iris.xlsx") 
        ruta_diabetes = os.path.join(directorio_datos, "diabetes.csv")
        ruta_wine = os.path.join(directorio_datos, "wine.data")
        ruta_boston = os.path.join(directorio_datos, "BostonHousing.csv")

        print("Cargando datasets reales con la Factoría Universal...")
        ds_iris = FactoriaUniversal.crear_dataset_clasificacion(ruta_iris, indice_objetivo=-1)
        ds_diabetes = FactoriaUniversal.crear_dataset_clasificacion(ruta_diabetes, indice_objetivo=-1)
        ds_wine = FactoriaUniversal.crear_dataset_clasificacion(ruta_wine, indice_objetivo=0)
        ds_boston = FactoriaUniversal.crear_dataset_regresion(ruta_boston, indice_objetivo=12)
        print("¡Datasets cargados con éxito!\n")
        
    except Exception as e:
        print(f"Error cargando los archivos: {e}")
        return

    print("--- 🌸 DATASET IRIS ---")
    for k_val in [3, 5]:
        modelo = Clasificador_kNN(k=k_val, distancia="euclídea")
        modelo.entrenar(ds_iris)
        evaluar_modelo(modelo, ds_iris, "IRIS")

    print("\n--- 🍷 DATASET WINE (Distancia Ponderada) ---")
    pesos_wine = [1.0] * 13 
    pesos_wine[0] = 5.0  
    pesos_wine[9] = 3.0  
    mod_wine_pond = Clasificador_kNN(k=5, distancia="ponderada", pesos=pesos_wine)
    mod_wine_pond.entrenar(ds_wine)
    evaluar_modelo(mod_wine_pond, ds_wine, "WINE")


    print("\n\n==================================================")
    print("   PARTE 3: PREPROCESADO Y VALIDACIÓN (LABORATORIO 3) ")
    print("==================================================\n")

    val_clasificacion = ValidacionClasificacion()
    val_regresion = ValidacionRegresion()
    norm_maxmin = NormalizadorMaxMin()
    norm_zscore = NormalizadorZ_Score()

    print("--- 🌸 IRIS: CLASIFICADOR CENTROIDE + Z-SCORE ---")
    modelo_centroide = Clasificador_centroide(distancia="euclídea")
    nota_centroide = val_clasificacion.validacion_cruzada(
        modelo=modelo_centroide, dataset=ds_iris, m_bolsas=5, normalizador=norm_zscore
    )
    # Ahora 'nota_centroide' es un diccionario con Accuracy y Error Rate
    print(f"[CENTROIDE] Cross-Validation (5 bolsas) -> Resultados: {nota_centroide}")

    print("\n--- 🩸 DIABETES: KNN + HOLD-OUT + MAX-MIN ---")
    modelo_knn_diab = Clasificador_kNN(k=7, distancia="euclídea")
    nota_diab = val_clasificacion.validacion_simple(
        modelo=modelo_knn_diab, dataset=ds_diabetes, porcentaje_test=0.25, normalizador=norm_maxmin
    )
    print(f"[KNN k=7] Hold-Out (25% test) -> Resultados: {nota_diab}")


    print("\n--- 🏠 BOSTON HOUSING: PREDECIR PRECIOS (REGRESIÓN) ---")
    modelo_knn_boston = Regresor_kNN(k=5, distancia="euclídea")
    nota_knn_boston = val_regresion.validacion_cruzada(
        modelo=modelo_knn_boston, dataset=ds_boston, m_bolsas=5, normalizador=norm_zscore 
    )
    print(f"[Regresor KNN k=5] Cross-Validation -> Resultados: {nota_knn_boston}")

    modelo_lineal = Regresor_lineal_multiple(tasa_aprendizaje=0.000001, epocas=50)
    nota_lineal = val_regresion.validacion_simple(
        modelo=modelo_lineal, dataset=ds_boston, porcentaje_test=0.2, normalizador=None 
    )
    print(f"[Regresor Lineal] Hold-Out (20% test) -> Resultados: {nota_lineal}")


    print("\n\n==================================================")
    print("   PARTE 4: ETAPAS VOLUNTARIAS (9, 10, 11 y 12)   ")
    print("==================================================\n")

    # ETAPA 12: Filtro de Varianza en Iris
    print("--- 🧹 FILTRO DE VARIANZA (Limpieza de ruido) ---")
    filtro_var = FiltroVarianza(umbral=0.15) # Eliminamos columnas que varíen menos de 0.15
    filtro_var.ajustar(ds_iris)
    print(f"Índices detectados con varianza casi nula: {filtro_var.indices_a_eliminar}")
    ds_iris_limpio = filtro_var.transformar_dataSet(ds_iris)
    print(f"Iris original tenía {len(ds_iris.registros[0].atributos)} columnas. El limpio tiene {len(ds_iris_limpio.registros[0].atributos)}.")


    # ETAPA 11: Selección por Correlación de Pearson en Boston Housing
    print("\n--- 🎯 SELECCIÓN POR CORRELACIÓN DE PEARSON ---")
    # Buscamos el top 50% (p=0.5) de las columnas que más afectan al precio de la casa
    mejores_indices_boston = SeleccionAtributos.seleccion_correlacion(dataset=ds_boston, p=0.5)
    print(f"Los índices de las columnas que más determinan el precio son: {mejores_indices_boston}")
    
    # ETAPA 10: Eliminamos los atributos malos
    num_columnas_boston = len(ds_boston.registros[0].atributos)
    indices_a_borrar = [i for i in range(num_columnas_boston) if i not in mejores_indices_boston]
    ds_boston_optimizado = ds_boston.eliminar_atributos(indices_a_borrar)
    
    print(f"Boston original tenía {num_columnas_boston} columnas. Optimizado tiene {len(ds_boston_optimizado.registros[0].atributos)}.")
    
    # Probamos si al quitar columnas basura el modelo mejora (MAE baja)
    nota_boston_opt = val_regresion.validacion_simple(
        modelo=modelo_knn_boston, dataset=ds_boston_optimizado, porcentaje_test=0.2, normalizador=norm_zscore 
    )
    print(f"[KNN en Boston Optimizado] Resultados: {nota_boston_opt}")

    print("\n==============================================")
    print("¡Laboratorios 1, 2 y 3 ejecutados al 100% (incluyendo extras)!")

# ==============================================================================
# BLOQUE DE EJECUCIÓN
# ==============================================================================
if __name__ == "__main__":
    main()