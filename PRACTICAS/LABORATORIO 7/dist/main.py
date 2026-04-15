import math
import numpy as np
import retos_optimizacion as reto

# =============================================================================
# CONFIGURACIÓN INICIAL
# =============================================================================
# El PDF exige fijar la semilla aleatoria a 1 para asegurar que 
# los experimentos sean reproducibles (siempre den el mismo resultado).
np.random.seed(1)


# =============================================================================
# 1. DEFINICIÓN DE LOS 5 ALGORITMOS HEURÍSTICOS
# =============================================================================

def busqueda_aleatoria(funcion, bounds=(-10, 10), max_evals=2000):
    """
    Genera soluciones al azar sin seguir ninguna lógica de cercanía.
    Sirve como "línea base" para comprobar si los otros algoritmos son inteligentes.
    """
    # 1. Creamos un vector inicial de 10 dimensiones con valores entre -10 y 10
    mejor_solucion = np.random.uniform(bounds[0], bounds[1], 10)
    mejor_valor = funcion.evaluar(mejor_solucion)
    evaluaciones = 1
    
    # 2. Mientras nos quede presupuesto...
    while evaluaciones < max_evals:
        # Generamos un vector completamente nuevo y aleatorio
        candidato = np.random.uniform(bounds[0], bounds[1], 10)
        valor_candidato = funcion.evaluar(candidato)
        evaluaciones += 1
        
        # Si es mejor que lo que teníamos, nos lo guardamos
        if valor_candidato < mejor_valor:
            mejor_solucion = candidato
            mejor_valor = valor_candidato
            
    return mejor_solucion, mejor_valor


def escalada_simple(funcion, bounds=(-10, 10), max_evals=2000, step_size=0.5):
    """
    Evalúa un vecino aleatorio cercano. Si es mejor, se mueve a él inmediatamente.
    Es rápido y agresivo, pero se atasca fácil en mínimos locales.
    """
    mejor_solucion = np.random.uniform(bounds[0], bounds[1], 10)
    mejor_valor = funcion.evaluar(mejor_solucion)
    evaluaciones = 1
    
    while evaluaciones < max_evals:
        # 1. Generamos 'ruido' (un pequeño salto) usando una campana de Gauss
        ruido = np.random.normal(0, step_size, 10)
        
        # 2. Sumamos el ruido a nuestra posición y 'recortamos' (np.clip) 
        # para no salirnos nunca del límite [-10, 10]
        vecino = np.clip(mejor_solucion + ruido, bounds[0], bounds[1])
        valor_vecino = funcion.evaluar(vecino)
        evaluaciones += 1
        
        # 3. Si el vecino es mejor, nos movemos a esa nueva posición
        if valor_vecino < mejor_valor:
            mejor_solucion = vecino
            mejor_valor = valor_vecino
            
    return mejor_solucion, mejor_valor


def escalada_maxima_pendiente(funcion, bounds=(-10, 10), max_evals=2000, step_size=0.5, num_vecinos=10):
    """
    Mira a varios vecinos alrededor (num_vecinos) ANTES de moverse.
    Se mueve solo al MEJOR de todos ellos. Si ninguno mejora, se detiene (break).
    """
    mejor_solucion = np.random.uniform(bounds[0], bounds[1], 10)
    mejor_valor = funcion.evaluar(mejor_solucion)
    evaluaciones = 1
    
    while evaluaciones + num_vecinos <= max_evals:
        mejor_vecino = None
        mejor_valor_vecino = float('inf')
        
        # 1. Miramos a N vecinos a nuestro alrededor
        for _ in range(num_vecinos):
            ruido = np.random.normal(0, step_size, 10)
            vecino = np.clip(mejor_solucion + ruido, bounds[0], bounds[1])
            valor_vecino = funcion.evaluar(vecino)
            evaluaciones += 1
            
            # Guardamos el mejor de estos N vecinos
            if valor_vecino < mejor_valor_vecino:
                mejor_vecino = vecino
                mejor_valor_vecino = valor_vecino
                
        # 2. Comparamos el mejor vecino encontrado con nuestra posición actual
        if mejor_valor_vecino < mejor_valor:
            mejor_solucion = mejor_vecino
            mejor_valor = mejor_valor_vecino
        else:
            # Si ninguno de los vecinos nos mejora, estamos en el fondo de un valle.
            # Nos detenemos para no gastar evaluaciones a lo tonto.
            break 
            
    return mejor_solucion, mejor_valor


