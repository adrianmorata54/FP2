from factoria import Factoria

def mostrar_diccionario(titulo, diccionario, formato_valor="{:.0f}"):
    """Función auxiliar solo para imprimir bonito en consola"""
    print(f"\n{'-'*10} {titulo} {'-'*10}")
    # Ordenamos por clave (coeficiente) para que salga ordenado visualmente
    for clave in sorted(diccionario.keys()):
        valor = diccionario[clave]
        # Usamos .format para dar formato al valor (enteros o decimales)
        print(f"   Coeficiente {clave}: {formato_valor.format(valor)}")
    print("-" * 60)


if __name__ == "__main__":
    print("=" * 70)
    print("   SISTEMA DE GESTIÓN DE DEPARTAMENTOS - UNIVERSIDAD DE SEVILLA")
    print("=" * 70)

    # ---------------------------------------------------------
    # FASE 1: LECTURA DEL PDF (EJERCICIO 2)
    # ---------------------------------------------------------
    print("\n📂 [FASE 1] Cargando datos desde el PDF...")
    mi_uni = Factoria.leer_universidad("departamentos.pdf")
    
    # Comprobamos si cargó algo
    if len(mi_uni.obtener_departamentos()) == 0:
        print("❌ Error: No se han cargado departamentos. Revisa la lectura.")
        exit()

    print(f"✅ ¡Éxito! {mi_uni}\n")


    # ---------------------------------------------------------
    # RESULTADOS EJERCICIO 2 (ESTADÍSTICAS Y EXPERIMENTALIDAD)
    # ---------------------------------------------------------
    print("📊 RESULTADOS DEL BOLETÍN 2:")
    
    # APARTADO 1: Número de departamentos por coeficiente
    distribucion = mi_uni.distribucion_experimentalidad()
    mostrar_diccionario("1) DISTRIBUCIÓN POR EXPERIMENTALIDAD", distribucion, "{:.0f} deptos")

    # APARTADO 2: Media de carga por coeficiente
    medias = mi_uni.media_carga_por_experimentalidad()
    mostrar_diccionario("2) MEDIA DE CARGA DOCENTE REAL POR EXPERIMENTALIDAD", medias, "{:.4f}")

    # APARTADO 3: Coeficientes extremos (Mayor y Menor media)
    max_coef, min_coef = mi_uni.coeficientes_extremos_carga()
    print("\n--- 3) COEFICIENTES CON MEDIAS EXTREMAS ---")
    print(f"   📈 MAYOR media de carga: Coeficiente {max_coef} (Media: {medias[max_coef]:.4f})")
    print(f"   📉 MENOR media de carga: Coeficiente {min_coef} (Media: {medias[min_coef]:.4f})")
    print("-" * 60)

    # APARTADO EXTRA: Top Departamentos
    print("\n--- EXTRA) TOP 3 DEPARTAMENTOS CON MÁS CARGA ---")
    top3 = mi_uni.departamentos_mayor_carga(3)
    for i, d in enumerate(top3, 1):
        print(f"   {i}. {d.nombre} (Carga: {d.carga_docente_real:.4f})")
    print("-" * 60)


# ---------------------------------------------------------
    # FASE 2: WEB SCRAPING Y FUSIÓN (EJERCICIO 3)
    # ---------------------------------------------------------
    print("\n\n🌐 [FASE 2] Iniciando Web Scraping de Sedes...")
    diccionario_web = Factoria.extraer_sedes_web() 
    
    # PARCHE MANUAL: El departamento de "Ciencias Jurídicas Básicas" no figura 
    # correctamente en el listado actual de la web de la US. 
    # Inyectamos su sede manualmente ANTES del cruce para intentar mitigar la asimetría.
    diccionario_web["DEPARTAMENTO DE CIENCIAS JURÍDICAS BÁSICAS"] = "FACULTAD DE DERECHO"

    print("\n🔗 Cruzando datos del PDF con la Web...")
    fallos = mi_uni.asignar_sedes(diccionario_web)
    print(f"✅ Fusión completada. Fallos de coincidencia documentados: {fallos}\n")


    # ---------------------------------------------------------
    # RESULTADOS EJERCICIO 3 (EXTREMOS POR SEDE Y MEDIAS)
    # ---------------------------------------------------------
    print("🏢 RESULTADOS DEL BOLETÍN 3: ANÁLISIS POR FACULTAD/SEDE\n")
    
    # 1️⃣ CÁLCULO E IMPRESIÓN DE MEDIAS POR SEDE
    print("--- 🏫 MEDIA DE CARGA DOCENTE POR SEDE ---")
    
    # Llamamos al método que ahora nos devuelve un diccionario {sede: media}
    medias_sedes = mi_uni.media_carga_por_sede()
    
    for sede, media in medias_sedes.items():
        if media > 0:
            print(f"📍 {sede}: {media:.2f} carga/profesor")
        else:
            print(f"📍 {sede}: No hay profesores para calcular la media.")
            
    print("\n" + "=" * 70)
    print("🏆 EXTREMOS DE CARGA DOCENTE POR SEDE")
    print("=" * 70)
    
    # 2️⃣ CÁLCULO E IMPRESIÓN DE EXTREMOS (Mayor y menor carga)
    extremos = mi_uni.obtener_extremos_por_sede()
    
    for sede, (d_mayor, d_menor) in extremos.items():
        print(f"📍 Sede: {sede}")
        
        if d_mayor == d_menor:
            print(f"   🔸 Único departamento: {d_mayor.nombre} (Carga: {d_mayor.carga_docente_real})")
        else:
            print(f"   🔺 MAYOR carga: {d_mayor.nombre} (Carga: {d_mayor.carga_docente_real})")
            print(f"   🔻 MENOR carga: {d_menor.nombre} (Carga: {d_menor.carga_docente_real})")
            
        print("-" * 70)
        
    print("\n🚀 EJECUCIÓN FINALIZADA CON ÉXITO.")
    print("=" * 70)

# NUEVO EJERCICIO: diccionario con claves (sedes) y valores (media de coeficiente de carga docente X nºprofesores) riquelem@us.es