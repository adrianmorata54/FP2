# src/factoria.py
import openpyxl
from dataset import DataSetRegresion
from registro import RegistroRegresion

class FactoriaSerieTemporal:
    @staticmethod
    def leer_desde_excel(ruta_archivo: str, ph: int) -> DataSetRegresion:
        """
        Lee un archivo .xlsx y crea un DataSet de Regresión usando PH (Past History).
        No usa numpy ni pandas.
        """
        # 1. Cargar el Excel (asegúrate de tener instalado: pip install openpyxl)
        wb = openpyxl.load_workbook(ruta_archivo, data_only=True)
        hoja = wb.active

        # 2. Extraer los valores de la serie (Columna B / Índice 1)
        valores_serie = []
        for fila in hoja.iter_rows(min_row=2, values_only=True):
            if fila[1] is not None:
                valores_serie.append(float(fila[1]))

        # 3. Crear el dataset y aplicar Ventana Deslizante
        dataset = DataSetRegresion()
        # Nombres de columnas sugeridos: Lag_12, Lag_11... Lag_1
        nombres = [f"Lag_{i}" for i in range(ph, 0, -1)]
        dataset.set_cabeceras(nombres)

        for i in range(ph, len(valores_serie)):
            atributos = valores_serie[i-ph : i] # Los 'ph' valores anteriores
            objetivo = valores_serie[i]        # El valor actual que queremos predecir
            
            reg = RegistroRegresion(atributos, objetivo)
            dataset.agregar_registro(reg)

        return dataset