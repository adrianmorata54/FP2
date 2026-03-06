from collections import defaultdict
class Universidad:
    def __init__(self, nombre, departamentos):
        self.nombre = nombre
        self.departamentos = departamentos # Lista de objetos Departamento

    def obtener_departamentos(self):
        return self.departamentos

    
    def departamentos_mayor_carga(self, n):
        """Devuelve los n departamentos con mayor carga."""
        return sorted(self.departamentos, 
                      key=lambda d: d.carga_docente_real, 
                      reverse=True)[:n]

    def departamentos_menor_carga(self, n):
        """Devuelve los n departamentos con menor carga."""
        return sorted(self.departamentos, 
                      key=lambda d: d.carga_docente_real)[:n]


    def distribucion_experimentalidad(self):
        """
        1) Devuelve un diccionario {coeficiente: cantidad_departamentos}
        Ejemplo: {1.2: 15, 1.5: 8...}
        """
        conteo = defaultdict(int)
        for d in self.departamentos:
            conteo[d.experimentalidad] += 1
        return dict(conteo)

    def media_carga_por_experimentalidad(self):
        """
        2) Devuelve un diccionario {coeficiente: media_carga_real}
        """
        # Primero agrupamos las cargas en una lista por cada coeficiente
        grupos = defaultdict(list)
        for d in self.departamentos:
            grupos[d.experimentalidad].append(d.carga_docente_real)
        
        # Ahora calculamos la media de cada grupo
        medias = {}
        for coef, cargas in grupos.items():
            if cargas: # Evitar división por cero si la lista estuviera vacía
                medias[coef] = sum(cargas) / len(cargas)
            else:
                medias[coef] = 0.0
        
        return medias

    def coeficientes_extremos_carga(self):
        """
        3) Devuelve una tupla (coef_mayor_media, coef_menor_media)
        usando el método anterior.
        """
        dic_medias = self.media_carga_por_experimentalidad()
        
        if not dic_medias:
            return None, None
            
        # Buscamos la clave (coeficiente) correspondiente al valor máximo y mínimo
        max_coef = max(dic_medias, key=dic_medias.get)
        min_coef = min(dic_medias, key=dic_medias.get)
        
        return max_coef, min_coef
    
    def asignar_sedes(self, diccionario_sedes_web):
        from factoria import Factoria
        """
        Recibe el diccionario de la web, normaliza las claves 
        y asigna la sede correspondiente a cada objeto Departamento.
        """
        # 1. Limpiamos las claves del diccionario web una sola vez por eficiencia
        # Nota: Asumimos que la clase Factoria está importada o definida en el mismo archivo
        sedes_web_limpias = {}
        for nombre_web, sede in diccionario_sedes_web.items():
            clave_limpia = Factoria.normalizar_nombre(nombre_web)
            sedes_web_limpias[clave_limpia] = sede
            
        departamentos_no_encontrados = 0

        # 2. Recorremos los departamentos que ya tiene la universidad (del PDF)
        for dep in self.departamentos:
            # Limpiamos el nombre de nuestro departamento
            nombre_pdf_limpio = Factoria.normalizar_nombre(dep.nombre)
            
            # 3. Buscamos coincidencia exacta de claves limpias
            if nombre_pdf_limpio in sedes_web_limpias:
                dep.sede = sedes_web_limpias[nombre_pdf_limpio]
            else:
                dep.sede = "SEDE DESCONOCIDA"
                departamentos_no_encontrados += 1
                print(f"⚠️ Aviso: No se encontró sede para -> {dep.nombre}")
                
        # Podemos devolver el número de fallos para que el main decida si imprimirlo
        return departamentos_no_encontrados
    
    def obtener_extremos_por_sede(self):
        """
        Devuelve un diccionario con el formato:
        { "Nombre de la Sede": (Depto_Mayor_Carga, Depto_Menor_Carga) }
        """
        # 1. Agrupamos los departamentos por sede
        agrupacion_sedes = {}
        for dep in self.departamentos:
            if getattr(dep, 'sede', "SEDE DESCONOCIDA") == "SEDE DESCONOCIDA":
                continue # Ignoramos los que no tengan sede
                
            if dep.sede not in agrupacion_sedes:
                agrupacion_sedes[dep.sede] = []
            agrupacion_sedes[dep.sede].append(dep)
            
        resultado_final = {}
        
        # 2. Calculamos el mayor y menor por cada sede
        for sede, lista_deptos in agrupacion_sedes.items():
            if not lista_deptos:
                continue
                
            # Ordenamos la lista de departamentos de esta sede según su carga
            lista_ordenada = sorted(lista_deptos, key=lambda d: d.carga_docente_real, reverse=True)
            
            depto_mayor = lista_ordenada[0]   # El primero es el que tiene más (reverse=True)
            depto_menor = lista_ordenada[-1]  # El último es el que tiene menos
            
            # Guardamos la tupla en el diccionario final
            resultado_final[sede] = (depto_mayor, depto_menor)
            
        return resultado_final

    def media_carga_por_sede(self):
        """
        Agrupa los departamentos por sede y calcula la media de carga docente real
        por profesor para cada una de ellas.
        Retorna un diccionario con la estructura: {'Nombre Sede': media_float}
        """
        # 1. Diccionario temporal para acumular los totales
        datos_temporales = {}

        for depto in self.departamentos:
            nombre_sede = depto.sede if depto.sede else "Sin sede asignada"
            
            if nombre_sede not in datos_temporales:
                datos_temporales[nombre_sede] = {'carga_total': 0.0, 'profesores_total': 0}
            
            # Acumulamos usando tus @property
            datos_temporales[nombre_sede]['carga_total'] += depto.carga_docente_real* depto.total_profesores
            datos_temporales[nombre_sede]['profesores_total'] += depto.total_profesores

        # 2. Diccionario final a devolver
        resultado_medias = {}
        
        for sede, totales in datos_temporales.items():
            carga = totales['carga_total']
            profesores = totales['profesores_total']
            
            # Calculamos la media y la guardamos directamente como valor de la clave
            if profesores > 0:
                resultado_medias[sede] = carga / profesores
            else:
                resultado_medias[sede] = 0.0  # Por seguridad si no hay profesores
                
        return resultado_medias
        
    def __str__(self):
        return f"Universidad: {self.nombre} ({len(self.departamentos)} departamentos)"