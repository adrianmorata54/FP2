import openpyxl

from factoria import FactoriaSerieTemporal
from modelos import Regresor_kNN_Correlacion
from registro import Registro

# ==============================================================================
# CONFIGURACIÓN DE RUTAS
# ==============================================================================

RUTA_DATOS_TRAIN = r"PRACTICAS\LABORATORIO 10\datos\serie_temporal_alumnos.xlsx"
RUTA_DATOS_TEST = r"PRACTICAS\LABORATORIO 10\datos\serie_temporal_test.xlsx"

# ==============================================================================
# FUNCIONES AUXILIARES
# ==============================================================================

def calcular_mae(reales: list, predicciones: list) -> float:
    """Calcula el Error Absoluto Medio (MAE)."""
    suma_error = sum(abs(r - p) for r, p in zip(reales, predicciones))
    return suma_error / len(reales)


def obtener_valores_reales_test(ruta_test: str, fh: int) -> list:
    """Extrae los valores reales del Excel de test para poder comparar."""
    wb = openpyxl.load_workbook(ruta_test, data_only=True)
    hoja = wb.active
    valores = []
    
    for fila in hoja.iter_rows(min_row=2, max_row=fh + 1, values_only=True):
        if fila[1] is not None:
            valores.append(float(fila[1]))
            
    return valores


def predecir_iterativo(modelo, ds_train, ph, fh, preprocesador=None):
    """Predice la serie temporal clásica sobre los valores originales (brutos)."""
    ultimos_datos = [reg.objetivo for reg in ds_train.registros[-ph:]]
    predicciones = []

    for _ in range(fh):
        reg_entrada = Registro(ultimos_datos[-ph:])

        if preprocesador:
            reg_entrada = preprocesador.transformar_registro(reg_entrada)

        y_pred = modelo.predecir(reg_entrada)
        
        predicciones.append(y_pred)
        ultimos_datos.append(y_pred)

    return predicciones


def predecir_iterativo_diferencias(modelo, ds_train_diff, ph, fh, ultimo_valor_real, preprocesador=None):
    """
    Predice la serie temporal sobre un modelo entrenado con diferencias, y deshace 
    el cambio sobre la marcha para devolver las predicciones como valores reales.
    """
    ultimos_datos_diff = [reg.objetivo for reg in ds_train_diff.registros[-ph:]]
    predicciones_reales = []
    
    # El ancla actual es el último valor real conocido del Excel de entrenamiento
    valor_actual_real = ultimo_valor_real

    for _ in range(fh):
        reg_entrada = Registro(ultimos_datos_diff[-ph:])

        if preprocesador:
            reg_entrada = preprocesador.transformar_registro(reg_entrada)

        # El modelo predice la DIFERENCIA (el salto)
        y_pred_diff = modelo.predecir(reg_entrada)
        ultimos_datos_diff.append(y_pred_diff)

        # RECONSTRUCCIÓN: Valor anterior + incremento
        valor_actual_real += y_pred_diff
        predicciones_reales.append(valor_actual_real)

    return predicciones_reales

# ==============================================================================
# EJECUCIÓN PRINCIPAL: EJERCICIO 1 (LAB 10)
# ==============================================================================

def ejecutar_ejercicio_1():
    print("\n--- EJERCICIO 1 (LAB 10): TABLA COMPARATIVA AMPLIADA ---")
    print(f"{'Modelo':<18} | {'PH':<4} | {'K':<3} | {'MAE Original':<15} | {'MAE Diferencias':<15}")
    print("-" * 65)
    
    fh = 24
    reales_test = obtener_valores_reales_test(RUTA_DATOS_TEST, fh)

    # Configuraciones de prueba para demostrar robustez
    configuraciones = [(12, 1), (12, 3), (24, 1), (24, 3)]

    for ph, k in configuraciones:
        # ---- 1. ORIGINAL ----
        ds_train_orig = FactoriaSerieTemporal.leer_desde_excel(RUTA_DATOS_TRAIN, ph)
        modelo_orig = Regresor_kNN_Correlacion(k=k)
        modelo_orig.entrenar(ds_train_orig)
        preds_orig = predecir_iterativo(modelo_orig, ds_train_orig, ph, fh)
        mae_orig = calcular_mae(reales_test, preds_orig)
        
        # ---- 2. DIFERENCIAS ----
        ds_train_diff, ultimo_real_train = FactoriaSerieTemporal.leer_desde_excel_diferencias(RUTA_DATOS_TRAIN, ph)
        modelo_diff = Regresor_kNN_Correlacion(k=k)
        modelo_diff.entrenar(ds_train_diff)
        preds_diff = predecir_iterativo_diferencias(modelo_diff, ds_train_diff, ph, fh, ultimo_real_train)
        mae_diff = calcular_mae(reales_test, preds_diff)
        
        # Imprimir fila
        print(f"{'KNN Correlación':<18} | {ph:<4} | {k:<3} | {mae_orig:<15.4f} | {mae_diff:<15.4f}")

    print("-" * 65)

# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__": 
    try:
        ejecutar_ejercicio_1()
    except FileNotFoundError:
        print("Error: No se encuentran los archivos Excel. Verifica las rutas de la configuración.")