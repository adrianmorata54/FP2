from equipo import Equipo
from collections import defaultdict
import itertools

class Liga:
    """
    Clase principal que gestiona el histórico de todas las temporadas de LaLiga.
    Permite cargar datos y extraer estadísticas históricas, aplicando reglas 
    de negocio y filtros estadísticos específicos.
    """
    def __init__(self):
        # Estructura: self.historico[temporada][nombre_equipo] = Objeto Equipo
        self.historico = {}

    def agregar_registro(self, temporada, nombre_equipo, jugador):
        """Añade un jugador al equipo y temporada correspondientes."""
        if temporada not in self.historico:
            self.historico[temporada] = {}
        if nombre_equipo not in self.historico[temporada]:
            self.historico[temporada][nombre_equipo] = Equipo(nombre_equipo)
            
        self.historico[temporada][nombre_equipo].agregar_jugador(jugador)

    def _buscar_registros(self, nombre_jugador=None, nombre_equipo=None, temporada=None):
        """
        Método de utilidad para filtrar la base de datos.
        Devuelve una lista de tuplas: (temporada, equipo, Objeto_Jugador).
        Si no se pasan parámetros, devuelve el histórico completo.
        """
        resultados = []
        for temp_actual, equipos in self.historico.items():
            if temporada and temp_actual != temporada:
                continue
            for eq_nombre, equipo_obj in equipos.items():
                if nombre_equipo and nombre_equipo.upper() not in eq_nombre.upper():
                    continue
                
                if nombre_jugador:
                    for j in equipo_obj.jugadores:
                        if j.nombre.upper() == nombre_jugador.upper():
                            resultados.append((temp_actual, eq_nombre, j))
                            break
                else:
                    for j in equipo_obj.jugadores:
                        resultados.append((temp_actual, eq_nombre, j))
        return resultados

    def _extraer_anio_inicio(self, temporada):
        """Convierte el formato 'YYYY-YY' a un entero 'YYYY' para hacer comparaciones numéricas."""
        try:
            return int(str(temporada).split('-')[0])
        except:
            return 0

    # =========================================================
    # EJERCICIOS 1 al 6
    # =========================================================

    def estadisticas_jugador(self, nombre_jugador, temporada):
        """Busca a un jugador en una temporada específica y devuelve sus datos."""
        regs = self._buscar_registros(nombre_jugador=nombre_jugador, temporada=temporada)
        if regs:
            return f"{regs[0][2].nombre.upper()} ({regs[0][1]} - Temporada {regs[0][0]}) | Partidos: {regs[0][2].partidos} | Goles: {regs[0][2].goles}"
        return "Sin datos."

    def goles_totales(self, nombre_jugador):
        """Suma todos los goles de la carrera de un jugador."""
        regs = self._buscar_registros(nombre_jugador=nombre_jugador)
        if regs:
            total = sum(j.goles for _, _, j in regs)
            return f"{regs[0][2].nombre.upper()}: {int(total)} goles"
        return "Sin datos."

    def historial_equipos(self, nombre_jugador):
        """
        Devuelve los equipos por los que ha pasado un jugador, ordenados cronológicamente.
        """
        regs = self._buscar_registros(nombre_jugador=nombre_jugador)
        
        regs = [r for r in regs if r[2].partidos > 0] 
        
        if regs:
            regs_ordenados = sorted(regs, key=lambda x: self._extraer_anio_inicio(x[0]))
            equipos_unicos = list(dict.fromkeys(eq for _, eq, _ in regs_ordenados))
            nombre = regs[0][2].nombre.upper()
            return f"{nombre} - Equipos: {', '.join(equipos_unicos)}"
        return "Sin datos."
    
    def historial_equipos2(self, nombre_jugador):
        """
        Devuelve los equipos por los que ha pasado un jugador, ordenados cronológicamente. 
        (Filtramos solo los equipos donde haya metido gol)
        """
        regs = self._buscar_registros(nombre_jugador=nombre_jugador)
        
        regs = [r for r in regs if r[2].goles > 0] 
        
        if regs:
            regs_ordenados = sorted(regs, key=lambda x: self._extraer_anio_inicio(x[0]))
            equipos_unicos = list(dict.fromkeys(eq for _, eq, _ in regs_ordenados))
            nombre = regs[0][2].nombre.upper()
            return f"{nombre} - Equipos: {', '.join(equipos_unicos)}"
        return "Sin datos."

    def partidos_y_equipo_principal(self, nombre_jugador):
        """Encuentra el total de partidos de un jugador y determina en qué equipo jugó más."""
        regs = self._buscar_registros(nombre_jugador=nombre_jugador)
        if regs:
            total_partidos = sum(j.partidos for _, _, j in regs)
            conteo_eq = defaultdict(int)
            for _, eq, j in regs: 
                conteo_eq[eq] += j.partidos
            eq_principal = max(conteo_eq, key=conteo_eq.get)
            return f"{regs[0][2].nombre.upper()} - Equipo: {eq_principal}, Partidos: {int(total_partidos)}"
        return "Sin datos."

    def minutos_totales(self, nombre_jugador):
        """Suma el total de minutos jugados en la carrera."""
        regs = self._buscar_registros(nombre_jugador=nombre_jugador)
        if regs:
            total = sum(j.minutos for _, _, j in regs)
            return f"{regs[0][2].nombre.upper()} con {int(total)} minutos."
        return "Sin datos."

    # =========================================================
    # EJERCICIOS GLOBALES Y RANKINGS (7 al 16)
    # =========================================================

    def ranking_temporadas_seguidas(self, limite=5):
        """Encuentra la racha ininterrumpida más larga de temporadas disputadas en un mismo club."""
        todas_las_temporadas = sorted(list(set(temp for temp, _, _ in self._buscar_registros())))
        trayectorias = defaultdict(set)
        
        for temp, eq, j in self._buscar_registros():
            if j.partidos > 0:
                trayectorias[(j.nombre, eq)].add(temp)
        
        resultados = []
        for (jugador, equipo), temporadas_jugador in trayectorias.items():
            if not temporadas_jugador: continue
            
            indices = sorted([todas_las_temporadas.index(t) for t in temporadas_jugador])
            max_racha = racha_actual = 1
            for i in range(1, len(indices)):
                if indices[i] == indices[i-1] + 1:
                    racha_actual += 1
                else:
                    max_racha = max(max_racha, racha_actual)
                    racha_actual = 1
            max_racha = max(max_racha, racha_actual)
            resultados.append((max_racha, jugador, equipo))
                
        resultados.sort(key=lambda x: (-x[0], x[1]))
        return [f"{j} - Equipo: {e}, Temporadas seguidas: {r}" for r, j, e in resultados[:limite]]

    def ranking_minutos_juntos(self, limite=10):
        """Calcula qué pareja de jugadores ha coincidido más minutos sobre el campo."""
        plantillas = defaultdict(list)
        for temp, eq, j in self._buscar_registros():
            plantillas[(temp, eq)].append(j)
            
        parejas_minutos = defaultdict(int)
        for (temp, eq), jugadores in plantillas.items():
            for j1, j2 in itertools.combinations(jugadores, 2):
                pareja = tuple(sorted([j1.nombre, j2.nombre]))
                parejas_minutos[(pareja, eq)] += (j1.minutos + j2.minutos)
                
        resultados = [(mins, pareja, eq) for (pareja, eq), mins in parejas_minutos.items()]
        resultados.sort(reverse=True, key=lambda x: x[0])
        return [f"{p[0]} & {p[1]} - Equipo: {eq}, Minutos juntos: {int(m)}" for m, p, eq in resultados[:limite]]

    def ranking_partidos_completos(self, limite=3):
        """
        Busca a los jugadores que jugaron toda su etapa en un club sin ser sustituidos.
        Nota: Se filtra a partir de 1980 para excluir a los jugadores de la época clásica.
        """
        totales = defaultdict(lambda: {'partidos': 0, 'valido': True})
        for temp, _, j in self._buscar_registros():
            if self._extraer_anio_inicio(temp) >= 1980:
                totales[j.nombre]['partidos'] += j.partidos
                if j.partidos != j.pcompletos:
                    totales[j.nombre]['valido'] = False
        
        resultados = [(s['partidos'], j) for j, s in totales.items() if s['valido'] and s['partidos'] > 0]
        resultados.sort(key=lambda x: (-x[0], x[1]))
        return [f"- {j}: {int(p)} partidos enteros jugados." for p, j in resultados[:limite]]

    def ranking_equipos_tarjeteros_temporada(self, limite=5):
        """Suma de tarjetas (amarillas + rojas) de toda una plantilla en un año natural."""
        tarjetas = defaultdict(int)
        for temp, eq, j in self._buscar_registros():
            tarjetas[(eq, temp)] += (j.tarjetas + j.expulsiones)
        ordenado = sorted(tarjetas.items(), key=lambda x: x[1], reverse=True)
        return [f"- {eq} ({temp}): {int(t)} tarjetas conjuntas." for (eq, temp), t in ordenado[:limite]]
    
    def ranking_revulsivos(self, limite=3):
        """Mejores Revulsivos: Más partidos suplentes que titulares, >10 goles, ordenado por ratio Mins/Gol."""
        totales = defaultdict(lambda: {'goles': 0, 'minutos': 0, 'psuplente': 0, 'ptitular': 0})
        for _, _, j in self._buscar_registros():
            totales[j.nombre]['goles'] += j.goles
            totales[j.nombre]['minutos'] += j.minutos
            totales[j.nombre]['psuplente'] += j.psuplente
            totales[j.nombre]['ptitular'] += j.ptitular
            
        resultados = []
        for jugador, stats in totales.items():
            if stats['psuplente'] > stats['ptitular'] and stats['goles'] >= 10:
                ratio = stats['minutos'] / stats['goles']
                resultados.append((ratio, jugador, stats['goles']))
                
        resultados.sort(key=lambda x: x[0]) 
        return [f"- {j}: {int(g)} goles. Marca un gol cada {int(r)} minutos." for r, j, g in resultados[:limite]]

    def ranking_anios_en_activo(self, limite=5):
        """Calcula la longevidad de un jugador (Año final - Año inicial)."""
        trayectorias = defaultdict(list)
        for temp, _, j in self._buscar_registros():
            trayectorias[j.nombre].append(self._extraer_anio_inicio(temp))
            
        resultados = []
        for jugador, anios in trayectorias.items():
            if anios:
                anio_inicio = min(anios)
                anio_inicio_ultima_temp = max(anios)
                anios_activo = anio_inicio_ultima_temp - anio_inicio 
                
                if anios_activo >= 19: 
                    resultados.append((anios_activo, jugador, anio_inicio, anio_inicio_ultima_temp + 1))
                    
        resultados.sort(reverse=True, key=lambda x: x[0])
        return [f"- {j}: {a} años en activo (De {mn} a {mx})." for a, j, mn, mx in resultados[:limite]]

    def ranking_impolutos(self, limite=3):
        """
        Jugadores más limpios: 0 tarjetas en la etapa moderna (desde 1980).
        Se desempata a favor del que más minutos haya estado sobre el campo sin hacer falta.
        """
        totales = defaultdict(lambda: {'partidos': 0, 'minutos': 0, 'valido': True})
        for temp, _, j in self._buscar_registros():
            if self._extraer_anio_inicio(temp) >= 1980:
                totales[j.nombre]['partidos'] += j.partidos
                totales[j.nombre]['minutos'] += j.minutos
                if j.tarjetas > 0 or j.expulsiones > 0:
                    totales[j.nombre]['valido'] = False
                    
        resultados = [(s['partidos'], s['minutos'], j) for j, s in totales.items() if s['valido'] and s['partidos'] > 0]
        resultados.sort(key=lambda x: (-x[0], -x[1], x[2]))
        
        return [f"- {j}: {int(p)} partidos disputados de forma impoluta." for p, m, j in resultados[:limite]]

    def ranking_veces_cambiado(self, limite=3):
        """Veces sustituido: (Partidos como Titular) - (Partidos Completos)."""
        totales = defaultdict(int)
        for _, _, j in self._buscar_registros():
            sustituciones = j.ptitular - j.pcompletos
            if sustituciones > 0:
                totales[j.nombre] += sustituciones
                
        ordenado = sorted(totales.items(), key=lambda x: x[1], reverse=True)
        return [f"- {j}: Cambiado en {int(c)} ocasiones." for j, c in ordenado[:limite]]

    def ranking_goles_unica_temporada(self, limite=4):
        """'One Season Wonders': Anotaron todos los goles de su carrera en una sola temporada."""
        goles_por_jugador = defaultdict(lambda: defaultdict(int))
        for temp, _, j in self._buscar_registros():
            if j.goles > 0:
                goles_por_jugador[j.nombre][temp] += j.goles
                
        resultados = []
        for jugador, stats_temp in goles_por_jugador.items():
            if len(stats_temp) == 1: 
                temp_unica, goles = list(stats_temp.items())[0]
                if goles >= 16:
                    resultados.append((goles, jugador, temp_unica))
                    
        resultados.sort(reverse=True, key=lambda x: x[0])
        return [f"- {j}: {int(g)} goles. Todos anotados en la {t}." for g, j, t in resultados[:limite]]

    def ranking_ratio_goles_minutos(self, min_goles=50, limite=10):
        """Ratio Minutos/Gol para goleadores históricos (>=50 goles)."""
        totales = defaultdict(lambda: {'goles': 0, 'minutos': 0})
        for _, _, j in self._buscar_registros():
            if j.goles > 0 and j.minutos > 0:
                totales[j.nombre]['goles'] += j.goles
                totales[j.nombre]['minutos'] += j.minutos
            
        resultados = []
        for jugador, stats in totales.items():
            if stats['goles'] >= min_goles:
                ratio = stats['minutos'] / stats['goles']
                resultados.append((ratio, jugador, stats['goles']))
                
        resultados.sort(key=lambda x: x[0]) 
        return [f"- {j}: {int(g)} goles. Marca un gol cada {r:.1f} minutos." for r, j, g in resultados[:limite]]