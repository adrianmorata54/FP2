import os
from lector import LectorDatos

def imprimir_comparativa(numero_ejercicio, titulo, obtenidos, esperados):
    """
    Función auxiliar para imprimir por consola de forma limpia y ordenada
    el resultado que calcula nuestro código frente al que espera el profesor.
    """
    print(f"\n[{numero_ejercicio}] {titulo}")
    print("=" * 70)
    print("  RESULTADO OBTENIDO (Calculado por nuestro código):")
    if isinstance(obtenidos, list):
        for o in obtenidos: print(f"    {o}")
    else:
        print(f"    {obtenidos}")
        
    print("\n  RESULTADO ESPERADO (Según PDF del profesor):")
    if isinstance(esperados, list):
        for e in esperados: print(f"    {e}")
    else:
        print(f"    {esperados}")
    print("-" * 70)

def main():
    # 1. Configurar rutas relativas para que funcione en cualquier ordenador
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_datos = os.path.join(directorio_actual, '..', 'datos', 'Plantillas1D-2017-18.xls')
    
    # 2. Cargar la base de datos (Esto tardará unos segundos la primera vez)
    print("Cargando la base de datos histórica... (Por favor, espera un momento)")
    mi_liga = LectorDatos.construir_liga(ruta_datos)
    
    print("\n" + "#"*70 + "\n RESOLUCIÓN BOLETÍN 4 - PRIMERA SEMANA (Ejercicios 1 al 16)\n" + "#"*70)

    # ---------------------------------------------------------
    # EJERCICIOS INDIVIDUALES (1 al 6)
    # ---------------------------------------------------------
    imprimir_comparativa("Ejercicio 1", "Estadísticas de Temporada",
                         mi_liga.estadisticas_jugador("MESSI", "2011-12"),
                         "MESSI (F.C. Barcelona - Temporada 2011-12) | Partidos: 37 | Goles: 50")
                         
    imprimir_comparativa("Ejercicio 2", "Goles Históricos Totales",
                         mi_liga.goles_totales("MESSI"),
                         "MESSI: 383 goles")
                         
    imprimir_comparativa("Ejercicio 3", "Historial de Equipos",
                         mi_liga.historial_equipos("ARANDA, C."),
                         "ARANDA, C. - Equipos: C.D. Numancia, Sevilla F.C., C. At. Osasuna, Albacete Balomp., Levante U.D., Real Zaragoza CD, Granada C.F., Villarreal C.F.")
                         
    imprimir_comparativa("Ejercicio 4", "Partidos y Equipo Principal",
                         mi_liga.partidos_y_equipo_principal("RAUL GONZALEZ"),
                         "RAUL GONZALEZ - Equipo: Real Madrid C.F., Partidos: 550")
                         
    imprimir_comparativa("Ejercicio 5", "Minutos Totales",
                         mi_liga.minutos_totales("ZUBIZARRETA"),
                         "ZUBIZARRETA con 55746 minutos.")
                         
    imprimir_comparativa("Ejercicio 6", "Historial de Equipos (Varios Jugadores)",
                         [mi_liga.historial_equipos2("JULIO SALINAS"), 
                          mi_liga.historial_equipos2("SALVA B."),
                          mi_liga.historial_equipos2("ARIZMENDI")],
                         ["JULIO SALINAS - Equipos: Real S. de Gijón, C.D. Alavés, R.C. Deportivo, F.C. Barcelona, Athletic Club, At. de Madrid",
                          "SALVA B. - Equipos: Málaga C.F., Sevilla F.C., Levante U.D., Real Racing Club, At. de Madrid, Valencia C.F.",
                          "ARIZMENDI - Equipos: Getafe C.F., R.C. Deportivo, Real Zaragoza CD, Real Racing Club, Valencia C.F., R.C.D. Mallorca"])

    # ---------------------------------------------------------
    # EJERCICIOS GLOBALES Y RANKINGS (7 al 16)
    # ---------------------------------------------------------
    imprimir_comparativa("Ejercicio 7", "Rachas de Temporadas Seguidas",
                         mi_liga.ranking_temporadas_seguidas(5),
                         ["GAINZA - Equipo: Athletic Club, Temporadas seguidas: 19",
                          "GENTO - Equipo: Real Madrid C.F., Temporadas seguidas: 18",
                          "IRIBAR - Equipo: Athletic Club, Temporadas seguidas: 18",
                          "M. SANCHIS - Equipo: Real Madrid C.F., Temporadas seguidas: 18",
                          "ADELARDO - Equipo: At. de Madrid, Temporadas seguidas: 17"])

    imprimir_comparativa("Ejercicio 8", "Minutos jugados juntos",
                         mi_liga.ranking_minutos_juntos(10),
                         ["GORRIZ & LARRAÑAGA - Equipo: Real Sociedad, Minutos juntos: 76143",
                          "ARCONADA & ZAMORA - Equipo: Real Sociedad, Minutos juntos: 74867",
                          "JIMENEZ, M. & JOAQUIN A. - Equipo: Real S. de Gijón, Minutos juntos: 73167",
                          "CHENDO & M. SANCHIS - Equipo: Real Madrid C.F., Minutos juntos: 70757",
                          "PUYOL & XAVI - Equipo: F.C. Barcelona, Minutos juntos: 68786",
                          "M. SANCHIS & MICHEL - Equipo: Real Madrid C.F., Minutos juntos: 68320",
                          "IRIBAR & ROJO I - Equipo: Athletic Club, Minutos juntos: 67917",
                          "GAJATE & GORRIZ - Equipo: Real Sociedad, Minutos juntos: 65973",
                          "VICTOR VALDES & XAVI - Equipo: F.C. Barcelona, Minutos juntos: 65124",
                          "J.M. GUTI & RAUL GONZALEZ - Equipo: Real Madrid C.F., Minutos juntos: 64884"])

    imprimir_comparativa("Ejercicio 9", "Más partidos enteros jugados",
                         mi_liga.ranking_partidos_completos(3),
                         ["- N'KONO: 241 partidos enteros jugados.",
                          "- ESNAOLA: 166 partidos enteros jugados.",
                          "- MATE: 148 partidos enteros jugados."])

    imprimir_comparativa("Ejercicio 10", "Equipos con más tarjetas conjuntas en una temporada",
                         mi_liga.ranking_equipos_tarjeteros_temporada(3),
                         ["- R.C.D. Espanyol (2012-13): 165 tarjetas conjuntas.",
                          "- Real Zaragoza CD (1996-97): 155 tarjetas conjuntas.",
                          "- Real Zaragoza CD (1995-96): 153 tarjetas conjuntas."])

    imprimir_comparativa("Ejercicio 11", "Los Revulsivos de Oro",
                         mi_liga.ranking_revulsivos(3),
                         ["- MORATA: 24 goles. Marca un gol cada 97 minutos.",
                          "- LOINAZ: 12 goles. Marca un gol cada 158 minutos.",
                          "- BOJAN: 26 goles. Marca un gol cada 175 minutos."])

    imprimir_comparativa("Ejercicio 12", "Años en Activo",
                         mi_liga.ranking_anios_en_activo(5),
                         ["- CASTRO: 38 años en activo (De 1934 a 1973).",
                          "- ZUBIETA: 20 años en activo (De 1935 a 1956).",
                          "- CESAR SANCHEZ: 20 años en activo (De 1991 a 2012).",
                          "- IRARAGORRI: 19 años en activo (De 1929 a 1949).",
                          "- M. SOLER: 19 años en activo (De 1983 a 2003)."])

    imprimir_comparativa("Ejercicio 13", "Partidos de forma impoluta (Sin tarjetas/expulsiones)",
                         mi_liga.ranking_impolutos(3),
                         ["- LIAÑO: 165 partidos disputados de forma impoluta.",
                          "- LINEKER: 103 partidos disputados de forma impoluta.",
                          "- M. ANGEL G.: 78 partidos disputados de forma impoluta."])

    imprimir_comparativa("Ejercicio 14", "Veces cambiado",
                         mi_liga.ranking_veces_cambiado(3),
                         ["- JOAQUIN S.: Cambiado en 170 ocasiones.",
                          "- GUSTAVO LOPEZ: Cambiado en 168 ocasiones.",
                          "- ETXEBERRIA: Cambiado en 155 ocasiones."])

    imprimir_comparativa("Ejercicio 15", "Goles concentrados en una temporada",
                         mi_liga.ranking_goles_unica_temporada(4),
                         ["- VIERI: 24 goles. Todos anotados en la 1997-98.",
                          "- HASSELBAINK: 24 goles. Todos anotados en la 1999-00.",
                          "- MAXI GOMEZ: 18 goles. Todos anotados en la 2017-18.",
                          "- IBRAHIMOVIC: 16 goles. Todos anotados en la 2009-10."])
    
    imprimir_comparativa("Ejercicio 16", "Mejor Ratio Goles/Minuto",
                         mi_liga.ranking_ratio_goles_minutos(min_goles=50, limite=10),
                         ["- LANGARA: 104 goles. Marca un gol cada 77.9 minutos.",
                          "- RONALDO, C.: 311 goles. Marca un gol cada 80.7 minutos.",
                          "- MESSI: 383 goles. Marca un gol cada 87.6 minutos.",
                          "- URTIZBEREA: 70 goles. Marca un gol cada 91.3 minutos.",
                          "- BATA: 108 goles. Marca un gol cada 98.3 minutos.",
                          "- IRIONDO O.: 50 goles. Marca un gol cada 99.0 minutos.",
                          "- ZARRA: 251 goles. Marca un gol cada 99.2 minutos.",
                          "- LUIS SUAREZ: 109 goles. Marca un gol cada 101.6 minutos.",
                          "- PRUDEN: 91 goles. Marca un gol cada 101.9 minutos.",
                          "- PUSKAS: 156 goles. Marca un gol cada 103.7 minutos."])

if __name__ == "__main__":
    main()