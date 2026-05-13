from factoria import FactoriaMetro
from linea import Linea
from estacion import Estacion

def main():
    """
    Punto de entrada principal del programa. 
    Coordina la carga de datos, validación del sistema, análisis de red,
    búsqueda de rutas y geolocalización (Adaptado a Boletín 9 con Objetos).
    """
    
    # 1. RUTA AL ARCHIVO
    # Se utiliza una cadena 'raw' (r"") para evitar problemas con las barras invertidas en Windows.
    ruta = r"EJERCICIOS (TEORIA)\EJERCICIO 8\datos\líneas y estaciones Metro Madrid.xlsx"
    
    # 2. CARGA DE DATOS (Patrón Factoría)
    # Encapsulamos la complejidad de leer Excel/CSV en una clase externa.
    # Ahora la factoría carga los objetos Linea y Estacion con sus coordenadas.
    lineas_obj = FactoriaMetro.cargar_desde_excel(ruta)

    # 3. TRANSFORMACIÓN DE VISIONES (Líneas -> Estaciones)
    # El boletín pide poder ver la red desde la perspectiva de la estación (nodos).
    # Este método crea un objeto donde cada llave es una parada y contiene sus líneas.
    estaciones_obj = lineas_obj.to_estaciones()
    
    # 4. COMPROBACIÓN DE RECIPROCIDAD (Estaciones -> Líneas)
    # Reconvertimos de vuelta para verificar que el proceso es reversible y no hay pérdida.
    lineas_recuperadas = estaciones_obj.to_lineas()

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
    # Ahora hubs es una lista de objetos, imprimimos sus nombres
    print(f"Estación/es con más transbordos: {', '.join([h.nombre for h in hubs])}")
    
    # Conectividad: Determinar si el grafo está totalmente unido (sin islas).
    conexo = lineas_obj.es_conexo()
    print(f"¿Es la red de Metro totalmente conexa?: {'Sí' if conexo else 'No'}")
    
    # Análisis de líneas circulares: Comparación leyendo la propiedad del objeto.
    # Buscamos los objetos concretos en nuestro grafo
    l12 = next((l for l in lineas_obj.grafo_lineas if l.nombre == "Linea 12"), None)
    if l12:
        print(f"¿Es la {l12.nombre} una línea circular?: {'Sí' if l12.escircular else 'No'}")
    
    l6 = next((l for l in lineas_obj.grafo_lineas if l.nombre == "Linea 6"), None)
    if l6:
        print(f"¿Es la {l6.nombre} una línea circular?: {'Sí' if l6.escircular else 'No'}")
    
    # 7. LÍNEA MÁS CRÍTICA (Análisis de vulnerabilidad)
    print("\n--- Vulnerabilidad de la Red ---")
    criticas = lineas_obj.lineas_criticas()
    if criticas:
        nombres_criticas = [c.nombre for c in criticas]
        print(f"Líneas críticas (Si caen, aíslan estaciones): {', '.join(nombres_criticas)}")
    else:
        print("No hay líneas críticas absolutas en esta red.")

    # 8. BÚSQUEDA DE RUTAS (Algoritmo BFS Generalizado)
    print("\n--- Buscador de Rutas Avanzado ---")
    
    # Prueba: Ruta óptima libre (Búsqueda del camino más corto global).
    origen_lejos, destino_lejos = "Pinar de Chamartín", "Príncipe Pío"
    print(f"\nBuscando la ruta libre ({origen_lejos} -> {destino_lejos}):")
    ruta_libre = lineas_obj.buscar_ruta(origen_lejos, destino_lejos) 
    
    if "error" in ruta_libre:
        print(f"❌ {ruta_libre['error']}")
    else:
        print(f"✅ Encontrada ruta con {ruta_libre['paradas']} paradas.")
        # camino es una lista de objetos Estacion, extraemos los nombres
        nombres_camino = [est.nombre for est in ruta_libre['camino']]
        print(f"📍 Camino exacto:\n  {' -> '.join(nombres_camino)}")
    
    # 9. RETO OPCIONAL: API GEOGRÁFICA Y HAVERSINE
    print("\n--- Conexión a Satélite (Coordenadas pre-cargadas) ---")
    
    origen_geo = "Sol"
    destino_geo = "Plaza Castilla"
    print(f"📡 Calculando distancia entre '{origen_geo}' y '{destino_geo}'...")
    
    e1 = next((e for e in estaciones_obj.grafo_estaciones if e.nombre == origen_geo), None)
    e2 = next((e for e in estaciones_obj.grafo_estaciones if e.nombre == destino_geo), None)
    
    if e1 and e2:
        # AÑADIMOS ESTA LÍNEA DE SEGURIDAD: Comprobamos que sí haya coordenadas
        if e1.latitud is not None and e2.latitud is not None:
            dist = lineas_obj.distancia_km(e1, e2)
            print(f"✅ ¡Coordenadas procesadas!")
            print(f"  📍 {e1.nombre}: Latitud {e1.latitud:.4f}, Longitud {e1.longitud:.4f}")
            print(f"  📍 {e2.nombre}: Latitud {e2.latitud:.4f}, Longitud {e2.longitud:.4f}")
            print(f"📏 Distancia en línea recta (vuelo de pájaro): {dist:.2f} km")
        else:
            print("❌ Error: La API no pudo conseguir las coordenadas de estas estaciones y están vacías.")
    else:
        print("❌ Error: Una de las estaciones no existe.")

if __name__ == "__main__":
    main()