# ==============================================================================
# MÓDULO: preprocesado.py
# Propósito: Preparar, limpiar y escalar los datos antes de entrenar al modelo.
# Implementa el patrón de diseño "Fit/Transform" (Ajustar y Transformar).
# ==============================================================================

from abc import ABC, abstractmethod
from dataset import DataSet
from registro import Registro

class Preprocesamiento(ABC):
    """
    Clase base abstracta para cualquier técnica de preprocesado de datos.
    Establece un contrato estricto: todo filtro o escalador debe saber 'ajustar'
    (aprender los parámetros matemáticos) y 'transformar' (aplicar las matemáticas).
    """
    
    @abstractmethod
    def ajustar(self, dataset: DataSet):
        """Aprende de los datos (ej: busca el mínimo, el máximo, la media...)."""
        pass

    @abstractmethod
    def transformar_registro(self, registro: Registro) -> Registro:
        """Aplica la transformación aprendida a un solo registro."""
        pass

    @abstractmethod
    def transformar_dataSet(self, dataset: DataSet) -> DataSet:
        """Aplica la transformación aprendida a un DataSet entero."""
        pass



class NormalizadorMaxMin(Preprocesamiento):
    """
    Escala los datos para que todos los atributos estén estrictamente entre 0 y 1.
    Útil para algoritmos basados en distancias (como KNN) para evitar que una columna
    con valores muy altos (ej: el precio en millones) eclipse a columnas con valores
    muy bajos (ej: el número de habitaciones).
    """
    
    def __init__(self):
        # Empezamos sin saber nada de los datos
        self.minimos = []
        self.maximos = []

    def ajustar(self, dataset: DataSet):
        # Fase FIT: Solo miramos los datos para aprender cuáles son sus límites
        self.minimos, self.maximos = dataset.calcular_min_max() 

    def transformar_registro(self, registro: Registro) -> Registro:
        # Fase TRANSFORM: Si no hemos aprendido los límites antes, lanzamos error
        if not self.minimos or not self.maximos:
            raise ValueError("Debes llamar a 'ajustar' antes de transformar.")
            
        # Delegamos la matemática en el propio registro
        return registro.normalizar(self.minimos, self.maximos)

    def transformar_dataSet(self, dataset: DataSet) -> DataSet:
        if not self.minimos or not self.maximos:
            raise ValueError("Debes llamar a 'ajustar' antes de transformar.")
            
        # Transformamos toda la lista de pacientes/flores usando una List Comprehension
        registros_transformados = [self.transformar_registro(r) for r in dataset.registros]
        
        # Aprovechamos el método crear_subconjunto para devolver un clon intacto
        # en lugar de sobrescribir el dataset original (Programación Funcional).
        return dataset.crear_subconjunto(registros_transformados)


class NormalizadorZ_Score(Preprocesamiento):
    """
    Estandariza los datos para que tengan media 0 y desviación típica 1.
    A diferencia del MaxMin, este método no enjaula los datos entre 0 y 1, 
    sino que los centra, lo cual es mucho más robusto frente a valores atípicos (outliers).
    """
    
    def __init__(self):
        self.medias = []
        self.desviaciones = []

    def ajustar(self, dataset: DataSet):
        # Fase FIT: Aprendemos la media y la desviación de la campana de Gauss
        self.medias, self.desviaciones = dataset.calcular_medias_desviaciones()

    def transformar_registro(self, registro: Registro) -> Registro:
        if not self.medias or not self.desviaciones:
            raise ValueError("Debes llamar a 'ajustar' antes de transformar.")
        return registro.estandarizar(self.medias, self.desviaciones)

    def transformar_dataSet(self, dataset: DataSet) -> DataSet:
        if not self.medias or not self.desviaciones:
            raise ValueError("Debes llamar a 'ajustar' antes de transformar.")
            
        registros_transformados = [self.transformar_registro(r) for r in dataset.registros]
        return dataset.crear_subconjunto(registros_transformados)


class FiltroVarianza(Preprocesamiento):
    """
    (LABORATORIO 3 - ETAPA 12: PREPROCESADOS AVANZADOS)
    Selección de atributos: Elimina las columnas que casi no cambian de valor
    (varianza cercana a 0), ya que no aportan información discriminativa al modelo.
    """
    def __init__(self, umbral: float = 0.01):
        # umbral dicta lo mínimo que tiene que variar una columna para que la salvemos
        self.umbral = umbral
        self.indices_a_eliminar = []

    def ajustar(self, dataset: DataSet):
        import statistics # Lo usamos para calcular la varianza
        num_atributos = len(dataset.registros[0].atributos)
        self.indices_a_eliminar = []
        
        # Recorremos cada columna de arriba a abajo
        for i in range(num_atributos):
            columna = [reg.atributos[i] for reg in dataset.registros]
            
            if len(columna) > 1:
                varianza = statistics.variance(columna)
                # Si la varianza de esta columna es sospechosamente baja, la apuntamos en la "lista negra"
                if varianza < self.umbral:
                    self.indices_a_eliminar.append(i)

    def transformar_registro(self, registro: Registro) -> Registro:
        # Quitamos los atributos censurados de este paciente en concreto
        nuevos_attrs = [val for i, val in enumerate(registro.atributos) if i not in self.indices_a_eliminar]
        
        # Instanciamos dinámicamente un nuevo registro limpio
        if hasattr(registro, 'objetivo'):
            return registro.__class__(nuevos_attrs, registro.objetivo)
        else:
            return registro.__class__(nuevos_attrs)

    def transformar_dataSet(self, dataset: DataSet) -> DataSet:
        if self.indices_a_eliminar is None: 
            raise ValueError("Debes llamar a 'ajustar' antes de transformar.")
            
        # ¡Usamos el método super-potente de la Etapa 10!
        # Este método ya se encarga de crear un dataset nuevo borrando las columnas feas
        return dataset.eliminar_atributos(self.indices_a_eliminar)