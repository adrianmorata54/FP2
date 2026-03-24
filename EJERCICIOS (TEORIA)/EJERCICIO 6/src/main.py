from factoria import FactoriaElecciones

if __name__ == "__main__":
    print("Iniciando programa de análisis electoral...")
    nacion = FactoriaElecciones.cargar_datos()
    
    if nacion:
        print("\n" + "="*50)
        print("  📊 ANÁLISIS DE RESULTADOS ELECTORALES 📊")
        print("="*50)

        # --- PREGUNTA 2 ---
        nacion.analizar_votos_nulos_blancos()
        
        # --- PREGUNTA 3 ---
        nacion.analizar_participacion_cera_real()
        
        # --- PREGUNTA 4 ---
        nacion.partidos_en_n_circunscripciones(50) # Cambia el 50 por el número que quieras probar
        
        # --- PREGUNTA 5 ---
        nacion.cera_proporcion_poblacion()
        
        # --- PREGUNTA 6 ---
        nacion.escanos_por_circunscripcion("Huelva")
        
        # --- PREGUNTA 7 ---
        nacion.comprobar_escanos_oficiales() 
        
        # --- PREGUNTA 9 ---
        nacion.analizar_ultimo_escano()
        
        # --- PREGUNTAS 10 y 11 ---
        nacion.analizar_coste_escanos()
        
        # --- PREGUNTA 12 ---
        nacion.circunscripciones_escanos_baratos()
        
        # --- PREGUNTA 13 ---
        nacion.partido_mas_votado_sin_escano()
        
        # --- PREGUNTA 14 ---
        nacion.peores_parejas_partido_circunscripcion(5)
        
        # --- PREGUNTA 15 ---
        nacion.pactometro(escanos_necesarios=176) # 176 es la mayoría absoluta
        
        
        # --- PREGUNTAS 1 y 8: GRÁFICOS MULTINIVEL ---
        print("\n" + "="*50)
        print("   📈 GENERANDO GRÁFICOS ELECTORALES (P1 y P8)")
        print("="*50)
        print("💡 NOTA: Cierra la ventana de un gráfico para que el programa continúe y aparezca el siguiente.\n")
        
        # 1. Nivel Nacional
        print("📊 1/3: Generando gráfico a nivel NACIONAL...")
        nacion.graficar_resultados(nivel="nacional")
        
        # 2. Nivel Comunidad Autónoma (Asegúrate de que el nombre coincide EXACTO con tu Excel)
        print("\n📊 2/3: Generando gráfico a nivel AUTONÓMICO (Andalucía)...")
        nacion.graficar_resultados(nivel="ccaa", nombre_filtro="Andalucía") 
        
        # 3. Nivel Circunscripción (Asegúrate de que el nombre coincide EXACTO con tu Excel)
        print("\n📊 3/3: Generando gráfico a nivel PROVINCIAL (Sevilla)...")
        nacion.graficar_resultados(nivel="circunscripcion", nombre_filtro="Sevilla")

        print("\n✅ ¡Ejecución del programa completada con éxito!")
    else:
        print("❌ Error: No se pudo cargar la información de la nación desde la factoría.")