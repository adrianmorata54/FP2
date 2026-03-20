# ==============================================================================
# MÓDULO: validacion.py
# Propósito: Evaluar el rendimiento de los modelos de Machine Learning.
# Implementa técnicas para evitar el Overfitting (sobreajuste) y medir el error real.
# ==============================================================================

import random
from abc import ABC, abstractmethod
from dataset import DataSet
from modelos import Modelo
from preprocesado import Preprocesamiento
import math

class Validacion(ABC):
    """
    Clase base abstracta para orquestar los 'exámenes' de los modelos.
    Al usar una clase abstracta, obligamos a que las validaciones concretas
    (Clasificación y Regresión) implementen sus propias métricas matemáticas.
    """
    
    @abstractmethod
    def calcular_metricas(self, predichas: list, reales: list) -> dict:
        """
        Dada una lista de predicciones del modelo y las etiquetas correctas reales, 
        devuelve un diccionario con las notas (ej: Accuracy, MAE, etc.).
        """
        pass

    def validacion_simple(self, modelo: Modelo, dataset: DataSet, porcentaje_test: float, normalizador: Preprocesamiento = None) -> dict:
        """
        Técnica 'Hold-Out'. Divide el dataset en un conjunto de entrenamiento (Train)
        y un conjunto de prueba (Test).
        Ejemplo: porcentaje_test = 0.2 (20% para examen, 80% para estudio).
        """
        # 1. Barajamos los datos para que el corte sea aleatorio y representativo
        registros = dataset.registros.copy()
        random.shuffle(registros)

        # 2. Calculamos el índice exacto donde hacer el corte ("tijeretazo")
        corte = int(len(registros) * (1 - porcentaje_test))
        train_registros = registros[:corte]
        test_registros = registros[corte:]

        # 3. Fabricamos los dos nuevos DataSets independientes
        ds_train = dataset.crear_subconjunto(train_registros)
        ds_test = dataset.crear_subconjunto(test_registros)

        # 4. PREPROCESADO ESTRICTO (¡Punto clave para evitar Data Leakage!)
        if normalizador is not None:
            # El normalizador SOLO se ajusta (aprende min/max o medias) con los datos de Train
            normalizador.ajustar(ds_train)
            
            # Una vez aprendidos los parámetros de Train, transformamos AMBOS conjuntos
            ds_train = normalizador.transformar_dataSet(ds_train)
            ds_test = normalizador.transformar_dataSet(ds_test)

        # 5. Fase de Entrenamiento: El modelo estudia
        modelo.entrenar(ds_train)

        # 6. Fase de Inferencia: El modelo hace el examen
        predichas = []
        reales = []
        for reg in ds_test.registros:
            predichas.append(modelo.predecir(reg))
            reales.append(reg.objetivo)

        # 7. Evaluación: Calculamos la nota final
        return self.calcular_metricas(predichas, reales)

    

    def validacion_cruzada(self, modelo: Modelo, dataset: DataSet, m_bolsas: int, normalizador: Preprocesamiento = None, shuffle: bool = True) -> dict:
        """
        Técnica 'K-Fold Cross-Validation' (Validación Cruzada en m bolsas).
        Es mucho más robusta que el Hold-Out porque todo dato se usa para entrenar
        y TODO dato se usa (una vez) para testear. Devuelve la nota media.
        """
        registros = dataset.registros.copy()
        if shuffle:
            random.shuffle(registros)

        # Repartimos los registros en 'm' bolsas equitativamente usando List Comprehension con saltos
        bolsas = [registros[i::m_bolsas] for i in range(m_bolsas)]
        
        notas_examenes = []

        # Hacemos 'm' iteraciones. En cada vuelta, una bolsa distinta es el Test.
        for i in range(m_bolsas):
            # La bolsa 'i' es nuestro examen (Test)
            test_registros = bolsas[i]
            
            # Y TODAS las demás bolsas se juntan para formar el material de estudio (Train)
            train_registros = []
            for j in range(m_bolsas):
                if i != j:
                    train_registros.extend(bolsas[j])

            ds_train = dataset.crear_subconjunto(train_registros)
            ds_test = dataset.crear_subconjunto(test_registros)

            # Prevención estricta de Data Leakage en cada iteración
            if normalizador is not None:
                normalizador.ajustar(ds_train)
                ds_train = normalizador.transformar_dataSet(ds_train)
                ds_test = normalizador.transformar_dataSet(ds_test)

            modelo.entrenar(ds_train)

            predichas = []
            reales = []
            for reg in ds_test.registros:
                predichas.append(modelo.predecir(reg))
                reales.append(reg.objetivo)

            # Guardamos el diccionario de notas de esta ronda específica
            nota_ronda = self.calcular_metricas(predichas, reales)
            notas_examenes.append(nota_ronda)

        # Agregación de resultados: Calculamos la media de todas las métricas en las 'm' rondas
        nota_media = {}
        # Iteramos por cada clave (ej: "Accuracy", "MAE")
        for clave in notas_examenes[0].keys():
            nota_media[clave] = sum(nota[clave] for nota in notas_examenes) / m_bolsas
            
        return nota_media


