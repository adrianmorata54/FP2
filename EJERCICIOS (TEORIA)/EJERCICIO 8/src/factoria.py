import pandas as pd
from lineas import Lineas

class FactoriaMetro:
    """
    Esta clase implementa el patrón Factoría. 
    Su única responsabilidad es la persistencia: leer archivos externos 
    y transformarlos en objetos listos para ser usados por la lógica del programa.
    """

    @staticmethod
    def cargar_desde_excel(ruta_archivo: str) -> Lineas:
        """
        Lee el archivo de datos (Excel o CSV), valida la integridad de la 
        información y devuelve un objeto de la clase Lineas.
        """
        try:
            # 1. Detección de formato y lectura robusta con Pandas
            # Soporta tanto el formato antiguo .xls/.xlsx como el formato .csv
            if ruta_archivo.endswith('.csv'):
                df = pd.read_csv(ruta_archivo)
            else:
                df = pd.read_excel(ruta_archivo)
            
            diccionario_red = {}

            # 2. Iteramos sobre cada fila del DataFrame (cada línea de Metro)
            for _, fila in df.iterrows():
                # Extraemos y limpiamos los nombres de columnas (ajustar según el Excel real)
                nombre_linea = str(fila['Línea']).strip()
                texto_estaciones = str(fila['Estaciones'])
                total_declarado = int(fila['Total Paradas'])

                # 3. Limpieza de datos:
                # Convertimos el string de estaciones en una lista real, eliminando espacios
                # Si el Excel usa guiones '-' o comas ',', aquí se define el separador
                separador = ',' if ',' in texto_estaciones else '-'
                lista_estaciones = [est.strip() for est in texto_estaciones.split(separador)]
                
                # 4. Validación de integridad (Exigencia del Boletín)
                # Comparamos si el número de elementos en la lista coincide con la columna C
                conteo_real = len(lista_estaciones)
                if conteo_real != total_declarado:
                    print(f"⚠️ Alerta en {nombre_linea}: el Excel dice {total_declarado} "
                          f"paradas pero se han contado {conteo_real}.")
                
                # 5. Construcción del diccionario intermedio
                # Clave: Nombre de la línea | Valor: Lista ordenada de paradas
                diccionario_red[nombre_linea] = lista_estaciones

            print(f"✅ Carga finalizada: {len(diccionario_red)} líneas procesadas.")
            
            # Devolvemos el objeto principal de la lógica de negocio
            return Lineas(diccionario_red)

        except FileNotFoundError:
            print(f"❌ Error: El archivo '{ruta_archivo}' no existe en la ruta especificada.")
            raise
        except KeyError as e:
            print(f"❌ Error: El archivo no tiene las columnas esperadas: {e}")
            raise
        except Exception as e:
            print(f"❌ Error crítico al procesar los datos: {e}")
            raise