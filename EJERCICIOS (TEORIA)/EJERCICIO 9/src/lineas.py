import math
from linea import Linea
from estacion import Estacion

class Lineas:
    """
    Esta clase actúa como el cerebro de la red de Metro. 
    Gestiona objetos Linea y Estacion según el Boletín 9.
    """

    def __init__(self, grafo_lineas: dict):
        """
        Inicializa la red.
        grafo_lineas: { ObjetoLinea: [ObjetoEstacion1, ObjetoEstacion2, ...] }
        """
        # El PDF exige que la propiedad se llame exactamente grafo_lineas
        self.grafo_lineas = grafo_lineas

    def to_estaciones(self):
        from estaciones import Estaciones  
        grafo_est = {}
        
        for linea_obj, lista_estaciones in self.grafo_lineas.items():
            for orden, est_obj in enumerate(lista_estaciones):
                if est_obj not in grafo_est:
                    grafo_est[est_obj] = {}
                
                # CREAMOS UNA LISTA PARA NO SOBREESCRIBIR SI LA LÍNEA ES CIRCULAR
                if linea_obj not in grafo_est[est_obj]:
                    grafo_est[est_obj][linea_obj] = []
                
                grafo_est[est_obj][linea_obj].append(orden)
        
        return Estaciones(grafo_est)

    # --- MÉTODOS GEOGRÁFICOS (AHORA MÁS SIMPLES) ---

    def distancia_km(self, e1: Estacion, e2: Estacion) -> float:
        """
        Calcula la distancia Haversine entre dos objetos Estacion.
        Como el objeto ya tiene latitud y longitud, no necesitamos APIs aquí.
        """
        if None in (e1.latitud, e1.longitud, e2.latitud, e2.longitud):
            return 0.0

        rad = math.pi / 180
        dlat = (e2.latitud - e1.latitud) * rad
        dlon = (e2.longitud - e1.longitud) * rad
        
        a = (math.sin(dlat/2)**2 + math.cos(e1.latitud*rad) * math.cos(e2.latitud*rad) * math.sin(dlon/2)**2)
        distancia = 2 * 6371 * math.asin(math.sqrt(a))
        return distancia

    def longitud_total_linea(self, linea_obj: Linea) -> float:
        """Calcula los kms totales de una línea sumando tramos entre estaciones."""
        paradas = self.grafo_lineas.get(linea_obj, [])
        total = 0.0
        for i in range(len(paradas) - 1):
            total += self.distancia_km(paradas[i], paradas[i+1])
        return total

    # --- MÉTODOS DE ANÁLISIS DE RED ---

    def eliminar_linea(self, nombre_linea: str):
        """Elimina una línea buscando por su nombre string."""
        linea_a_borrar = next((l for l in self.grafo_lineas if l.nombre == nombre_linea), None)
        if linea_a_borrar:
            del self.grafo_lineas[linea_a_borrar]

    def es_conexo(self) -> bool:
        """Verifica si todas las estaciones están conectadas entre sí (BFS)."""
        if not self.grafo_lineas: return True
        
        # 1. Construir lista de adyacencia usando los objetos
        adj = {}
        todas = set()
        for paradas in self.grafo_lineas.values():
            for i, est in enumerate(paradas):
                todas.add(est)
                if est not in adj: adj[est] = set()
                if i > 0: adj[est].add(paradas[i-1])
                if i < len(paradas) - 1: adj[est].add(paradas[i+1])
        
        if not todas: return True
        
        # 2. BFS desde una estación cualquiera
        inicio = next(iter(todas))
        visitados = {inicio}
        cola = [inicio]
        while cola:
            actual = cola.pop(0)
            for vecino in adj.get(actual, []):
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(vecino)
        
        return len(visitados) == len(todas)

    def buscar_ruta(self, nombre_origen: str, nombre_destino: str) -> dict:
        """
        Encuentra el camino más corto entre dos estaciones por su nombre.
        Devuelve el camino de objetos Estacion y las instrucciones.
        """
        # Convertimos nombres a objetos para trabajar internamente
        estaciones_dict = self.to_estaciones().grafo_estaciones
        origen_obj = next((e for e in estaciones_dict if e.nombre == nombre_origen), None)
        destino_obj = next((e for e in estaciones_dict if e.nombre == nombre_destino), None)

        if not origen_obj or not destino_obj:
            return {"error": "Estaciones no encontradas"}

        # BFS para encontrar el camino más corto
        cola = [[origen_obj]]
        visitados = {origen_obj}
        
        adj = {est: set() for est in estaciones_dict}
        for paradas in self.grafo_lineas.values():
            for i, est in enumerate(paradas):
                if i > 0: adj[est].add(paradas[i-1])
                if i < len(paradas) - 1: adj[est].add(paradas[i+1])

        camino_final = []
        while cola:
            camino = cola.pop(0)
            actual = camino[-1]
            if actual == destino_obj:
                camino_final = camino
                break
            for vecino in adj[actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(camino + [vecino])

        return {"camino": camino_final, "paradas": len(camino_final)}

    def lineas_criticas(self) -> list:
        """
        Una línea es crítica si al quitarla alguna estación se queda sin servicio.
        """
        estaciones_info = self.to_estaciones().grafo_estaciones
        criticas = []
        for linea in self.grafo_lineas:
            for est in self.grafo_lineas[linea]:
                # Si esta estación solo pertenece a 1 línea, esa línea es crítica
                if len(estaciones_info[est]) == 1:
                    criticas.append(linea)
                    break 
        return criticas

    def linea_mas_larga(self) -> Linea:
        """Devuelve el objeto Linea con más kilómetros totales."""
        return max(self.grafo_lineas.keys(), key=self.longitud_total_linea)

    def __eq__(self, otro) -> bool:
        if not isinstance(otro, Lineas): return False
        return self.grafo_lineas == otro.grafo_lineas