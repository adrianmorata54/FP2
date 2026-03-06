import pdfplumber
import re
import os
from departamento import Departamento
from universidad import Universidad
import unicodedata
import re
import requests
from bs4 import BeautifulSoup
import time

class Factoria:
    @staticmethod
    def leer_universidad(nombre_fichero="departamentos.pdf"):
        # 1. Construir ruta
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_pdf = os.path.join(ruta_base, "..", "datos", nombre_fichero)
        
        print(f"--- LECTURA CON PDFPLUMBER ---")
        print(f"Abriendo: {ruta_pdf}")

        if not os.path.exists(ruta_pdf):
            raise FileNotFoundError(f"No existe el fichero: {ruta_pdf}")

        lista_deps = []

        try:
            # Abrimos el PDF con la nueva librería
            with pdfplumber.open(ruta_pdf) as pdf:
                print(f"El PDF tiene {len(pdf.pages)} páginas.")
                
                for pagina in pdf.pages:
                    # Extraemos todo el texto de la página respetando la estructura visual
                    texto = pagina.extract_text()
                    if not texto:
                        continue

                    # Procesamos línea a línea
                    lineas = texto.split('\n')
                    
                    for linea in lineas:
                        # Buscamos filas que sean departamentos
                        if "DEPARTAMENTO" in linea.upper():
                            try:
                                # ESTRATEGIA:
                                # La línea suele ser: "NOMBRE DEL DEPTO   1.400,50   10   5   120,00   1,50"
                                # Usamos Expresiones Regulares (Regex) para sacar todos los números de la línea
                                # El patrón busca: números que pueden tener puntos y comas
                                numeros_encontrados = re.findall(r'[0-9]+[.,][0-9]+|[0-9]+', linea)
                                
                                # Si encontramos al menos 4 números (ETC, TC, TP, Exp), intentamos procesar
                                if len(numeros_encontrados) >= 4:
                                    
                                    # Función de limpieza (1.400,50 -> 1400.50)
                                    def limpiar(val):
                                        val = val.replace('.', '') # Quitar punto de mil
                                        val = val.replace(',', '.') # Coma a punto
                                        return float(val)

                                    # ASIGNACIÓN INTELIGENTE:
                                    # Los números están al final de la línea.
                                    # Normalmente el orden es: [ETC, TC, TP, Total(ignorar), Exp]
                                    # Cogemos los encontrados de derecha a izquierda o por posición relativa.
                                    
                                    # Asumimos que el último es Exp, el penúltimo es Total...
                                    # Ejemplo visual: [ETC, TC, TP, Total, Exp] -> Son 5 números
                                    # A veces TC o TP son 0 y salen como '0' o '0,00'
                                    
                                    # Vamos a coger:
                                    # El primero de la serie numérica -> ETC
                                    # El segundo -> TC
                                    # El tercero -> TP
                                    # El último -> Experimentalidad
                                    
                                    val_etc = limpiar(numeros_encontrados[0])
                                    val_tc = limpiar(numeros_encontrados[1])
                                    val_tp = limpiar(numeros_encontrados[2])
                                    val_exp = limpiar(numeros_encontrados[-1]) # El último siempre es Exp
                                    
                                    # El nombre es todo lo que hay ANTES del primer número
                                    # Buscamos dónde empieza el primer número en la línea original
                                    index_numero = linea.find(numeros_encontrados[0])
                                    nombre = linea[:index_numero].strip()

                                    # Crear objeto
                                    d = Departamento(nombre, val_etc, val_tc, val_tp, val_exp)
                                    lista_deps.append(d)
                                    
                            except Exception as e:
                                print("="*40)
                                print(f"💥 EL PROGRAMA EXPLOTÓ AL INTENTAR CREAR EL DEPARTAMENTO:")
                                print(f"Línea del PDF: {linea}")
                                print(f"Motivo técnico: {e}")
                                print("="*40)
                                continue

            print(f"ÉXITO: Se han procesado {len(lista_deps)} departamentos.")
            return Universidad("Universidad de Sevilla", lista_deps)

        except Exception as e:
            print(f"Error leyendo PDF: {e}")
            return Universidad("Error", [])
            
    
    @staticmethod
    def normalizar_nombre(nombre):
        """Limpia un string para usarlo como clave de cruce perfecta."""
        if not nombre:
            return ""
        
        # 1. Pasamos a mayúsculas
        nombre = nombre.upper()
        
        # 2. Eliminamos el prefijo
        nombre = nombre.replace("DEPARTAMENTO DE ", "")
        
        # 3. Eliminamos tildes
        nombre = ''.join(c for c in unicodedata.normalize('NFD', nombre) if unicodedata.category(c) != 'Mn')
        
        # 4. Eliminamos espacios extra
        nombre = re.sub(r'\s+', ' ', nombre).strip()
        
        return nombre
    @staticmethod
    def extraer_sedes_web(limite=None):
        print("🌐 Iniciando escaneo de páginas en www.us.es/centros/departamentos...")
        url_base = "https://www.us.es"
        
        enlaces_deptos = []
        pagina = 0
        
        # 1. BUCLE DE PAGINACIÓN: Recorremos todas las páginas (0, 1, 2...)
        while True:
            url_directorio = f"{url_base}/centros/departamentos?page={pagina}"
            respuesta = requests.get(url_directorio)
            soup = BeautifulSoup(respuesta.content, "html.parser")
            
            # Buscar enlaces en esta página concreta
            enlaces_pagina = soup.find_all('a', href=True)
            deptos_pagina = [a for a in enlaces_pagina if "/centros/departamentos/" in a['href'] and a['href'] != "/centros/departamentos"]
            
            # Filtramos duplicados dentro de la misma página
            deptos_pagina = list({a['href']: a for a in deptos_pagina}.values())
            
            # Si la página ya no devuelve enlaces a departamentos, hemos llegado al final
            if not deptos_pagina:
                break
                
            enlaces_deptos.extend(deptos_pagina)
            print(f"   📄 Página {pagina} escaneada. Acumulados: {len(enlaces_deptos)} enlaces.")
            pagina += 1
            time.sleep(0.1) # Ser respetuosos con el servidor
            
        # Filtramos duplicados globales por si acaso
        enlaces_deptos = list({a['href']: a for a in enlaces_deptos}.values())
        print(f"\n🔗 Total de departamentos encontrados en todas las páginas: {len(enlaces_deptos)}")
        
        lista_final = enlaces_deptos[:limite] if limite else enlaces_deptos
        diccionario_sedes = {}
        
        print(f"🔍 Extrayendo sedes entrando ficha a ficha (esto tomará un minuto)...")
        # 2. ENTRAR FICHA A FICHA (Igual que antes)
        for enlace in lista_final: 
            nombre_dept_web = enlace.text.strip().upper()
            url_ficha = url_base + enlace['href'] if enlace['href'].startswith('/') else enlace['href']
            
            try:
                res_ficha = requests.get(url_ficha)
                soup_ficha = BeautifulSoup(res_ficha.content, "html.parser")
                
                etiqueta_sede = soup_ficha.find(string=lambda text: text and "Sede" in text and "electrónica" not in text.lower())
                
                if etiqueta_sede:
                    padre = etiqueta_sede.parent
                    enlace_facultad = padre.find_next('a')
                    
                    if enlace_facultad:
                        diccionario_sedes[nombre_dept_web] = enlace_facultad.get_text(strip=True).upper()
                    else:
                        import re
                        texto_bruto = padre.get_text(separator=" ", strip=True)
                        texto_limpio = re.sub(r'(?i)sede\s*[:\-]?\s*', '', texto_bruto).strip()
                        diccionario_sedes[nombre_dept_web] = texto_limpio.upper()
                else:
                    diccionario_sedes[nombre_dept_web] = "ETIQUETA SEDE NO ENCONTRADA"
                    
                time.sleep(0.1) 
                
            except Exception as e:
                print(f"Error accediendo a {url_ficha}: {e}")
                
        return diccionario_sedes