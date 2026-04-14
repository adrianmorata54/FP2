import os
from factoria import Factoria

def main():
    ruta_src = os.path.dirname(os.path.abspath(__file__))
    ruta_excel = os.path.abspath(os.path.join(ruta_src, '..', 'datos', 'frecuencia_nombres.xlsx'))
    
    print("Iniciando la lectura del Excel...")
    nomenclador = Factoria.crear_desde_excel(ruta_excel)
    print(f"¡Carga completada! Se han procesado {len(nomenclador.nombres)} nombres únicos.\n")
    
    print("="*50)
    print(" RESULTADOS BOLETÍN 7 - SEMANA 1 (EJERCICIOS 1 AL 8) ")
    print("="*50)

    # Ejercicio 2
    print(f"2. Nombre de hombre con mayor frec. absoluta: {nomenclador.mayor_frecuencia_absoluta('H')}")
    
    # Ejercicio 3
    print(f"3. Top 5 nombres históricos de mujer: {nomenclador.n_mas_usados(5, 'M')}")
    
    # Ejercicio 4
    # (Imprimimos solo la inicial 'A' de mujeres para no saturar la pantalla)
    dicc_iniciales = nomenclador.frecuencia_por_inicial('M')
    print(f"4. Evolución de la inicial 'A' en mujeres: {dicc_iniciales.get('A', [])}")
    
    # Ejercicio 5
    print(f"5. Letra más frecuente en mujeres en 2020: {nomenclador.letra_mas_frecuente_por_decada('M').get(2020)}")
    
    # Ejercicio 6
    evolucion_c = nomenclador.evolucion_compuestos('H')
    print(f"6. Evolución compuestos Hombres (1920 y 2020): {evolucion_c[0]} ... {evolucion_c[-1]}")
    
    # Ejercicio 7
    long_media = nomenclador.longitud_media_por_decada('M')
    print(f"7. Longitud media Mujeres (1920 y 2020): {long_media[0]} ... {long_media[-1]}")
    
    # Ejercicio 8
    print(f"8. Mujeres en el top durante al menos 9 décadas: {nomenclador.en_top_n_decadas(9, 'M')}")
    
    # Ejercicio 1 (Lo ponemos al final para que exporte tranquilamente)
    ruta_salida = os.path.abspath(os.path.join(ruta_src, '..', 'datos', 'resultado_nomenclator.xlsx'))
    print(f"\n1. Exportando a Excel en: {ruta_salida}")
    nomenclador.exportar_a_excel(ruta_salida)
    print("¡Todo listo!")

if __name__ == "__main__":
    main()