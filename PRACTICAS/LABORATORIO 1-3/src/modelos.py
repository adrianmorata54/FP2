# ==============================================================================
# MÓDULO: modelos.py
# Propósito: Definir la estructura general de cualquier algoritmo predictivo 
# y programar la lógica específica de varios modelos de Machine Learning.
# ==============================================================================

# Importamos ABC para obligar a que las clases hijas sigan unas reglas estrictas
from abc import ABC, abstractmethod

# Counter es una herramienta fantástica de Python que sirve para contar 
# cuántas veces se repite un elemento en una lista (ideal para hacer "votaciones")
from collections import Counter

from dataset import DataSet
from registro import Registro
import random

class Modelo(ABC):
    """
    Clase base abstracta (plantilla) para cualquier algoritmo de Machine Learning.
    Sea cual sea el algoritmo (KNN, Centroide, Regresión Lineal...), 
    todos deben tener un comportamiento común: poder "entrenarse" y "predecir".
    Esto se conoce como el Patrón de Diseño 'Strategy' o 'Estrategia'.
    """
    
    def __init__(self):
        # Un modelo recién instanciado está "vacío", no ha aprendido nada aún.
        self.datos_entrenamiento = None

    def entrenar(self, dataset: DataSet):
        """
        Fase de aprendizaje base. 
        Guarda los datos en la memoria del modelo. Las clases hijas pueden 
        sobreescribir este método si necesitan hacer cálculos matemáticos previos.
        """
        self.datos_entrenamiento = dataset

    @abstractmethod
    def predecir(self, registro: Registro):
        """
        Método abstracto. Obligamos a que cada algoritmo concreto programe 
        su propia forma matemática de adivinar el futuro.
        """
        pass


# ==============================================================================
# ALGORITMOS BASADOS EN INSTANCIAS (LAZY LEARNING)
# ==============================================================================

class Clasificador_kNN(Modelo):
    """
    Modelo KNN (K-Nearest Neighbors) para problemas de clasificación.
    Predice la categoría de un nuevo elemento basándose en lo que son sus 'k' vecinos más parecidos.
    """
    
    def __init__(self, k: int, distancia: str = "euclídea", pesos: list[float] = None):
        super().__init__()
        self.k = k
        self.distancia = distancia
        self.pesos = pesos

    def predecir(self, registro: Registro) -> str:
        # Medida de seguridad vital:
        if self.datos_entrenamiento is None:
            raise ValueError("¡El modelo no ha sido entrenado todavía!")
            
        # 1. BUSCAR LOS VECINOS
        indices_vecinos = registro.k_vecinos(
            self.datos_entrenamiento.registros, 
            self.k, 
            self.distancia,
            self.pesos
        )
        
        # 2. EXTRAER LAS ETIQUETAS
        etiquetas_vecinos = []
        for indice in indices_vecinos:
            vecino = self.datos_entrenamiento.registros[indice]
            etiquetas_vecinos.append(vecino.objetivo)
            
        # 3. VOTACIÓN DEMOCRÁTICA (MODA)
        # Counter coge la lista (ej: ["Sano", "Enfermo", "Sano"]) y las cuenta.
        conteo = Counter(etiquetas_vecinos)
        
        # most_common(1) devuelve una lista de tuplas: [('Sano', 2)]
        # El primer [0] accede a la tupla ('Sano', 2). El segundo [0] extrae el texto "Sano".
        etiqueta_ganadora = conteo.most_common(1)[0][0]
        
        return etiqueta_ganadora


class Regresor_kNN(Modelo):
    """
    Modelo KNN adaptado para Regresión (predecir números continuos, como el precio de una casa).
    En lugar de hacer una "votación" para ver qué clase gana, calcula la MEDIA de sus vecinos.
    """
    def __init__(self, k: int, distancia: str = "euclídea", pesos: list[float] = None):
        super().__init__()
        self.k = k
        self.distancia = distancia
        self.pesos = pesos

    def predecir(self, registro: Registro) -> float:
        if self.datos_entrenamiento is None:
            raise ValueError("¡El modelo no ha sido entrenado todavía!")
            
        indices_vecinos = registro.k_vecinos(
            self.datos_entrenamiento.registros, 
            self.k, 
            self.distancia,
            self.pesos
        )
        
        # En Regresión, en lugar de contar etiquetas de texto, SUMAMOS los números
        suma_objetivos = 0.0
        for indice in indices_vecinos:
            vecino = self.datos_entrenamiento.registros[indice]
            suma_objetivos += vecino.objetivo
            
        # Y devolvemos la Media Aritmética
        return suma_objetivos / self.k


