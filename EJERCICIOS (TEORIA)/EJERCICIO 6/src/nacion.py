import itertools
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from typing import Dict, List, Optional

from comunidad_autonoma import ComunidadAutonoma

class Nacion:
    """
    Clase principal que gestiona todas las Comunidades Autónomas y centraliza 
    la lógica para responder a las preguntas de la práctica.
    """
    
    # ==========================================
    # 🛠️ MÉTODOS BASE Y CONFIGURACIÓN
    # ==========================================
    
    def __init__(self, nombre: str = "España"):
        self.nombre = nombre
        self.comunidades: Dict[str, ComunidadAutonoma] = {} 
        
    def agregar_comunidad(self, comunidad: ComunidadAutonoma) -> None:
        """Añade un objeto ComunidadAutonoma al diccionario de la nación."""
        self.comunidades[comunidad.nombre] = comunidad

    def _filtrar(self, tipo_retorno: str, nombre_ccaa: Optional[str] = None, nombre_circ: Optional[str] = None, nombre_partido: Optional[str] = None) -> list:
        """
        Filtro universal de la Nación. Altamente optimizado delegando iteraciones a C (extend).
        """
        resultados = []
        f_ccaa = nombre_ccaa.strip().upper() if nombre_ccaa else None
        f_circ = nombre_circ.strip().upper() if nombre_circ else None
        f_part = nombre_partido.strip().upper() if nombre_partido else None

        for ccaa in self.comunidades.values():
            if f_ccaa and ccaa.nombre.upper() != f_ccaa:
                continue
            
            if tipo_retorno == 'ccaa':
                resultados.append(ccaa)
                continue
                
            for circ in ccaa.circunscripciones:
                if f_circ and circ.nombre.upper() != f_circ:
                    continue
                    
                if tipo_retorno == 'circunscripcion':
                    resultados.append(circ)
                    continue
                    
                # 🔥 OPTIMIZACIÓN MÁXIMA CON EXTEND 🔥
                if tipo_retorno == 'partido':
                    if f_part:
                        resultados.extend([p for p in circ.partidos if p.nombre.upper() == f_part])
                    else:
                        resultados.extend(circ.partidos)
                        
        return resultados

    # ==========================================
    # 📊 PREGUNTAS DE LA PRÁCTICA (EN ORDEN)
    # ==========================================

    # --- PREGUNTAS 1 y 8: Gráficos de Votos y Escaños (INTERACTIVO) ---
    def graficar_resultados(self, nivel: str = "nacional", nombre_filtro: Optional[str] = None) -> None:
        """
        Muestra gráficos interactivos (Sectores y Barras) pudiendo alternar 
        entre Votos (P1) y Escaños (P8) en tiempo real con un botón.
        """
        datos_escanos: Dict[str, int] = {}
        datos_votos: Dict[str, int] = {}
        titulo_extra = "Nacional"

        partidos_a_graficar = []
        if nivel == "nacional":
            partidos_a_graficar = self._filtrar('partido')
        elif nivel == "ccaa":
            titulo_extra = nombre_filtro
            partidos_a_graficar = self._filtrar('partido', nombre_ccaa=nombre_filtro)
        elif nivel == "circunscripcion":
            titulo_extra = nombre_filtro
            partidos_a_graficar = self._filtrar('partido', nombre_circ=nombre_filtro)

        if not partidos_a_graficar:
            print(f"⚠️ No se encontraron datos para el nivel '{nivel}' con filtro '{nombre_filtro}'")
            return

        for p in partidos_a_graficar:
            datos_escanos[p.nombre] = datos_escanos.get(p.nombre, 0) + p.escanos_oficiales
            datos_votos[p.nombre] = datos_votos.get(p.nombre, 0) + p.votos

        # --- Lógica de Matplotlib ---
        fig, ax = plt.subplots(figsize=(14, 8))
        estado = {'pagina': 0, 'tipo': 'escanos'} 
        
        def dibujar_grafico():
            ax.clear() 
            datos_actuales = datos_escanos if estado['tipo'] == 'escanos' else datos_votos
            datos_filtrados = {k: v for k, v in datos_actuales.items() if v > 0}
            
            if not datos_filtrados:
                ax.text(0.5, 0.5, f"No hay {estado['tipo']} que mostrar en {titulo_extra}", 
                        ha='center', va='center', fontsize=12)
                fig.canvas.draw_idle()
                return

            ordenados = dict(sorted(datos_filtrados.items(), key=lambda x: x[1], reverse=True))
            nombres = list(ordenados.keys())
            valores = list(ordenados.values())
            tipo_str = "Escaños" if estado['tipo'] == 'escanos' else "Votos"

            if estado['pagina'] == 0:
                fig.subplots_adjust(left=0.05, right=0.65, top=0.90, bottom=0.15) 
                wedges, texts, autotexts = ax.pie(valores, autopct='%1.1f%%', pctdistance=0.85, textprops={'fontsize': 10})
                ax.legend(wedges, nombres, title="Partidos", loc="center left", bbox_to_anchor=(1.05, 0.5), fontsize=9)
                ax.set_title(f'Reparto de {tipo_str} - {titulo_extra}', fontsize=15, fontweight='bold')
                ax.axis('equal') 
            else:
                fig.subplots_adjust(left=0.08, right=0.95, top=0.90, bottom=0.45)
                ax.axis('auto')
                x_pos = range(len(nombres))
                ax.bar(x_pos, valores, color='steelblue', width=0.8)
                ax.set_xticks(x_pos)
                ax.set_xticklabels(nombres, rotation=45, ha='right', fontsize=9)
                ax.set_ylabel(f'Número de {tipo_str}')
                ax.set_title(f'{tipo_str} por Partido - {titulo_extra}', fontsize=15, fontweight='bold')
                
                for i, v in enumerate(valores):
                    formato = f"{v:,}".replace(",", ".") if estado['tipo'] == 'votos' else str(v)
                    rotacion = 90 if estado['tipo'] == 'votos' else 0
                    margen = max(valores) * 0.02
                    ax.text(i, v + margen, formato, color='black', ha='center', fontweight='bold', fontsize=8, rotation=rotacion)
                    
                ax.set_xlim(-0.6, len(nombres) - 0.4)
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
                
            fig.canvas.draw_idle()

        def actualizar_pagina(pag):
            estado['pagina'] = pag
            dibujar_grafico()

        def alternar_tipo(event):
            if estado['tipo'] == 'escanos':
                estado['tipo'] = 'votos'
                btn_tipo.label.set_text('Ver Escaños')
            else:
                estado['tipo'] = 'escanos'
                btn_tipo.label.set_text('Ver Votos')
            dibujar_grafico()

        ax_btn_sectores = plt.axes([0.25, 0.02, 0.12, 0.05])
        ax_btn_barras = plt.axes([0.40, 0.02, 0.12, 0.05])
        ax_btn_tipo = plt.axes([0.65, 0.02, 0.15, 0.05])

        btn_sectores = Button(ax_btn_sectores, 'Ver Sectores')
        btn_barras = Button(ax_btn_barras, 'Ver Barras')
        btn_tipo = Button(ax_btn_tipo, 'Ver Votos')

        btn_sectores.on_clicked(lambda event: actualizar_pagina(0))
        btn_barras.on_clicked(lambda event: actualizar_pagina(1))
        btn_tipo.on_clicked(alternar_tipo)

        fig.btn_sectores, fig.btn_barras, fig.btn_tipo = btn_sectores, btn_barras, btn_tipo
        
        try:
            mng = plt.get_current_fig_manager()
            mng.window.state('zoomed')
        except: pass
        
        dibujar_grafico()
        plt.show()

    # --- PREGUNTA 2: Análisis de votos nulos y blancos ---
    def analizar_votos_nulos_blancos(self) -> None:
        """Calcula las circunscripciones y CCAA con mayor % de nulos y blancos."""
        print("\n--- P2: ANÁLISIS DE VOTOS NULOS Y BLANCOS ---")
        
        # 1. Por Provincia
        max_pct_prov, prov_max = 0.0, ""
        for circ in self._filtrar('circunscripcion'):
            if circ.porcentaje_nulos_blancos > max_pct_prov:
                max_pct_prov, prov_max = circ.porcentaje_nulos_blancos, circ.nombre
        print(f"La circunscripción con mayor porcentaje de nulos/blancos es {prov_max} con un {max_pct_prov:.2f}%")

        # 2. Por CCAA
        max_pct_ccaa, ccaa_max = 0.0, ""
        for ccaa in self._filtrar('ccaa'):
            if ccaa.porcentaje_nulos_blancos > max_pct_ccaa:
                max_pct_ccaa, ccaa_max = ccaa.porcentaje_nulos_blancos, ccaa.nombre
        print(f"La CCAA con mayor porcentaje de nulos/blancos es {ccaa_max} con un {max_pct_ccaa:.2f}%")

    # --- PREGUNTA 3: Participación CERA real ---
    def analizar_participacion_cera_real(self) -> None:
        """Calcula qué proporción del Censo CERA acudió realmente a votar."""
        print("\n--- P3: PARTICIPACIÓN CERA ---")
        
        # 1. Por circunscripción
        max_circ_pct, max_circ_nombre = 0.0, ""
        for circ in self._filtrar('circunscripcion'):
            if circ.participacion_cera_porcentaje > max_circ_pct:
                max_circ_pct, max_circ_nombre = circ.participacion_cera_porcentaje, circ.nombre
                        
        if max_circ_pct > 0:
            print(f"Circunscripción con mayor participación CERA: {max_circ_nombre} ({max_circ_pct:.2f}%)")
        else:
            print("⚠️ No constan votos CERA emitidos.")

        # 2. Por CCAA
        max_ccaa_pct, max_ccaa_nombre = 0.0, ""
        for ccaa in self._filtrar('ccaa'):
            if ccaa.participacion_cera_porcentaje > max_ccaa_pct:
                max_ccaa_pct, max_ccaa_nombre = ccaa.participacion_cera_porcentaje, ccaa.nombre
        
        if max_ccaa_pct > 0:
            print(f"CCAA con mayor participación CERA: {max_ccaa_nombre} ({max_ccaa_pct:.2f}%)")
            
    # --- PREGUNTA 4: Partidos en exactamente N circunscripciones ---
    def partidos_en_n_circunscripciones(self, n: int) -> List[str]:
        """Devuelve una lista de partidos que se presentaron exactamente en N provincias."""
        print(f"\n--- P4: PARTIDOS EN EXACTAMENTE {n} CIRCUNSCRIPCIONES ---")
        apariciones: Dict[str, int] = {}
        
        for p in self._filtrar('partido'):
            apariciones[p.nombre] = apariciones.get(p.nombre, 0) + 1
                    
        resultado = [partido for partido, count in apariciones.items() if count == n]
        print(f"Partidos encontrados: {resultado}")
        return resultado

    # --- PREGUNTA 5: CCAA con mayor proporción Censo CERA / Censo Total ---
    def cera_proporcion_poblacion(self) -> None:
        """Identifica la CCAA con mayor peso de votantes extranjeros respecto a su censo total."""
        print("\n--- P5: PROPORCIÓN CENSO CERA VS CENSO TOTAL ---")
        max_prop_cera, ccaa_cera_max = 0.0, ""
        
        for ccaa in self._filtrar('ccaa'):
            if ccaa.proporcion_cera_sobre_censo > max_prop_cera:
                max_prop_cera, ccaa_cera_max = ccaa.proporcion_cera_sobre_censo, ccaa.nombre
                    
        print(f"La CCAA con mayor proporción CERA es {ccaa_cera_max} con un {max_prop_cera:.2f}%")

    # --- PREGUNTA 6: Escaños en una circunscripción concreta ---
    def escanos_por_circunscripcion(self, nombre_circ: str) -> Optional[Dict[str, int]]:
        """Devuelve y muestra el número de escaños de cada partido en una circunscripción."""
        print(f"\n--- P6: REPARTO D'HONDT EN {nombre_circ.upper()} ---")
        
        circunscripciones = self._filtrar("circunscripcion", nombre_circ=nombre_circ)
        
        if not circunscripciones:
            print(f"⚠️ No se encontró la circunscripción '{nombre_circ}'.")
            return None
            
        circ = circunscripciones[0] 
        circ.aplicar_ley_dhondt()
        
        resultados = {}
        partidos_con_escano = [p for p in circ.partidos if p.escanos_calculados > 0]
        partidos_con_escano.sort(reverse=True)
        
        for p in partidos_con_escano:
            resultados[p.nombre] = p.escanos_calculados
            print(f" - {p.nombre}: {p.escanos_calculados} escaños")
            
        return resultados

    # --- PREGUNTA 7: Comprobación con los datos del Excel ---
    def comprobar_escanos_oficiales(self) -> None:
        """Comprueba que los escaños calculados coinciden exactamente con los datos oficiales."""
        print("\n--- P7: COMPROBACIÓN REPARTO D'HONDT VS OFICIAL EXCEL ---")
        errores = 0
        
        for circ in self._filtrar('circunscripcion'):
            circ.aplicar_ley_dhondt() 
            for p in circ.partidos:
                if p.escanos_calculados != p.escanos_oficiales:
                    print(f"❌ Discrepancia en {circ.nombre} para {p.nombre}: Oficial={p.escanos_oficiales}, Calculado={p.escanos_calculados}")
                    errores += 1
                        
        if errores == 0:
            print("✅ ¡ÉXITO! Todos los escaños calculados coinciden con los oficiales.")
        else:
            print(f"⚠️ Se encontraron {errores} discrepancias.")
    
    # --- PREGUNTA 9: Último escaño de cada provincia ---
    def analizar_ultimo_escano(self) -> None:
        """Muestra quién se llevó el último escaño en cada provincia y quién fue el subcampeón."""
        print("\n--- P9: ANÁLISIS DEL ÚLTIMO ESCAÑO ---")
        for circ in self._filtrar('circunscripcion'):
            if circ.ultimo_escano:
                print(f"{circ.nombre}: Último escaño -> {circ.ultimo_escano.nombre}. Subcampeón -> {circ.subcampeon.nombre} (Faltaron {circ.votos_faltantes} votos).")

    # --- PREGUNTAS 10 y 11: Escaños más baratos y más caros ---
    def analizar_coste_escanos(self) -> None:
        """Calcula cuántos votos ha costado cada escaño a nivel Nacional y Provincial."""
        print("\n--- P10 y P11: COSTE DE ESCAÑOS ---")
        votos_nac: Dict[str, int] = {}
        escanos_nac: Dict[str, int] = {}
        costes_circ: Dict[tuple, float] = {}
        
        for circ in self._filtrar('circunscripcion'):
            for p in circ.partidos:
                votos_nac[p.nombre] = votos_nac.get(p.nombre, 0) + p.votos
                escanos_nac[p.nombre] = escanos_nac.get(p.nombre, 0) + p.escanos_oficiales
                
                if p.escanos_oficiales > 0:
                    costes_circ[(p.nombre, circ.nombre)] = p.votos / p.escanos_oficiales
                    
        costes_nac = {p: (votos_nac[p] / escanos_nac[p]) for p in escanos_nac if escanos_nac[p] > 0}
        
        if costes_nac:
            mas_caro_nac = max(costes_nac, key=costes_nac.get)
            mas_barato_nac = min(costes_nac, key=costes_nac.get)
            print(f"[NACIONAL] Escaño más CARO: {mas_caro_nac} ({costes_nac[mas_caro_nac]:.0f} votos/escaño)")
            print(f"[NACIONAL] Escaño más BARATO: {mas_barato_nac} ({costes_nac[mas_barato_nac]:.0f} votos/escaño)")

        if costes_circ:
            mas_caro_circ = max(costes_circ, key=costes_circ.get)
            mas_barato_circ = min(costes_circ, key=costes_circ.get)
            print(f"[PROVINCIAL] Escaño más CARO: {mas_caro_circ[0]} en {mas_caro_circ[1]} ({costes_circ[mas_caro_circ]:.0f} votos/escaño)")
            print(f"[PROVINCIAL] Escaño más BARATO: {mas_barato_circ[0]} en {mas_barato_circ[1]} ({costes_circ[mas_barato_circ]:.0f} votos/escaño)")

    # --- PREGUNTA 12: Circunscripciones con escaños más "baratos" ---
    def circunscripciones_escanos_baratos(self) -> None:
        """Calcula la provincia donde hacen falta menos votos de media para conseguir representación."""
        print("\n--- P12: COSTE MEDIO DE ESCAÑO POR CIRCUNSCRIPCIÓN ---")
        costes_circ: Dict[str, float] = {}
        
        for circ in self._filtrar('circunscripcion'):
            if circ.total_escanos > 0:
                costes_circ[circ.nombre] = circ.votos_validos / circ.total_escanos
                    
        if costes_circ:
            circ_mas_barata = min(costes_circ, key=costes_circ.get)
            print(f"La circunscripción donde 'cuesta' menos votos sacar un diputado es {circ_mas_barata} ({costes_circ[circ_mas_barata]:.0f} votos de media).")

    # --- PREGUNTA 13: Partido con más votos que NO consiguió escaño ---
    def partido_mas_votado_sin_escano(self) -> None:
        """Encuentra al partido a nivel nacional que más votos obtuvo sin lograr representación."""
        print("\n--- P13: PARTIDO MÁS VOTADO SIN ESCAÑO (NACIONAL) ---")
        votos: Dict[str, int] = {}
        escanos: Dict[str, int] = {}
        
        for p in self._filtrar('partido'):
            votos[p.nombre] = votos.get(p.nombre, 0) + p.votos
            escanos[p.nombre] = escanos.get(p.nombre, 0) + p.escanos_oficiales
                    
        partidos_sin_escano = {k: v for k, v in votos.items() if escanos[k] == 0}
        if partidos_sin_escano:
            perdedor_ganador = max(partidos_sin_escano, key=partidos_sin_escano.get)
            print(f"El partido con más votos sin rascar escaño fue {perdedor_ganador} con {partidos_sin_escano[perdedor_ganador]} votos.")

    # --- PREGUNTA 14: Parejas (partido-circunscripción) con menos votos ---
    def peores_parejas_partido_circunscripcion(self, n: int = 5) -> None:
        """Muestra los N partidos que obtuvieron los peores resultados en provincias concretas."""
        print(f"\n--- P14: LAS {n} PAREJAS PARTIDO-CIRCUNSCRIPCIÓN CON MENOS VOTOS ---")
        parejas = []
        for circ in self._filtrar('circunscripcion'):
            for p in circ.partidos:
                if p.votos > 0:
                    parejas.append((p.votos, p.nombre, circ.nombre))
                        
        parejas.sort()
        for i in range(min(n, len(parejas))):
            votos, partido, circ = parejas[i]
            print(f"{i+1}. {partido} en {circ} con solo {votos} votos.")

    # --- PREGUNTA 15: Pactómetro ---
    def pactometro(self, escanos_necesarios: int = 176) -> None:
        """Genera combinaciones de partidos que superen la mayoría absoluta."""
        print(f"\n--- P15: PACTÓMETRO (Objetivo: {escanos_necesarios} escaños) ---")
        escanos_totales: Dict[str, int] = {}
        
        for p in self._filtrar('partido'):
            escanos_totales[p.nombre] = escanos_totales.get(p.nombre, 0) + p.escanos_oficiales
        
        partidos_con_escanos = {k: v for k, v in escanos_totales.items() if v > 0}
        nombres = list(partidos_con_escanos.keys())
        
        pactos_posibles = []
        for r in range(2, min(6, len(nombres) + 1)):
            for comb in itertools.combinations(nombres, r):
                suma = sum(partidos_con_escanos[partido] for partido in comb)
                if suma >= escanos_necesarios:
                    pactos_posibles.append((suma, comb))
        
        pactos_posibles.sort()
        print(f"Mostrando algunas de las alianzas posibles (de menor a mayor sobrante):")
        for suma, comb in pactos_posibles[:10]:
            print(f"Suma: {suma} escaños -> {', '.join(comb)}")