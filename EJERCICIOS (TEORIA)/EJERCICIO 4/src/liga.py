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
        # Estructura principal: self.historico[temporada][nombre_equipo] = Objeto Equipo
        self.historico = {}

    # =========================================================
    # MÉTODOS DE INSERCIÓN Y UTILIDAD (PRIVADOS/INTERNOS)
    # =========================================================

    def agregar_registro(self, temporada, nombre_equipo, jugador):
        """Añade un jugador al equipo y temporada correspondientes."""
        if temporada not in self.historico:
            self.historico[temporada] = {}
            
        if nombre_equipo not in self.historico[temporada]:
            self.historico[temporada][nombre_equipo] = Equipo(nombre_equipo)
            
        self.historico[temporada][nombre_equipo].agregar_jugador(jugador)

    def _buscar_registros(self, nombre_jugador=None, nombre_equipo=None, temporada=None):
        """
        Método de utilidad para filtrar la base de datos completa.
        Devuelve una lista de tuplas: (temporada, equipo, Objeto_Jugador).
        Si no se pasan parámetros, devuelve el histórico completo.
        """
        resultados = []
        for temp_actual, equipos in self.historico.items():
            # Filtro por temporada
            if temporada and temp_actual != temporada:
                continue
                
            for eq_nombre, equipo_obj in equipos.items():
                # Filtro por nombre de equipo
                if nombre_equipo and nombre_equipo.upper() not in eq_nombre.upper():
                    continue
                
                # Filtro por jugador
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
        except (ValueError, AttributeError):
            return 0

    def _goles_historicos_equipos(self):
        """
        Suma todos los goles anotados por todos los jugadores de un club en la historia.
        Devuelve una lista de tuplas ordenadas de mayor a menor cantidad de goles.
        """
        goles = defaultdict(int)
        for _, eq_nombre, j in self._buscar_registros():
            goles[eq_nombre] += j.goles
        return sorted(goles.items(), key=lambda x: x[1], reverse=True)

    def _calcular_descensos_y_ascensos(self):
        """
        Calcula matemáticamente los ascensos y descensos comparando los equipos 
        de una temporada con los de la siguiente.
        """
        temporadas = sorted(self.historico.keys(), key=self._extraer_anio_inicio)
        descensos_temp, ascensos_temp = {}, {}
        conteo_desc, conteo_asc = defaultdict(int), defaultdict(int)
        
        for i in range(len(temporadas) - 1):
            temp_actual = temporadas[i]
            temp_sig = temporadas[i+1]
            
            eq_actual = set(self.historico[temp_actual].keys())
            eq_sig = set(self.historico[temp_sig].keys())
            
            # Equipos que estaban y ya no están = Descendidos
            descendidos = eq_actual - eq_sig
            if descendidos:
                descensos_temp[temp_actual] = sorted(list(descendidos))
                for eq in descendidos: 
                    conteo_desc[eq] += 1
                
            # Equipos que no estaban y ahora están = Ascendidos
            ascendidos = eq_sig - eq_actual
            # Evitamos la temporada post Guerra Civil por anomalías en los ascensos
            if ascendidos and temp_sig != "1939-40":
                ascensos_temp[temp_sig] = sorted(list(ascendidos))
                for eq in ascendidos: 
                    conteo_asc[eq] += 1
                
        return descensos_temp, conteo_desc, ascensos_temp, conteo_asc

    def _conteo_temporadas_equipos(self):
        """Cuenta el número total de temporadas que ha disputado cada equipo en Primera."""
        conteo = defaultdict(int)
        for temp, equipos in self.historico.items():
            for eq in equipos.keys():
                conteo[eq] += 1
        return sorted(conteo.items(), key=lambda x: x[1], reverse=True)

    def _maximos_goleadores_por_temporada(self):
        """Calcula qué equipo marcó más goles en cada temporada histórica."""
        ganadores_temp = {}
        for temp, equipos in self.historico.items():
            goles_eq = {eq: sum(j.goles for j in obj.jugadores) for eq, obj in equipos.items()}
            if goles_eq:
                max_goles = max(goles_eq.values())
                # En caso de empate, guardamos todos los equipos con ese máximo
                ganadores_temp[temp] = [eq for eq, g in goles_eq.items() if g == max_goles]
        return ganadores_temp

    # =========================================================
    # EJERCICIOS 1 al 6 (Estadísticas Individuales Básicas)
    # =========================================================

    def estadisticas_jugador(self, nombre_jugador, temporada):
        """Busca a un jugador en una temporada específica y devuelve sus datos básicos."""
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
        """Devuelve los equipos por los que ha pasado un jugador, ordenados cronológicamente."""
        regs = self._buscar_registros(nombre_jugador=nombre_jugador)
        regs = [r for r in regs if r[2].partidos > 0] 
        
        if regs:
            regs_ordenados = sorted(regs, key=lambda x: self._extraer_anio_inicio(x[0]))
            # Mantenemos el orden preservando la unicidad
            equipos_unicos = list(dict.fromkeys(eq for _, eq, _ in regs_ordenados))
            nombre = regs[0][2].nombre.upper()
            return f"{nombre} - Equipos: {', '.join(equipos_unicos)}"
        return "Sin datos."
    
    def historial_equipos2(self, nombre_jugador):
        """
        Devuelve los equipos por los que ha pasado un jugador, ordenados cronológicamente. 
        A diferencia del método anterior, filtra solo los equipos donde haya marcado al menos un gol.
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
        """Suma el total de minutos jugados a lo largo de la carrera del jugador."""
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
            if not temporadas_jugador: 
                continue
            
            # Buscamos índices consecutivos en la lista cronológica de todas las temporadas
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
            # Generamos todas las combinaciones posibles de 2 jugadores en el equipo
            for j1, j2 in itertools.combinations(jugadores, 2):
                pareja = tuple(sorted([j1.nombre, j2.nombre]))
                parejas_minutos[(pareja, eq)] += (j1.minutos + j2.minutos)
                
        resultados = [(mins, pareja, eq) for (pareja, eq), mins in parejas_minutos.items()]
        resultados.sort(reverse=True, key=lambda x: x[0])
        
        return [f"{p[0]} & {p[1]} - Equipo: {eq}, Minutos juntos: {int(m)}" for m, p, eq in resultados[:limite]]

    def ranking_partidos_completos(self, limite=3):
        """
        Busca a los jugadores que jugaron toda su etapa en un club sin ser sustituidos.
        Nota: Se filtra a partir de 1980 para excluir a los jugadores de la época clásica
        donde no existían las sustituciones.
        """
        totales = defaultdict(lambda: {'partidos': 0, 'valido': True})
        for temp, _, j in self._buscar_registros():
            if self._extraer_anio_inicio(temp) >= 1980:
                totales[j.nombre]['partidos'] += j.partidos
                # Si algún partido no fue completo, se invalida para el ranking
                if j.partidos != j.pcompletos:
                    totales[j.nombre]['valido'] = False
        
        resultados = [(s['partidos'], j) for j, s in totales.items() if s['valido'] and s['partidos'] > 0]
        resultados.sort(key=lambda x: (-x[0], x[1]))
        
        return [f"- {j}: {int(p)} partidos enteros jugados." for p, j in resultados[:limite]]

    def ranking_equipos_tarjeteros_temporada(self, limite=5):
        """Suma de tarjetas (amarillas + rojas) de toda una plantilla en una sola temporada."""
        tarjetas = defaultdict(int)
        for temp, eq, j in self._buscar_registros():
            tarjetas[(eq, temp)] += (j.tarjetas + j.expulsiones)
            
        ordenado = sorted(tarjetas.items(), key=lambda x: x[1], reverse=True)
        return [f"- {eq} ({temp}): {int(t)} tarjetas conjuntas." for (eq, temp), t in ordenado[:limite]]
    
    def ranking_revulsivos(self, limite=3):
        """
        Mejores Revulsivos: Jugadores con más partidos suplentes que titulares, 
        que han marcado >=10 goles, ordenados por mejor ratio Mins/Gol.
        """
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
        """Calcula la longevidad de un jugador (Diferencia entre su última y su primera temporada)."""
        trayectorias = defaultdict(list)
        for temp, _, j in self._buscar_registros():
            trayectorias[j.nombre].append(self._extraer_anio_inicio(temp))
            
        resultados = []
        for jugador, anios in trayectorias.items():
            if anios:
                anio_inicio = min(anios)
                anio_inicio_ultima_temp = max(anios)
                anios_activo = anio_inicio_ultima_temp - anio_inicio 
                
                # Filtramos por carreras muy longevas (>=19 años)
                if anios_activo >= 19: 
                    resultados.append((anios_activo, jugador, anio_inicio, anio_inicio_ultima_temp + 1))
                    
        resultados.sort(reverse=True, key=lambda x: x[0])
        return [f"- {j}: {a} años en activo (De {mn} a {mx})." for a, j, mn, mx in resultados[:limite]]

    def ranking_impolutos(self, limite=3):
        """
        Jugadores más limpios: 0 tarjetas en la etapa moderna (desde 1980).
        Se desempata a favor del jugador que más minutos haya estado sobre el campo.
        """
        totales = defaultdict(lambda: {'partidos': 0, 'minutos': 0, 'valido': True})
        for temp, _, j in self._buscar_registros():
            if self._extraer_anio_inicio(temp) >= 1980:
                totales[j.nombre]['partidos'] += j.partidos
                totales[j.nombre]['minutos'] += j.minutos
                # A la primera tarjeta, queda excluido
                if j.tarjetas > 0 or j.expulsiones > 0:
                    totales[j.nombre]['valido'] = False
                    
        resultados = [(s['partidos'], s['minutos'], j) for j, s in totales.items() if s['valido'] and s['partidos'] > 0]
        # Orden: Partidos (descendente), Minutos (descendente), Nombre (ascendente)
        resultados.sort(key=lambda x: (-x[0], -x[1], x[2]))
        
        return [f"- {j}: {int(p)} partidos disputados de forma impoluta." for p, m, j in resultados[:limite]]

    def ranking_veces_cambiado(self, limite=3):
        """Calcula la cantidad de veces que un jugador fue sustituido."""
        totales = defaultdict(int)
        for _, _, j in self._buscar_registros():
            # Las veces cambiado equivalen a partidos como titular menos los que terminó completos
            sustituciones = j.ptitular - j.pcompletos
            if sustituciones > 0:
                totales[j.nombre] += sustituciones
                
        ordenado = sorted(totales.items(), key=lambda x: x[1], reverse=True)
        return [f"- {j}: Cambiado en {int(c)} ocasiones." for j, c in ordenado[:limite]]

    def ranking_goles_unica_temporada(self, limite=4):
        """'One Season Wonders': Jugadores que anotaron todos los goles de su carrera en una sola temporada."""
        goles_por_jugador = defaultdict(lambda: defaultdict(int))
        for temp, _, j in self._buscar_registros():
            if j.goles > 0:
                goles_por_jugador[j.nombre][temp] += j.goles
                
        resultados = []
        for jugador, stats_temp in goles_por_jugador.items():
            # Evaluamos solo si han marcado en exactamente una temporada
            if len(stats_temp) == 1: 
                temp_unica, goles = list(stats_temp.items())[0]
                if goles >= 16:
                    resultados.append((goles, jugador, temp_unica))
                    
        resultados.sort(reverse=True, key=lambda x: x[0])
        return [f"- {j}: {int(g)} goles. Todos anotados en la {t}." for g, j, t in resultados[:limite]]

    def ranking_ratio_goles_minutos(self, min_goles=50, limite=10):
        """Muestra el mejor Ratio Minutos/Gol para goleadores históricos (Mínimo de goles preestablecido)."""
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

    # =========================================================
    # EJERCICIOS DEL BOLETÍN 4 (17 al 33)
    # =========================================================

    def jugadores_sin_celebrar_gol(self, limite=3):
        """[Ejercicio 17] Jugadores con más partidos totales sin marcar gol a lo largo de su carrera."""
        totales = defaultdict(lambda: {'partidos': 0, 'goles': 0})
        
        for _, _, j in self._buscar_registros():
            totales[j.nombre]['partidos'] += j.partidos
            totales[j.nombre]['goles'] += j.goles
        
        resultados = [(s['partidos'], j) for j, s in totales.items() if s['goles'] == 0 and s['partidos'] > 0]
        resultados.sort(reverse=True, key=lambda x: x[0])
        
        return [f"- {j}: {int(p)} partidos enteros sin celebrar un gol." for p, j in resultados[:limite]]

    def goleadores_tres_decadas(self, limite=5):
        """
        [Ejercicio 18] Encuentra a los jugadores que lograron marcar goles en tres décadas
        específicas: los años 20, los 30 y los 40.
        """
        decadas_goles = defaultdict(set)
        
        for temp, _, j in self._buscar_registros():
            if j.goles > 0:
                anio = self._extraer_anio_inicio(temp)
                if 1920 <= anio <= 1949:
                    # Cálculo matemático simple para truncar a la década (ej: 1934 // 10 * 10 = 1930)
                    decada = (anio // 10) * 10
                    decadas_goles[j.nombre].add(decada)
        
        # Filtramos a los que tienen exactamente 3 entradas distintas
        resultados = [j for j, decs in decadas_goles.items() if len(decs) == 3]
        
        return [f"- {j}: Goles en 3 décadas distintas (1920, 1930, 1940)." for j in resultados[:limite]]

    def temporadas_mas_descensos(self):
        """[Ejercicio 19] Busca las temporadas puntuales en las que descendieron 4 o más equipos."""
        descensos_temp, _, _, _ = self._calcular_descensos_y_ascensos()
        res = []
        for temp, eqs in descensos_temp.items():
            if len(eqs) >= 4:
                res.append(f"- Temporada {temp}: Descendieron {len(eqs)} equipos: {', '.join(eqs)}")
        return res

    def equipos_con_mas_descensos(self, limite=3):
        """[Ejercicio 20] Genera el ranking histórico de los clubes con más descensos."""
        _, conteo_desc, _, _ = self._calcular_descensos_y_ascensos()
        ordenado = sorted(conteo_desc.items(), key=lambda x: x[1], reverse=True)
        return [f"- {eq}: {d} descensos" for eq, d in ordenado[:limite]]

    def temporadas_mas_ascensos(self):
        """[Ejercicio 21] Busca las temporadas puntuales en las que ascendieron 4 o más equipos."""
        _, _, ascensos_temp, _ = self._calcular_descensos_y_ascensos()
        res = []
        for temp, eqs in ascensos_temp.items():
            if len(eqs) >= 4:
                res.append(f"- Temporada {temp}: Ascendieron {len(eqs)} equipos: {', '.join(eqs)}")
        return res

    def equipos_con_mas_ascensos(self, limite=1):
        """[Ejercicio 22] Genera el ranking histórico de los clubes con más ascensos."""
        _, _, _, conteo_asc = self._calcular_descensos_y_ascensos()
        ordenado = sorted(conteo_asc.items(), key=lambda x: x[1], reverse=True)
        return [f"- {eq}: {a} ascensos" for eq, a in ordenado[:limite]]

    def equipos_mas_temporadas_primera(self, limite=10):
        """[Ejercicio 23] Top de equipos históricos (clubes con más temporadas en Primera División)."""
        ordenado = self._conteo_temporadas_equipos()
        return [f"- {eq}: {t} temporadas" for eq, t in ordenado[:limite]]

    def equipos_menos_temporadas_primera(self, limite=10):
        """[Ejercicio 24] Equipos con menos temporadas en Primera (ordenados alfabéticamente en caso de empate)."""
        ordenado = sorted(self._conteo_temporadas_equipos(), key=lambda x: (x[1], x[0]))
        return [f"- {eq}: {t} temporadas" for eq, t in ordenado[:limite]]

    def equipos_mas_goleadores(self, limite=10):
        """[Ejercicio 25] Top de equipos con más goles acumulados en toda su historia."""
        ordenado = self._goles_historicos_equipos()
        return [f"- {eq}: {int(g)} goles" for eq, g in ordenado[:limite]]

    def equipos_menos_goleadores(self, limite=10):
        """[Ejercicio 26] Equipos con menos goles históricos (descartando los de 0 goles por datos incompletos)."""
        ordenado = sorted(self._goles_historicos_equipos(), key=lambda x: (x[1], x[0]))
        ordenado = [x for x in ordenado if x[1] > 0]
        return [f"- {eq}: {int(g)} goles" for eq, g in ordenado[:limite]]

    def media_goles_por_temporada(self):
        """
        [Ejercicio 27] Calcula la media de goles global de cada liga. 
        Muestra solo las temporadas que superan la barrera de los 4.0 goles por partido.
        """
        resultados = []
        for temp, equipos in self.historico.items():
            n_equipos = len(equipos)
            # Partidos por temporada en formato liga todos contra todos (Ida y vuelta)
            partidos = n_equipos * (n_equipos - 1) 
            goles = sum(j.goles for eq in equipos.values() for j in eq.jugadores)
            
            if partidos > 0:
                media = goles / partidos
                if media >= 4.0:
                    resultados.append((self._extraer_anio_inicio(temp), temp, goles, partidos, media))
        
        resultados.sort(key=lambda x: x[0])
        return [f"- Temporada {t}: {int(g)} goles en {p} partidos. Media: {m:.2f} goles/partido." for _, t, g, p, m in resultados]

    def empates_maximo_goleador_temporada(self):
        """
        [Ejercicio 28] Temporadas donde dos o más equipos compartieron la corona de máximos goleadores.
        Devuelve resultados ordenados inversamente (alfabéticamente) por requerimiento específico.
        """
        ganadores = self._maximos_goleadores_por_temporada()
        res = []
        for temp in sorted(ganadores.keys(), key=self._extraer_anio_inicio):
            if len(ganadores[temp]) > 1:
                equipos_str = ', '.join(sorted(ganadores[temp], reverse=True))
                res.append(f"- Temporada {temp}: Máximo goleador fue {equipos_str}")
        return res

    def racha_temporadas_consecutivas_max_goleador(self, limite=3):
        """[Ejercicio 29] Mayor racha ininterrumpida de años siendo el club más goleador del torneo."""
        goles_temp = defaultdict(lambda: defaultdict(int))
        
        # 1. Sumamos los goles de cada equipo por temporada
        for temp, eq, j in self._buscar_registros():
            try:
                goles = int(getattr(j, 'goles', 0))
                if goles > 0:
                    goles_temp[temp][eq] += goles
            except ValueError:
                pass
                
        # 2. Sacamos los ganadores de cada temporada
        ganadores_temp = {}
        for temp, equipos in goles_temp.items():
            max_goles = max(equipos.values())
            ganadores_temp[temp] = [eq for eq, g in equipos.items() if g == max_goles]
            
        # 3. Guardamos los años numéricos en un set para evitar duplicados
        años_ganadores = defaultdict(set)
        for temp, ganadores in ganadores_temp.items():
            anio = self._extraer_anio_inicio(temp)
            for eq in ganadores:
                años_ganadores[eq].add(anio)
                
        # 4. Calculamos matemáticamente las rachas evaluando la lista cronológica
        resultados = []
        for eq, anios_set in años_ganadores.items():
            anios = sorted(list(anios_set))
            max_racha = racha_actual = 1
            
            for i in range(1, len(anios)):
                if anios[i] == anios[i-1] + 1:
                    racha_actual += 1
                else:
                    max_racha = max(max_racha, racha_actual)
                    racha_actual = 1
                    
            max_racha = max(max_racha, racha_actual)
            resultados.append((max_racha, eq))
            
        resultados.sort(key=lambda x: (x[0], x[1]), reverse=True)
        return [f"- {eq}: Racha de {r} temporadas consecutivas siendo el máximo goleador." for r, eq in resultados[:limite]]

    def jugadores_comunes_sevilla_betis(self):
        """[Ejercicio 30] Encuentra los jugadores que cruzaron la acera y jugaron en ambos equipos sevillanos."""
        jugadores_sevilla = set(j.nombre for _, eq, j in self._buscar_registros(nombre_equipo="Sevilla F.C.") if j.partidos > 0)
        jugadores_betis = set(j.nombre for _, eq, j in self._buscar_registros(nombre_equipo="Real Betis B. S.") if j.partidos > 0)
        
        # Intersección de sets para encontrar coincidencias exactas
        comunes = sorted(list(jugadores_sevilla.intersection(jugadores_betis)))
        
        return f"- Sevilla F.C. vs Real Betis B. S.: {len(comunes)} jugadores. Ejemplos: {', '.join(comunes[:5])} ..."

    def promedio_minutos_por_temporada(self, limite=5):
        """
        [Ejercicio 31] Calcula el promedio de minutos jugados.
        Filtro específico aplicado: Jugadores con trayectorias de exactamente 8 temporadas en Primera.
        """
        totales = defaultdict(lambda: {'minutos': 0, 'temporadas': set()})
        
        for temp, _, j in self._buscar_registros():
            if j.minutos > 0:
                totales[j.nombre]['minutos'] += j.minutos
                totales[j.nombre]['temporadas'].add(temp)
                
        resultados = []
        for j, stats in totales.items():
            num_temps = len(stats['temporadas'])
            if num_temps == 8:
                promedio = stats['minutos'] / num_temps
                resultados.append((promedio, j, stats['minutos'], num_temps))
                
        resultados.sort(key=lambda x: x[0])
        return [f"- {j}: Promedio de {p:.1f} minutos por temporada (Total: {int(m)} minutos en {t} temporadas)." for p, j, m, t in resultados[:limite]]

    def hijos_prodigos_anios_fuera(self, limite=5):
        """
        [Ejercicio 32] Hijos pródigos: Jugadores que abandonaron un club y volvieron a él.
        Busca las "fugas" más largas de tiempo entre la marcha y el regreso a un mismo equipo.
        """
        trayectorias = defaultdict(list)
        for temp, eq, j in self._buscar_registros():
            if j.partidos > 0:
                trayectorias[(j.nombre, eq)].append(self._extraer_anio_inicio(temp))
                
        resultados = []
        for (jugador, equipo), anios in trayectorias.items():
            anios.sort()
            max_gap = 0
            # Buscamos huecos o "gaps" sin jugar entre los diferentes años computados
            for i in range(1, len(anios)):
                gap = anios[i] - anios[i-1]
                max_gap = max(max_gap, gap)
                
            if max_gap >= 13:
                resultados.append((max_gap, jugador, equipo))
                
        resultados.sort(key=lambda x: x[0], reverse=True)
        return [f"- {j} - Equipo: {eq}, Años fuera: {gap}." for gap, j, eq in resultados[:limite]]

    def racha_temporadas_sin_tarjetas(self, limite=3):
        """
        [Ejercicio 33 Modificado] Calcula la racha máxima de temporadas consecutivas sin tarjetas amarillas.
        Desempata por la racha más reciente (el año en el que terminó dicha racha).
        """
        stats_por_anio = {}
        
        # 1. Recopilamos y agrupamos estadísticas por año
        for temporada, equipos_dict in self.historico.items():
            try:
                anio = int(str(temporada).strip()[:4])
            except ValueError:
                continue
                
            for nombre_equipo, equipo in equipos_dict.items():
                for j in equipo.jugadores:
                    if j.nombre not in stats_por_anio:
                        stats_por_anio[j.nombre] = {}
                    
                    if anio not in stats_por_anio[j.nombre]:
                        stats_por_anio[j.nombre][anio] = {'partidos': 0, 'tarjetas': 0}
                    
                    stats_por_anio[j.nombre][anio]['partidos'] += j.partidos
                    stats_por_anio[j.nombre][anio]['tarjetas'] += j.tarjetas

        resultados = []
        
        # 2. Calculamos la racha y guardamos en qué año terminó
        for jugador, anios_dict in stats_por_anio.items():
            # Filtro desde 1971 (tarjetas ya normalizadas)
            anios_limpios = [
                anio for anio, stats in anios_dict.items() 
                if anio >= 1971 and stats['partidos'] > 0 and stats['tarjetas'] == 0
            ]
            
            if not anios_limpios:
                continue
                
            anios_limpios.sort()
            
            racha_max = 1
            racha_actual = 1
            anio_fin_max = anios_limpios[0]
            anio_fin_actual = anios_limpios[0]
            
            for i in range(1, len(anios_limpios)):
                if anios_limpios[i] == anios_limpios[i-1] + 1:
                    racha_actual += 1
                    anio_fin_actual = anios_limpios[i]
                else:
                    if racha_actual > racha_max:
                        racha_max = racha_actual
                        anio_fin_max = anio_fin_actual
                    elif racha_actual == racha_max:
                        # Si empata consigo mismo, nos quedamos con su racha más moderna
                        anio_fin_max = max(anio_fin_max, anio_fin_actual)
                    
                    racha_actual = 1
                    anio_fin_actual = anios_limpios[i]
                    
            # Comprobación al salir del bucle
            if racha_actual > racha_max:
                racha_max = racha_actual
                anio_fin_max = anio_fin_actual
            elif racha_actual == racha_max:
                anio_fin_max = max(anio_fin_max, anio_fin_actual)
                
            # Filtramos un poco para que la lista no sea kilométrica
            if racha_max >= 5:
                resultados.append((racha_max, anio_fin_max, jugador))
            
        # 3. Ordenamos: 1º Mayor racha, 2º Año MÁS RECIENTE, 3º Orden alfabético
        resultados.sort(key=lambda x: (-x[0], -x[1], x[2]))
        
        return [f"- {x[2]}: Racha de {x[0]} temporadas consecutivas." for x in resultados[:limite]]