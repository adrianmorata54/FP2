import random
import openpyxl

from factoria import FactoriaSerieTemporal

from modelos import (
    Regresor_lineal_multiple,
    Regresor_kNN_Correlacion,
    Regresor_kNN_Ponderado,
    FuncionObjetivoKNN
)

from registro import Registro

from preprocesado import (
    NormalizadorMaxMin,
    NormalizadorZ_Score
)

# ==============================================================================
# CONFIGURACIÓN DE RUTAS
# ==============================================================================

RUTA_DATOS_TRAIN = r"PRACTICAS\LABORATORIO 9\datos\serie_temporal_alumnos.xlsx"
RUTA_DATOS_TEST = r"PRACTICAS\LABORATORIO 9\datos\serie_temporal_test.xlsx"

# ==============================================================================

def calcular_mae(reales: list, predicciones: list) -> float:

    suma_error = sum(abs(r - p) for r, p in zip(reales, predicciones))

    return suma_error / len(reales)


def obtener_valores_reales_test(ruta_test: str, fh: int) -> list:

    wb = openpyxl.load_workbook(ruta_test, data_only=True)

    hoja = wb.active

    valores = []

    for fila in hoja.iter_rows(
        min_row=2,
        max_row=fh + 1,
        values_only=True
    ):

        if fila[1] is not None:
            valores.append(float(fila[1]))

    return valores


def predecir_iterativo(modelo, ds_train, ph, fh, preprocesador=None):

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


# ==============================================================================
# EJERCICIO 1
# ==============================================================================

def ejecutar_ejercicio_1():

    print("\n--- RECTA DE REGRESIÓN (MAE) ---")

    print(
        f"{'PH':<5} | "
        f"{'Tasa':<12} | "
        f"{'Min-Max?':<10} | "
        f"{'Z-Score?':<10} | "
        f"{'MAE FH=24':<15}"
    )

    print("-" * 75)

    escenarios = [

        # ==========================================================
        # SIN NORMALIZACIÓN
        # ==========================================================
        {"ph": 12, "tasa": 0.0001,  "norm": True, "std": False},
        {"ph": 24, "tasa": 0.001,  "norm": True, "std": False},

        # ==========================================================
        # MIN-MAX
        # ==========================================================
        {"ph": 12, "tasa": 0.001, "norm": True,  "std": False},
        {"ph": 24, "tasa": 0.001, "norm": True,  "std": False},

        # ==========================================================
        # Z-SCORE
        # ==========================================================
        {"ph": 12, "tasa": 0.0001, "norm": True, "std": True},
        {"ph": 24, "tasa": 0.001, "norm": False, "std": True},

        # ==========================================================
        # EXPERIMENTOS EXTRA
        # ==========================================================
        {"ph": 48, "tasa": 1e-9,  "norm": False, "std": True},
        {"ph": 48, "tasa": 0.001, "norm": True,  "std": False},
    ]

    reales_test = obtener_valores_reales_test(
        RUTA_DATOS_TEST,
        24
    )

    for esc in escenarios:

        ds_train = FactoriaSerieTemporal.leer_desde_excel(
            RUTA_DATOS_TRAIN,
            esc["ph"]
        )

        pre = None

        if esc["norm"]:

            pre = NormalizadorMaxMin()

            pre.ajustar(ds_train)

            ds_train = pre.transformar_dataSet(ds_train)

        elif esc["std"]:

            pre = NormalizadorZ_Score()

            pre.ajustar(ds_train)

            ds_train = pre.transformar_dataSet(ds_train)

        modelo = Regresor_lineal_multiple(
            tasa_aprendizaje=esc["tasa"],
            epocas=1000
        )

        modelo.entrenar(ds_train)

        preds = predecir_iterativo(
            modelo,
            ds_train,
            esc["ph"],
            24,
            pre
        )

        if pre:
            preds = [pre.destransformar_valor(p) for p in preds]

        mae = calcular_mae(reales_test, preds)

        print(
            f"{esc['ph']:<5} | "
            f"{esc['tasa']:<12} | "
            f"{str(esc['norm']):<10} | "
            f"{str(esc['std']):<10} | "
            f"{mae:.4f}"
        )


# ==============================================================================
# EJERCICIO 2
# ==============================================================================

def ejecutar_ejercicio_2():

    print("\n--- kNN PONDERADO CON CORRELACIÓN ---")

    print(
        f"{'PH':<5} | "
        f"{'K':<5} | "
        f"{'MAE FH=24':<15}"
    )

    print("-" * 40)

    phs = [6, 12, 24, 48]

    ks = [1, 3, 5]

    reales_test = obtener_valores_reales_test(
        RUTA_DATOS_TEST,
        24
    )

    for ph in phs:

        ds_train = FactoriaSerieTemporal.leer_desde_excel(
            RUTA_DATOS_TRAIN,
            ph
        )

        for k in ks:

            modelo = Regresor_kNN_Correlacion(k=k)

            modelo.entrenar(ds_train)

            preds = predecir_iterativo(
                modelo,
                ds_train,
                ph,
                24
            )

            mae = calcular_mae(reales_test, preds)

            print(
                f"{ph:<5} | "
                f"{k:<5} | "
                f"{mae:.4f}"
            )


# ==============================================================================
# EJERCICIO 3
# ==============================================================================

def ejecutar_ejercicio_3():

    print("\n--- kNN CON HEURÍSTICA ---")

    print(
        f"{'PH':<5} | "
        f"{'K':<5} | "
        f"{'MAE FH=24':<15}"
    )

    print("-" * 40)

    mejor_ph = 12

    ks = [1, 3, 5]

    reales_test = obtener_valores_reales_test(
        RUTA_DATOS_TEST,
        24
    )

    ds_train = FactoriaSerieTemporal.leer_desde_excel(
        RUTA_DATOS_TRAIN,
        mejor_ph
    )

    for k in ks:

        funcion = FuncionObjetivoKNN(
            ds_train,
            k
        )

        # ==========================================================
        # HEURÍSTICA SIMPLE ALEATORIA
        # ==========================================================

        mejor_mae_train = float("inf")

        mejores_pesos = None

        for _ in range(10):

            pesos = [
                random.uniform(0, 1)
                for _ in range(funcion.dimension)
            ]

            mae_actual = funcion.evaluar(pesos)

            if mae_actual < mejor_mae_train:

                mejor_mae_train = mae_actual

                mejores_pesos = pesos

        # ==========================================================
        # ENTRENAR MODELO FINAL
        # ==========================================================

        modelo = Regresor_kNN_Ponderado(
            k=k,
            pesos=mejores_pesos
        )

        modelo.entrenar(ds_train)

        preds = predecir_iterativo(
            modelo,
            ds_train,
            mejor_ph,
            24
        )

        mae_test = calcular_mae(
            reales_test,
            preds
        )

        print(
            f"{mejor_ph:<5} | "
            f"{k:<5} | "
            f"{mae_test:.4f}"
        )


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":

    try:

        ejecutar_ejercicio_1()

        #ejecutar_ejercicio_2()

        #ejecutar_ejercicio_3()

    except FileNotFoundError:

        print("Error: No se encuentran los archivos Excel.")

        print(
            f"Verifica las rutas:\n"
            f"1. {RUTA_DATOS_TRAIN}\n"
            f"2. {RUTA_DATOS_TEST}"
        )

    except Exception as e:

        print(f"Ocurrió un error inesperado: {e}")
