import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Tuple, Optional
from nombre import Nombre

class Nomenclator:
    # =========================================================
    # 0. INICIALIZACIÓN Y MÉTODOS DE APOYO (USO INTERNO)
    # =========================================================
    def __init__(self):
        """Prepara el objeto para guardar los datos al leer el Excel."""
        self.nombres: Dict[str, Nombre] = {}
        self.decadas_ordenadas: List[int] = []

    def _filtrar(self, genero: Optional[str]) -> List[Nombre]:
        """
        Método 'privado' (por el guion bajo) que usan los demás métodos.
        Si le pasas un género ('H' o 'M'), te devuelve solo esos nombres. 
        Si le pasas None, te devuelve todos.
        """
        if genero:
            return [n for n in self.nombres.values() if n.genero == genero]
        return list(self.nombres.values())


    # =========================================================
    # EJERCICIOS BOLETÍN - SEMANA 1 (PREGUNTAS 1 A 8)
    # =========================================================

    # --- PREGUNTA 1 ---
    def exportar_a_excel(self, ruta_salida: str):
        """Exporta todos los datos guardados en la clase a un nuevo archivo Excel."""
        filas = []
        for n in self.nombres.values():
            # Creamos la base de la fila con el nombre y su género
            d = {'Nombre': n.nombre, 'Genero': n.genero}
            
            # Añadimos dinámicamente las columnas de cada década
            for decada, (frec, pmil) in n.datos_por_decada.items():
                d[f"{decada}_Frec"] = frec
                d[f"{decada}_PMil"] = pmil
            filas.append(d)
            
        # Convertimos la lista de diccionarios a un DataFrame de pandas y lo guardamos
        pd.DataFrame(filas).to_excel(ruta_salida, index=False)

    # --- PREGUNTA 2 ---
    def mayor_frecuencia_absoluta(self, genero: Optional[str] = None) -> str:
        """Devuelve el nombre con el número total más alto de personas registradas."""
        filtrados = self._filtrar(genero)
        # La función max busca el objeto con la 'frecuencia_acumulada' más alta
        if filtrados:
            return max(filtrados, key=lambda x: x.frecuencia_acumulada).nombre 
        return ""

    # --- PREGUNTA 3 ---
    def n_mas_usados(self, n: int, genero: Optional[str] = None) -> List[str]:
        """Devuelve el top 'n' de nombres más puestos en la historia."""
        # Ordenamos de mayor a menor (reverse=True) según la frecuencia acumulada
        ordenados = sorted(self._filtrar(genero), key=lambda x: x.frecuencia_acumulada, reverse=True)
        # Extraemos solo la palabra (el nombre) de los primeros 'n' objetos
        return [obj.nombre for obj in ordenados[:n]]

    # --- PREGUNTA 4 ---
    def frecuencia_por_inicial(self, genero: Optional[str] = None) -> Dict[str, List[Tuple[int, int]]]:
        """Calcula cuántas personas nacieron en cada década sumando por la inicial de su nombre."""
        res = {}
        for nom in self._filtrar(genero):
            ini = nom.nombre[0] # Cogemos la primera letra del nombre
            
            # Si la letra no está registrada, le creamos su plantilla de décadas a cero
            if ini not in res: 
                res[ini] = {d: 0 for d in self.decadas_ordenadas}
                
            # Sumamos las frecuencias a la década correspondiente de esa inicial
            for decada, (frec, _) in nom.datos_por_decada.items():
                res[ini][decada] += frec
                
        # Transformamos el diccionario interno en listas de tuplas (como pide el boletín)
        return {k: list(v.items()) for k, v in res.items()}

    # --- PREGUNTA 5 ---
    def letra_mas_frecuente_por_decada(self, genero: Optional[str] = None) -> Dict[int, Tuple[str, float]]:
        """Averigua qué letra inicial triunfó en cada década y qué porcentaje representaba."""
        frec_iniciales = self.frecuencia_por_inicial(genero)
        
        # Diccionarios para llevar la cuenta de los totales y la letra ganadora
        totales_decada = {d: 0 for d in self.decadas_ordenadas}
        max_letras = {d: {'letra': '', 'frec': -1} for d in self.decadas_ordenadas}
        
        for inicial, lista_datos in frec_iniciales.items():
            for decada, frec in lista_datos:
                totales_decada[decada] += frec # Sumamos para saber el total de nacidos en la década
                # Si esta letra tiene más frecuencia que la actual ganadora, la sustituimos
                if frec > max_letras[decada]['frec']:
                    max_letras[decada] = {'letra': inicial, 'frec': frec}
                    
        # Calculamos el porcentaje final
        resultado = {}
        for d in self.decadas_ordenadas:
            if totales_decada[d] > 0:
                porcentaje = (max_letras[d]['frec'] / totales_decada[d]) * 100
                resultado[d] = (max_letras[d]['letra'], round(porcentaje, 2))
        return resultado

    # --- PREGUNTA 6 ---
    def evolucion_compuestos(self, genero: Optional[str] = None) -> List[Tuple[int, float, float]]:
        """Calcula el porcentaje de nombres simples frente a compuestos en cada década."""
        # Plantilla para contar simples y compuestos por década
        conteo = {d: {'simples': 0, 'compuestos': 0} for d in self.decadas_ordenadas}
        
        for nom in self._filtrar(genero):
            tipo = 'compuestos' if nom.es_compuesto else 'simples'
            for decada, (frec, _) in nom.datos_por_decada.items():
                conteo[decada][tipo] += frec
        
        # Convertir a porcentajes y agrupar en tuplas
        evolucion = []
        for d in self.decadas_ordenadas:
            total = conteo[d]['simples'] + conteo[d]['compuestos']
            if total > 0:
                pct_simples = (conteo[d]['simples'] / total) * 100
                pct_compuestos = (conteo[d]['compuestos'] / total) * 100
                evolucion.append((d, round(pct_simples, 2), round(pct_compuestos, 2)))
        return evolucion

    # --- PREGUNTA 7 ---
    def longitud_media_por_decada(self, genero: Optional[str] = None) -> List[Tuple[int, float]]:
        """Calcula la media de letras que tienen los nombres en cada época."""
        # Un diccionario para guardar todas las longitudes medidas en cada década
        longitudes = {d: [] for d in self.decadas_ordenadas}
        
        for nom in self._filtrar(genero):
            for decada in nom.datos_por_decada.keys():
                longitudes[decada].append(len(nom.nombre))
                
        # Sacamos la media (Suma de longitudes / Cantidad de nombres medidos)
        resultado = []
        for d in self.decadas_ordenadas:
            if longitudes[d]:
                media = sum(longitudes[d]) / len(longitudes[d])
                resultado.append((d, round(media, 2)))
        return resultado
    
    # --- PREGUNTA 8 ---
    def en_top_n_decadas(self, n: int, genero: Optional[str] = None) -> List[str]:
        """Devuelve los nombres clásicos que han estado 'n' décadas o más en el histórico."""
        res = []
        for nom in self._filtrar(genero):
            # Si el tamaño de su diccionario es mayor o igual a 'n', significa que sobrevivió 'n' décadas
            if len(nom.datos_por_decada) >= n:
                res.append(nom.nombre)
        return res

    # =========================================================
    # PREPARATIVOS PARA SEMANA 2 (MÉTODOS GRÁFICOS Y EXTRAS)
    # =========================================================
    def grafica_tendencia(self, lista_nombres: List[str]):
        """Dibuja una gráfica con la evolución del 'tanto por mil' de los nombres pedidos."""
        plt.figure(figsize=(10,5))
        for s in lista_nombres:
            if s in self.nombres:
                n = self.nombres[s]
                # Eje X (décadas) y Eje Y (tanto por mil, que es el segundo valor de la tupla)
                x = list(n.datos_por_decada.keys())
                y = [pmil for _, pmil in n.datos_por_decada.values()]
                plt.plot(x, y, label=s, marker='o')
        
        plt.legend()
        plt.grid()
        plt.show()