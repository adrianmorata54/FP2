# src/main.py

# Importamos Path para manejar rutas de archivos de forma profesional y compatible
from pathlib import Path
# Importamos nuestra Factoría, que es la que hará el trabajo duro
from factoria import Factoria

def main():
    # =====================================================================
    # 0. CONFIGURACIÓN DE RUTAS DINÁMICAS
    # =====================================================================
    ruta_base = Path(__file__).resolve().parent.parent
    
    # Ahora bajamos a la carpeta 'datos'
    ruta_datos = ruta_base / 'datos'

    print("Cargando datos de la carpeta 'datos', por favor espera...")
    
    # Unimos la carpeta 'datos' con el nombre exacto de cada Excel
    ruta_anexo1 = ruta_datos / 'Anexo I.xlsx'
    ruta_anexo2 = ruta_datos / 'Anexo II.xlsx'
    ruta_anexo3 = ruta_datos / 'Anexo III.xlsx'
    ruta_anexo4 = ruta_datos / 'Anexo IV.xlsx'

    # Bucle de seguridad: antes de que el programa explote intentando leer 
    # algo que no existe, comprobamos si los archivos están ahí con .exists()
    archivos_requeridos = [ruta_anexo1, ruta_anexo2, ruta_anexo3, ruta_anexo4]
    for ruta in archivos_requeridos:
        if not ruta.exists():
            print(f"⚠️ Error: No se encuentra el archivo en {ruta}")
            return # Detiene la ejecución del programa si falta algún Excel

    # =====================================================================
    # 1. EJECUCIÓN DEL PROCESAMIENTO
    # =====================================================================
    # Le pasamos las rutas a nuestra Factoría. Ella hace su magia y nos 
    # devuelve ('return') las 3 cajas llenas de objetos.
    gestor_todos, gestor_concedidos, gestor_contratos = Factoria.leer_datos(
        ruta_anexo1, ruta_anexo2, ruta_anexo3, ruta_anexo4
    )
    
    # =====================================================================
    # APARTADO 1: Mostrar el total de registros almacenados
    # =====================================================================
    print("\n" + "="*40)
    print(" 1. TOTAL DE REGISTROS ALMACENADOS")
    print("="*40)
    
    # Aquí es donde brilla el ENCAPSULAMIENTO que vimos en gestor.py.
    # No tocamos las listas, simplemente le pedimos al gestor: "dime tu total()"
    print(f"Total proyectos (solicitados y denegados): {gestor_todos.total()} (Esperado: 7092)")
    print(f"Total proyectos concedidos:               {gestor_concedidos.total()} (Esperado: 3252)")
    print(f"Total proyectos con contrato predoctoral: {gestor_contratos.total()} (Esperado: 1149)")

    # =====================================================================
    # APARTADO 2: Tasa de proyectos concedidos sobre solicitados por CCAA
    # =====================================================================
    print("\n" + "="*40)
    print(" 2. TASA DE ÉXITO POR COMUNIDAD AUTÓNOMA")
    print("="*40)
    
    comunidad_objetivo = "ANDALUCIA" 
    
    # LIST COMPREHENSION (Comprensión de listas): Es una forma "Pythonica" y rápida 
    # de filtrar. Se lee: "Guarda 'p' (cada proyecto) de la lista global, SOLO SI 
    # su comunidad autónoma es igual a Andalucía".
    solicitados_ca = [p for p in gestor_todos.lista_proyectos if p.comunidad_autonoma == comunidad_objetivo]
    
    # Hacemos lo mismo, pero filtrando la lista anterior para quedarnos solo 
    # con los que tienen el atributo 'concedido' a True.
    concedidos_ca = [p for p in solicitados_ca if p.concedido]
    
    # Calculamos el porcentaje (para evitar dividir por cero, comprobamos que > 0)
    if len(solicitados_ca) > 0:
        tasa = (len(concedidos_ca) / len(solicitados_ca)) * 100
        print(f"Comunidad: {comunidad_objetivo}")
        print(f"Proyectos Solicitados: {len(solicitados_ca)}")
        print(f"Proyectos Concedidos:  {len(concedidos_ca)}")
        print(f"Tasa de éxito:         {tasa:.2f}%") # :.2f formatea a 2 decimales
    else:
        print(f"No hay registros para la comunidad '{comunidad_objetivo}'.")

    # =====================================================================
    # APARTADO 3: Total de importes global y por comunidad autónoma
    # =====================================================================
    print("\n" + "="*40)
    print(" 3. IMPORTES GLOBALES Y POR COMUNIDAD")
    print("="*40)
    
    importe_global = 0
    importes_por_ca = {} # Usamos un DICCIONARIO para agrupar (clave: CCAA, valor: Dinero)

    # Recorremos la lista de proyectos aprobados
    for p in gestor_concedidos.lista_proyectos:
        
        # 1. Sumamos al bote global usando la @property 'presupuesto' de la clase
        importe_global += p.presupuesto
        
        # 2. Sumamos al bote de su comunidad
        ca = p.comunidad_autonoma
        # Si es la primera vez que vemos esta comunidad, la creamos en el diccionario con 0€
        if ca not in importes_por_ca:
            importes_por_ca[ca] = 0
        # Le sumamos el presupuesto de este proyecto a su comunidad
        importes_por_ca[ca] += p.presupuesto
        
    # Imprimimos el total formateado (la coma hace de separador de miles en Python)
    print(f"Importe global total concedido: {importe_global:,.2f} €\n")
    print("Desglose del importe total por Comunidad Autónoma:")
    
    # ORDENAR EL DICCIONARIO:
    # .items() convierte el diccionario en una lista de tuplas: [('ANDALUCIA', 82000), ('MADRID', 113000)...]
    # lambda item: item[1] significa "ordena fijándote en el elemento 1 de la tupla (el dinero)".
    # reverse=True lo ordena de mayor a menor.
    importes_ordenados = sorted(importes_por_ca.items(), key=lambda item: item[1], reverse=True)
    
    # Recorremos la lista ya ordenada y la imprimimos bonita
    # :<25 alinea el texto a la izquierda ocupando 25 espacios. :>15 alinea los números a la derecha.
    for ca, importe in importes_ordenados:
        print(f" - {ca:<25}: {importe:>15,.2f} €")

# Este bloque final es un estándar en Python. Significa: "Si ejecuto este archivo 
# directamente desde la terminal, arranca la función main(). Pero si lo importo 
# desde otro archivo, no hagas nada automático".
if __name__ == "__main__":
    main()