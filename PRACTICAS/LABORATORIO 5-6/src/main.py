"""
MÓDULO PRINCIPAL: Ejecución y Visualización
===========================================
Este script es el punto de entrada de la aplicación. Se encarga de:
1. Configurar las rutas de los archivos de datos.
2. Llamar a la Factoría para crear los objetos.
3. Ejecutar y mostrar por consola todos los análisis del Laboratorio 6.
"""

# Importamos Path para manejar rutas de archivos de forma profesional y multiplataforma (Windows/Mac/Linux)
from pathlib import Path

# Importamos nuestra Factoría, encargada de leer los Excel y construir los objetos
from factoria import Factoria

def main():
    # =====================================================================
    # 0. CONFIGURACIÓN DE RUTAS DINÁMICAS Y SEGURIDAD
    # =====================================================================
    # __file__ es este script. .resolve() saca la ruta absoluta. .parent.parent sube dos carpetas.
    ruta_base = Path(__file__).resolve().parent.parent
    ruta_datos = ruta_base / 'datos'

    print("Cargando datos de la carpeta 'datos', por favor espera...")
    
    # Definimos las rutas exactas de los 4 anexos
    ruta_anexo1 = ruta_datos / 'Anexo I.xlsx'
    ruta_anexo2 = ruta_datos / 'Anexo II.xlsx'
    ruta_anexo3 = ruta_datos / 'Anexo III.xlsx'
    ruta_anexo4 = ruta_datos / 'Anexo IV.xlsx'

    # Bucle de seguridad defensiva: Evita que el programa "explote" si falta un Excel
    archivos_requeridos = [ruta_anexo1, ruta_anexo2, ruta_anexo3, ruta_anexo4]
    for ruta in archivos_requeridos:
        if not ruta.exists():
            print(f"⚠️ Error Crítico: No se encuentra el archivo en {ruta}")
            return # Detiene la ejecución inmediatamente si falta algo

    # =====================================================================
    # 1. LECTURA Y CREACIÓN DE OBJETOS (FACTORÍA)
    # =====================================================================
    # Desempaquetamos los 3 gestores que nos devuelve la Factoría
    gestor_todos, gestor_concedidos, gestor_contratos = Factoria.leer_datos(
        ruta_anexo1, ruta_anexo2, ruta_anexo3, ruta_anexo4
    )
    
    # =====================================================================
    # APARTADO 1: TOTAL DE REGISTROS ALMACENADOS
    # =====================================================================
    print("\n" + "="*50)
    print(" 1. TOTAL DE REGISTROS ALMACENADOS")
    print("="*50)
    
    # Usamos f-strings para imprimir variables dentro de texto fácilmente
    print(f"Total proyectos (solicitados y denegados): {gestor_todos.total()} (Esperado: 7092)")
    print(f"Total proyectos concedidos:                {gestor_concedidos.total()} (Esperado: 3252)")
    print(f"Total proyectos con contrato predoctoral:  {gestor_contratos.total()} (Esperado: 1149)")

    # =====================================================================
    # APARTADO 2: TASA DE ÉXITO BÁSICA (Ejemplo: Andalucía)
    # =====================================================================
    print("\n" + "="*50)
    print(" 2. TASA DE ÉXITO POR COMUNIDAD AUTÓNOMA (Andalucía)")
    print("="*50)
    
    comunidad_objetivo = "ANDALUCIA" 
    
    # List Comprehension: Filtramos en una sola línea de forma muy eficiente
    solicitados_ca = [p for p in gestor_todos.lista_proyectos if p.comunidad_autonoma == comunidad_objetivo]
    concedidos_ca = [p for p in solicitados_ca if p.concedido]
    
    # Prevención de división por cero
    if len(solicitados_ca) > 0:
        tasa = (len(concedidos_ca) / len(solicitados_ca)) * 100
        print(f"Comunidad: {comunidad_objetivo}")
        print(f"Proyectos Solicitados: {len(solicitados_ca)}")
        print(f"Proyectos Concedidos:  {len(concedidos_ca)}")
        print(f"Tasa de éxito:         {tasa:.2f}%") # ':.2f' recorta a 2 decimales
    else:
        print(f"No hay registros para la comunidad '{comunidad_objetivo}'.")

    # =====================================================================
    # APARTADO 3: IMPORTES GLOBALES Y POR COMUNIDAD
    # =====================================================================
    print("\n" + "="*50)
    print(" 3. IMPORTES GLOBALES Y POR COMUNIDAD")
    print("="*50)
    
    importe_global = 0
    importes_por_ca = {} # Diccionario para agrupar dinámicamente

    for p in gestor_concedidos.lista_proyectos:
        importe_global += p.presupuesto
        ca = p.comunidad_autonoma
        
        # Inicializamos la CCAA si no existe en el diccionario
        if ca not in importes_por_ca:
            importes_por_ca[ca] = 0
        importes_por_ca[ca] += p.presupuesto
        
    print(f"Importe global total concedido: {importe_global:,.2f} €\n")
    print("Desglose del importe total por Comunidad Autónoma:")
    
    # Ordenamos el diccionario por valor monetario (item[1]) de mayor a menor (reverse=True)
    importes_ordenados = sorted(importes_por_ca.items(), key=lambda item: item[1], reverse=True)
    
    for ca, importe in importes_ordenados:
        # ':<25' alinea a la izquierda (25 espacios). ':>15,.2f' alinea a la derecha con separador de miles
        print(f" - {ca:<25}: {importe:>15,.2f} €")
    
    # =====================================================================
    # =====================================================================
    #                 INICIO DEL LABORATORIO 6
    # =====================================================================
    # =====================================================================

    # --- TAREAS 1 Y 2: TASAS Y FINANCIACIÓN POR CCAA ---
    print("\n" + "="*50)
    print(" LABORATORIO 6 - TAREAS 1 Y 2")
    print("="*50)
    
    print("\n--- 1. Tasa de Éxito por CCAA ---")
    tasas = gestor_todos.tasa_exito_ccaa(gestor_concedidos, gestor_contratos)
    for ca, datos in tasas.items():
        print(f"{ca:<20} -> Concedidos: {datos['tasa_concedidos']:>5.2f}% | Contratos: {datos['tasa_contratos']:>5.2f}%")

    print("\n--- 2. Financiación por Habitante ---")
    ruta_poblacion = ruta_datos / 'poblacion.xlsx'
    financiacion = gestor_todos.financiacion_por_habitante(gestor_concedidos, ruta_poblacion)
    
    financiacion_ordenada = sorted(financiacion.items(), key=lambda x: x[1], reverse=True)
    for ca, ratio in financiacion_ordenada:
        print(f"{ca:<20} -> {ratio:>6.2f} €/habitante")

    # --- TAREAS 3 Y 4: ENTIDADES Y MACROÁREAS ---
    print("\n" + "="*50)
    print(" LABORATORIO 6 - TAREAS 3 Y 4")
    print("="*50)
    
    n_top = 5
    print(f"\n--- 3. Top {n_top} Entidades con mayor éxito (Mín. 5 solicitudes) ---")
    top_conc, top_cont = gestor_todos.top_entidades_exito(gestor_concedidos, gestor_contratos, n=n_top)
    
    print(">> TOP EN PROYECTOS CONCEDIDOS:")
    # enumerate(lista, 1) nos da un contador automático que empieza en 1
    for i, (ent, datos) in enumerate(top_conc, 1):
        print(f" {i}. {ent[:40]:<40} | Tasa: {datos['tasa_concedidos']:>5.2f}% ({datos['solicitados']} sol.)")
        
    print("\n>> TOP EN CONTRATOS PREDOCTORALES:")
    for i, (ent, datos) in enumerate(top_cont, 1):
        print(f" {i}. {ent[:40]:<40} | Tasa: {datos['tasa_contratos']:>5.2f}% ({datos['solicitados']} sol.)")

    print("\n--- 4. Tasa de Éxito por Macro Áreas ---")
    tasas_macro = gestor_todos.tasa_exito_por_agrupacion(gestor_concedidos, gestor_contratos, tipo="macroarea")
    
    for macro, datos in tasas_macro.items():
        print(f"\n[{macro}]")
        print(f" Solicitados: {datos['solicitados']} | Concedidos: {datos['tasa_concedidos']:.2f}% | Contratos: {datos['tasa_contratos']:.2f}%")
    
    # --- TAREA 5: NUBE DE PALABRAS ---
    print("\n" + "="*50)
    print(" LABORATORIO 6 - TAREA 5 (Nube de Palabras)")
    print("="*50)
    print("Generando gráficos... ¡Atento a las ventanas emergentes (Matplotlib)!")
    
    gestor_todos.nube_de_palabras(gestor_contratos)

    # --- TAREA 6: SUBPROYECTOS HUÉRFANOS ---
    print("\n" + "="*50)
    print(" LABORATORIO 6 - TAREA 6 (Subproyectos Huérfanos)")
    print("="*50)
    print("Buscando secundarios sin dinero cuyo proyecto principal sí cobró...")
    
    huerfanos = gestor_todos.subproyectos_huerfanos(gestor_concedidos)
    print(f"\nSe han encontrado {len(huerfanos)} subproyectos huérfanos.")
    
    if len(huerfanos) > 0:
        print("Lista de referencias afectadas:")
        for ref in huerfanos:
            print(f" - {ref}")
    
    # --- TAREA 7: ORIENTADA VS BÁSICA ---
    print("\n" + "="*50)
    print(" LABORATORIO 6 - TAREA 7 (Orientada vs Básica)")
    print("="*50)
    
    datos_ori = gestor_todos.analisis_orientacion(gestor_concedidos)
    
    print(f"{'Tipo de Proyecto':<35} | {'Solicitados':>11} | {'Concedidos':>10} | {'Tasa Éxito':>11} | {'Presupuesto Total'}")
    print("-" * 95)
    for tipo, d in datos_ori.items():
        print(f"{d['nombre']:<35} | {d['solicitados']:>11} | {d['concedidos']:>10} | {d['tasa']:>10.2f}% | {d['dinero']:>15,.2f} €")

    mejor_ori = max(datos_ori.values(), key=lambda x: x['tasa'])
    print(f"\n>> RESPUESTA T7: Basado en la tasa de éxito, es estadísticamente mejor presentarse por: {mejor_ori['nombre']}.")

    # --- TAREA 8: INDIVIDUAL VS COORDINADO ---
    print("\n" + "="*50)
    print(" LABORATORIO 6 - TAREA 8 (Individual vs Coordinado)")
    print("="*50)
    
    datos_ind = gestor_todos.analisis_individual_vs_coordinado(gestor_concedidos)
    
    print(f"{'Modalidad':<15} | {'Solicitados':>11} | {'Concedidos':>10} | {'Tasa Éxito':>11}")
    print("-" * 55)
    for tipo, d in datos_ind.items():
        print(f"{tipo:<15} | {d['solicitados']:>11} | {d['concedidos']:>10} | {d['tasa']:>10.2f}%")

    mejor_ind = max(datos_ind.items(), key=lambda x: x[1]['tasa'])
    print(f"\n>> RESPUESTA T8: La modalidad con mayor probabilidad de éxito es la: {mejor_ind[0]}")


# =====================================================================
# PUNTO DE ENTRADA DEL SCRIPT
# =====================================================================
# Esta condición es un estándar en Python. Significa: 
# "Si el usuario ejecuta ESTE archivo directamente desde la terminal, 
# arranca la función main(). Si importa este archivo desde otro sitio, no hagas nada."
if __name__ == "__main__":
    main()