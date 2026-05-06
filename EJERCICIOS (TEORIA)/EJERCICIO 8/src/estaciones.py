import math
import json
import urllib.request
import urllib.parse
import time

class Estaciones:
    """
    Esta clase gestiona la red desde la perspectiva de los nodos (paradas).
    Permite analizar transbordos, realizar búsquedas geográficas y 
    reconvertir los datos de vuelta a líneas.
    """

    def __init__(self, diccionario_estaciones: dict):
        """
        Inicializa la colección de estaciones.
        Estructura de self._nodos: 
        { 'Sol': {'Linea 1': [14], 'Linea 2': [5]}, ... }
        """
        self._nodos = diccionario_estaciones

    def crear_lineas(self):
        """
        Realiza la operación inversa: a partir de las estaciones, reconstruye las líneas.
        Es vital para verificar que la conversión de datos no ha perdido información.
        """
        from lineas import Lineas # Importación local para evitar bucles de importación
        temp_red = {}
        
        # 1. Agrupamos las estaciones por el nombre de su línea
        for nombre_est, lineas_info in self._nodos.items():
            for nombre_linea, lista_posiciones in lineas_info.items():
                if nombre_linea not in temp_red:
                    temp_red[nombre_linea] = []
                
                # Guardamos tuplas (posición, nombre) para poder ordenar luego
                for posicion in lista_posiciones:
                    temp_red[nombre_linea].append((posicion, nombre_est))
        
        # 2. Ordenamos cada línea según el número de parada y limpiamos la estructura
        red_final = {}
        for nombre_linea, paradas_con_orden in temp_red.items():
            paradas_con_orden.sort() # Ordena por el primer elemento de la tupla (la posición)
            red_final[nombre_linea] = [p[1] for p in paradas_con_orden]
            
        return Lineas(red_final)

    def estaciones_con_mas_lineas(self) -> list:
        """
        Identifica los puntos neurálgicos del Metro (donde hay más transbordos).
        """
        if not self._nodos: return []
        # Calculamos cuál es el número máximo de líneas en una sola estación
        max_lineas = max(len(lineas) for lineas in self._nodos.values())
        # Devolvemos todas las estaciones que empaten con ese máximo
        return [est for est, lineas in self._nodos.items() if len(lineas) == max_lineas]

    def misma_linea(self, est1: str, est2: str) -> bool:
        """
        Verifica si es posible ir de una estación a otra sin cambiar de línea.
        Usa conjuntos (sets) para una comparación eficiente.
        """
        if est1 not in self._nodos or est2 not in self._nodos:
            return False
            
        lineas_est1 = set(self._nodos[est1].keys())
        lineas_est2 = set(self._nodos[est2].keys())
        
        # .isdisjoint devuelve True si no tienen NADA en común. 
        # Al negarlo con 'not', devuelve True si comparten al menos una línea.
        return not lineas_est1.isdisjoint(lineas_est2)
    
    def _pedir_coordenadas(self, nombre_estacion: str) -> tuple:
        """
        MÉTODO PRIVADO: Consulta la API de OpenStreetMap (Nominatim).
        Implementa un sistema de reintentos y esperas para respetar los límites de la API.
        """
        # Definimos varias formas de preguntar para asegurar el éxito
        intentos = [
            f"Estación {nombre_estacion}, Madrid",
            f"{nombre_estacion}, Madrid",
            f"Plaza de {nombre_estacion.replace('Plaza ', '')}, Madrid"
        ]
        
        for query in intentos:
            # Codificamos el texto para URL (ej: espacios -> %20)
            url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(query)}&format=json&limit=1"
            
            # Es obligatorio enviar un User-Agent para que la API no nos bloquee
            req = urllib.request.Request(url, headers={'User-Agent': 'ProyectoUniversidad_FP2/1.0'})
            
            try:
                with urllib.request.urlopen(req) as response:
                    datos = json.loads(response.read().decode())
                    if datos:
                        time.sleep(1) # Pausa de cortesía entre peticiones
                        return float(datos[0]['lat']), float(datos[0]['lon'])
            except Exception as e:
                print(f"  [!] Error de conexión: {e}")
            
            time.sleep(1) # Espera antes del siguiente reintento si este falló
            
        return None, None

    def distancia_real_km(self, estacion1: str, estacion2: str) -> dict:
        """
        Calcula la distancia física entre dos puntos usando trigonometría esférica.
        """
        if estacion1 not in self._nodos or estacion2 not in self._nodos:
            return {"error": "Estación no encontrada."}

        # Obtenemos latitudes y longitudes
        lat1, lon1 = self._pedir_coordenadas(estacion1)
        lat2, lon2 = self._pedir_coordenadas(estacion2)

        if not lat1 or not lat2:
            return {"error": "No se han podido obtener las coordenadas de Internet."}

        # --- Algoritmo de Haversine ---
        R = 6371.0 # Radio medio de la Tierra en kilómetros

        # Convertimos grados a radianes (necesario para las funciones de math)
        lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
        lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)

        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad

        # Fórmula matemática para la distancia sobre una esfera
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.asin(math.sqrt(a))
        distancia = R * c

        return {
            "estacion1": {"nombre": estacion1, "coords": (lat1, lon1)},
            "estacion2": {"nombre": estacion2, "coords": (lat2, lon2)},
            "distancia_km": distancia
        }

    def __eq__(self, otro) -> bool:
        """Compara si dos objetos Estaciones contienen los mismos datos."""
        if not isinstance(otro, Estaciones): return False
        return self._nodos == otro._nodos