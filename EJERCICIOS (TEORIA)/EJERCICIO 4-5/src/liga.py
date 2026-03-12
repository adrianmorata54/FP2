from collections import defaultdict
import itertools

class Liga:
    """
    Clase principal que gestiona el histórico de todas las temporadas de LaLiga.
    Adaptada al Boletín 5 con metodología de POO, propiedades derivadas y generadores.
    """
    
    def __init__(self):
        # Nivel más alto de la jerarquía: Diccionario de objetos Temporada
        self.temporadas = {}

    # =========================================================
    # MÉTODOS DE INSERCIÓN Y UTILIDAD (BOLETÍN 5)
    # =========================================================

    def agregar_temporada(self, temporada):
        """Añade un objeto Temporada al diccionario principal."""
        self.temporadas[temporada.identificador] = temporada

    @property
    def num_temporadas(self):
        """Propiedad derivada: Número total de temporadas registradas."""
        return len(self.temporadas)

    @property
    def num_temporadas_no_jugadas(self):
        """Propiedad derivada: Años en los que no hubo liga (ej. Guerra Civil)."""
        if not self.temporadas:
            return 0
        anios = sorted(t.año_inicio for t in self.temporadas.values())
        rango_teorico = (anios[-1] - anios[0]) + 1
        return rango_teorico - self.num_temporadas

    def _iterar_historial(self):
        """
        Itera sobre toda la base de datos y devuelve una tupla con el contexto:
        (Objeto Temporada, Objeto Equipo, Objeto Jugador)
        """
        for temporada in self.temporadas.values():
            for equipo in temporada.equipos.values():
                for jugador in equipo.jugadores:
                    yield temporada, equipo, jugador

    # =========================================================
    # MÉTODOS AUXILIARES ADAPTADOS AL NUEVO GENERADOR
    # =========================================================

    def _goles_historicos_equipos(self):
        """Suma todos los goles anotados por los equipos en la historia."""
        goles = defaultdict(int)
        for _, equipo, jugador in self._iterar_historial():
            goles[equipo.nombre] += jugador.goles
        return sorted(goles.items(), key=lambda x: x[1], reverse=True)

    def _calcular_descensos_y_ascensos(self):
        """Calcula matemáticamente los ascensos y descensos comparando temporadas."""
        temps_ordenadas = sorted(self.temporadas.values(), key=lambda t: t.año_inicio)
        descensos_temp, ascensos_temp = {}, {}
        conteo_desc, conteo_asc = defaultdict(int), defaultdict(int)
        
        for i in range(len(temps_ordenadas) - 1):
            temp_actual = temps_ordenadas[i]
            temp_sig = temps_ordenadas[i+1]
            
            eq_actual = set(temp_actual.equipos.keys())
            eq_sig = set(temp_sig.equipos.keys())
            
            descendidos = eq_actual - eq_sig
            if descendidos:
                descensos_temp[temp_actual.identificador] = sorted(list(descendidos))
                for eq in descendidos: conteo_desc[eq] += 1
                
            ascendidos = eq_sig - eq_actual
            if ascendidos and temp_sig.identificador != "1939-40":
                ascensos_temp[temp_sig.identificador] = sorted(list(ascendidos))
                for eq in ascendidos: conteo_asc[eq] += 1
                
        return descensos_temp, conteo_desc, ascensos_temp, conteo_asc

    def _conteo_temporadas_equipos(self):
        """Cuenta el número total de temporadas que ha disputado cada equipo."""
        conteo = defaultdict(int)
        for temporada in self.temporadas.values():
            for nombre_eq in temporada.equipos.keys():
                conteo[nombre_eq] += 1
        return sorted(conteo.items(), key=lambda x: x[1], reverse=True)

    def _maximos_goleadores_por_temporada(self):
        """Calcula qué equipo marcó más goles en cada temporada."""
        ganadores_temp = {}
        for temporada in self.temporadas.values():
            # Usamos la propiedad derivada goles_marcados del equipo
            goles_eq = {eq.nombre: eq.goles_marcados for eq in temporada.equipos.values()}
            if goles_eq:
                max_goles = max(goles_eq.values())
                ganadores_temp[temporada.identificador] = [nombre for nombre, g in goles_eq.items() if g == max_goles]
        return ganadores_temp

    # =========================================================
    # EJERCICIOS 1 al 6 (Estadísticas Individuales Básicas)
    # =========================================================

    def estadisticas_jugador(self, nombre_jugador, id_temporada):
        """Ejercicio 1: Busca a un jugador en una temporada específica."""
        for temporada, equipo, jugador in self._iterar_historial():
            if temporada.identificador == id_temporada and jugador.nombre.upper() == nombre_jugador.upper():
                return f"{jugador.nombre.upper()} ({equipo.nombre} - Temporada {temporada.identificador}) | Partidos: {jugador.partidos} | Goles: {jugador.goles}"
        return "Sin datos."

    def goles_totales(self, nombre_jugador):
        """Ejercicio 2: Suma todos los goles de la carrera de un jugador."""
        total = 0
        encontrado = False
        for _, _, jugador in self._iterar_historial():
            if jugador.nombre.upper() == nombre_jugador.upper():
                total += jugador.goles
                encontrado = True
        return f"{nombre_jugador.upper()}: {int(total)} goles" if encontrado else "Sin datos."

    def historial_equipos(self, nombre_jugador):
        """Ejercicio 3: Equipos por los que ha pasado un jugador (cronológicamente)."""
        equipos_jugados = []
        for temporada, equipo, jugador in self._iterar_historial():
            if jugador.nombre.upper() == nombre_jugador.upper() and jugador.partidos > 0:
                equipos_jugados.append((temporada.año_inicio, equipo.nombre))
        
        if equipos_jugados:
            equipos_jugados.sort(key=lambda x: x[0])
            equipos_unicos = list(dict.fromkeys(eq for _, eq in equipos_jugados))
            return f"{nombre_jugador.upper()} - Equipos: {', '.join(equipos_unicos)}"
        return "Sin datos."
    
    def historial_equipos2(self, nombre_jugador):
        """Ejercicio 4: Equipos por los que ha pasado un jugador donde haya marcado gol."""
        equipos_jugados = []
        for temporada, equipo, jugador in self._iterar_historial():
            if jugador.nombre.upper() == nombre_jugador.upper() and jugador.goles > 0:
                equipos_jugados.append((temporada.año_inicio, equipo.nombre))
        
        if equipos_jugados:
            equipos_jugados.sort(key=lambda x: x[0])
            equipos_unicos = list(dict.fromkeys(eq for _, eq in equipos_jugados))
            return f"{nombre_jugador.upper()} - Equipos: {', '.join(equipos_unicos)}"
        return "Sin datos."

    def partidos_y_equipo_principal(self, nombre_jugador):
        """Ejercicio 5: Total de partidos y en qué equipo jugó más."""
        total_partidos = 0
        conteo_eq = defaultdict(int)
        
        for _, equipo, jugador in self._iterar_historial():
            if jugador.nombre.upper() == nombre_jugador.upper():
                total_partidos += jugador.partidos
                conteo_eq[equipo.nombre] += jugador.partidos
                
        if total_partidos > 0:
            eq_principal = max(conteo_eq, key=conteo_eq.get)
            return f"{nombre_jugador.upper()} - Equipo: {eq_principal}, Partidos: {int(total_partidos)}"
        return "Sin datos."

    def minutos_totales(self, nombre_jugador):
        """Ejercicio 6: Suma el total de minutos jugados."""
        total = 0
        encontrado = False
        for _, _, jugador in self._iterar_historial():
            if jugador.nombre.upper() == nombre_jugador.upper():
                total += jugador.minutos
                encontrado = True
        return f"{nombre_jugador.upper()} con {int(total)} minutos." if encontrado else "Sin datos."

    # =========================================================
    # EJERCICIOS GLOBALES Y RANKINGS (7 al 16) - BOLETÍN 5
    # =========================================================

    def ranking_temporadas_seguidas(self, limite=5):
        """Ejercicio 7: Encuentra la racha ininterrumpida más larga de temporadas en un mismo club."""
        trayectorias = defaultdict(set)
        
        # Usamos el generador y extraemos directamente el año de inicio
        for temporada, equipo, jugador in self._iterar_historial():
            if jugador.partidos > 0:
                trayectorias[(jugador.nombre, equipo.nombre)].add(temporada.año_inicio)
        
        resultados = []
        for (nombre_jug, nombre_eq), anios_jugador in trayectorias.items():
            if not anios_jugador: 
                continue
            
            # Ahora es mucho más fácil: comprobamos si los años son consecutivos matemáticamente
            anios = sorted(list(anios_jugador))
            max_racha = racha_actual = 1
            
            for i in range(1, len(anios)):
                if anios[i] == anios[i-1] + 1:
                    racha_actual += 1
                else:
                    max_racha = max(max_racha, racha_actual)
                    racha_actual = 1
                    
            max_racha = max(max_racha, racha_actual)
            resultados.append((max_racha, nombre_jug, nombre_eq))
                
        resultados.sort(key=lambda x: (-x[0], x[1]))
        return [f"{j} - Equipo: {e}, Temporadas seguidas: {r}" for r, j, e in resultados[:limite]]

    def ranking_minutos_juntos(self, limite=10):
        """Ejercicio 8: Calcula qué pareja de jugadores ha coincidido más minutos sobre el campo."""
        parejas_minutos = defaultdict(int)
        
        # En POO puro, en lugar de agrupar, navegamos por la jerarquía
        for temporada in self.temporadas.values():
            for equipo in temporada.equipos.values():
                # Generamos combinaciones directamente desde la lista de jugadores del equipo
                for j1, j2 in itertools.combinations(equipo.jugadores, 2):
                    pareja = tuple(sorted([j1.nombre, j2.nombre]))
                    parejas_minutos[(pareja, equipo.nombre)] += (j1.minutos + j2.minutos)
                
        resultados = [(mins, pareja, eq) for (pareja, eq), mins in parejas_minutos.items()]
        resultados.sort(reverse=True, key=lambda x: x[0])
        
        return [f"{p[0]} & {p[1]} - Equipo: {eq}, Minutos juntos: {int(m)}" for m, p, eq in resultados[:limite]]

    def ranking_partidos_completos(self, limite=3):
        """
        Ejercicio 9: Jugadores que jugaron toda su etapa sin ser sustituidos (desde 1980).
        """
        totales = defaultdict(lambda: {'partidos': 0, 'valido': True})
        
        for temporada, equipo, jugador in self._iterar_historial():
            if temporada.año_inicio >= 1980:
                totales[jugador.nombre]['partidos'] += jugador.partidos
                # Volvemos a la condición matemática estricta para no contar suplencias
                if jugador.partidos != jugador.pcompletos:
                    totales[jugador.nombre]['valido'] = False
        
        resultados = [(s['partidos'], j) for j, s in totales.items() if s['valido'] and s['partidos'] > 0]
        resultados.sort(key=lambda x: (-x[0], x[1]))
        
        return [f"- {j}: {int(p)} partidos enteros jugados." for p, j in resultados[:limite]]

    def ranking_equipos_tarjeteros_temporada(self, limite=5):
        """Ejercicio 10: Suma de tarjetas de toda una plantilla en una sola temporada."""
        tarjetas = []
        
        # FÍJATE AQUÍ: No hace falta iterar jugadores. Usamos la propiedad del Equipo.
        for temporada in self.temporadas.values():
            for equipo in temporada.equipos.values():
                tarjetas.append((equipo.nombre, temporada.identificador, equipo.total_tarjetas))
            
        # Ordenamos por la propiedad total_tarjetas (el índice 2 de la tupla)
        tarjetas.sort(key=lambda x: x[2], reverse=True)
        return [f"- {eq} ({temp}): {int(t)} tarjetas conjuntas." for eq, temp, t in tarjetas[:limite]]
    
    def ranking_revulsivos(self, limite=3):
        """
        Ejercicio 11: Mejores Revulsivos históricos (Mínimo 10 goles).
        """
        totales = defaultdict(lambda: {'goles': 0, 'minutos': 0, 'psuplente': 0, 'ptitular': 0})
        
        for _, _, jugador in self._iterar_historial():
            totales[jugador.nombre]['goles'] += jugador.goles
            totales[jugador.nombre]['minutos'] += jugador.minutos
            totales[jugador.nombre]['psuplente'] += jugador.psuplente
            totales[jugador.nombre]['ptitular'] += jugador.ptitular
            
        resultados = []
        for jug, stats in totales.items():
            # Comprobamos la lógica de revulsivo en el global de la carrera
            if stats['psuplente'] > stats['ptitular'] and stats['goles'] >= 10:
                ratio = stats['minutos'] / stats['goles'] if stats['goles'] > 0 else 0
                resultados.append((ratio, jug, stats['goles']))
                
        resultados.sort(key=lambda x: x[0]) 
        return [f"- {j}: {int(g)} goles. Marca un gol cada {int(r)} minutos." for r, j, g in resultados[:limite]]

    def ranking_anios_en_activo(self, limite=5):
        """Ejercicio 12: Calcula la longevidad de un jugador."""
        trayectorias = defaultdict(list)
        
        for temporada, _, jugador in self._iterar_historial():
            if jugador.partidos > 0:
                trayectorias[jugador.nombre].append(temporada.año_inicio)
            
        resultados = []
        for jugador, anios in trayectorias.items():
            if anios:
                anio_inicio = min(anios)
                anio_fin = max(anios)
                anios_activo = anio_fin - anio_inicio 
                
                if anios_activo >= 19: 
                    resultados.append((anios_activo, jugador, anio_inicio, anio_fin + 1))
                    
        resultados.sort(reverse=True, key=lambda x: x[0])
        return [f"- {j}: {a} años en activo (De {mn} a {mx})." for a, j, mn, mx in resultados[:limite]]

    def ranking_impolutos(self, limite=3):
        """
        Ejercicio 13: Jugadores más limpios (0 tarjetas) desde 1980.
        """
        totales = defaultdict(lambda: {'partidos': 0, 'minutos': 0, 'valido': True})
        
        for temporada, _, jugador in self._iterar_historial():
            if temporada.año_inicio >= 1980:
                totales[jugador.nombre]['partidos'] += jugador.partidos
                totales[jugador.nombre]['minutos'] += jugador.minutos
                # USAMOS LA PROPIEDAD DERIVADA 'tarjetas_totales' de la clase Jugador
                if jugador.tarjetas_totales > 0:
                    totales[jugador.nombre]['valido'] = False
                    
        resultados = [(s['partidos'], s['minutos'], j) for j, s in totales.items() if s['valido'] and s['partidos'] > 0]
        resultados.sort(key=lambda x: (-x[0], -x[1], x[2]))
        
        return [f"- {j}: {int(p)} partidos disputados de forma impoluta." for p, m, j in resultados[:limite]]

    def ranking_veces_cambiado(self, limite=3):
        """Ejercicio 14: Calcula la cantidad de veces que un jugador fue sustituido."""
        totales = defaultdict(int)
        
        for _, _, jugador in self._iterar_historial():
            # USAMOS LA PROPIEDAD DERIVADA 'veces_sustituido'
            if jugador.veces_sustituido > 0:
                totales[jugador.nombre] += jugador.veces_sustituido
                
        ordenado = sorted(totales.items(), key=lambda x: x[1], reverse=True)
        return [f"- {j}: Cambiado en {int(c)} ocasiones." for j, c in ordenado[:limite]]

    def ranking_goles_unica_temporada(self, limite=4):
        """Ejercicio 15: 'One Season Wonders' (16 goles o más en una única temporada)."""
        goles_por_jugador = defaultdict(lambda: defaultdict(int))
        
        for temporada, _, jugador in self._iterar_historial():
            if jugador.goles > 0:
                goles_por_jugador[jugador.nombre][temporada.identificador] += jugador.goles
                
        resultados = []
        for jugador, stats_temp in goles_por_jugador.items():
            if len(stats_temp) == 1: 
                temp_unica, goles = list(stats_temp.items())[0]
                if goles >= 16:
                    resultados.append((goles, jugador, temp_unica))
                    
        resultados.sort(reverse=True, key=lambda x: x[0])
        return [f"- {j}: {int(g)} goles. Todos anotados en la {t}." for g, j, t in resultados[:limite]]

    def ranking_ratio_goles_minutos(self, min_goles=50, limite=10):
        """Ejercicio 16: Mejor Ratio Minutos/Gol para goleadores históricos."""
        totales = defaultdict(lambda: {'goles': 0, 'minutos': 0})
        
        for _, _, jugador in self._iterar_historial():
            if jugador.goles > 0 and jugador.minutos > 0:
                totales[jugador.nombre]['goles'] += jugador.goles
                totales[jugador.nombre]['minutos'] += jugador.minutos
            
        resultados = []
        for jugador, stats in totales.items():
            if stats['goles'] >= min_goles:
                ratio = stats['minutos'] / stats['goles']
                resultados.append((ratio, jugador, stats['goles']))
                
        resultados.sort(key=lambda x: x[0]) 
        return [f"- {j}: {int(g)} goles. Marca un gol cada {r:.1f} minutos." for r, j, g in resultados[:limite]]

    # =========================================================
    # EJERCICIOS DEL BOLETÍN 4 ADAPTADOS (17 al 33)
    # =========================================================

    def jugadores_sin_celebrar_gol(self, limite=3):
        """[Ejercicio 17] Jugadores con más partidos totales sin marcar gol."""
        totales = defaultdict(lambda: {'partidos': 0, 'goles': 0})
        
        for _, _, j in self._iterar_historial():
            totales[j.nombre]['partidos'] += j.partidos
            totales[j.nombre]['goles'] += j.goles
        
        resultados = [(s['partidos'], j) for j, s in totales.items() if s['goles'] == 0 and s['partidos'] > 0]
        resultados.sort(reverse=True, key=lambda x: x[0])
        
        return [f"- {j}: {int(p)} partidos enteros sin celebrar un gol." for p, j in resultados[:limite]]

    def goleadores_tres_decadas(self, limite=5):
        """[Ejercicio 18] Goles en tres décadas (20s, 30s, 40s)."""
        decadas_goles = defaultdict(set)
        
        for temp, _, j in self._iterar_historial():
            if j.goles > 0:
                anio = temp.año_inicio # Usamos la propiedad
                if 1920 <= anio <= 1949:
                    decada = (anio // 10) * 10
                    decadas_goles[j.nombre].add(decada)
        
        resultados = [j for j, decs in decadas_goles.items() if len(decs) == 3]
        return [f"- {j}: Goles en 3 décadas distintas (1920, 1930, 1940)." for j in resultados[:limite]]

    def temporadas_mas_descensos(self):
        """[Ejercicio 19] Temporadas en las que descendieron 4 o más equipos."""
        descensos_temp, _, _, _ = self._calcular_descensos_y_ascensos()
        res = []
        for temp, eqs in descensos_temp.items():
            if len(eqs) >= 4:
                res.append(f"- Temporada {temp}: Descendieron {len(eqs)} equipos: {', '.join(eqs)}")
        return res

    def equipos_con_mas_descensos(self, limite=3):
        """[Ejercicio 20] Ranking histórico de los clubes con más descensos."""
        _, conteo_desc, _, _ = self._calcular_descensos_y_ascensos()
        ordenado = sorted(conteo_desc.items(), key=lambda x: x[1], reverse=True)
        return [f"- {eq}: {d} descensos" for eq, d in ordenado[:limite]]

    def temporadas_mas_ascensos(self):
        """[Ejercicio 21] Temporadas en las que ascendieron 4 o más equipos."""
        _, _, ascensos_temp, _ = self._calcular_descensos_y_ascensos()
        res = []
        for temp, eqs in ascensos_temp.items():
            if len(eqs) >= 4:
                res.append(f"- Temporada {temp}: Ascendieron {len(eqs)} equipos: {', '.join(eqs)}")
        return res

    def equipos_con_mas_ascensos(self, limite=1):
        """[Ejercicio 22] Ranking histórico de clubes con más ascensos."""
        _, _, _, conteo_asc = self._calcular_descensos_y_ascensos()
        ordenado = sorted(conteo_asc.items(), key=lambda x: x[1], reverse=True)
        return [f"- {eq}: {a} ascensos" for eq, a in ordenado[:limite]]

    def equipos_mas_temporadas_primera(self, limite=10):
        """[Ejercicio 23] Clubes con más temporadas en Primera División."""
        ordenado = self._conteo_temporadas_equipos()
        return [f"- {eq}: {t} temporadas" for eq, t in ordenado[:limite]]

    def equipos_menos_temporadas_primera(self, limite=10):
        """[Ejercicio 24] Equipos con menos temporadas en Primera."""
        ordenado = sorted(self._conteo_temporadas_equipos(), key=lambda x: (x[1], x[0]))
        return [f"- {eq}: {t} temporadas" for eq, t in ordenado[:limite]]

    def equipos_mas_goleadores(self, limite=10):
        """[Ejercicio 25] Top de equipos con más goles acumulados."""
        ordenado = self._goles_historicos_equipos()
        return [f"- {eq}: {int(g)} goles" for eq, g in ordenado[:limite]]

    def equipos_menos_goleadores(self, limite=10):
        """[Ejercicio 26] Equipos con menos goles históricos (>0)."""
        ordenado = sorted(self._goles_historicos_equipos(), key=lambda x: (x[1], x[0]))
        ordenado = [x for x in ordenado if x[1] > 0]
        return [f"- {eq}: {int(g)} goles" for eq, g in ordenado[:limite]]

    def media_goles_por_temporada(self):
        """
        [Ejercicio 27] Media de goles global de cada liga (solo >= 4.0).
        Usa las propiedades derivadas de la clase Temporada.
        """
        resultados = []
        # Iteramos directamente por los objetos Temporada
        for temp in self.temporadas.values():
            if temp.media_goles_por_partido >= 4.0:
                resultados.append((temp.año_inicio, temp.identificador, temp.goles_totales, temp.num_partidos, temp.media_goles_por_partido))
        
        resultados.sort(key=lambda x: x[0])
        return [f"- Temporada {t}: {int(g)} goles en {p} partidos. Media: {m:.2f} goles/partido." for _, t, g, p, m in resultados]

    def empates_maximo_goleador_temporada(self):
        """[Ejercicio 28] Temporadas con dos o más equipos como máximos goleadores."""
        ganadores = self._maximos_goleadores_por_temporada()
        res = []
        for temp in sorted(ganadores.keys(), key=lambda x: int(x.split('-')[0])):
            if len(ganadores[temp]) > 1:
                equipos_str = ', '.join(sorted(ganadores[temp], reverse=True))
                res.append(f"- Temporada {temp}: Máximo goleador fue {equipos_str}")
        return res

    def racha_temporadas_consecutivas_max_goleador(self, limite=3):
        """[Ejercicio 29] Mayor racha ininterrumpida siendo el club más goleador."""
        # Utilizamos nuestro método interno para no recalcular todo
        ganadores_temp = self._maximos_goleadores_por_temporada()
        
        años_ganadores = defaultdict(set)
        for id_temp, ganadores in ganadores_temp.items():
            anio = int(id_temp.split('-')[0])
            for eq in ganadores:
                años_ganadores[eq].add(anio)
                
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
        """[Ejercicio 30] Jugadores que cruzaron la acera (Sevilla y Betis)."""
        jugadores_sevilla = set()
        jugadores_betis = set()
        
        for _, equipo, jugador in self._iterar_historial():
            if jugador.partidos > 0:
                if equipo.nombre == "Sevilla F.C.":
                    jugadores_sevilla.add(jugador.nombre)
                elif equipo.nombre == "Real Betis B. S.":
                    jugadores_betis.add(jugador.nombre)
        
        comunes = sorted(list(jugadores_sevilla.intersection(jugadores_betis)))
        return f"- Sevilla F.C. vs Real Betis B. S.: {len(comunes)} jugadores. Ejemplos: {', '.join(comunes[:5])} ..."

    def promedio_minutos_por_temporada(self, limite=5):
        """[Ejercicio 31] Promedio de minutos jugados (Filtro: Exactamente 8 temporadas)."""
        totales = defaultdict(lambda: {'minutos': 0, 'temporadas': set()})
        
        for temp, _, j in self._iterar_historial():
            if j.minutos > 0:
                totales[j.nombre]['minutos'] += j.minutos
                totales[j.nombre]['temporadas'].add(temp.identificador)
                
        resultados = []
        for j, stats in totales.items():
            num_temps = len(stats['temporadas'])
            if num_temps == 8:
                promedio = stats['minutos'] / num_temps
                resultados.append((promedio, j, stats['minutos'], num_temps))
                
        resultados.sort(key=lambda x: x[0])
        return [f"- {j}: Promedio de {p:.1f} minutos por temporada (Total: {int(m)} minutos en {t} temporadas)." for p, j, m, t in resultados[:limite]]

    def hijos_prodigos_anios_fuera(self, limite=5):
        """[Ejercicio 32] Hijos pródigos: Fugas más largas antes de volver a un mismo equipo."""
        trayectorias = defaultdict(list)
        for temp, eq, j in self._iterar_historial():
            if j.partidos > 0:
                trayectorias[(j.nombre, eq.nombre)].append(temp.año_inicio)
                
        resultados = []
        for (jugador, equipo), anios in trayectorias.items():
            anios.sort()
            max_gap = 0
            for i in range(1, len(anios)):
                gap = anios[i] - anios[i-1]
                max_gap = max(max_gap, gap)
                
            if max_gap >= 13:
                resultados.append((max_gap, jugador, equipo))
                
        resultados.sort(key=lambda x: x[0], reverse=True)
        return [f"- {j} - Equipo: {eq}, Años fuera: {gap}." for gap, j, eq in resultados[:limite]]

    def racha_temporadas_sin_tarjetas(self, limite=3):
        """[Ejercicio 33] Racha máxima de temporadas consecutivas sin tarjetas."""
        stats_por_anio = {}
        
        # 1. Recopilamos y agrupamos estadísticas usando el generador
        for temp, _, j in self._iterar_historial():
            anio = temp.año_inicio
            
            if j.nombre not in stats_por_anio:
                stats_por_anio[j.nombre] = {}
            if anio not in stats_por_anio[j.nombre]:
                stats_por_anio[j.nombre][anio] = {'partidos': 0, 'tarjetas': 0}
            
            stats_por_anio[j.nombre][anio]['partidos'] += j.partidos
            # OJO: Usamos la propiedad tarjetas_totales de la clase Jugador
            stats_por_anio[j.nombre][anio]['tarjetas'] += j.tarjetas_totales

        resultados = []
        
        # 2. Calculamos la racha (A partir de 1980 para desempate alfabético exacto)
        for jugador, anios_dict in stats_por_anio.items():
            anios_limpios = [anio for anio, stats in anios_dict.items() if anio >= 1980 and stats['partidos'] > 0 and stats['tarjetas'] == 0]
            
            if not anios_limpios: continue
                
            anios_limpios.sort()
            racha_max = racha_actual = 1
            
            for i in range(1, len(anios_limpios)):
                if anios_limpios[i] == anios_limpios[i-1] + 1:
                    racha_actual += 1
                else:
                    racha_max = max(racha_max, racha_actual)
                    racha_actual = 1
                    
            racha_max = max(racha_max, racha_actual)
                
            if racha_max >= 5:
                resultados.append((racha_max, jugador))
            
        # Ordenamos: Mayor racha y desempate alfabético
        resultados.sort(key=lambda x: (-x[0], x[1]))
        return [f"- {j}: Racha de {r} temporadas consecutivas." for r, j in resultados[:limite]]