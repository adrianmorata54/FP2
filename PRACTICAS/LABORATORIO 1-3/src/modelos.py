# ==============================================================================
# MÓDULO: modelos.py
# Propósito: Definir la estructura general de cualquier algoritmo predictivo 
# y programar la lógica específica del algoritmo K-Nearest Neighbors (KNN).
# ==============================================================================

# Importamos ABC para obligar a que las clases hijas sigan unas reglas estrictas
from abc import ABC, abstractmethod

# Counter es una herramienta fantástica de Python que sirve para contar 
# cuántas veces se repite un elemento en una lista (ideal para hacer "votaciones")
from collections import Counter

from dataset import DataSet
from registro import Registro

class Modelo(ABC):
    """
    Clase base abstracta (plantilla) para cualquier algoritmo de Machine Learning.
    Sea cual sea el algoritmo (KNN, Redes Neuronales, Árboles de Decisión...), 
    todos deben poder "entrenarse" y "predecir".
    """
    
    def __init__(self):
        # El PDF pide inicializar los datos de entrenamiento a nulo (None en Python).
        # Un modelo recién nacido está "vacío", no ha aprendido nada aún.
        self.datos_entrenamiento = None

    def entrenar(self, dataset: DataSet):
        """
        Fase de aprendizaje. 
        En el algoritmo KNN, "entrenar" es simplemente memorizar los datos.
        A esto en Machine Learning se le llama "Lazy Learning" (Aprendizaje Vago),
        porque el algoritmo no hace ningún cálculo matemático complejo ahora, 
        sino que lo deja todo para el momento en que se le pida predecir.
        """
        self.datos_entrenamiento = dataset

    @abstractmethod
    def predecir(self, registro: Registro):
        """
        Método abstracto. Obligamos a que cada algoritmo concreto (como nuestro KNN)
        programe su propia forma matemática de adivinar el futuro.
        """
        pass


# ==============================================================================
# ALGORITMO ESPECÍFICO: K-NEAREST NEIGHBORS (K-Vecinos más cercanos)
# ==============================================================================



class Clasificador_kNN(Modelo):
    """
    Modelo KNN (K-Nearest Neighbors) para problemas de clasificación.
    Predice la categoría de un nuevo elemento basándose en lo que son sus 'k' vecinos más parecidos.
    """
    
    def __init__(self, k: int, distancia: str = "euclídea", pesos: list[float] = None):
        # super().__init__() llama al constructor del padre (Modelo) para que 
        # nos cree la variable self.datos_entrenamiento = None automáticamente.
        super().__init__()
        
        # Guardamos la configuración de nuestro algoritmo
        self.k = k
        self.distancia = distancia
        self.pesos = pesos

    def predecir(self, registro: Registro) -> str:
        """
        Dado un paciente nuevo (registro) sin etiqueta, el algoritmo compara sus atributos
        con todos los pacientes que memorizó durante el entrenamiento para adivinar su enfermedad.
        """
        # 1. Medida de seguridad: Un estudiante no puede hacer un examen si no ha estudiado.
        # Un modelo no puede predecir si no ha sido entrenado.
        if self.datos_entrenamiento is None:
            raise ValueError("¡El modelo no ha sido entrenado todavía!")
            
        # 2. BUSCAR LOS VECINOS: Invocamos al método de nuestro Laboratorio 1
        # Le pasamos la lista de tooooodos los pacientes almacenados, la 'k', el tipo de distancia y los pesos.
        # Esto nos devuelve una lista con las POSICIONES (índices) de los ganadores.
        indices_vecinos = registro.k_vecinos(
            self.datos_entrenamiento.registros, 
            self.k, 
            self.distancia,
            self.pesos
        )
        
        # 3. EXTRAER LAS ETIQUETAS:
        # Ya sabemos quiénes son los pacientes más cercanos, ahora queremos ver 
        # qué enfermedad (o clase) tenían esos pacientes en la vida real.
        etiquetas_vecinos = []
        for indice in indices_vecinos:
            # Buscamos al paciente original en la base de datos de entrenamiento
            vecino = self.datos_entrenamiento.registros[indice]
            # Nos guardamos su etiqueta (ej: "Iris-setosa", "Diabetes Positiva")
            etiquetas_vecinos.append(vecino.objetivo)
            
        # 4. VOTACIÓN DEMOCRÁTICA (MODA):
        # Counter coge la lista (ej: ["Grave", "Leve", "Grave"]) y las cuenta.
        conteo = Counter(etiquetas_vecinos)
        
        # most_common(1) devuelve una lista con el elemento más repetido y cuántas veces salió.
        # Ejemplo del resultado: [('Grave', 2)]
        # El primer [0] accede a la tupla ('Grave', 2). El segundo [0] extrae el texto "Grave".
        etiqueta_ganadora = conteo.most_common(1)[0][0]
        
        # Devolvemos nuestra predicción final
        return etiqueta_ganadora