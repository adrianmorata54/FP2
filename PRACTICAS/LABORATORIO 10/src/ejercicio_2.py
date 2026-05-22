import math
import csv
import matplotlib.pyplot as plt

# ==============================================================================
# CONFIGURACIÓN
# ==============================================================================
RUTA_CSV = r"PRACTICAS\LABORATORIO 10\datos\reto_4_dias.csv"

# ==============================================================================
# CLASE PRINCIPAL (PUNTOS 1 AL 8 y 10)
# ==============================================================================

class GestorAnomalias:
    def __init__(self):
        # PUNTO 1: Propiedad "datos" que sea un diccionario.
        self.datos = {}

    # PUNTO 1: Método que lea el fichero csv
    def leer_csv(self, ruta_archivo: str):
        with open(ruta_archivo, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            cabeceras = next(reader) 
            for cabecera in cabeceras:
                self.datos[cabecera.strip()] = []
            
            for fila in reader:
                if not fila: continue
                for i, valor in enumerate(fila):
                    cabecera = cabeceras[i].strip()
                    self.datos[cabecera].append(float(valor))

    # PUNTO 2: Método que represente ST originales (de 4 en 4)
    def representar_st_originales(self):
        variables = [v for v in self.datos.keys() if v != 'Minuto']
        minutos = self.datos['Minuto']
        
        fig, axs = plt.subplots(5, 1, figsize=(14, 18))
        fig.suptitle("Punto 2: Series Temporales Originales (Días 1 al 4)", fontsize=16, fontweight='bold')
        
        for i in range(5):
            grupo = variables[i*4 : (i+1)*4]
            for var in grupo:
                axs[i].plot(minutos, self.datos[var], label=var, alpha=0.8)
            axs[i].set_title(f"Grupo: {', '.join(grupo)}")
            axs[i].legend(loc="upper right")
            axs[i].grid(True)
            axs[i].axvline(1440, color='black', linestyle='--', linewidth=2, label="Fin Día 1")
            
        plt.tight_layout(rect=[0, 0.03, 1, 0.97])
        plt.show()

    # PUNTO 3: Método correlación de Pearson
    @staticmethod
    def correlacion_pearson(lista1: list, lista2: list) -> float:
        n = len(lista1)
        if n < 2: return 0.0
        m1 = sum(lista1) / n
        m2 = sum(lista2) / n
        num = sum((a - m1) * (b - m2) for a, b in zip(lista1, lista2))
        den = math.sqrt(sum((a - m1)**2 for a in lista1) * sum((b - m2)**2 for b in lista2))
        return num / den if den != 0 else 0.0

    # PUNTO 4: Método ventana deslizante
    def correlacion_ventana_deslizante(self, lista1: list, lista2: list, tam_ventana: int) -> list:
        resultado = [1.0] * (tam_ventana - 1)
        for i in range(tam_ventana, len(lista1) + 1):
            ventana1 = lista1[i - tam_ventana : i]
            ventana2 = lista2[i - tam_ventana : i]
            resultado.append(self.correlacion_pearson(ventana1, ventana2))
        return resultado

    # PUNTO 5: Método serie diferencias
    @staticmethod
    def obtener_diferencias(lista: list) -> list:
        return [0.0] + [lista[i] - lista[i-1] for i in range(1, len(lista))]

    # PUNTO 6: Método variables correlacionadas Día 1
    def variables_correlacionadas_dia1(self, umbral: float = 0.8) -> list:
        variables = [v for v in self.datos.keys() if v != 'Minuto']
        pares = []
        fin_dia1 = 1440 
        for i in range(len(variables)):
            for j in range(i + 1, len(variables)):
                v1, v2 = variables[i], variables[j]
                d1 = self.obtener_diferencias(self.datos[v1][:fin_dia1])
                d2 = self.obtener_diferencias(self.datos[v2][:fin_dia1])
                if abs(self.correlacion_pearson(d1, d2)) >= umbral:
                    pares.append((v1, v2))
        return pares

    # PUNTO 7: Método detectar rupturas
    def detectar_rupturas(self, pares: list, umbral_ruptura: float = 0.1) -> dict:
        rupturas = {}
        ventana = 60 # 1 hora
        for v1, v2 in pares:
            d1 = self.obtener_diferencias(self.datos[v1])
            d2 = self.obtener_diferencias(self.datos[v2])
            evolucion = self.correlacion_ventana_deslizante(d1, d2, ventana)
            # Buscamos anomalías desde el día 2 (minuto 1440 en adelante)
            minutos_fallo = [m for m in range(1440, len(evolucion)) if abs(evolucion[m]) < umbral_ruptura]
            if minutos_fallo:
                rupturas[(v1, v2)] = minutos_fallo
        return rupturas

    # PUNTO 8: Método agrupar intervalos
    @staticmethod
    def agrupar_en_intervalos(minutos: list, umbral_dist: int, umbral_duracion: int) -> list:
        if not minutos: return []
        intervalos = []
        inicio = actual = minutos[0]
        for m in minutos[1:]:
            if m - actual <= umbral_dist:
                actual = m
            else:
                if actual - inicio >= umbral_duracion:
                    intervalos.append((inicio, actual))
                inicio = actual = m
        if actual - inicio >= umbral_duracion:
            intervalos.append((inicio, actual))
        return intervalos

    # PUNTO 10: Representación gráfica final (10 gráficas de 2 en 2)
    def representar_resumen_anomalias_diff(self, info_rupturas: dict):
        # Tomamos los 10 primeros pares que hayan registrado anomalías para llenar las 10 gráficas
        pares_a_mostrar = list(info_rupturas.keys())[:10]
        
        # Creamos una figura grande con 5 filas y 2 columnas (10 subgráficas en total)
        fig, axs = plt.subplots(5, 2, figsize=(18, 22))
        fig.suptitle("Punto 10: Rupturas de Correlación en ST de Diferencias (Pares de 2 en 2)", fontsize=18, fontweight='bold')
        
        # Aplanamos la matriz de subgráficas para poder iterar sobre ella fácilmente
        axs = axs.flatten()
        
        for i in range(10):
            if i < len(pares_a_mostrar):
                par = pares_a_mostrar[i]
                v1, v2 = par
                d1 = self.obtener_diferencias(self.datos[v1])
                d2 = self.obtener_diferencias(self.datos[v2])
                
                axs[i].plot(self.datos['Minuto'], d1, label=f"Diff {v1}", alpha=0.7)
                axs[i].plot(self.datos['Minuto'], d2, label=f"Diff {v2}", alpha=0.7)
                
                # Pintar franjas rojas donde el algoritmo detectó la anomalía
                for i_ini, i_fin in info_rupturas[par]:
                    axs[i].axvspan(i_ini, i_fin, color='red', alpha=0.3)
                    
                axs[i].set_title(f"Anomalía detectada: {v1} - {v2}")
                axs[i].set_ylabel("Diferencia")
                axs[i].legend(loc="upper right")
                axs[i].grid(True)
                axs[i].set_xlim(left=1440) # Hacemos zoom a partir del Día 2 (operación real)
            else:
                # Si por algún motivo se detectaron menos de 10 pares, ocultamos los recuadros vacíos
                axs[i].axis('off')
                
        # Etiqueta de eje X solo para las gráficas de abajo del todo
        axs[-1].set_xlabel("Minuto")
        axs[-2].set_xlabel("Minuto")
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.97])
        plt.show()

