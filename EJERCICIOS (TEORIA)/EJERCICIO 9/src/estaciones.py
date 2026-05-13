import math

class Estaciones:
    """
    Esta clase gestiona la red desde la perspectiva de los nodos (paradas).
    Adaptada para trabajar con objetos Estacion y Linea.
    """

    def __init__(self, grafo_estaciones: dict):
        """
        Inicializa la colección de estaciones.
        Estructura de grafo_estaciones: 
        { ObjetoEstacion: { ObjetoLinea: orden_entero, ObjetoLinea2: orden_entero }, ... }
        """
        self.grafo_estaciones = grafo_estaciones

    def to_lineas(self):
        from lineas import Lineas
        temp_red = {}
        
        for est_obj, lineas_info in self.grafo_estaciones.items():
            for linea_obj, lista_posiciones in lineas_info.items():
                if linea_obj not in temp_red:
                    temp_red[linea_obj] = []
                
                # RECORREMOS LA LISTA DE POSICIONES QUE AHORA HEMOS CREADO
                for posicion in lista_posiciones:
                    temp_red[linea_obj].append((posicion, est_obj))
        
        red_final = {}
        for linea_obj, paradas_con_orden in temp_red.items():
            paradas_con_orden.sort(key=lambda x: x[0]) 
            red_final[linea_obj] = [p[1] for p in paradas_con_orden]
            
        return Lineas(red_final)

    def estaciones_con_mas_lineas(self) -> list:
        """
        Identifica los puntos neurálgicos del Metro (donde hay más transbordos).
        Devuelve una lista de objetos Estacion.
        """
        if not self.grafo_estaciones: return []
        max_lineas = max(len(lineas) for lineas in self.grafo_estaciones.values())
        return [est for est, lineas in self.grafo_estaciones.items() if len(lineas) == max_lineas]

    def misma_linea(self, nombre_est1: str, nombre_est2: str) -> bool:
        """
        Verifica si es posible ir de una estación a otra sin cambiar de línea.
        Recibe strings (nombres) por comodidad y busca los objetos internamente.
        """
        # Buscamos los objetos Estacion correspondientes a los nombres dados
        est1 = next((e for e in self.grafo_estaciones if e.nombre == nombre_est1), None)
        est2 = next((e for e in self.grafo_estaciones if e.nombre == nombre_est2), None)
        
        if not est1 or not est2:
            return False
            
        lineas_est1 = set(self.grafo_estaciones[est1].keys())
        lineas_est2 = set(self.grafo_estaciones[est2].keys())
        
        # Si comparten al menos un objeto Linea, devuelve True
        return not lineas_est1.isdisjoint(lineas_est2)
    
    def _haversine(self, lat1, lon1, lat2, lon2):
        """Fórmula matemática pura para distancias."""
        R = 6371.0
        lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
        lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)

        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad

        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.asin(math.sqrt(a))
        return R * c

    def estacion_mas_cercana(self, mi_lat: float, mi_lon: float) -> dict:
        """
        Dada una ubicación GPS, busca la estación más cercana.
        """
        mejor_estacion = None
        distancia_minima = float('inf')

        for est_obj in self.grafo_estaciones.keys():
            # Nos aseguramos de que el objeto tenga las coordenadas cargadas
            if est_obj.latitud is not None and est_obj.longitud is not None:
                dist = self._haversine(mi_lat, mi_lon, est_obj.latitud, est_obj.longitud)
                
                if dist < distancia_minima:
                    distancia_minima = dist
                    mejor_estacion = est_obj

        # Devolvemos el mismo formato de diccionario para no romper el main.py
        return {
            "estacion": mejor_estacion.nombre if mejor_estacion else None,
            "distancia_km": distancia_minima
        }

    def __eq__(self, otro) -> bool:
        """Compara si dos objetos Estaciones contienen los mismos datos."""
        if not isinstance(otro, Estaciones): return False
        return self.grafo_estaciones == otro.grafo_estaciones