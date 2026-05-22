from typing import Dict, List, Tuple

# Clases auxiliares ya construidas
class Temporada:
    def __init__(self, anio: int):
        self.anio = anio
        
    def __repr__(self):
        return f"Temporada({self.anio})"
        
    # Necesario para usar la clase como clave de un diccionario
    def __hash__(self):
        return hash(self.anio)
        
    def __eq__(self, other):
        return isinstance(other, Temporada) and self.anio == other.anio
        
    # Útil para el método 10 (ordenar temporadas)
    def __lt__(self, other):
        return self.anio < other.anio

class Equipo:
    def __init__(self, nombre: str):
        self.nombre = nombre
        
    def __repr__(self):
        return f"Equipo('{self.nombre}')"
        
    # Necesario para usar la clase como clave de un diccionario
    def __hash__(self):
        return hash(self.nombre)
        
    def __eq__(self, other):
        return isinstance(other, Equipo) and self.nombre == other.nombre


class Futbol:
    def __init__(self, datos: Dict[Temporada, Dict[Equipo, int]]):
        self.datos = datos

    # 1. Método que devuelve un diccionario agrupado por Equipo
    def agrupar_por_equipo(self) -> Dict[Equipo, Dict[Temporada, int]]:
        dict_final = {}
        for temporada, equipos_dict in self.datos.items():
            for equipo, goles in equipos_dict.items():
                if equipo not in dict_final:
                    dict_final[equipo] = {}
                dict_final[equipo][temporada] = goles
        return dict_final

    # 2. Método que devuelve la suma total de goles por equipo
    def goles_totales_por_equipo(self) -> Dict[Equipo, int]:
        dict_goles = {}
        for temporada, equipos_dict in self.datos.items():
            for equipo, goles in equipos_dict.items():
                if equipo not in dict_goles:
                    dict_goles[equipo] = 0
                dict_goles[equipo] += goles
        return dict_goles


    # 3. Método que devuelve la Temporada con más goles en total
    def temporada_mas_goles(self) -> Temporada:
        temporadas_goles = []
        for temporada, equipos_dict in self.datos.items():
            total = 0
            for equipo, goles in equipos_dict.items():
                total += goles
            temporadas_goles.append((temporada, total))
        return max(temporadas_goles, key=lambda x:x[1])[0]
        

    # 4. Método que devuelve para cada temporada una lista ordenada de equipos y sus goles
    def clasificacion_por_temporada(self) -> Dict[Temporada, List[Tuple[Equipo, int]]]:
        dict_final = {}
        for temporada, equipos_dict in self.datos.items():
            if temporada not in dict_final:
                dict_final[temporada] = []
            for equipo, goles in equipos_dict.items():
                dict_final[temporada].append((equipo, goles))
            dict_final[temporada].sort(key= lambda x:x[1])
        return dict_final


    # 5. Método que devuelve equipos que marcaron más de n goles en una temporada
    def equipos_goleadores(self, n: int) -> List[Tuple[Equipo, Temporada]]:
        lista_goleadores = []
        for temporada, equipos_dict in self.datos.items():
            for equipo, goles in equipos_dict.items():
                if goles > n:
                    lista_goleadores.append((equipo, temporada))
        return lista_goleadores

    # 6. Método que devuelve cuántas temporadas ha disputado cada equipo
    def temporadas_disputadas_por_equipo(self) -> Dict[Equipo, int]:
        dict_temp = {}
        for temporada, equipos_dict in self.datos.items():
            for equipo, _ in equipos_dict.items():
                if equipo not in dict_temp:
                    dict_temp[equipo] = 0
                dict_temp[equipo] += 1
        return dict_temp

    # 7. Método que devuelve la media de goles de cada equipo en el total de temporadas
    def media_goles_por_equipo(self) -> Dict[Equipo, float]:
        dict_datos = {}
        for temporada, equipos_dict in self.datos.items():
            for equipo, goles in equipos_dict.items():
                if equipo not in dict_datos:
                    dict_datos[equipo] = {'total_temporadas': 0, 'total_goles': 0}
                dict_datos[equipo]['total_temporadas'] +=1
                dict_datos[equipo]['total_goles'] += goles
        dict_final = {}
        for equipo, datos in dict_datos.items():
            dict_final[equipo] = datos['total_goles']/datos['total_temporadas']
        return dict_final



    # 8. Método que devuelve el porcentaje de goles de cada equipo sobre el total de la temporada
    def porcentaje_goles_por_temporada(self) -> Dict[Temporada, Dict[Equipo, float]]:
        dict_final = {}
        for temporada, equipos_dict in self.datos.items():
            if temporada not in dict_final:
                dict_final[temporada] = {}
            total_goles_temp = sum(equipos_dict.values())
            for equipo, goles in equipos_dict.items():
                dict_final[temporada][equipo] = (goles/total_goles_temp)*100
        return dict_final
            

    # 9. Método que devuelve el equipo máximo goleador de cada temporada
    def pichichi_por_temporada(self) -> Dict[Temporada, Equipo]:
        dict_final = {}
        for temporada, equipos_dict in self.datos.items():
            equipo_goleador = None
            top_goles = 0
            for equipo, goles in equipos_dict.items():
                if goles > top_goles:
                    top_goles = goles
                    equipo_goleador = equipo
            dict_final[temporada] = equipo_goleador
        return dict_final


    # 10. Método que devuelve las temporadas en las que cada equipo descendió
    def temporadas_descenso(self) -> Dict[Equipo, List[Temporada]]:
        dict_final = {}
        lista_temporadas = sorted(self.datos.keys())
        for i in range(len(lista_temporadas)-1):
            for equipo, _ in self.datos[lista_temporadas[i]].items():
                if equipo not in dict_final:
                    dict_final[equipo] = []
                if equipo in self.datos[lista_temporadas[i]] and equipo not in self.datos[lista_temporadas[i+1]]:
                    dict_final[equipo].append(lista_temporadas[i])
        return dict_final
            

# ==========================================
# DATOS DE PRUEBA (Para que compruebes tu código)
# ==========================================
if __name__ == "__main__":
    t1 = Temporada(2021)
    t2 = Temporada(2022)
    t3 = Temporada(2023)

    eqA = Equipo("Betis")
    eqB = Equipo("Sevilla")
    eqC = Equipo("Cadiz")

    datos_prueba = {
        t1: {eqA: 50, eqB: 45, eqC: 30},  # En 2021 juegan los tres
        t2: {eqA: 55, eqB: 60},           # En 2022 el Cadiz no está (descendió en 2021)
        t3: {eqA: 40, eqB: 35, eqC: 25}   # En 2023 vuelve el Cadiz
    }

    liga = Futbol(datos_prueba)

    # Ejemplo de cómo probar un método una vez lo programes:
    print("1. Agrupado por equipo:")
    print(liga.agrupar_por_equipo())