# ==============================================================================
# PUNTO 9: PROGRAMA PRINCIPAL 
# ==============================================================================

def ejecutar_ejercicio_2():
    print("--- INICIANDO DETECTOR DE ANOMALÍAS INDUSTRIALES ---\n")
    
    gestor = GestorAnomalias()
    gestor.leer_csv(RUTA_CSV)
    
    print("Mostrando Gráficas Originales (Punto 2)...")
    gestor.representar_st_originales()
    
    pares_control = gestor.variables_correlacionadas_dia1(umbral=0.8)
    print(f"Punto 6: Pares base detectados en Día 1 (umbral 0.8): {len(pares_control)}\n")

    # PUNTO 9: PROBAMOS DISTINTOS UMBRALES PARA VER CÓMO VARÍAN LOS RESULTADOS
    configuraciones = [
        {"ruptura": 0.10, "dist": 15, "dur": 3},
        {"ruptura": 0.15, "dist": 20, "dur": 5}
    ]
    
    info_rupturas_final = {}
    
    for conf in configuraciones:
        print(f"===========================================================")
        print(f"PRUEBA DE UMBRALES: Ruptura <{conf['ruptura']}, Distancia: {conf['dist']}m, Duración min: {conf['dur']}m")
        print(f"===========================================================")
        
        rupturas_brutas = gestor.detectar_rupturas(pares_control, conf['ruptura'])
        info_rupturas_final = {} # La última iteración se usará para la gráfica
        
        for par, minutos in rupturas_brutas.items():
            intervalos = gestor.agrupar_en_intervalos(minutos, conf['dist'], conf['dur'])
            if intervalos:
                info_rupturas_final[par] = intervalos
                
                # Imprimimos de forma resumida para que se vea claro en consola
                str_intervalos = " | ".join([f"{i}-{f}" for i, f in intervalos])
                print(f"Anomalía en {par[0]}-{par[1]}: {str_intervalos}")
        print("\n")

    print("Mostrando Gráficas de Diferencias con Anomalías (Punto 10)...")
    gestor.representar_resumen_anomalias_diff(info_rupturas_final)

if __name__ == "__main__":
    try:
        ejecutar_ejercicio_2()
    except FileNotFoundError:
        print(f"Error: No se encuentra el archivo en {RUTA_CSV}")