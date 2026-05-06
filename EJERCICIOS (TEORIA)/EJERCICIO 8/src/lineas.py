class Lineas:
    """
    Esta clase actúa como el cerebro de la red de Metro. 
    Se encarga de gestionar la relación entre las líneas y las estaciones, 
    además de realizar análisis de conectividad y rutas.
    """

    def __init__(self, diccionario_lineas: dict):
        """
        Inicializa la red.
        Recibe un diccionario donde la clave es el nombre de la línea 
        y el valor es una lista ordenada de sus paradas.
        """
        self._red = diccionario_lineas

    def crear_estaciones(self):
        """
        Transforma la visión de 'Líneas' a una visión de 'Estaciones'.
        Es fundamental para saber qué líneas pasan por cada parada (transbordos).
        """
        from estaciones import Estaciones  # Import local para evitar importación circular
        nodos = {}
        
        for nombre_linea, lista_paradas in self._red.items():
            for indice, nombre_estacion in enumerate(lista_paradas):
                # Si la estación no está en nuestro mapa de nodos, la añadimos
                if nombre_estacion not in nodos:
                    nodos[nombre_estacion] = {}
                
                # En cada estación, guardamos en qué líneas aparece y en qué posición (índice)
                # Esto es clave para la Línea 6, que puede pasar dos veces por la misma estación
                if nombre_linea not in nodos[nombre_estacion]:
                    nodos[nombre_estacion][nombre_linea] = []
                
                nodos[nombre_estacion][nombre_linea].append(indice)
        
        return Estaciones(nodos)

    def es_circular(self, nombre_linea: str) -> bool:
        """
        Verifica si una línea es un anillo cerrado.
        Condición: El primer y último elemento de la lista deben ser iguales.
        """
        if nombre_linea not in self._red:
            return False
        paradas = self._red[nombre_linea]
        return len(paradas) > 1 and paradas[0] == paradas[-1]

    def eliminar_linea(self, nombre_linea: str):
        """Elimina una línea completa del sistema."""
        if nombre_linea in self._red:
            del self._red[nombre_linea]

    def es_conexo(self) -> bool:
        """
        Comprueba si la red está totalmente unida.
        Usa BFS (Breadth-First Search) para intentar llegar de una estación 
        cualquiera a todas las demás. Si al final hemos visitado todas, es conexa.
        """
        if not self._red: return True
        
        # 1. Crear una lista de adyacencia (qué estación está pegada a cuál)
        adj = {}
        todas_estaciones = set()
        for paradas in self._red.values():
            for i in range(len(paradas)):
                todas_estaciones.add(paradas[i])
                if paradas[i] not in adj: adj[paradas[i]] = set()
                if i > 0: adj[paradas[i]].add(paradas[i-1]) # Conexión con la anterior
                if i < len(paradas) - 1: adj[paradas[i]].add(paradas[i+1]) # Conexión con la siguiente
        
        if not todas_estaciones: return True
        
        # 2. Algoritmo de exploración (BFS)
        inicio = next(iter(todas_estaciones))
        visitados = {inicio}
        cola = [inicio]
        
        while cola:
            actual = cola.pop(0)
            for vecino in adj.get(actual, []):
                if vecino not in visitados:
                    visitados.add(vecino)
                    cola.append(vecino)
        
        # Si el número de visitados coincide con el total, no hay islas aisladas
        return len(visitados) == len(todas_estaciones)
    
    def linea_mas_critica(self) -> dict:
        """
        Analiza qué línea causaría más daño si dejara de funcionar.
        Una estación queda aislada si esa línea es la ÚNICA que pasa por ella.
        """
        estaciones_obj = self.crear_estaciones()
        nodos = estaciones_obj._nodos
        estadisticas = []
        
        for nombre_linea, lista_paradas in self._red.items():
            paradas_unicas = set(lista_paradas)
            aisladas = 0
            
            for parada in paradas_unicas:
                # Si la estación solo tiene 1 línea, al quitarla, la estación muere
                if len(nodos[parada]) == 1:
                    aisladas += 1
            
            # Proporción: ¿Qué % de la línea depende exclusivamente de ella misma?
            proporcion = (aisladas / len(paradas_unicas)) * 100 if paradas_unicas else 0
            
            estadisticas.append({
                'linea': nombre_linea,
                'aisladas': aisladas,
                'proporcion': proporcion,
                'total_estaciones': len(paradas_unicas)
            })
            
        # Buscamos los peores casos
        max_absoluto = max(estadisticas, key=lambda x: x['aisladas'])
        max_proporcion = max(estadisticas, key=lambda x: x['proporcion'])
        
        return {'absoluto': max_absoluto, 'proporcional': max_proporcion}
    
    def buscar_ruta(self, origen: str, destino: str, max_transbordos: int = None) -> dict:
        """
        El algoritmo GPS del Metro.
        Encuentra el camino con menos paradas totales usando BFS.
        Posteriormente, calcula dónde se producen los transbordos.
        """
        estaciones_obj = self.crear_estaciones()
        nodos = estaciones_obj._nodos
        
        # Validaciones de seguridad
        if origen not in nodos or destino not in nodos:
            return {"error": "Estación no encontrada."}
        if origen == destino:
            return {"error": "Ya estás en el destino."}

        # Construcción del grafo de adyacencia para el buscador
        adj = {est: set() for est in nodos.keys()}
        for paradas in self._red.values():
            for i in range(len(paradas)):
                if i > 0: adj[paradas[i]].add(paradas[i-1])
                if i < len(paradas) - 1: adj[paradas[i]].add(paradas[i+1])

        # Búsqueda del camino más corto (BFS)
        cola = [[origen]]
        visitados = {origen}
        camino_final = []

        while cola:
            camino = cola.pop(0)
            nodo_actual = camino[-1]

            if nodo_actual == destino:
                camino_final = camino
                break

            for vecino in adj[nodo_actual]:
                if vecino not in visitados:
                    visitados.add(vecino)
                    nuevo_camino = list(camino) + [vecino]
                    cola.append(nuevo_camino)

        if not camino_final:
            return {"error": "No hay conexión."}

        # Lógica de transbordos: Comparar líneas de la estación actual vs la siguiente
        instrucciones = []
        linea_actual = None
        transbordos = 0

        for i in range(len(camino_final) - 1):
            est_actual = camino_final[i]
            est_siguiente = camino_final[i+1]
            
            lineas_en_comun = set(nodos[est_actual].keys()) & set(nodos[est_siguiente].keys())
            
            # Si podemos seguir en la misma línea, lo hacemos. Si no, transbordo.
            if linea_actual not in lineas_en_comun:
                linea_tomada = list(lineas_en_comun)[0] 
                if linea_actual is not None:
                    transbordos += 1
                    instrucciones.append(f"🔄 En '{est_actual}', haz transbordo a la {linea_tomada}")
                else:
                    instrucciones.append(f"🚇 Empieza en '{est_actual}' cogiendo la {linea_tomada}")
                linea_actual = linea_tomada

        instrucciones.append(f"🏁 Bájate en '{destino}'")

        # Filtro de transbordos opcional solicitado por el usuario
        if max_transbordos is not None and transbordos > max_transbordos:
            return {"error": f"Supera el límite de {max_transbordos} transbordos."}

        return {
            "camino": camino_final,
            "paradas_totales": len(camino_final) - 1,
            "transbordos": transbordos,
            "instrucciones": instrucciones
        }

    def __eq__(self, otro) -> bool:
        """Permite comparar si dos redes son idénticas."""
        if not isinstance(otro, Lineas): return False
        return self._red == otro._red