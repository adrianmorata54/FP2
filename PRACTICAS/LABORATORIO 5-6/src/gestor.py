"""
MÓDULO GESTOR: Almacenamiento y Análisis de Datos
=================================================
Este archivo contiene las clases encargadas de almacenar los proyectos 
y realizar todos los cálculos estadísticos solicitados en el Laboratorio 6.
"""

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re

# =====================================================================
# 1. GESTOR PRINCIPAL (Proyectos Solicitados/Globales)
# =====================================================================
class Gestor_Proyecto:
    """
    Clase contenedor principal. Almacena TODOS los proyectos (concedidos y denegados)
    y concentra la lógica analítica del Laboratorio 6.
    """
    
    def __init__(self):
        # Lista interna que guarda los objetos de tipo 'Proyecto'
        self.lista_proyectos = []
        
    # --- MÉTODOS BÁSICOS (ENCAPSULAMIENTO) ---
    
    def añadir(self, proyecto):
        """Añade un objeto Proyecto al final de la lista interna."""
        self.lista_proyectos.append(proyecto)

    def total(self):
        """Devuelve el número total de proyectos almacenados."""
        return len(self.lista_proyectos)

    def obtener_lista_ccaa(self):
        """Devuelve una lista con los nombres únicos de todas las CCAA registradas.
        Usamos set() para eliminar duplicados de forma automática."""
        return list(set([p.comunidad_autonoma for p in self.lista_proyectos]))

    # =================================================================
    # --- LABORATORIO 6: ANÁLISIS DE DATOS ---
    # =================================================================

    # --- TAREA 1: Tasa de Éxito por CCAA ---
    def tasa_exito_ccaa(self, gestor_concedidos, gestor_contratos):
        """Calcula el porcentaje de éxito (concedidos y contratos) por cada CCAA."""
        resultados = {}
        comunidades = self.obtener_lista_ccaa()
        
        for ca in comunidades:
            # Filtramos usando List Comprehensions (muy eficiente en Python)
            solicitados = len([p for p in self.lista_proyectos if p.comunidad_autonoma == ca])
            concedidos = len([p for p in gestor_concedidos.lista_proyectos if p.comunidad_autonoma == ca])
            contratos = len([p for p in gestor_contratos.lista_proyectos if p.comunidad_autonoma == ca])
            
            # Evitamos división por cero
            tasa_concedidos = (concedidos / solicitados) * 100 if solicitados > 0 else 0
            tasa_contratos = (contratos / solicitados) * 100 if solicitados > 0 else 0
            
            # Agrupamos los datos en un diccionario
            resultados[ca] = {
                'solicitados': solicitados,
                'tasa_concedidos': tasa_concedidos,
                'tasa_contratos': tasa_contratos
            }
        return resultados

    # --- TAREA 2: Financiación por Habitante ---
    def financiacion_por_habitante(self, gestor_concedidos, ruta_excel_poblacion):
        """Calcula los euros invertidos por cada habitante de una CCAA."""
        try:
            # Usamos Pandas para leer el Excel externo fácilmente
            df_poblacion = pd.read_excel(ruta_excel_poblacion)
        except Exception as e:
            print(f"Error al leer el Excel de población: {e}")
            return {}

        resultados = {}
        comunidades = self.obtener_lista_ccaa()
        
        for ca in comunidades:
            # Buscamos la fila correspondiente a esta comunidad en el DataFrame
            fila_ca = df_poblacion[df_poblacion['CCAA Entidad Solicitante'] == ca]
            if fila_ca.empty:
                continue 
            
            poblacion = fila_ca.iloc[0]['Poblacion']
            # Sumamos el presupuesto de todos los proyectos concedidos a esta CCAA
            dinero_total = sum([p.presupuesto for p in gestor_concedidos.lista_proyectos if p.comunidad_autonoma == ca])
            
            # Calculamos el ratio (€ / habitante)
            ratio = dinero_total / poblacion if poblacion > 0 else 0
            resultados[ca] = ratio
            
        return resultados
    
    # --- TAREA 3: Top Entidades ---
    def top_entidades_exito(self, gestor_concedidos, gestor_contratos, n):
        """Devuelve las 'n' entidades con mayor tasa de éxito (mínimo 5 solicitudes)."""
        resultados = {}
        # Obtenemos entidades únicas
        entidades = list(set([p.entidad_solicitante for p in self.lista_proyectos]))

        for ent in entidades:
            solicitados = len([p for p in self.lista_proyectos if p.entidad_solicitante == ent])
            
            # Filtro estadístico: Mínimo 5 solicitudes para evitar falsos 100% de éxito
            if solicitados >= 5:
                concedidos = len([p for p in gestor_concedidos.lista_proyectos if p.entidad_solicitante == ent])
                contratos = len([p for p in gestor_contratos.lista_proyectos if p.entidad_solicitante == ent])

                resultados[ent] = {
                    'solicitados': solicitados,
                    'tasa_concedidos': (concedidos / solicitados) * 100,
                    'tasa_contratos': (contratos / solicitados) * 100
                }

        # Ordenamos usando una función lambda para fijarnos en la tasa correspondiente
        top_concedidos = sorted(resultados.items(), key=lambda x: x[1]['tasa_concedidos'], reverse=True)[:n]
        top_contratos = sorted(resultados.items(), key=lambda x: x[1]['tasa_contratos'], reverse=True)[:n]

        return top_concedidos, top_contratos

    # --- TAREA 4: Macro Áreas ---
    def obtener_diccionario_macroareas(self):
        """Diccionario constante que mapea subáreas con su Macro Área principal."""
        return {
            'Ciencias Matemáticas, Físicas, Químicas e Ingenierías': [
                'MTM', 'FIS', 'QMC', 'PIN', 'ENE', 'TIC', 'MAT', 'TCO', 'ESP', 'CTQ', 
                'CYA', 'INF', 'ARQ', 'AYA', 'BIA', 'DPI', 'IQU', 'TEC', 'TRN', 'TEP',
                'EIC', 'MNM', 'MDT', 'CAA', 'FCM', 'ICA', 'FPN', 'INA', 'IEA', 'MNF', 
                'TRA', 'MFU', 'IQM', 'TMA', 'MES', 'IIT', 'FAB', 'GEO'
            ],
            'Ciencias de la Vida': [
                'BMC', 'BIO', 'BVA', 'ALI', 'MED', 'AYF', 'CGL', 'VET', 'BME', 
                'CVI', 'AGR', 'GAN', 'MBI', 'SAF', 'SAL', 'MCB', 'VTC', 'BIF',
                'MAR', 'IBI', 'CTA', 'FOS', 'BDV', 'GYA', 'MBM', 'BTC', 'CAN', 'ESN'
            ],
            'Ciencias Sociales y Humanidades': [
                'DER', 'ECO', 'EDU', 'FIL', 'HIS', 'PSI', 'LYL', 'FEM', 'EMA', 'LFL', 
                'ART', 'CSO', 'DPC', 'FLA', 'SOC', 'GEE', 'JUR', 'HAX', 'FEX', 'HDT',
                'DPT', 'COM', 'POL', 'EYF', 'CPO', 'MEN'
            ]
        }

    def obtener_macroarea(self, subarea, diccionario):
        """Busca y devuelve el nombre de la macroárea dado el código de una subárea."""
        for macro, subareas in diccionario.items():
            if subarea in subareas:
                return macro
        return "OTRAS"

    def tasa_exito_por_agrupacion(self, gestor_concedidos, gestor_contratos, tipo="area"):
        """Calcula la tasa de éxito agrupando por 'area' o 'macroarea'."""
        resultados = {}
        dicc_macro = self.obtener_diccionario_macroareas()

        for p in self.lista_proyectos:
            # Decidimos la clave de agrupación según el parámetro 'tipo'
            clave = p.area if tipo == "area" else self.obtener_macroarea(p.area, dicc_macro)
            
            # Inicializamos el contador si la clave no existe
            if clave not in resultados:
                resultados[clave] = {'solicitados': 0, 'concedidos': 0, 'contratos': 0}
            
            resultados[clave]['solicitados'] += 1
            if p.concedido:
                resultados[clave]['concedidos'] += 1
                if p.contratado_predoctoral:
                    resultados[clave]['contratos'] += 1

        # Calculamos los porcentajes finales
        tasas = {}
        for clave, datos in resultados.items():
            sol = datos['solicitados']
            tasas[clave] = {
                'solicitados': sol,
                'tasa_concedidos': (datos['concedidos'] / sol) * 100 if sol > 0 else 0,
                'tasa_contratos': (datos['contratos'] / sol) * 100 if sol > 0 else 0
            }
        return tasas
    
    # --- TAREA 5: Nube de Palabras ---
    def nube_de_palabras(self, gestor_contratos):
        """Genera nubes de palabras (General y por Macro Área) filtrando stopwords."""
        
        # Palabras comunes sin valor semántico que queremos eliminar
        stopwords = {
            "de", "la", "el", "en", "y", "a", "los", "las", "un", "una", "del", "por", 
            "para", "con", "al", "su", "como", "sobre", "este", "esta", "se", "o", 
            "sus", "es", "estudio", "analisis", "desarrollo", "evaluacion", "sistema", 
            "sistemas", "mediante", "hacia", "uso", "basado", "efectos", "papel", 
            "nuevas", "nuevos", "impacto", "aplicacion", "entre", "uno", "unos", 
            "unas", "desde", "que", "tecnologias", "modelos", "diseño"
        }

        textos_por_macro = {'General': ""}
        dicc_macro = self.obtener_diccionario_macroareas()

        for p in gestor_contratos.lista_proyectos:
            titulo = p.titulo_proyecto.lower()
            # Quitamos signos de puntuación usando expresiones regulares
            titulo_limpio = re.sub(r'[^\w\s]', '', titulo)

            # Nos quedamos con palabras válidas y largas
            palabras_validas = [palabra for palabra in titulo_limpio.split() 
                                if palabra not in stopwords and len(palabra) > 2]
            
            texto_final = " ".join(palabras_validas) + " "

            # Añadimos a la categoría General y a su Macro Área específica
            textos_por_macro['General'] += texto_final
            
            macro = self.obtener_macroarea(p.area, dicc_macro)
            if macro not in textos_por_macro:
                textos_por_macro[macro] = ""
            textos_por_macro[macro] += texto_final

        # Generación visual de los gráficos
        for macro, texto in textos_por_macro.items():
            if texto.strip() == "": continue 
                
            wordcloud = WordCloud(width=800, height=400, background_color='white', 
                                  colormap='viridis').generate(texto)

            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off') # Ocultar ejes numéricos
            plt.title(f"Nube de palabras: {macro}", fontsize=16)
            plt.show()

    # --- TAREA 6: Subproyectos Huérfanos ---
    def subproyectos_huerfanos(self, gestor_concedidos):
        """Devuelve subproyectos denegados cuyo proyecto principal (1) sí fue aprobado."""
        huerfanos = []
        
        # Rendimiento: Usamos set() porque buscar en un conjunto es instantáneo en Python
        refs_concedidas = set([p.referencia for p in gestor_concedidos.lista_proyectos])
        bases_concedidas = set()
        
        # 1. Almacenar las 'raíces' de los proyectos coordinados principales aprobados
        for ref in refs_concedidas:
            if "-C" in ref and ref.endswith("1"):
                base = ref[:-1] # Cortamos el último número
                bases_concedidas.add(base)
                
        # 2. Buscar secundarios (terminados en 2, 3...) sin financiación
        for p in self.lista_proyectos:
            ref = p.referencia
            if "-C" in ref and not ref.endswith("1"):
                base = ref[:-1]
                # Condición: La base tiene dinero, pero esta referencia exacta no
                if (base in bases_concedidas) and (ref not in refs_concedidas):
                    huerfanos.append(ref)
                    
        return huerfanos

    # --- TAREA 7: Investigación Orientada vs Básica ---
    def analisis_orientacion(self, gestor_concedidos):
        """Compara éxito y presupuesto entre proyectos Orientados (O) y No Orientados (N)."""
        resultados = {
            'N': {'nombre': 'Investigación Básica (No Orientada)', 'solicitados': 0, 'concedidos': 0, 'dinero': 0},
            'O': {'nombre': 'Investigación Aplicada (Orientada)', 'solicitados': 0, 'concedidos': 0, 'dinero': 0}
        }

        # Extraemos la letra central que define la orientación
        for p in self.lista_proyectos:
            partes = p.referencia.split('-')
            if len(partes) >= 2:
                tipo = partes[1][-2] 
                if tipo in resultados:
                    resultados[tipo]['solicitados'] += 1

        for p in gestor_concedidos.lista_proyectos:
            partes = p.referencia.split('-')
            if len(partes) >= 2:
                tipo = partes[1][-2]
                if tipo in resultados:
                    resultados[tipo]['concedidos'] += 1
                    resultados[tipo]['dinero'] += p.presupuesto

        # Calculamos la tasa
        for tipo in resultados:
            sol = resultados[tipo]['solicitados']
            conc = resultados[tipo]['concedidos']
            resultados[tipo]['tasa'] = (conc / sol * 100) if sol > 0 else 0

        return resultados

    # --- TAREA 8: Individual vs Coordinado ---
    def analisis_individual_vs_coordinado(self, gestor_concedidos):
        """Compara la tasa de éxito entre proyectos Individuales y Coordinados."""
        resultados = {
            'Individual': {'solicitados': 0, 'concedidos': 0},
            'Coordinado': {'solicitados': 0, 'concedidos': 0}
        }

        def obtener_tipo(referencia):
            # Analizamos el sufijo final ('I00' o 'C31')
            partes = referencia.split('-')
            if len(partes) == 3:
                sufijo = partes[2]
                if sufijo.startswith('I'): return 'Individual'
                if sufijo.startswith('C'): return 'Coordinado'
            return None

        for p in self.lista_proyectos:
            tipo = obtener_tipo(p.referencia)
            if tipo: resultados[tipo]['solicitados'] += 1

        for p in gestor_concedidos.lista_proyectos:
            tipo = obtener_tipo(p.referencia)
            if tipo: resultados[tipo]['concedidos'] += 1

        for tipo in resultados:
            sol = resultados[tipo]['solicitados']
            conc = resultados[tipo]['concedidos']
            resultados[tipo]['tasa'] = (conc / sol * 100) if sol > 0 else 0

        return resultados


# =====================================================================
# 2. GESTORES ESPECÍFICOS (Separación de conceptos)
# =====================================================================

class Gestor_ProyectoConcedido:
    """
    Clase contenedor exclusiva para los proyectos aprobados financieramente.
    Cumple con el requisito de diseño de mantener las listas separadas.
    """
    def __init__(self):
        self.lista_proyectos = []
        
    def añadir(self, proyecto):
        self.lista_proyectos.append(proyecto)
        
    def total(self):
        return len(self.lista_proyectos)


class Gestor_ProyectoContrato:
    """
    Clase contenedor exclusiva para la 'élite': proyectos concedidos
    que además incluyen un contrato predoctoral.
    """
    def __init__(self):
        self.lista_proyectos = []
        
    def añadir(self, proyecto):
        self.lista_proyectos.append(proyecto)
        
    def total(self):
        return len(self.lista_proyectos)