import math
import numpy as np
import matplotlib.pyplot as plt
import retos_optimizacion as reto

# =============================================================================
# CONFIGURACIÓN INICIAL
# =============================================================================
np.random.seed(1)

# =============================================================================
# 1. LOS 5 ALGORITMOS DE BÚSQUEDA HEURÍSTICA
# =============================================================================

def busqueda_aleatoria(funcion, bounds=(-10, 10), max_evals=2000):
    mejor_solucion = np.random.uniform(bounds[0], bounds[1], 10)
    mejor_valor = funcion.evaluar(mejor_solucion)
    evaluaciones = 1
    
    while evaluaciones < max_evals:
        candidato = np.random.uniform(bounds[0], bounds[1], 10)
        valor_candidato = funcion.evaluar(candidato)
        evaluaciones += 1
        if valor_candidato < mejor_valor:
            mejor_solucion = candidato
            mejor_valor = valor_candidato
            
    return mejor_solucion, mejor_valor


def escalada_paso_variable(funcion, bounds=(-10, 10), max_evals=2000, step_inicial=5.0, step_final=0.01):
    mejor_solucion = np.random.uniform(bounds[0], bounds[1], 10)
    mejor_valor = funcion.evaluar(mejor_solucion)
    evaluaciones = 1
    historial = [mejor_valor]
    
    while evaluaciones < max_evals:
        progreso = evaluaciones / max_evals
        step_actual = step_inicial - progreso * (step_inicial - step_final)
        
        ruido = np.random.normal(0, step_actual, 10)
        vecino = np.clip(mejor_solucion + ruido, bounds[0], bounds[1])
        valor_vecino = funcion.evaluar(vecino)
        evaluaciones += 1
        
        if valor_vecino < mejor_valor:
            mejor_solucion = vecino
            mejor_valor = valor_vecino
            
        historial.append(mejor_valor)
            
    return mejor_solucion, mejor_valor, historial


def escalada_maxima_pendiente(funcion, bounds=(-10, 10), max_evals=2000, step_size=0.5, num_vecinos=10):
    mejor_solucion = np.random.uniform(bounds[0], bounds[1], 10)
    mejor_valor = funcion.evaluar(mejor_solucion)
    evaluaciones = 1
    
    while evaluaciones + num_vecinos <= max_evals:
        mejor_vecino = None
        mejor_valor_vecino = float('inf')
        
        for _ in range(num_vecinos):
            ruido = np.random.normal(0, step_size, 10)
            vecino = np.clip(mejor_solucion + ruido, bounds[0], bounds[1])
            valor_vecino = funcion.evaluar(vecino)
            evaluaciones += 1
            
            if valor_vecino < mejor_valor_vecino:
                mejor_vecino = vecino
                mejor_valor_vecino = valor_vecino
                
        if mejor_valor_vecino < mejor_valor:
            mejor_solucion = mejor_vecino
            mejor_valor = mejor_valor_vecino
        else:
            break 
            
    return mejor_solucion, mejor_valor, []


def escalada_con_reinicios(funcion, bounds=(-10, 10), max_evals=2000, step_inicial=5.0, step_final=0.01, reinicios=4):
    evals_por_reinicio = max_evals // reinicios
    mejor_solucion_global = None
    mejor_valor_global = float('inf')
    
    for _ in range(reinicios):
        solucion, valor, _ = escalada_paso_variable(funcion, bounds, evals_por_reinicio, step_inicial, step_final)
        if valor < mejor_valor_global:
            mejor_valor_global = valor
            mejor_solucion_global = solucion
            
    return mejor_solucion_global, mejor_valor_global


def recocido_simulado(funcion, bounds=(-10, 10), max_evals=2000, temp_inicial=100, alpha=0.95, step_size=0.5):
    solucion_actual = np.random.uniform(bounds[0], bounds[1], 10)
    valor_actual = funcion.evaluar(solucion_actual)
    evaluaciones = 1
    mejor_solucion = solucion_actual.copy()
    mejor_valor = valor_actual
    temp = temp_inicial
    
    while evaluaciones < max_evals:
        ruido = np.random.normal(0, step_size, 10)
        vecino = np.clip(solucion_actual + ruido, bounds[0], bounds[1])
        valor_vecino = funcion.evaluar(vecino)
        evaluaciones += 1
        
        delta = valor_vecino - valor_actual
        if delta < 0 or np.random.rand() < math.exp(-delta / temp):
            solucion_actual = vecino
            valor_actual = valor_vecino
            if valor_actual < mejor_valor:
                mejor_solucion = solucion_actual.copy()
                mejor_valor = valor_actual
                
        temp *= alpha 
        
    return mejor_solucion, mejor_valor


# =============================================================================
# 2. HERRAMIENTAS ADICIONALES: GRID SEARCH Y GRÁFICAS
# =============================================================================

def grid_search_recocido(funcion, bounds=(-10, 10), valores_step=[0.1, 0.5, 1.0, 2.0]):
    valores_alpha = [0.85, 0.90, 0.95, 0.99]
    evals_por_prueba = 100 
    
    mejor_valor = float('inf')
    mejor_step, mejor_alpha = None, None
    
    for step in valores_step:
        for alpha in valores_alpha:
            _, valor = recocido_simulado(funcion, bounds, max_evals=evals_por_prueba, 
                                         step_size=step, alpha=alpha)
            if valor < mejor_valor:
                mejor_valor, mejor_step, mejor_alpha = valor, step, alpha
                
    return mejor_step, mejor_alpha, 1600


def plot_convergencia(historial, nombre_algoritmo="Hill Climbing Paso Variable"):
    plt.figure(figsize=(10, 6))
    historial_seguro = [max(v, 1e-10) for v in historial]
    plt.plot(historial_seguro, label="Mejor Fitness", color='b')
    plt.yscale('log')
    plt.xlabel('Número de Evaluaciones')
    plt.ylabel('Valor de la Función (Fitness)')
    plt.title(f'Curva de Convergencia: {nombre_algoritmo}')
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend()
    print("\n[!] Mostrando gráfica de convergencia. Cierra la ventana para continuar...")
    plt.show()