def escalada_con_reinicios(funcion, bounds=(-10, 10), max_evals=2000, step_size=0.5, reinicios=4):
    """
    Ejecuta la Escalada Simple varias veces desde distintos puntos de inicio
    para evitar quedarse atascado en un solo mínimo local.
    """
    # Repartimos el presupuesto entre los reinicios (ej: 2000 / 4 = 500 por reinicio)
    evals_por_reinicio = max_evals // reinicios
    
    mejor_solucion_global = None
    mejor_valor_global = float('inf')
    
    for _ in range(reinicios):
        # Lanzamos la escalada simple con su trocito de presupuesto
        solucion, valor = escalada_simple(funcion, bounds, evals_por_reinicio, step_size)
        
        # Si este intento ha llegado más profundo que los anteriores, lo guardamos
        if valor < mejor_valor_global:
            mejor_valor_global = valor
            mejor_solucion_global = solucion
            
    return mejor_solucion_global, mejor_valor_global


def recocido_simulado(funcion, bounds=(-10, 10), max_evals=2000, temp_inicial=100, alpha=0.95, step_size=0.5):
    """
    Inspirado en cómo se enfría el metal. A veces acepta "pasos a peor" para
    escapar de mínimos locales. Cuanto más se enfría (temp baja), menos pasos malos acepta.
    """
    solucion_actual = np.random.uniform(bounds[0], bounds[1], 10)
    valor_actual = funcion.evaluar(solucion_actual)
    evaluaciones = 1
    
    mejor_solucion = solucion_actual.copy()
    mejor_valor = valor_actual
    temp = temp_inicial
    
    while evaluaciones < max_evals:
        # Generamos un vecino
        ruido = np.random.normal(0, step_size, 10)
        vecino = np.clip(solucion_actual + ruido, bounds[0], bounds[1])
        valor_vecino = funcion.evaluar(vecino)
        evaluaciones += 1
        
        # Calculamos la diferencia entre el vecino y nuestra posición
        delta = valor_vecino - valor_actual
        
        # CRITERIO DE ACEPTACIÓN:
        # Si delta < 0 (es mejor) -> Aceptamos siempre.
        # Si es peor -> Aceptamos con una probabilidad matemática que depende de la Temperatura.
        if delta < 0 or np.random.rand() < math.exp(-delta / temp):
            solucion_actual = vecino
            valor_actual = valor_vecino
            
            # Actualizamos el récord global si procede
            if valor_actual < mejor_valor:
                mejor_solucion = solucion_actual.copy()
                mejor_valor = valor_actual
                
        # Enfriamos el sistema multiplicando la temperatura por Alpha (ej: 0.95)
        temp *= alpha 
        
    return mejor_solucion, mejor_valor


# =============================================================================
# 2. BÚSQUEDA DE HIPERPARÁMETROS (GRID SEARCH)
# =============================================================================

def grid_search_recocido(funcion, bounds=(-10, 10)):
    """
    Prueba combinaciones automáticas de parámetros (step y alpha) 
    para ver cuáles se adaptan mejor a la forma de la función matemática.
    """
    valores_step = [0.1, 0.5, 1.0, 2.0]
    valores_alpha = [0.85, 0.90, 0.95, 0.99]
    evals_por_prueba = 100 
    
    # Coste fijo: 4 steps * 4 alphas * 100 evals = 1600 llamadas
    
    mejor_valor = float('inf')
    mejor_step = None
    mejor_alpha = None
    
    for step in valores_step:
        for alpha in valores_alpha:
            # Lanzamos un recocido muy cortito (100 intentos) para testear
            _, valor = recocido_simulado(funcion, bounds, max_evals=evals_por_prueba, 
                                         step_size=step, alpha=alpha)
            
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_step = step
                mejor_alpha = alpha
                
    # Retornamos los ganadores y las 1600 llamadas que hemos gastado
    return mejor_step, mejor_alpha, 1600


# =============================================================================
# 3. BLOQUE PRINCIPAL (FRAMEWORK DE COMPARACIÓN)
# =============================================================================

