import pandas as pd
import re
from nombre import Nombre
from nomenclator import Nomenclator

class Factoria:
    """
    Clase de tipo 'Factory' encargada de la lógica de extracción, 
    transformación y carga (ETL) de los datos del Excel del INE.
    """
    

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
        
        try:
            xls = pd.ExcelFile(ruta_excel)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: No se encontró el archivo en {ruta_excel}")

        mapa_hojas = {Factoria.HOJA_HOMBRES: 'H', Factoria.HOJA_MUJERES: 'M'}

        for hoja, gen in mapa_hojas.items():
            if hoja not in xls.sheet_names: 
                continue
            
            df = pd.read_excel(xls, sheet_name=hoja, header=[0, 1])
            
            decadas_cols = [c for c in df.columns.levels[0] if re.search(r'\d{4}', str(c))]
            
            for _, fila in df.iterrows():
                for dec_label in decadas_cols:
                    
                    if (dec_label, Factoria.COL_NOMBRE) not in fila: 
                        continue
                    
                    valor_celda_nombre = str(fila[(dec_label, Factoria.COL_NOMBRE)]).strip().upper()
                    
                    if not valor_celda_nombre or valor_celda_nombre in [Factoria.VALOR_NULO, 'NONE', 'NOMBRE']: 
                        continue
                    

                    anio = int(re.search(r'\d{4}', str(dec_label)).group())
                    decadas_encontradas.add(anio)
                    
                    if valor_celda_nombre not in nomenclator.nombres:
                        nomenclator.nombres[valor_celda_nombre] = Nombre(valor_celda_nombre, gen)
                    
                    frec = fila[(dec_label, Factoria.COL_FREC)]
                    mil = fila[(dec_label, Factoria.COL_PMIL)]
                    
                    if pd.notna(frec) and frec > 0:
                        nomenclator.nombres[valor_celda_nombre].datos_por_decada[anio] = (int(frec), float(mil))

        nomenclator.decadas_ordenadas = sorted(list(decadas_encontradas))
        
        return nomenclator