
# Importamos pandas (nuestra herramienta para leer Excels) y nuestras clases
import pandas as pd
from proyectos import Proyecto, ProyectoConcedido, ProyectoContrato
from gestor import Gestor_Proyecto, Gestor_ProyectoConcedido, Gestor_ProyectoContrato

class Factoria:
    """
    Clase Factoría. Su misión es leer los Excel, transformar cada fila en 
    un objeto de Python y meterlos en las "cajas" (gestores) correspondientes.
    """
    
    @staticmethod
    def leer_datos(ruta_anexo1, ruta_anexo2, ruta_anexo3, ruta_anexo4):
        
        # =====================================================================
        # 1. PREPARAMOS LAS "CAJAS" (Instanciar los Gestores)
        # =====================================================================
        gestor_todos = Gestor_Proyecto()            
        gestor_concedidos = Gestor_ProyectoConcedido() 
        gestor_contratos = Gestor_ProyectoContrato()   
        
        # =====================================================================
        # 2. LEER LOS EXCEL (Cargar datos en memoria)
        # =====================================================================
        df_concedidos = pd.read_excel(ruta_anexo1)   # Anexo I: Datos básicos aprobados
        df_presupuestos = pd.read_excel(ruta_anexo2) # Anexo II: Dinero de los aprobados
        df_denegados = pd.read_excel(ruta_anexo3)    # Anexo III: Proyectos denegados
        df_contratos = pd.read_excel(ruta_anexo4)    # Anexo IV: Proyectos con contrato

        # =====================================================================
        # 3. PROCESAR PROYECTOS DENEGADOS (La parte fácil)
        # =====================================================================
        # iterrows() es un bucle que recorre la tabla fila a fila. 
        # El guion bajo '_' ignora el número de fila, solo nos importan los datos ('fila').
        for _, fila in df_denegados.iterrows():
            
            # Como están denegados, usamos el molde más básico: Proyecto.
            # Accedemos a los datos de la fila usando el nombre exacto de la columna del Excel.
            p = Proyecto(
                referencia=fila['REFERENCIA'], 
                area=fila['AREA'], 
                entidad_solicitante=fila['ENTIDAD SOLICITANTE'], 
                comunidad_autonoma=fila['CCAA Entidad Solicitante']
            )
            gestor_todos.añadir(p)

        # =====================================================================
        # 4. PROCESAR PROYECTOS CONCEDIDOS (La parte compleja)
        # =====================================================================

        # pd.merge es como un BUSCARV de Excel. Une dos tablas en una sola.
        # Le decimos: "Junta la tabla de concedidos y la de presupuestos, emparejando 
        # las filas que tengan el mismo valor en la columna 'REFERENCIA'".
        df_aprobados_datos = pd.merge(df_concedidos, df_presupuestos, on='REFERENCIA', how='inner')

        # Ahora recorremos esta nueva súper-tabla unida, fila a fila
        for _, fila in df_aprobados_datos.iterrows():
            
            # 4.1. Extraemos las anualidades en una lista como pide el enunciado
            anualidades = [
                fila['SUBVENCION_2025_TOTAL'], 
                fila['SUBVENCION_2026'], 
                fila['SUBVENCION_2027'], 
                fila['SUBVENCION_2028']
            ]
            
            # 4.2. ¿Tendrá contrato este proyecto? 
            # Filtramos la tabla del Anexo IV buscando si existe esta misma REFERENCIA
            es_contrato = df_contratos[df_contratos['REFERENCIA'] == fila['REFERENCIA']]
            
            # .empty comprueba si el filtro anterior dio algún resultado o está vacío
            if not es_contrato.empty:
                # ¡NO está vacío! Significa que SÍ está en el Anexo IV y tiene contrato.
                
                # .iloc[0] coge la primera fila de ese resultado y extrae el título
                titulo = es_contrato.iloc[0]['TITULO DEL PROYECTO']
                
                # Usamos el molde más completo: ProyectoContrato
                p = ProyectoContrato(
                    referencia=fila['REFERENCIA'], 
                    area=fila['AREA'], 
                    entidad_solicitante=fila['ENTIDAD SOLICITANTE'], 
                    comunidad_autonoma=fila['CCAA Entidad Solicitante'],
                    costes_directos=fila['CD_COSTES_DIRECTOS'], 
                    costes_indirectos=fila['CI_COSTES_INDIRECTOS'], 
                    anticipo=fila['ANTICIPO_REEMBOLSABLE'], 
                    subvencion=fila['SUBVENCION'], 
                    anualidades=anualidades, 
                    titulo_proyecto=titulo
                )
                # Como tiene contrato, va a la caja exclusiva de contratos
                gestor_contratos.añadir(p)
                
            else:
                # Sí está vacío. Significa que NO está en el Anexo IV. 
                # Es un proyecto aprobado normal y corriente. Usamos ProyectoConcedido.
                p = ProyectoConcedido(
                    referencia=fila['REFERENCIA'], 
                    area=fila['AREA'], 
                    entidad_solicitante=fila['ENTIDAD SOLICITANTE'], 
                    comunidad_autonoma=fila['CCAA Entidad Solicitante'],
                    costes_directos=fila['CD_COSTES_DIRECTOS'], 
                    costes_indirectos=fila['CI_COSTES_INDIRECTOS'], 
                    anticipo=fila['ANTICIPO_REEMBOLSABLE'], 
                    subvencion=fila['SUBVENCION'], 
                    anualidades=anualidades
                )
            
            # 4.3. Sea cual sea de los dos tipos anteriores (con o sin contrato), 
            # ambos son proyectos aprobados, así que van a estas dos cajas:
            gestor_concedidos.añadir(p)
            gestor_todos.añadir(p) 

        # =====================================================================
        # 5. DEVOLVER RESULTADOS
        # =====================================================================
        # La factoría ha terminado. Devuelve las 3 cajas llenas al programa principal.
        return gestor_todos, gestor_concedidos, gestor_contratos