def main():
    try:
        # 1. Inicializamos los objetos de las funciones encriptadas
        funciones = [
            reto.Funcion_1(),
            reto.Funcion_2(),
            reto.Funcion_3(),
            reto.Funcion_4()
        ]
        
        # 2. Definimos el presupuesto global indicado por el PDF
        LIMITE_TOTAL = 10000
        EVALS_BASE = 1000 
        
        # 3. Iteramos sobre cada una de las 4 funciones
        for i, funcion in enumerate(funciones, start=1):
            print("\n" + "═"*60)
            print(f" 🚀 FRAMEWORK DE COMPARACIÓN - FUNCIÓN {i} ")
            print("═"*60)
            
            # Variables de seguimiento para coronar al algoritmo ganador
            mejor_valor_global = float('inf')
            mejor_vector_global = None
            algoritmo_ganador = ""

            # Sub-función interna para llevar el registro del mejor modelo
            def actualizar_ganador(nombre_algo, vector, valor):
                nonlocal mejor_valor_global, mejor_vector_global, algoritmo_ganador
                if valor < mejor_valor_global:
                    mejor_valor_global = valor
                    mejor_vector_global = vector
                    algoritmo_ganador = nombre_algo

            # --- EJECUCIÓN Y REPARTO DE PRESUPUESTO ---
            
            # Algoritmo 1
            vec_alea, v_alea = busqueda_aleatoria(funcion, max_evals=EVALS_BASE)
            print(f" ├── [1] Búsqueda Aleatoria:       {v_alea:10.4f}")
            actualizar_ganador("Búsqueda Aleatoria", vec_alea, v_alea)
            
            # Algoritmo 2
            vec_esca, v_esca = escalada_simple(funcion, max_evals=EVALS_BASE)
            print(f" ├── [2] Escalada Simple:          {v_esca:10.4f}")
            actualizar_ganador("Escalada Simple", vec_esca, v_esca)
            
            # Algoritmo 3
            vec_max, v_max = escalada_maxima_pendiente(funcion, max_evals=EVALS_BASE)
            print(f" ├── [3] Escalada Máx. Pendiente:  {v_max:10.4f}")
            actualizar_ganador("Escalada Máxima Pendiente", vec_max, v_max)
            
            # Algoritmo 4
            vec_rein, v_rein = escalada_con_reinicios(funcion, max_evals=EVALS_BASE)
            print(f" ├── [4] Escalada con Reinicios:   {v_rein:10.4f}")
            actualizar_ganador("Escalada con Reinicios", vec_rein, v_rein)
            
            # Algoritmo 5 (Grid Search + Recocido Simulado)
            print(" │")
            print(" ├── ⚙️  Iniciando Grid Search para Recocido Simulado...")
            mejor_step, mejor_alpha, evals_gs = grid_search_recocido(funcion)
            
            # El recocido se lleva todo el presupuesto que sobra para explotar sus parámetros
            evals_restantes = LIMITE_TOTAL - (EVALS_BASE * 4) - evals_gs
            
            vec_rec, v_rec = recocido_simulado(
                funcion, max_evals=evals_restantes, step_size=mejor_step, alpha=mejor_alpha
            )
            print(f" ├── [5] Recocido Simulado (step={mejor_step}, α={mejor_alpha}): {v_rec:.4f}")
            actualizar_ganador("Recocido Simulado", vec_rec, v_rec)
            
            # --- RESULTADOS FINALES DE LA FUNCIÓN ---
            gastado = funcion.presupuesto_gastado
            print(" │")
            print(" └─> 📊 VERIFICACIÓN DE PRESUPUESTO:")
            print(f"     Evaluaciones consumidas: {gastado} / {LIMITE_TOTAL}")
            print("\n" + "★"*60)
            print(f" 🏆 GANADOR: {algoritmo_ganador}")
            print(f" 🎯 Mínimo Encontrado: {mejor_valor_global:.6f}")
            print(" 📍 Vector Solución:")
            print(f" {np.round(mejor_vector_global, 4)}")
            print("★"*60 + "\n")
            
    except Exception as e:
        print(f"\n[!] Error crítico durante la ejecución: {e}")

# Punto de entrada estándar de Python
if __name__ == "__main__":
    main()