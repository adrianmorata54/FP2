# ==============================================================================
# MÓDULO: dataset.py
# Propósito: Gestionar conjuntos de datos (colecciones de registros).
# Actúa como el contenedor principal donde almacenamos la información de entrenamiento.
# ==============================================================================

# Importamos las herramientas de Python para crear Clases Abstractas (Abstract Base Classes)
# Una clase abstracta es como un "contrato" o "molde base". Obliga a las clases hijas
# a implementar ciertas funciones, garantizando una estructura consistente.
from abc import ABC, abstractmethod

# Importamos las clases de 'registro.py' para poder validar la información
# que se inserta en este contenedor.
from registro import Registro, RegistroClasificacion, RegistroRegresion

import statistics

class DataSet(ABC):
    """
    Clase abstracta contenedora de registros. 
    Al heredar de ABC, Python nos prohíbe hacer un 'DataSet()' genérico.
    Siempre tendremos que instanciar sus especializaciones: 'DataSetClasificacion' o 'DataSetRegresion'.
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
        # Por tanto, los "atributos" descriptivos son todos menos el último.
        self.nombres_atributos = cabeceras[:-1]

    @abstractmethod
    def agregar_registro(self, registro: Registro):
        """
        Método abstracto (vacío). 
        El decorador @abstractmethod obliga por ley a que cualquier clase hija 
        tenga que programar obligatoriamente este método. Garantiza que cada tipo
        de DataSet valide sus propios registros antes de insertarlos.
        """
        pass

    def calcular_min_max(self) -> tuple[list[float], list[float]]:
        """
        Recorre todos los registros para encontrar el valor más pequeño y el más 
        grande de cada columna. Fundamental para el preprocesado 'NormalizadorMaxMin'.
        """
        # Si el dataset está vacío, devolvemos listas vacías para evitar errores de ejecución.
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
                # Si encontramos un valor más extremo, actualizamos nuestras listas
                if valor < minimos[i]:
                    minimos[i] = valor
                if valor > maximos[i]:
                    maximos[i] = valor

        # Devolvemos ambas listas simultáneamente en una tupla
        return minimos, maximos

    def calcular_medias_desviaciones(self) -> tuple[list[float], list[float]]:
        """
        Calcula la media y la desviación típica para cada columna (atributo).
        Fundamental para el preprocesado 'NormalizadorZ_Score' (Estandarización).
        """
        if not self.registros:
            raise ValueError("El DataSet está vacío.")
            
        num_atributos = len(self.registros[0].atributos)
        medias = []
        desviaciones = []
        
        for i in range(num_atributos):
            # Extraemos toda la columna 'i' iterando sobre todos los registros
            columna = [registro.atributos[i] for registro in self.registros]
            
            # Calculamos la media de esa columna
            medias.append(statistics.mean(columna))
            
            # La desviación típica necesita al menos 2 datos para calcularse
            if len(columna) > 1:
                desviaciones.append(statistics.stdev(columna))
            else:
                desviaciones.append(0.0)
                
        return medias, desviaciones
    
    def crear_subconjunto(self, lista_registros: list[Registro]) -> 'DataSet':
        """
        Crea un "clon" del DataSet actual pero conteniendo únicamente los registros proporcionados.
        Crucial para la Validación Cruzada y Hold-Out, donde separamos datos de Train y Test.
        """
        # TRUCO MÁGICO DE PYTHON: self.__class__()
        # Instanciamos dinámicamente un objeto de la misma clase que hizo la llamada
        # (DataSetClasificacion o DataSetRegresion), sin necesidad de usar bloques 'if/else'.
        nuevo_dataset = self.__class__()
        
        # Copiamos las cabeceras originales
        nuevo_dataset.nombres_atributos = self.nombres_atributos.copy()
        
        # Insertamos los nuevos registros
        nuevo_dataset.registros = lista_registros.copy()
        
        return nuevo_dataset
    
    def eliminar_atributos(self, indices_a_eliminar: list[int]) -> 'DataSet':
        """
        Devuelve un DataSet nuevo eliminando las columnas especificadas.
        Permite la reducción de dimensionalidad para mejorar el rendimiento del modelo.
        """
        if not self.registros:
            raise ValueError("El DataSet está vacío.")
            
        num_atributos = len(self.registros[0].atributos)
        
        # Validación de seguridad: Asegurar que los índices solicitados existen
        for idx in indices_a_eliminar:
            if idx < 0 or idx >= num_atributos:
                raise ValueError(f"Índice {idx} fuera de rango. Debe estar entre 0 y {num_atributos-1}.")

        # Filtramos los nombres de las cabeceras usando List Comprehension
        nuevos_nombres = [nom for i, nom in enumerate(self.nombres_atributos) if i not in indices_a_eliminar]

        # Reconstruimos cada registro omitiendo las columnas marcadas
        nuevos_registros = []
        for reg in self.registros:
            # Filtramos los valores numéricos del registro
            nuevos_attrs = [val for i, val in enumerate(reg.atributos) if i not in indices_a_eliminar]
            
            # Instanciamos un nuevo Registro dinámicamente, comprobando si tiene etiqueta objetivo
            if hasattr(reg, 'objetivo'):
                nuevos_registros.append(reg.__class__(nuevos_attrs, reg.objetivo))
            else:
                nuevos_registros.append(reg.__class__(nuevos_attrs))

        # Ensamblamos el nuevo DataSet depurado
        nuevo_dataset = self.__class__()
        nuevo_dataset.nombres_atributos = nuevos_nombres
        nuevo_dataset.registros = nuevos_registros
        return nuevo_dataset


# ==============================================================================
# CLASES HIJAS (CONCRETAS)
# ==============================================================================

class DataSetClasificacion(DataSet):
    """
    Contenedor específico para problemas predictivos categóricos (Clasificación).
    """
    
    def agregar_registro(self, registro: Registro):
        # PATRÓN GUARDIÁN: isinstance() asegura la integridad de los datos.
        # Bloquea la inserción de registros de regresión o mal formados.
        if not isinstance(registro, RegistroClasificacion):
            raise TypeError("Error: Solo puedes añadir objetos RegistroClasificacion a un DataSetClasificacion.")
        
        self.registros.append(registro)


class DataSetRegresion(DataSet):
    """
    Contenedor específico para problemas predictivos numéricos continuos (Regresión).
    """
    
    def agregar_registro(self, registro: Registro):
        # PATRÓN GUARDIÁN: Protege la pureza del dataset asegurando que solo
        # entren registros con etiquetas numéricas (RegistroRegresion).
        if not isinstance(registro, RegistroRegresion):
            raise TypeError("Error: Solo puedes añadir objetos RegistroRegresion a un DataSetRegresion.")
        
        self.registros.append(registro)