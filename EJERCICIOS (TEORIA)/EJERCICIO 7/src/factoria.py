import pandas as pd
import re
from nombre import Nombre
from nomenclator import Nomenclator

class Factoria:
    """
    Clase encargada de leer el archivo Excel y construir el objeto Nomenclator.
    """
    
    # --- CONSTANTES (Evitamos "Cadenas Mágicas") ---
    # Si el INE cambia los nombres de las columnas en el futuro, 
    # solo cambiamos estas variables y el resto del programa seguirá funcionando.
    HOJA_HOMBRES = 'Hombres'
    HOJA_MUJERES = 'Mujeres'
    COL_NOMBRE = 'NOMBRE'
    COL_FREC = 'FRECUENCIA'
    COL_PMIL = 'Por 1.000'
    VALOR_NULO = 'NAN'

    @staticmethod
    def crear_desde_excel(ruta_excel: str) -> Nomenclator:
        nomenclator = Nomenclator()
        decadas_encontradas = set()
        
        # Intentamos abrir el archivo. Si no existe, lanzamos un error claro.
        try:
            xls = pd.ExcelFile(ruta_excel)
        except FileNotFoundError:
            raise FileNotFoundError(f"No se encontró el archivo Excel en: {ruta_excel}")

        mapa_hojas = {Factoria.HOJA_HOMBRES: 'H', Factoria.HOJA_MUJERES: 'M'}

        for hoja, gen in mapa_hojas.items():
            if hoja not in xls.sheet_names: 
                continue
            
            df = pd.read_excel(xls, sheet_name=hoja, header=[0, 1])
            decadas_cols = [c for c in df.columns.levels[0] if re.search(r'\d{4}', str(c))]
            
            for _, fila in df.iterrows():
                for dec_label in decadas_cols:
                    # Usamos las constantes en lugar del texto escrito a mano
                    if (dec_label, Factoria.COL_NOMBRE) not in fila: 
                        continue
                    
                    nombre_str = str(fila[(dec_label, Factoria.COL_NOMBRE)]).strip().upper()
                    
                    if nombre_str == Factoria.VALOR_NULO or not nombre_str: 
                        continue
                    
                    anio = int(re.search(r'\d{4}', str(dec_label)).group())
                    decadas_encontradas.add(anio)
                    
                    if nombre_str not in nomenclator.nombres:
                        nomenclator.nombres[nombre_str] = Nombre(nombre_str, gen)
                    
                    frec = fila[(dec_label, Factoria.COL_FREC)]
                    mil = fila[(dec_label, Factoria.COL_PMIL)]
                    
                    if pd.notna(frec) and frec > 0:
                        nomenclator.nombres[nombre_str].datos_por_decada[anio] = (int(frec), float(mil))

        nomenclator.decadas_ordenadas = sorted(list(decadas_encontradas))
        return nomenclator