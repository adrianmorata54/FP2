import pandas as pd
import time
import urllib.request
import urllib.parse
import json
from linea import Linea
from estacion import Estacion
from lineas import Lineas

class FactoriaMetro:
    """
    Factoría evolucionada para el Boletín 9.
    Ahora no solo lee, sino que construye el mapa de objetos completo.
    """

    @staticmethod
    def _obtener_coordenadas_api(nombre_estacion: str):
        """
        Método privado para geolocalización.
        Usa un sistema de intentos múltiples para mejorar la precisión de la API.
        """
        # Varias formas de preguntar por si la API es "quisquillosa"
        intentos = [
            f"Estación de metro {nombre_estacion}, Madrid",
            f"Metro {nombre_estacion}, Madrid",
            f"{nombre_estacion}, Madrid, España"
        ]
        
        headers = {'User-Agent': 'ProyectoMetroUniversidad/1.0'}
        
        for query in intentos:
            try:
                url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(query)}&format=json&limit=1"
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req) as response:
                    data = json.loads(response.read().decode())
                    if data:
                        # Si encuentra datos, los devuelve inmediatamente y sale del bucle
                        return float(data[0]['lat']), float(data[0]['lon'])
            except Exception:
                pass # Si este intento falla (error de red), simplemente pasa al siguiente
            
            time.sleep(0.5) # Pequeña pausa entre intentos para no saturar al servidor
            
        # Si termina todos los intentos y no encuentra nada, devuelve None
        return None, None

    @staticmethod
    def cargar_desde_excel(ruta_archivo: str) -> Lineas:
        try:
            if ruta_archivo.endswith('.csv'):
                df = pd.read_csv(ruta_archivo)
            else:
                df = pd.read_excel(ruta_archivo)
            
            grafo_lineas_objetos = {}
            # Caché para no repetir llamadas a la API si una estación sale en varias líneas
            estaciones_creadas = {}

            for _, fila in df.iterrows():
                # --- 1. DATOS DE LÍNEA ---
                nombre_linea = str(fila['Línea']).strip()
                total_declarado = int(fila['Total Paradas'])
                # Lógica para circulares (L6 y L12 suelen serlo en Madrid)
                es_circular = "6" in nombre_linea or "12" in nombre_linea
                
                linea_obj = Linea(nombre_linea, es_circular)

                # --- 2. DATOS DE ESTACIONES (Limpieza de tu código anterior) ---
                texto_estaciones = str(fila['Estaciones'])
                separador = ',' if ',' in texto_estaciones else '-'
                nombres_est = [n.strip() for n in texto_estaciones.split(separador)]
                
                # --- 3. VALIDACIÓN DE INTEGRIDAD (Tu código original) ---
                if len(nombres_est) != total_declarado:
                    print(f"⚠️ Alerta en {nombre_linea}: el Excel dice {total_declarado} "
                          f"paradas pero hay {len(nombres_est)}.")

                # --- 4. CONSTRUCCIÓN DE OBJETOS ESTACIÓN ---
                lista_objetos_estacion = []
                for nombre in nombres_est:
                    if nombre not in estaciones_creadas:
                        # Si es nueva, buscamos coordenadas
                        lat, lon = FactoriaMetro._obtener_coordenadas_api(nombre)
                        estaciones_creadas[nombre] = Estacion(nombre, lat, lon)
                        print(f"📍 Localizada: {nombre}")
                        time.sleep(1) # Respetamos el límite de la API
                    
                    lista_objetos_estacion.append(estaciones_creadas[nombre])

                # Guardamos: Clave objeto Linea, Valor lista de objetos Estacion
                grafo_lineas_objetos[linea_obj] = lista_objetos_estacion

            print(f"✅ Red cargada: {len(grafo_lineas_objetos)} líneas y {len(estaciones_creadas)} estaciones.")
            return Lineas(grafo_lineas_objetos)

        except Exception as e:
            print(f"❌ Error crítico en factoría: {e}")
            raise