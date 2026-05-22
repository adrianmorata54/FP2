from typing import Dict, List, Tuple, NamedTuple

# Clases auxiliares
class Usuario:
    def __init__(self, nombre: str):
        self.nombre = nombre
        
    def __repr__(self):
        return f"Usuario('{self.nombre}')"
        
    def __hash__(self):
        return hash(self.nombre)
        
    def __eq__(self, other):
        return isinstance(other, Usuario) and self.nombre == other.nombre

# Canción es una tupla (NamedTuple nos permite acceder a cancion.titulo, etc.)
class Cancion(NamedTuple):
    titulo: str
    genero: str
    duracion: float


class FPtify:
    def __init__(self, datos: Dict[Usuario, List[Cancion]]):
        # El diccionario asocia cada usuario a la lista de TODAS las canciones que ha escuchado.
        # ¡Ojo! Las canciones pueden estar repetidas en la lista si las ha escuchado varias veces.
        self.datos = datos

    # 1. Devuelve minutos totales escuchados por cada usuario
    def minutos_totales_por_usuario(self) -> Dict[Usuario, float]:
        dict_final = {}
        for usuario, canciones in self.datos.items():
            dict_final[usuario] = sum(cancion.duracion for cancion in canciones)
        return dict_final

    # 2. Dado el título de una canción, devuelve la lista de usuarios que la han escuchado (sin duplicados)
    def oyentes_por_cancion(self, titulo_cancion: str) -> List[Usuario]:
        oyentes = []
        for usuario, canciones in self.datos.items():
            titulos_canciones = list(cancion.titulo for cancion in canciones)
            if titulo_cancion in titulos_canciones:
                oyentes.append(usuario)
        return oyentes

    # 3. Devuelve los minutos totales acumulados para cada género musical (sumando los de todos los usuarios)
    def minutos_por_genero(self) -> Dict[str, float]:
        dict_final = {}
        for canciones_usuario in self.datos.values():
            for cancion in canciones_usuario:
                if cancion.genero not in dict_final:
                    dict_final[cancion.genero] = 0
                dict_final[cancion.genero] += cancion.duracion
        return dict_final


    # 4. Devuelve el género musical que más minutos ha escuchado cada usuario
    def genero_mas_escuchado_por_usuario(self) -> Dict[Usuario, str]:
        dict_final = {}
        for usuario, canciones in self.datos.items():
            dict_genero = {}
            for cancion in canciones:
                if cancion.genero not in dict_genero:
                    dict_genero[cancion.genero] = 0
                dict_genero[cancion.genero] += cancion.duracion
            dict_final[usuario] = max(dict_genero.items(), key=lambda x:x[1])[0]
        return dict_final


    # 5. Devuelve los 'n' usuarios con más minutos consumidos, ordenados de mayor a menor
    def top_n_usuarios_minutos(self, n: int) -> List[Tuple[Usuario, float]]:
        dict_minutos = self.minutos_totales_por_usuario()
        lista_final = list(dict_minutos.items())
        return sorted(lista_final, key=lambda x: x[1], reverse=True)[:n]


    # 6. Devuelve una lista ordenada alfabéticamente de los distintos géneros escuchados por cada usuario
    def generos_distintos_por_usuario(self) -> Dict[Usuario, List[str]]:
        dict_final = {}
        for usuario, canciones in self.datos.items():
            generos = set(cancion.genero for cancion in canciones)
            dict_final[usuario] = sorted(list(generos))
        return dict_final


    # 7. Devuelve qué usuario ha escuchado más minutos para cada género
    def usuario_mas_minutos_por_genero(self) -> Dict[str, Usuario]:
        dict_final = {}
        generos = self.minutos_por_genero().keys()
        for genero in generos:
            dict_genero = {}
            for usuario, canciones in self.datos.items():
                dict_genero[usuario] = sum(cancion.duracion for cancion in canciones if cancion.genero == genero)
            dict_final[genero] = max(dict_genero.items(), key=lambda x: x[1])[0]
        return dict_final
                

    # 8. Devuelve las 'n' canciones más escuchadas por cada usuario (ordenadas por nº de escuchas)
    def top_n_canciones_por_usuario(self, n: int) -> Dict[Usuario, List[Tuple[Cancion, int]]]:
        dict_final = {}
        for usuario, canciones in self.datos.items():
            dict_escuchas = {}
            for cancion in canciones:
                if cancion not in dict_escuchas:
                    dict_escuchas[cancion] = 0
                dict_escuchas[cancion] += 1
            dict_final[usuario] = sorted(dict_escuchas.items(), key=lambda x:x[1], reverse=True)[:n]
        return dict_final

    # 9. Devuelve las 'n' canciones más escuchadas de toda la plataforma (ordenadas por nº de escuchas)
    def top_n_canciones_plataforma(self, n: int) -> List[Tuple[Cancion, int]]:
        dict_escuchas = {}
        for canciones in self.datos.values():
            for cancion in canciones:
                if cancion not in dict_escuchas:
                    dict_escuchas[cancion] = 0
                dict_escuchas[cancion] += 1
        return sorted(dict_escuchas.items(), key=lambda x:x[1], reverse=True)[:n]

    # 10. Dado un usuario, devuelve el usuario con el gusto musical más parecido 
    # (el que comparte más canciones DISTINTAS escuchadas en común)
    def usuario_mas_parecido(self, usuario_dado: Usuario) -> Usuario:
        dict_canciones = {}
        canciones_usuario_dado = set(self.datos[usuario_dado])
        for usuario, canciones in self.datos.items():
            if usuario != usuario_dado:
                canciones_usuario = set(canciones)
                n_canciones_en_comun = len(canciones_usuario_dado.intersection(canciones_usuario))
                dict_canciones[usuario] = n_canciones_en_comun
        return max(dict_canciones.items(), key=lambda x:x[1])[0]



# ==========================================
# DATOS DE PRUEBA (Para que compruebes tu código)
# ==========================================
if __name__ == "__main__":
    # Creamos usuarios
    u1 = Usuario("Ana")
    u2 = Usuario("Luis")
    u3 = Usuario("Marta")

    # Creamos algunas canciones
    c1 = Cancion("Bohemian Rhapsody", "Rock", 5.5)
    c2 = Cancion("Despacito", "Pop", 3.5)
    c3 = Cancion("Hotel California", "Rock", 6.0)
    c4 = Cancion("Shape of You", "Pop", 4.0)

    # Creamos el diccionario de datos (fíjate que hay canciones repetidas)
    datos_prueba = {
        u1: [c1, c1, c3],           # Ana escucha 2 veces c1 y 1 vez c3 (Todo Rock)
        u2: [c2, c4, c2, c2],       # Luis escucha 3 veces c2 y 1 vez c4 (Todo Pop)
        u3: [c1, c4, c4, c3]        # Marta escucha c1, c3 (Rock) y c4 dos veces (Pop)
    }

    fptify = FPtify(datos_prueba)

    # Ejemplos para probar:
    # print("1. Minutos por usuario:")
    # print(fptify.minutos_totales_por_usuario())
    
    # print("\n2. Oyentes de 'Bohemian Rhapsody':")
    # print(fptify.oyentes_por_cancion("Bohemian Rhapsody"))