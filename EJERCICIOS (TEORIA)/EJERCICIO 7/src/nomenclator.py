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
            d = {'Nombre': n.nombre, 'Genero': n.genero}
            
            for decada, (frec, pmil) in n.datos_por_decada.items():
                d[f"{decada}_Frec"] = frec
                d[f"{decada}_PMil"] = pmil
            filas.append(d)
            
        pd.DataFrame(filas).to_excel(ruta_salida, index=False)

    # --- PREGUNTA 2 ---
    def mayor_frecuencia_absoluta(self, genero: Optional[str] = None) -> str:
        """Devuelve el nombre con el número total más alto de personas registradas."""
        filtrados = self._filtrar(genero)
        if filtrados:
            return max(filtrados, key=lambda x: x.frecuencia_acumulada).nombre 
        return ""

    # --- PREGUNTA 3 ---
    def n_mas_usados(self, n: int, genero: Optional[str] = None) -> List[str]:
        """Devuelve el top 'n' de nombres más puestos en la historia."""
        ordenados = sorted(self._filtrar(genero), key=lambda x: x.frecuencia_acumulada, reverse=True)
        return [obj.nombre for obj in ordenados[:n]]

    # --- PREGUNTA 4 ---
    def frecuencia_por_inicial(self, genero: Optional[str] = None) -> Dict[str, List[Tuple[int, int]]]:
        """Calcula cuántas personas nacieron en cada década sumando por la inicial de su nombre."""
        res = {}
        for nom in self._filtrar(genero):
            ini = nom.nombre[0] 
            
            if ini not in res: 
                res[ini] = {d: 0 for d in self.decadas_ordenadas}
                
            for decada, (frec, _) in nom.datos_por_decada.items():
                res[ini][decada] += frec
                
        return {k: list(v.items()) for k, v in res.items()}

    # --- PREGUNTA 5 ---
    def letra_mas_frecuente_por_decada(self, genero: Optional[str] = None) -> Dict[int, Tuple[str, float]]:
        """Averigua qué letra inicial triunfó en cada década y qué porcentaje representaba."""
        frec_iniciales = self.frecuencia_por_inicial(genero)
        
        totales_decada = {d: 0 for d in self.decadas_ordenadas}
        max_letras = {d: {'letra': '', 'frec': -1} for d in self.decadas_ordenadas}
        
        for inicial, lista_datos in frec_iniciales.items():
            for decada, frec in lista_datos:
                totales_decada[decada] += frec
                if frec > max_letras[decada]['frec']:
                    max_letras[decada] = {'letra': inicial, 'frec': frec}
                    
        resultado = {}
        for d in self.decadas_ordenadas:
            if totales_decada[d] > 0:
                porcentaje = (max_letras[d]['frec'] / totales_decada[d]) * 100
                resultado[d] = (max_letras[d]['letra'], round(porcentaje, 2))
        return resultado

    # --- PREGUNTA 6 ---
    def evolucion_compuestos(self, genero: Optional[str] = None) -> List[Tuple[int, float, float]]:
        """Calcula el porcentaje de nombres simples frente a compuestos en cada década."""
        conteo = {d: {'simples': 0, 'compuestos': 0} for d in self.decadas_ordenadas}
        
        for nom in self._filtrar(genero):
            tipo = 'compuestos' if nom.es_compuesto else 'simples'
            for decada, (frec, _) in nom.datos_por_decada.items():
                conteo[decada][tipo] += frec
        
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
        longitudes = {d: [] for d in self.decadas_ordenadas}
        
        for nom in self._filtrar(genero):
            for decada in nom.datos_por_decada.keys():
                longitudes[decada].append(len(nom.nombre))
                
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
            if len(nom.datos_por_decada) >= n:
                res.append(nom.nombre)
        return res
    
    # =========================================================
    # EJERCICIOS BOLETÍN - SEMANA 2 (PREGUNTAS 9 A 15)
    # =========================================================

    # --- PREGUNTA 9 ---
    def de_moda_y_olvidados(self, n: int, genero: Optional[str] = None) -> List[str]:
        """Estuvieron de moda las 'n' primeras décadas o menos y luego desaparecieron para siempre."""
        res = []
        # Seleccionamos cuáles son las 'n' primeras décadas de la historia registrada
        primeras_decadas = self.decadas_ordenadas[:n]
        
        for nom in self._filtrar(genero):
            decadas_nom = list(nom.datos_por_decada.keys())
            if not decadas_nom: 
                continue
            
            # Comprobamos si TODAS las apariciones del nombre están dentro de esas primeras décadas
            if all(d in primeras_decadas for d in decadas_nom):
                res.append(nom.nombre)
        return res

    # --- PREGUNTA 10 ---
    def recientes_y_nuevos(self, n: int, genero: Optional[str] = None) -> List[str]:
        """Se han puesto de moda SOLO en las últimas 'n' décadas (antes no existían en el top)."""
        res = []
        # Seleccionamos las últimas 'n' décadas
        ultimas_decadas = self.decadas_ordenadas[-n:]
        
        for nom in self._filtrar(genero):
            decadas_nom = list(nom.datos_por_decada.keys())
            if not decadas_nom: 
                continue
            
            # Comprobamos si TODAS sus apariciones ocurren solo al final del histórico
            if all(d in ultimas_decadas for d in decadas_nom):
                res.append(nom.nombre)
        return res

    # --- PREGUNTA 11 ---
    def nombres_resurgidos(self, n: int, m: int, genero: Optional[str] = None) -> List[str]:
        """Estuvieron de moda 'n' décadas, desaparecieron 'm' décadas y volvieron a resurgir."""
        import re
        res = []
        # Truco profesional: Creamos una "línea temporal" de 1s (aparece) y 0s (no aparece).
        # Luego usamos una Expresión Regular para buscar el patrón exacto.
        # Patron: 'n' unos seguidos, 'm' ceros seguidos, y al menos un 1 al final.
        patron = re.compile(rf"1{{{n},}}0{{{m},}}1")
        
        for nom in self._filtrar(genero):
            # Generamos la línea temporal del nombre (Ej: "1110001")
            timeline = "".join(["1" if d in nom.datos_por_decada else "0" for d in self.decadas_ordenadas])
            
            # Si la línea temporal encaja con el patrón, lo guardamos
            if patron.search(timeline):
                res.append(nom.nombre)
        return res

    # --- PREGUNTA 12 ---
    def grafica_tendencia(self, lista_nombres: List[str]):
        """Dibuja una gráfica con la evolución del 'tanto por mil' de los nombres pedidos."""
        plt.figure(figsize=(10,5))
        for s in lista_nombres:
            if s in self.nombres:
                n = self.nombres[s]
                
                decadas_ordenadas = sorted(n.datos_por_decada.keys())
                
                x = decadas_ordenadas
                y = [n.datos_por_decada[d][1] for d in decadas_ordenadas]
                
                plt.plot(x, y, label=s, marker='o')
        
        plt.title("Tendencia de nombres a lo largo del tiempo")
        plt.xlabel("Décadas")
        plt.ylabel("Tanto por mil")
        plt.legend()
        plt.grid()
        plt.show()

    # --- PREGUNTA 13 ---
    def mayor_incremento_absoluto(self, n: int, genero: Optional[str] = None) -> List[str]:
        """Devuelve los 'n' nombres con la mayor subida de tanto por mil de una década a la siguiente."""
        incrementos = []
        
        for nom in self._filtrar(genero):
            decadas_nom = sorted(nom.datos_por_decada.keys())
            max_inc = 0
            
            # Comparamos cada década en la que aparece con la siguiente
            for i in range(len(decadas_nom) - 1):
                d1 = decadas_nom[i]
                d2 = decadas_nom[i+1]
                
                # Verificamos que sean décadas consecutivas temporalmente (que no haya saltos)
                idx1 = self.decadas_ordenadas.index(d1)
                idx2 = self.decadas_ordenadas.index(d2)
                
                if idx2 - idx1 == 1: # Son consecutivas
                    # Restamos el tanto por mil de la segunda década menos el de la primera
                    inc = nom.datos_por_decada[d2][1] - nom.datos_por_decada[d1][1]
                    if inc > max_inc:
                        max_inc = inc
                        
            if max_inc > 0:
                incrementos.append((nom.nombre, max_inc))
                
        # Ordenamos por el incremento (de mayor a menor) y nos quedamos con los nombres
        incrementos.sort(key=lambda x: x[1], reverse=True)
        return [x[0] for x in incrementos[:n]]

    # --- PREGUNTA 14 ---
    def diversificacion_nombres(self, n: int, genero: Optional[str] = None) -> Dict[int, float]:
        """Calcula, para cada década, la suma de los 'tanto por mil' de los 'n' nombres más comunes."""
        # Agrupamos todos los tanto por mil registrados en cada década
        pmil_por_decada = {d: [] for d in self.decadas_ordenadas}
        
        for nom in self._filtrar(genero):
            for decada, (_, pmil) in nom.datos_por_decada.items():
                pmil_por_decada[decada].append(pmil)
                
        dict_diversificacion = {}
        for d in self.decadas_ordenadas:
            # Ordenamos de mayor a menor, cogemos los 'n' primeros y los sumamos
            top_n = sorted(pmil_por_decada[d], reverse=True)[:n]
            dict_diversificacion[d] = round(sum(top_n), 2)
            
        return dict_diversificacion

    # --- PREGUNTA 15 ---
    def grafica_diversificacion(self, n: int, genero: Optional[str] = None):
        """Dibuja una gráfica basada en los datos de diversificación."""
        datos = self.diversificacion_nombres(n, genero)
        x = list(datos.keys())
        y = list(datos.values())
        
        plt.figure(figsize=(10, 5))
        plt.plot(x, y, marker='s', color='purple', linestyle='--')
        plt.title(f"Diversificación: Suma del tanto por mil de los {n} nombres más comunes")
        plt.xlabel("Décadas")
        plt.ylabel("Suma del Tanto por Mil")
        plt.grid()
        plt.show()