# ==============================================================================
# ALGORITMOS BASADOS EN MODELO (EAGER LEARNING)
# ==============================================================================


class Clasificador_centroide(Modelo):
    """
    Clasificador basado en el "Punto Medio" (Centroide).
    Calcula un único punto central (registro fantasma) por cada clase durante el entrenamiento.
    """
    def __init__(self, distancia: str = "euclídea"):
        super().__init__()
        self.distancia = distancia
        self.centroides = {} 

    def entrenar(self, dataset: DataSet):
        # Sobreescribimos el método entrenar porque este algoritmo SÍ hace matemáticas al estudiar
        super().entrenar(dataset)
        
        # 1. Agrupamos los registros por su clase (ej: todos los "Iris-setosa" juntos)
        agrupados = {}
        for reg in dataset.registros:
            etiqueta = reg.objetivo
            if etiqueta not in agrupados:
                agrupados[etiqueta] = []
            agrupados[etiqueta].append(reg.atributos)
            
        # 2. Calculamos la media de cada columna para crear el "Centroide"
        num_atributos = len(dataset.registros[0].atributos)
        self.centroides = {}
        
        for etiqueta, lista_atributos in agrupados.items():
            centroide_attrs = []
            num_registros = len(lista_atributos)
            
            for i in range(num_atributos):
                suma = sum(atributos[i] for atributos in lista_atributos)
                centroide_attrs.append(suma / num_registros)
                
            # Creamos un Registro "fantasma" que representa el centro perfecto de esa clase
            self.centroides[etiqueta] = Registro(centroide_attrs)

    def predecir(self, registro: Registro) -> str:
        if not self.centroides:
            raise ValueError("¡El modelo no ha sido entrenado todavía!")
            
        etiqueta_ganadora = None
        distancia_minima = float('inf')
        
        # BÚSQUEDA SÚPER RÁPIDA: Solo comparamos contra los 3 o 4 centroides, no contra toda la base de datos
        for etiqueta, centroide in self.centroides.items():
            dist = registro.calcula_distancia(centroide, self.distancia)
            if dist < distancia_minima:
                distancia_minima = dist
                etiqueta_ganadora = etiqueta
                
        return etiqueta_ganadora



class Regresor_lineal_multiple(Modelo):
    """
    Aproximación heurística a una recta de regresión múltiple.
    Usa el algoritmo de Gradiente Descendente Estocástico (SGD).
    """
    def __init__(self, tasa_aprendizaje: float = 0.0001, epocas: int = 100):
        super().__init__()
        self.pesos = []
        self.sesgo = 0.0 # El punto donde la recta corta el eje Y (Intercepto)
        self.tasa_aprendizaje = tasa_aprendizaje # El tamaño de los "pasos" que da para aprender
        self.epocas = epocas # Cuántas veces repasa el dataset entero para aprender

    def entrenar(self, dataset: DataSet):
        super().entrenar(dataset)
        num_atributos = len(dataset.registros[0].atributos)
        
        # 1. Inicialización Aleatoria (Empezamos con una recta al azar)
        self.pesos = [random.uniform(-0.1, 0.1) for _ in range(num_atributos)]
        self.sesgo = random.uniform(-0.1, 0.1)
        
        # 2. Gradiente Descendente: Aprendemos de los errores a base de iteraciones
        for _ in range(self.epocas):
            for reg in dataset.registros:
                # Predecimos con la fórmula de la recta: Y = Sesgo + (Peso1*X1) + (Peso2*X2)...
                pred = self.sesgo + sum(w * x for w, x in zip(self.pesos, reg.atributos))
                
                # Vemos por cuánto nos hemos equivocado (Error real)
                error = pred - reg.objetivo
                
                # Penalizamos (corregimos) nuestro sesgo y nuestros pesos para equivocarnos menos
                # Restamos el error multiplicado por la tasa de aprendizaje
                self.sesgo -= self.tasa_aprendizaje * error
                for i in range(num_atributos):
                    self.pesos[i] -= self.tasa_aprendizaje * error * reg.atributos[i]

    def predecir(self, registro: Registro) -> float:
        if not self.pesos:
            raise ValueError("¡El modelo no ha sido entrenado todavía!")
            
        # Aplicamos la ecuación matemática de la recta aprendida de forma instantánea
        return self.sesgo + sum(w * x for w, x in zip(self.pesos, registro.atributos))