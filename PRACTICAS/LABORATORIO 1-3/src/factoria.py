# ==============================================================================
# MÓDULO: factoria.py
# Propósito: Implementar el "Patrón Factoría" (Factory Pattern) para leer 
# ficheros físicos (CSV/Excel) y "fabricar" objetos DataSet llenos de Registros.
# ==============================================================================

import pandas as pd # Pandas es la librería estándar en Python para leer y manipular tablas de datos
from dataset import DataSetClasificacion, DataSetRegresion
from registro import RegistroClasificacion, RegistroRegresion

class FactoriaUniversal:
    """
    Clase Factoría definitiva.
    En programación, una 'Factoría' es una clase que se encarga de fabricar objetos complejos
    por nosotros. En lugar de ensuciar nuestro main.py leyendo Excels o CSVs línea por línea, 
    le delegamos ese trabajo sucio a esta Factoría.
    """
    
    # El decorador @staticmethod significa que esta función pertenece a la clase,
    # pero NO necesita que creemos un objeto (no necesita 'self').
    # Podemos llamarla directamente escribiendo: FactoriaUniversal._leer_dataframe_seguro(...)
    @staticmethod
    def _leer_dataframe_seguro(ruta_fichero: str) -> pd.DataFrame:
        """
        Método auxiliar oculto (el guion bajo '_' al principio indica que es un método PRIVADO, 
        solo debe usarse dentro de esta clase, no en el main).
        Su trabajo es leer el archivo aplicando "programación defensiva": no se fía de la extensión.
        """
        try:
            # MAGIA: Intentamos leerlo como texto plano (CSV) primero, con codificación permisiva.
            df = pd.read_csv(ruta_fichero, encoding='latin-1')
            
            # Si el archivo era un Excel disfrazado de CSV, Pandas lo leerá como una sola 
            # columna gigante de texto incomprensible. Si hay menos de 2 columnas, sospechamos.
            if len(df.columns) < 2:
                raise ValueError("Parece un archivo binario/Excel, pasamos al Plan B")
                
        except Exception:
            # PLAN B: Si falló la lectura como texto, obligamos a Pandas a leerlo como Excel binario
            try:
                # 'openpyxl' es el motor moderno para leer archivos .xlsx
                df = pd.read_excel(ruta_fichero, engine='openpyxl')
            except:
                # Fallback: Por si es un archivo de Excel súper antiguo (.xls)
                df = pd.read_excel(ruta_fichero)
                
        # Devolvemos el DataFrame (la tabla de datos en memoria) ya limpio y listo
        return df

    @staticmethod
    def crear_dataset_clasificacion(ruta_fichero: str, indice_objetivo: int = -1) -> DataSetClasificacion:
        """
        Fabrica y devuelve un DataSetClasificacion lleno de registros listos para usar.
        indice_objetivo indica en qué columna está la etiqueta (por defecto -1, la última).
        """
        # 1. Creamos el contenedor vacío
        dataset = DataSetClasificacion()
        
        # 2. Leemos la tabla del disco duro usando nuestro método seguro
        df = FactoriaUniversal._leer_dataframe_seguro(ruta_fichero)
        
        # 3. Extraemos los nombres de las columnas y los guardamos en el dataset
        dataset.set_cabeceras(df.columns.tolist())
        
        # 4. Convertimos la tabla de Pandas a una matriz clásica de Python (lista de listas)
        datos = df.values.tolist()
        
        # 5. Recorremos fila a fila (paciente a paciente, o flor a flor)
        for fila in datos:
            # pop() saca el elemento de la lista y se lo queda. Al mismo tiempo, 
            # desaparece de 'fila', dejando solo los atributos numéricos.
            # Lo forzamos a ser str (texto) y usamos strip() para quitar espacios en blanco fantasma.
            objetivo_str = str(fila.pop(indice_objetivo)).strip()
            
            try:
                # Convertimos lo que queda en la fila a números decimales (float).
                # Usamos una list comprehension: "por cada valor en la fila, hazle un float()"
                atributos_float = [float(valor) for valor in fila]
            except ValueError:
                # Si una fila tiene una letra donde debería haber un número (dato corrupto),
                # el 'continue' hace que nos saltemos este paciente y pasemos al siguiente.
                continue
                
            # Fabricamos el registro individual y lo guardamos en nuestro contenedor
            dataset.agregar_registro(RegistroClasificacion(atributos_float, objetivo_str))
            
        return dataset

    @staticmethod
    def crear_dataset_regresion(ruta_fichero: str, indice_objetivo: int = -1) -> DataSetRegresion:
        """
        Igual que el anterior, pero fabrica un DataSetRegresion.
        La diferencia vital es que aquí la etiqueta objetivo DEBE ser un número.
        """
        dataset = DataSetRegresion()
        df = FactoriaUniversal._leer_dataframe_seguro(ruta_fichero)
        
        dataset.set_cabeceras(df.columns.tolist())
        datos = df.values.tolist()
        
        for fila in datos:
            try:
                # En Regresión, predecimos un NÚMERO (ej: precio de una casa).
                # Por tanto, forzamos que el objetivo extraído sea un float.
                objetivo_float = float(fila.pop(indice_objetivo))
                
                # Convertimos el resto de atributos también a float
                atributos_float = [float(valor) for valor in fila]
            except ValueError:
                # Si falla la conversión (ej: hay un texto donde debe haber un número), saltamos la fila
                continue
                
            dataset.agregar_registro(RegistroRegresion(atributos_float, objetivo_float))
            
        return dataset