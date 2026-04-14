import pandas as pd
import re
from nombre import Nombre
from nomenclator import Nomenclator

class Factoria:
    """
    Clase encargada exclusivamente de leer el archivo Excel y construir 
    el objeto Nomenclator con todos los datos estructurados.
    (Sigue el patrón de diseño 'Factory' o Creador).
    """

    @staticmethod
    def crear_desde_excel(ruta_excel: str) -> Nomenclator:
        """
        Lee el Excel del INE, procesa las hojas de Hombres y Mujeres,
        y devuelve un objeto Nomenclator lleno de objetos Nombre.
        """
        # 1. Preparamos el contenedor principal y un conjunto para guardar los años
        nomenclator = Nomenclator()
        decadas_encontradas = set() # Usamos 'set' para que no haya décadas repetidas
        
        # 2. Cargamos el archivo Excel en memoria
        xls = pd.ExcelFile(ruta_excel)
        
        # El INE divide los datos en dos hojas específicas
        mapa_hojas = {'Hombres': 'H', 'Mujeres': 'M'}

        for hoja, gen in mapa_hojas.items():
            # Si por algún motivo la hoja no está en el Excel, la saltamos
            if hoja not in xls.sheet_names: 
                continue
            
            # 3. Leer la hoja. 
            # El INE usa 2 filas de cabecera: 
            # Fila 0: "NACIDOS EN 1930", "NACIDOS EN 1940"...
            # Fila 1: "NOMBRE", "FRECUENCIA", "Por 1.000"...
            # Por eso usamos header=[0, 1] para leer ambas simultáneamente.
            df = pd.read_excel(xls, sheet_name=hoja, header=[0, 1])
            
            # 4. Buscamos qué columnas del nivel superior (nivel 0) tienen un año (4 números)
            # Ej: de "NACIDOS EN AÑOS 1930 A 1939" sabremos que es la columna de esa década
            decadas_cols = [c for c in df.columns.levels[0] if re.search(r'\d{4}', str(c))]
            
            # 5. Recorremos el Excel fila por fila
            for _, fila in df.iterrows():
                
                # Dentro de cada fila, miramos cada bloque de década
                for dec_label in decadas_cols:
                    
                    # Si esta década no tiene la sub-columna 'NOMBRE', pasamos de largo
                    if (dec_label, 'NOMBRE') not in fila: 
                        continue
                    
                    # Extraemos el nombre, le quitamos espacios extra y lo ponemos en mayúsculas
                    nombre_str = str(fila[(dec_label, 'NOMBRE')]).strip().upper()
                    
                    # Ignoramos celdas vacías o con errores (NAN)
                    if nombre_str == 'NAN' or not nombre_str: 
                        continue
                    
                    # 6. Extraemos el año exacto de la cabecera usando una expresión regular
                    # re.search busca 4 dígitos seguidos (\d{4}), y .group() extrae ese número
                    anio = int(re.search(r'\d{4}', str(dec_label)).group())
                    decadas_encontradas.add(anio)
                    
                    # 7. Si es la primera vez que vemos este nombre, le creamos su objeto Nombre
                    if nombre_str not in nomenclator.nombres:
                        nomenclator.nombres[nombre_str] = Nombre(nombre_str, gen)
                    
                    # 8. Extraemos los valores matemáticos
                    frec = fila[(dec_label, 'FRECUENCIA')]
                    mil = fila[(dec_label, 'Por 1.000')]
                    
                    # Si la frecuencia es válida (existe y es mayor que 0), la guardamos
                    if pd.notna(frec) and frec > 0:
                        # Se guarda en el diccionario interno del objeto Nombre:
                        # Clave: Año -> Valor: Tupla (frecuencia, tanto_por_mil)
                        nomenclator.nombres[nombre_str].datos_por_decada[anio] = (int(frec), float(mil))

        # 9. Por último, ordenamos los años de menor a mayor (1920, 1930...) 
        # y se los pasamos al Nomenclator para que los tenga siempre a mano.
        nomenclator.decadas_ordenadas = sorted(list(decadas_encontradas))
        
        return nomenclator