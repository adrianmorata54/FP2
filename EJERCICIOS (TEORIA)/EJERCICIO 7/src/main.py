import os
import sys
from factoria import Factoria

def main():
    ruta_src = os.path.dirname(os.path.abspath(__file__))
    ruta_excel = os.path.abspath(os.path.join(ruta_src, '..', 'datos', 'frecuencia_nombres.xlsx'))
    
    print("Iniciando la lectura del Excel...")
    
    try:
        nomenclador = Factoria.crear_desde_excel(ruta_excel)
        print(f"¡Carga completada! Se han procesado {len(nomenclador.nombres)} nombres únicos.\n")
    except FileNotFoundError as e:
        print(f"\n❌ ERROR CRÍTICO: No se encuentra el archivo.")
        print(f"   Detalles: {e}")
        print("   Por favor, revisa que el archivo 'frecuencia_nombres.xlsx' esté en la carpeta 'datos'.")
        sys.exit(1)

    
    # ======================================================================
    # BLOQUE 1: RESULTADOS SEMANA 1 (EJERCICIOS 1 AL 8)
    # ======================================================================
    print("="*60)
    print("           RESULTADOS BOLETÍN 7 - SEMANA 1")
    print("="*60)

    print(f"2. Nombre de hombre con mayor frec. absoluta: {nomenclador.mayor_frecuencia_absoluta('H')}")
    print(f"3. Top 5 nombres históricos de mujer: {nomenclador.n_mas_usados(5, 'M')}")
    
    dicc_iniciales = nomenclador.frecuencia_por_inicial('M')
    print(f"4. Evolución de la inicial 'A' en mujeres: {dicc_iniciales.get('A', [])}")
    print(f"5. Letra más frecuente en mujeres en 2020: {nomenclador.letra_mas_frecuente_por_decada('M').get(2020)}")
    
    evolucion_c = nomenclador.evolucion_compuestos('H')
    print(f"6. Evolución compuestos Hombres (1920 y 2020): {evolucion_c[0]} ... {evolucion_c[-1]}")
    
    long_media = nomenclador.longitud_media_por_decada('M')
    print(f"7. Longitud media Mujeres (1920 y 2020): {long_media[0]} ... {long_media[-1]}")
    print(f"8. Mujeres en el top durante al menos 9 décadas: {nomenclador.en_top_n_decadas(9, 'M')}")
    
    # --- MEJORA: Control de errores en la escritura (Permisos) ---
    ruta_salida = os.path.abspath(os.path.join(ruta_src, '..', 'datos', 'resultado_nomenclator.xlsx'))
    print(f"\n1. Exportando a Excel en: {ruta_salida}")
    try:
        nomenclador.exportar_a_excel(ruta_salida)
        print("   ✅ Archivo guardado correctamente.")
    except PermissionError:
        print("   ❌ ERROR: No se pudo guardar. ¿Tienes 'resultado_nomenclator.xlsx' abierto en Excel? Ciérralo y vuelve a intentar.")
    except Exception as e:
        print(f"   ❌ ERROR INESPERADO al guardar: {e}")


    # ======================================================================
    # BLOQUE 2: RESULTADOS SEMANA 2 (EJERCICIOS 9 AL 15)
    # ======================================================================
    print("\n" + "="*60)
    print("           RESULTADOS BOLETÍN 7 - SEMANA 2")
    print("="*60)

    olvidados_h = nomenclador.de_moda_y_olvidados(2, 'H')
    print(f"9. Hombres clásicos (moda las 2 primeras dec. y olvidados): {olvidados_h[:5]}...")
    
    nuevos_m = nomenclador.recientes_y_nuevos(2, 'M')
    print(f"10. Mujeres modernas (moda solo últimas 2 dec.): {nuevos_m[:5]}...")
    
    resurgidos = nomenclador.nombres_resurgidos(1, 2, 'M')
    print(f"11. Mujeres resurgidas (patrón 1-0-1): {resurgidos}")
    
    mayor_inc = nomenclador.mayor_incremento_absoluto(3, 'H')
    print(f"13. Top 3 hombres con mayor incremento repentino: {mayor_inc}")
    
    diversidad = nomenclador.diversificacion_nombres(5, 'M')
    print(f"14. Diversificación (Suma PMil top 5 mujeres): {diversidad}")

    # --- GRÁFICAS (EJERCICIOS 12 Y 15) ---
    print("\n" + "-"*60)
    print("GENERANDO GRÁFICAS... (Cierra la primera ventana para ver la segunda)")
    
    nomenclador.grafica_tendencia(['MARIA', 'LUCIA', 'MARTINA'])
    nomenclador.grafica_diversificacion(10, 'H')
    
    print("\n¡Boletín completo finalizado con éxito!")

if __name__ == "__main__":
    main()