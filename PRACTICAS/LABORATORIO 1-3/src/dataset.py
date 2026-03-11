# ==============================================================================
# MÓDULO: dataset.py
# Propósito: Gestionar conjuntos de datos (colecciones de registros).
# ==============================================================================

# Importamos las herramientas de Python para crear Clases Abstractas (Abstract Base Classes)
# Una clase abstracta es como un "molde base" que nunca se usa directamente, 
# sino que sirve para que otras clases (hijas) hereden de ella y completen sus funciones.
from abc import ABC, abstractmethod

# Importamos las clases de nuestro archivo 'registro.py' porque las vamos a necesitar
# para comprobar que los datos que metemos en el DataSet son correctos.
from registro import Registro, RegistroClasificacion, RegistroRegresion


class DataSet(ABC):
    """
    Clase abstracta contenedora de registros. 
    Al heredar de ABC, Python nos prohíbe hacer un 'DataSet()' genérico.
    Siempre tendremos que crear un 'DataSetClasificacion' o un 'DataSetRegresion'.
    """
    
    def __init__(self):
        # Inicializamos el dataset vacío. 
        # 'registros' guardará la lista de todos los pacientes/flores/casos.
        self.registros = []
        # 'nombres_atributos' guardará cómo se llama cada columna (ej: "Edad", "Presión").
        self.nombres_atributos = []

    def set_cabeceras(self, cabeceras: list[str]):
        """
        Guarda los nombres de las columnas (atributos), ignorando la última.
        """
        # ¿Por qué [:-1]? En Machine Learning, la última columna de un fichero 
        # suele ser la "etiqueta" o "resultado" que queremos predecir (ej: si tiene diabetes o no).
        # Por tanto, los "atributos" para calcular distancias son todos menos el último.
        self.nombres_atributos = cabeceras[:-1]

    @abstractmethod
    def agregar_registro(self, registro: Registro):
        """
        Método abstracto (vacío). 
        El decorador @abstractmethod obliga por ley a que cualquier clase hija 
        tenga que programar obligatoriamente este método. Si no lo hace, Python dará error.
        """
        pass

    def calcular_min_max(self) -> tuple[list[float], list[float]]:
        """
        Recorre todos los registros para encontrar el valor más pequeño y el más 
        grande de cada columna. Esto será vital para "Normalizar".
        """
        # Si el dataset está vacío, devolvemos listas vacías para que no explote.
        if not self.registros:
            return [], []

        # Miramos el primer registro para saber cuántas columnas (dimensiones) hay.
        num_atributos = len(self.registros[0].atributos)
        
        # TRUCO DE PROGRAMACIÓN:
        # Para buscar mínimos, empezamos con el número más grande posible (infinito).
        # Para buscar máximos, empezamos con el número más pequeño (menos infinito).
        minimos = [float('inf')] * num_atributos
        maximos = [float('-inf')] * num_atributos

        # Recorremos cada paciente/flor (reg) en nuestra lista de registros
        for reg in self.registros:
            # enumerate nos da la posición de la columna (i) y su valor
            for i, valor in enumerate(reg.atributos):
                # Si el valor actual es menor que el mínimo que teníamos guardado, lo actualizamos
                if valor < minimos[i]:
                    minimos[i] = valor
                # Si el valor actual es mayor que el máximo que teníamos guardado, lo actualizamos
                if valor > maximos[i]:
                    maximos[i] = valor

        # Devolvemos ambas listas de golpe (en forma de tupla)
        return minimos, maximos

    def crear_subconjunto(self, lista_registros: list[Registro]) -> 'DataSet':
        """
        Crea un "clon" del DataSet actual pero solo con los registros que le pasemos.
        Muy útil para dividir los datos en "Entrenamiento" y "Prueba" más adelante.
        """
        # TRUCO MÁGICO DE PYTHON: self.__class__()
        # Esto averigua automáticamente si somos de Clasificación o de Regresión
        # y crea un objeto nuevo de ese tipo exacto, sin tener que poner un 'if'.
        nuevo_dataset = self.__class__()
        
        # Le copiamos las cabeceras (nombres de columnas) del dataset original
        nuevo_dataset.nombres_atributos = self.nombres_atributos.copy()
        
        # Le metemos la lista de registros que nos han pasado por parámetro
        nuevo_dataset.registros = lista_registros.copy()
        
        return nuevo_dataset


# ==============================================================================
# CLASES HIJAS (CONCRETAS)
# ==============================================================================

class DataSetClasificacion(DataSet):
    """
    DataSet específico para problemas de clasificación (predecir categorías/textos).
    """
    
    def agregar_registro(self, registro: Registro):
        # isinstance() es un guardián: comprueba que el objeto 'registro' 
        # sea de la clase 'RegistroClasificacion'. Así evitamos mezclar tipos de datos.
        if not isinstance(registro, RegistroClasificacion):
            raise TypeError("Error: Solo puedes añadir objetos RegistroClasificacion a un DataSetClasificacion.")
        
        # Si pasa el filtro, lo añadimos a la lista heredada del padre
        self.registros.append(registro)


class DataSetRegresion(DataSet):
    """
    DataSet específico para problemas de regresión (predecir números continuos).
    """
    
    def agregar_registro(self, registro: Registro):
        # El mismo guardián, pero esta vez exige que sea de Regresión
        if not isinstance(registro, RegistroRegresion):
            raise TypeError("Error: Solo puedes añadir objetos RegistroRegresion a un DataSetRegresion.")
        
        self.registros.append(registro)