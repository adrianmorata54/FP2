import pandas as pd
import re
from nombre import Nombre
from nomenclator import Nomenclator

class Factoria:
    """
    Clase de tipo 'Factory' encargada de la lógica de extracción, 
    transformación y carga (ETL) de los datos del Excel del INE.
    """
    
    # --- CONSTANTES DE ESTRUCTURA ---
    # Centralizamos los nombres de las columnas para facilitar el mantenimiento.
    HOJA_HOMBRES = 'Hombres'
    HOJA_MUJERES = 'Mujeres'
    COL_NOMBRE = 'NOMBRE'
    COL_FREC = 'FRECUENCIA'
    COL_PMIL = 'Por 1.000'
    VALOR_NULO = 'NAN'

    @staticmethod
    def crear_desde_excel(ruta_excel: str) -> Nomenclator:
        """
        Lee un archivo Excel con múltiples hojas y cabeceras dobles (MultiIndex)
        y construye un objeto Nomenclator.
        """
        nomenclator = Nomenclator()
        decadas_encontradas = set()
        
        # 1. Intento de apertura del archivo con manejo de errores
        try:
            xls = pd.ExcelFile(ruta_excel)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: No se encontró el archivo en {ruta_excel}")

        # Mapeamos el nombre de la hoja con el código de género
        mapa_hojas = {Factoria.HOJA_HOMBRES: 'H', Factoria.HOJA_MUJERES: 'M'}

        for hoja, gen in mapa_hojas.items():
            # Si la hoja no existe en el Excel, pasamos a la siguiente
            if hoja not in xls.sheet_names: 
                continue
            
            # Leemos la hoja considerando que las filas 0 y 1 forman la cabecera (MultiIndex)
            df = pd.read_excel(xls, sheet_name=hoja, header=[0, 1])
            
            # Filtramos las columnas del nivel superior (Nivel 0) que contienen años (4 dígitos)
            # Esto ignora columnas de ranking o metadatos sin fecha.
            decadas_cols = [c for c in df.columns.levels[0] if re.search(r'\d{4}', str(c))]
            
            # 2. Iteración por cada fila (un nombre por fila)
            for _, fila in df.iterrows():
                # Iteramos por cada década detectada en la cabecera
                for dec_label in decadas_cols:
                    
                    # Verificamos que la celda de NOMBRE exista para esta década
                    if (dec_label, Factoria.COL_NOMBRE) not in fila: 
                        continue
                    
                    # Extraemos y limpiamos el nombre (le quita espacios y lo pone en mayúsculas)
                    valor_celda_nombre = str(fila[(dec_label, Factoria.COL_NOMBRE)]).strip().upper()
                    
                    # Si la celda está vacía, contiene NAN o es solo el título de la columna, saltamos
                    if not valor_celda_nombre or valor_celda_nombre in [Factoria.VALOR_NULO, 'NONE', 'NOMBRE']: 
                        continue
                    
                    # 3. Procesamiento del año y almacenamiento
                    # Extraemos el primer número de 4 cifras (ej: "1930" de "NACIDOS ANTES DE 1930")
                    anio = int(re.search(r'\d{4}', str(dec_label)).group())
                    decadas_encontradas.add(anio)
                    
                    # Si el nombre no ha sido registrado antes en el nomenclátor, se crea el objeto
                    if valor_celda_nombre not in nomenclator.nombres:
                        nomenclator.nombres[valor_celda_nombre] = Nombre(valor_celda_nombre, gen)
                    
                    # Extraemos frecuencia y tasa por mil
                    frec = fila[(dec_label, Factoria.COL_FREC)]
                    mil = fila[(dec_label, Factoria.COL_PMIL)]
                    
                    # Solo guardamos el dato si hay una frecuencia válida (mayor que cero)
                    if pd.notna(frec) and frec > 0:
                        nomenclator.nombres[valor_celda_nombre].datos_por_decada[anio] = (int(frec), float(mil))

        # 4. Finalización: ordenamos las décadas cronológicamente para el resto del programa
        nomenclator.decadas_ordenadas = sorted(list(decadas_encontradas))
        
        return nomenclator