# ==============================================================================
# MÉTRICAS CONCRETAS (ETAPA 9)
# ==============================================================================

class ValidacionClasificacion(Validacion):
    """Evaluación para problemas categóricos (ej: Iris o Diabetes)."""
    
    def calcular_metricas(self, predichas: list[str], reales: list[str]) -> dict:
        aciertos = sum(1 for p, r in zip(predichas, reales) if p == r)
        total = len(reales)
        
        # Accuracy: Porcentaje de aciertos totales
        accuracy = aciertos / total
        # Error Rate: La tasa de fallos complementaria
        error_rate = 1.0 - accuracy 
        
        return {
            "Accuracy": round(accuracy * 100, 2),
            "Error Rate": round(error_rate * 100, 2)
        }



class ValidacionRegresion(Validacion):
    """Evaluación para problemas numéricos continuos (ej: Boston Housing)."""
    
    def calcular_metricas(self, predichas: list[float], reales: list[float]) -> dict:
        n = len(reales)
        
        # MAE (Mean Absolute Error): Media de los errores absolutos. Es fácil de interpretar.
        errores_absolutos = [abs(p - r) for p, r in zip(predichas, reales)]
        mae = sum(errores_absolutos) / n
        
        # MSE (Mean Squared Error): Eleva los errores al cuadrado. Penaliza muchísimo
        # cuando el modelo hace una predicción MUY desencaminada.
        errores_cuadraticos = [(p - r)**2 for p, r in zip(predichas, reales)]
        mse = sum(errores_cuadraticos) / n
        
        return {
            "MAE": round(mae, 4),
            "MSE": round(mse, 4)
        }

# ==============================================================================
# SELECCIÓN DE ATRIBUTOS (ETAPA 11)
# ==============================================================================


class SeleccionAtributos:
    """Clase para encontrar y filtrar las características más importantes de un dataset."""
    
    @staticmethod
    def seleccion_correlacion(dataset: DataSet, p: float) -> list[int]:
        """
        Calcula la correlación de Pearson entre cada atributo (columna) y la variable objetivo (etiqueta).
        Pearson mide la relación lineal entre dos variables (de -1 a 1).
        Devuelve los índices del top p% de los atributos que más afectan al resultado.
        """
        # 1. Transformar objetivos a valores numéricos (necesario para Pearson)
        y = []
        mapa_clases = {}
        for reg in dataset.registros:
            try:
                # Si es Regresión, ya es un número (ej: precio de casa)
                y.append(float(reg.objetivo)) 
            except ValueError:
                # Si es Clasificación (texto), mapeamos cada texto a un ID numérico (0, 1, 2...)
                if reg.objetivo not in mapa_clases:
                    mapa_clases[reg.objetivo] = len(mapa_clases)
                y.append(float(mapa_clases[reg.objetivo]))
                
        media_y = sum(y) / len(y)
        num_atributos = len(dataset.registros[0].atributos)
        correlaciones = []

        # 2. Aplicar la fórmula matemática de la Correlación de Pearson para cada columna
        for i in range(num_atributos):
            x = [reg.atributos[i] for reg in dataset.registros]
            media_x = sum(x) / len(x)

            # Covarianza (numerador)
            numerador = sum((xi - media_x) * (yi - media_y) for xi, yi in zip(x, y))
            # Desviaciones estándar (denominador)
            denominador_x = sum((xi - media_x) ** 2 for xi in x)
            denominador_y = sum((yi - media_y) ** 2 for yi in y)

            # Prevención de división por cero si la columna es una constante
            if denominador_x == 0 or denominador_y == 0:
                r = 0.0
            else:
                r = numerador / math.sqrt(denominador_x * denominador_y)

            # Guardamos el valor absoluto |r|, porque una correlación fuerte negativa (-0.9) 
            # es igual de útil para predecir que una correlación fuerte positiva (+0.9).
            correlaciones.append((abs(r), i))

        # 3. Ordenamos de mayor a menor importancia
        correlaciones.sort(key=lambda item: item[0], reverse=True)

        # 4. Seleccionamos el top 'p' (ej: si p=0.5, nos quedamos con la mejor mitad)
        num_a_seleccionar = max(1, int(num_atributos * p))
        mejores_indices = [idx for corr, idx in correlaciones[:num_a_seleccionar]]
        
        return mejores_indices