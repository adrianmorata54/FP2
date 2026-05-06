import math
import numpy as np
import matplotlib.pyplot as plt
import retos_optimizacion as reto
import funcion8 as f8  # Importamos el archivo de la Función 8

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


# =============================================================================
# 3. BLOQUE PRINCIPAL DEL PROGRAMA (ORQUESTADOR)
# =============================================================================

def main():
    try:
        # Metemos TODAS las funciones, incluyendo la Función 8 en el torneo general
        funciones = [
            reto.Funcion_1(), reto.Funcion_2(), reto.Funcion_3(), reto.Funcion_4(),
            reto.Funcion_5(), reto.Funcion_6(), reto.Funcion_7(),
            f8.Funcion_8() # La de Schwefel ahora compite aquí
        ]
        
        LIMITE_TOTAL = 10000
        EVALS_BASE = 1000 
        
        for i, funcion in enumerate(funciones, start=1):
            print("\n" + "═"*75)
            print(f" 🚀 FRAMEWORK DE COMPARACIÓN - FUNCIÓN {i} ")
            print("═"*75)
            
            # --- ADAPTACIÓN DE MAPA PARA LA FUNCIÓN 8 ---
            if i == 8:
                # La función 8 es gigantesca, cambiamos los parámetros de búsqueda
                limites = (-500, 500)
                s_fijo = 25.0
                s_ini = 100.0
                s_fin = 0.1
                gs_steps = [10.0, 25.0, 50.0, 100.0]
            else:
                # Las funciones normales usan el mapa pequeño
                limites = (-10, 10)
                s_fijo = 0.5
                s_ini = 5.0
                s_fin = 0.01
                gs_steps = [0.1, 0.5, 1.0, 2.0]
            
            mejor_valor_global = float('inf')
            mejor_vector_global = None
            algoritmo_ganador = ""

            def actualizar_ganador(nombre_algo, vector, valor):
                nonlocal mejor_valor_global, mejor_vector_global, algoritmo_ganador
                if valor < mejor_valor_global:
                    mejor_valor_global = valor
                    mejor_vector_global = vector
                    algoritmo_ganador = nombre_algo

            # --- EJECUCIÓN DEL TORNEO (5 ALGORITMOS) ---
            
            vec_alea, v_alea = busqueda_aleatoria(funcion, bounds=limites, max_evals=EVALS_BASE)
            print(f" ├── [1] Búsqueda Aleatoria:       {v_alea:10.4f}")
            print(f" │       └─> Vector: {np.round(vec_alea, 4)}")
            actualizar_ganador("Búsqueda Aleatoria", vec_alea, v_alea)
            
            vec_din, v_din, _ = escalada_paso_variable(funcion, bounds=limites, max_evals=EVALS_BASE, step_inicial=s_ini, step_final=s_fin)
            print(f" ├── [2] Escalada Paso Variable:   {v_din:10.4f}")
            print(f" │       └─> Vector: {np.round(vec_din, 4)}")
            actualizar_ganador("Escalada Paso Variable", vec_din, v_din)
            
            vec_max, v_max, _ = escalada_maxima_pendiente(funcion, bounds=limites, max_evals=EVALS_BASE, step_size=s_fijo)
            print(f" ├── [3] Escalada Máx. Pendiente:  {v_max:10.4f}")
            print(f" │       └─> Vector: {np.round(vec_max, 4)}")
            actualizar_ganador("Escalada Máxima Pendiente", vec_max, v_max)
            
            vec_rein, v_rein = escalada_con_reinicios(funcion, bounds=limites, max_evals=EVALS_BASE, step_inicial=s_ini, step_final=s_fin)
            print(f" ├── [4] Escalada con Reinicios:   {v_rein:10.4f}")
            print(f" │       └─> Vector: {np.round(vec_rein, 4)}")
            actualizar_ganador("Escalada con Reinicios", vec_rein, v_rein)
            
            print(" │")
            print(" ├── ⚙️  Iniciando Grid Search para Recocido Simulado...")
            mejor_step, mejor_alpha, evals_gs = grid_search_recocido(funcion, bounds=limites, valores_step=gs_steps)
            
            evals_restantes = LIMITE_TOTAL - (EVALS_BASE * 4) - evals_gs
            
            vec_rec, v_rec = recocido_simulado(funcion, bounds=limites, max_evals=evals_restantes, step_size=mejor_step, alpha=mejor_alpha)
            print(f" ├── [5] Recocido Simulado (step={mejor_step}, α={mejor_alpha}): {v_rec:.4f}")
            print(f" │       └─> Vector: {np.round(vec_rec, 4)}")
            actualizar_ganador("Recocido Simulado", vec_rec, v_rec)
            
            # --- IMPRESIÓN DEL GANADOR DEL TORNEO ---
            gastado = funcion.presupuesto_gastado
            print(" │")
            print(" └─> 📊 VERIFICACIÓN DE PRESUPUESTO:")
            print(f"     Evaluaciones consumidas: {gastado} / {LIMITE_TOTAL}")
            print("\n" + "★"*75)
            print(f" 🏆 GANADOR: {algoritmo_ganador}")
            print(f" 🎯 Mínimo Encontrado: {mejor_valor_global:.6f}")
            print(" 📍 Vector Solución (Mejor Global):")
            print(f" {np.round(mejor_vector_global, 4)}")
            print("★"*75)


        # =====================================================================
        # 4. GRÁFICA DE CONVERGENCIA ARREGLADA (40.000 evals)
        # =====================================================================
        print("\n" + "="*75)
        print(" 📈 ANÁLISIS DE CONVERGENCIA (40.000 Evaluaciones)")
        print("="*75)
        
        # Usamos la Función 1 y un step_final minúsculo (0.00001) para que no se estanque
        funcion_plot = reto.Funcion_1()
        _, _, historial = escalada_paso_variable(funcion_plot, bounds=(-10, 10), max_evals=40000, step_inicial=2.0, step_final=0.00001)
        plot_convergencia(historial)


        # =====================================================================
        # 5. EJERCICIO VOLUNTARIO: COMPROBACIÓN DE TRAMPA SCHWEFEL
        # =====================================================================
        print("\n" + "★"*75)
        print(" 🎯 COMPROBACIÓN FINAL: 'TRAMPA' DE SCHWEFEL (F8)")
        print("★"*75)
        
        # Como la F8 normal ya ha competido en el bucle principal, aquí solo 
        # comprobamos matemáticamente la versión modificada como pide el PDF.
        f8_mod = f8.Funcion_8_modificada()
        vector_trampa = [1.0] * 10
        valor_trampa = f8_mod.evaluar(vector_trampa)
        
        print(f"\n[-] Función 8 Modificada:")
        print(f"    -> Evaluando en el vector exacto [1.0]*10...")
        print(f"    -> Resultado de la función: {valor_trampa:.6f}")
        
        if abs(valor_trampa) < 1e-5:
            print("    -> ¡Éxito! El mínimo se ha desplazado correctamente y la función vale 0.0.")
            
    except Exception as e:
        print(f"\n[!] Error crítico durante la ejecución: {e}")

if __name__ == "__main__":
    main()