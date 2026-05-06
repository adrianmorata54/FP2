from factoria import FactoriaMetro

def main():
    """
    Punto de entrada principal del programa. 
    Coordina la carga de datos, validación del sistema, análisis de red,
    búsqueda de rutas y geolocalización.
    """
    
    # 1. RUTA AL ARCHIVO
    # Se utiliza una cadena 'raw' (r"") para evitar problemas con las barras invertidas en Windows.
    ruta = r"EJERCICIOS (TEORIA)\EJERCICIO 8\datos\líneas y estaciones Metro Madrid.xlsx"
    
    # 2. CARGA DE DATOS (Patrón Factoría)
    # Encapsulamos la complejidad de leer Excel/CSV en una clase externa.
    lineas_obj = FactoriaMetro.cargar_desde_excel(ruta)

    # 3. TRANSFORMACIÓN DE VISIONES (Líneas -> Estaciones)
    # El boletín pide poder ver la red desde la perspectiva de la estación (nodos).
    # Este método crea un objeto donde cada llave es una parada y contiene sus líneas.
    estaciones_obj = lineas_obj.crear_estaciones()
    
    # 4. COMPROBACIÓN DE RECIPROCIDAD (Estaciones -> Líneas)
    # Reconvertimos de vuelta para verificar que el proceso es reversible y no hay pérdida.
    lineas_recuperadas = estaciones_obj.crear_lineas()

    # 5. VERIFICACIÓN DE INTEGRIDAD (Identidad vs Igualdad)
    # Aquí aplicamos el concepto de igualdad lógica sobreescribiendo el método __eq__.
    print("\n--- Verificaciones de Sistema ---")
    if lineas_obj == lineas_recuperadas:
        print("✅ Éxito: La conversión es recíproca. Los datos son idénticos.")
    else:
        print("❌ Error: Se ha perdido información en la conversión.")

    # 6. ANÁLISIS DE LA RED (Métodos interesantes solicitados)
    print("\n--- Análisis de la Red ---")
    
    # Hubs: Estaciones neurálgicas donde convergen más líneas.
    hubs = estaciones_obj.estaciones_con_mas_lineas()
    print(f"Estación/es con más transbordos: {', '.join(hubs)}")
    
    # Conectividad: Determinar si el grafo está totalmente unido (sin islas).
    conexo = lineas_obj.es_conexo()
    print(f"¿Es la red de Metro totalmente conexa?: {'Sí' if conexo else 'No'}")
    
    # Análisis de líneas circulares: Comparación de inicio y fin de trayecto.
    l12 = "Linea 12"
    if l12 in lineas_obj._red:
        es_circ = lineas_obj.es_circular(l12)
        print(f"¿Es la {l12} una línea circular?: {'Sí' if es_circ else 'No'}")
    
    l6 = "Linea 6"
    if l6 in lineas_obj._red:
        es_circ = lineas_obj.es_circular(l6)
        print(f"¿Es la {l6} una línea circular?: {'Sí' if es_circ else 'No'}")
    
    # 7. LÍNEA MÁS CRÍTICA (Análisis de vulnerabilidad)
    # Calculamos qué línea dejaría más estaciones aisladas si dejara de dar servicio.
    print("\n--- Vulnerabilidad de la Red ---")
    critica = lineas_obj.linea_mas_critica()
    
    abs_info = critica['absoluto']
    prop_info = critica['proporcional']
    
    print(f"Línea más crítica (Valor Absoluto): {abs_info['linea']}")
    print(f"  -> Si cae, aísla a {abs_info['aisladas']} estaciones (de las {abs_info['total_estaciones']} que tiene).")
    
    print(f"Línea más crítica (Proporcional): {prop_info['linea']}")
    print(f"  -> Si cae, aísla al {prop_info['proporcion']:.2f}% de sus estaciones.")

    # 8. BÚSQUEDA DE RUTAS (Algoritmo BFS Generalizado)
    print("\n--- Buscador de Rutas Avanzado ---")
    
    # Prueba 1: Restricción máxima (Sin transbordos).
    origen_directo, destino_directo = "Sol", "Cuatro Caminos"
    print(f"\n1️⃣ Buscando ruta SIN transbordos ({origen_directo} -> {destino_directo}):")
    ruta0 = lineas_obj.buscar_ruta(origen_directo, destino_directo, max_transbordos=0)
    if "error" in ruta0:
        print(f"❌ {ruta0['error']}")
    else:
        print("✅ " + " | ".join(ruta0["instrucciones"]))
        print(f"📍 Camino: {' -> '.join(ruta0['camino'])}")

    # Prueba 2: Ruta con límite de transbordos (Caso complejo).
    origen_lejos, destino_lejos = "Pinar de Chamartín", "Príncipe Pío"
    print(f"\n2️⃣ Buscando ruta con MÁXIMO 1 transbordo ({origen_lejos} -> {destino_lejos}):")
    ruta1 = lineas_obj.buscar_ruta(origen_lejos, destino_lejos, max_transbordos=1)
    if "error" in ruta1:
        print(f"❌ {ruta1['error']}")
    else:
        print("✅ Ruta encontrada")
        print("✅ " + " | ".join(ruta1["instrucciones"]))
        print(f"📍 Camino: {' -> '.join(ruta1['camino'])}")

    # Prueba 3: Ruta óptima libre (Búsqueda del camino más corto global).
    print(f"\n3️⃣ Buscando la ruta libre ({origen_lejos} -> {destino_lejos}):")
    ruta_libre = lineas_obj.buscar_ruta(origen_lejos, destino_lejos) 
    if "error" in ruta_libre:
        print(f"❌ {ruta_libre['error']}")
    else:
        print(f"✅ Encontrada con {ruta_libre['transbordos']} transbordos y {ruta_libre['paradas_totales']} paradas.")
        print("📝 Instrucciones:")
        for paso in ruta_libre['instrucciones']:
            print(f"  {paso}")
        print(f"📍 Camino exacto:\n  {' -> '.join(ruta_libre['camino'])}")
    
    # 9. RETO OPCIONAL: API GEOGRÁFICA Y HAVERSINE
    # Conexión real a OpenStreetMap para obtener latitud/longitud y calcular distancias.
    print("\n--- Conexión a Satélite (OpenStreetMap) ---")
    
    origen_geo = "Sol"
    destino_geo = "Plaza Castilla"
    print(f"📡 Buscando coordenadas de '{origen_geo}' y '{destino_geo}' en Internet...")
    
    resultado_geo = estaciones_obj.distancia_real_km(origen_geo, destino_geo)
    
    if "error" in resultado_geo:
        print(f"❌ {resultado_geo['error']}")
    else:
        e1 = resultado_geo['estacion1']
        e2 = resultado_geo['estacion2']
        dist = resultado_geo['distancia_km']
        
        print(f"✅ ¡Coordenadas obtenidas!")
        print(f"  📍 {e1['nombre']}: Latitud {e1['coords'][0]:.4f}, Longitud {e1['coords'][1]:.4f}")
        print(f"  📍 {e2['nombre']}: Latitud {e2['coords'][0]:.4f}, Longitud {e2['coords'][1]:.4f}")
        print(f"📏 Distancia en línea recta (vuelo de pájaro): {dist:.2f} km")

if __name__ == "__main__":
    main()