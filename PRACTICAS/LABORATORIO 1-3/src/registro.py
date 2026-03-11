# ==============================================================================
# MÓDULO: registro.py
# Propósito: Representar la unidad básica de datos (un paciente, una flor, una casa)
# y dotarla de la capacidad matemática para compararse con otros registros.
# ==============================================================================

import math

class Registro:
    """Clase base que representa un punto en el espacio multidimensional."""
    
    def __init__(self, atributos: list[float]):
        # El constructor acepta un vector de números (las coordenadas del punto)
        self.atributos = atributos
    
    def distancia_euclidea(self, otro: 'Registro') -> float:
        """Calcula la línea recta entre dos puntos (Teorema de Pitágoras multidimensional)."""
        # Programación defensiva: No puedes comparar un punto 3D con uno 2D.
        if len(self.atributos) != len(otro.atributos):
            raise ValueError("Los registros deben tener la misma dimensión para calcular la distancia.")
            
        # MAGIA PYTHONICA: zip()
        # zip() empareja iterables. Empareja el atributo 'a' (mío) con el 'b' (del otro).
        # Calcula la suma de las diferencias al cuadrado: Σ (a - b)²
        suma_cuadrados = sum((a - b) ** 2 for a, b in zip(self.atributos, otro.atributos))
        return math.sqrt(suma_cuadrados)

    def distancia_manhattan(self, otro: 'Registro') -> float:
        """Calcula la distancia moviéndose en ángulos rectos (como un taxi en una cuadrícula urbana)."""
        if len(self.atributos) != len(otro.atributos):
            raise ValueError("Los registros deben tener la misma dimensión para calcular la distancia.")        
            
        # Suma de los valores absolutos de las diferencias: Σ |a - b|
        return sum(abs(a - b) for a, b in zip(self.atributos, otro.atributos))

    def distancia_ponderada(self, otro: 'Registro', pesos: list[float]) -> float:
        """Calcula la distancia dando más importancia (peso) a unas variables que a otras."""
        if len(self.atributos) != len(otro.atributos):
            raise ValueError("Los registros deben tener la misma dimensión para calcular la distancia.")
            
        # zip() ahora empareja tres cosas a la vez: el atributo actual (a), el del otro (b) y el peso (w)
        return sum(w * ((a - b) ** 2) for a, b, w in zip(self.atributos, otro.atributos, pesos))

    def calcula_distancia(self, otro: 'Registro', tipo: str = "euclídea", pesos: list[float] = None) -> float:
        """Método 'enrutador' (Router). Recibe el tipo de distancia en texto y delega en la función adecuada."""
        tipo = tipo.lower() # Pasamos a minúsculas para evitar errores tipográficos del usuario
        
        if len(self.atributos) != len(otro.atributos):
            raise ValueError("Los registros deben tener la misma dimensión para calcular la distancia.")
            
        if tipo == "manhattan":
            return self.distancia_manhattan(otro)
        elif tipo == "ponderada":
            if pesos is None:
                raise ValueError("Se requieren pesos para calcular la distancia ponderada.")
            return self.distancia_ponderada(otro, pesos)
        else:
            return self.distancia_euclidea(otro)

    def normalizar(self, minimos: list[float], maximos: list[float]) -> 'Registro':
        """
        Escala todos los valores numéricos para que estén en un rango estricto entre 0 y 1.
        Fórmula matemática: x' = (x - min) / (max - min)
        """
        nuevos_atributos = []
        for x, min_val, max_val in zip(self.atributos, minimos, maximos):
            # Prevención de división por cero (si una columna tiene todo el rato el mismo valor)
            if max_val == min_val:
                valor_norm = 0.0
            else:
                valor_norm = (x - min_val) / (max_val - min_val)
            nuevos_atributos.append(valor_norm)
        
        # TRUCO DE LA INSTANCIACIÓN DINÁMICA:
        # Si esto lo llama un 'RegistroClasificacion', debe devolver un 'RegistroClasificacion'.
        if hasattr(self, 'objetivo'):
            return self.__class__(nuevos_atributos, self.objetivo)
        else:
            return self.__class__(nuevos_atributos)


    def estandarizar(self, medias: list[float], desviaciones: list[float]) -> 'Registro':
        """
        (LABORATORIO 3)
        Aplica la estandarización Z-Score. Centra los datos en media 0 y desviación típica 1.
        Fórmula matemática: z = (x - media) / desviacion_tipica
        """
        nuevos_atributos = []
        for x, media, desv in zip(self.atributos, medias, desviaciones):
            if desv == 0.0:
                valor_est = 0.0
            else:
                valor_est = (x - media) / desv
            nuevos_atributos.append(valor_est)
        
        if hasattr(self, 'objetivo'):
            return self.__class__(nuevos_atributos, self.objetivo)
        else:
            return self.__class__(nuevos_atributos)
    
    def k_vecinos(self, registros: list['Registro'], k: int, tipo_distancia: str = "euclídea", pesos: list[float] = None) -> list[int]:
        """
        Calcula la distancia de ESTE registro contra TODOS los de la lista,
        los ordena de menor a mayor distancia, y devuelve los índices de los 'k' ganadores.
        """
        distancias_con_indices = []
        
        # enumerate() nos da tanto el objeto como su posición original (índice)
        for indice, registro in enumerate(registros):
            # IDENTIDAD vs IGUALDAD: 'is' comprueba la dirección de memoria.
            # Evita que un paciente ya metido en la base de datos se elija a sí mismo como su mejor vecino.
            if registro is self:
                continue
                
            dist = self.calcula_distancia(registro, tipo_distancia, pesos)
            
            # Guardamos una tupla: (distancia, índice_original)
            distancias_con_indices.append((dist, indice))
            
        # ORDENACIÓN LAMBDA: Le decimos al método sort() que ordene basándose
        # ÚNICAMENTE en la posición 0 de la tupla (la distancia) y que ignore el índice.
        distancias_con_indices.sort(key=lambda item: item[0])
        
        # Devolvemos una lista por comprensión (List Comprehension) extrayendo solo los índices de los 'k' primeros
        return [indice for dist, indice in distancias_con_indices[:k]]

    def __str__(self):
        # Función auxiliar para imprimir el registro de forma legible por pantalla
        formato_atributos = [round(v, 2) for v in self.atributos]
        return f"Registro{formato_atributos}"


# ==============================================================================
# CLASES HIJAS (Añaden la "Etiqueta" / Variable Objetivo)
# ==============================================================================

class RegistroClasificacion(Registro):
    """Para problemas categóricos (ej: 'Enfermo', 'Sano')."""
    
    def __init__(self, atributos: list[float], objetivo: str):
        # Validación de tipos estricta para asegurar la pureza de los datos
        if not isinstance(objetivo, str):
            raise TypeError(f"El objetivo en clasificación debe ser texto (str). Has pasado: {type(objetivo).__name__}")
            
        super().__init__(atributos)
        self.objetivo = objetivo
        
    def __repr__(self):
        formato = [round(v, 2) for v in self.atributos]
        return f"RegistroClasificacion(atributos={formato}, objetivo='{self.objetivo}')"


class RegistroRegresion(Registro):
    """Para problemas numéricos (ej: Precio = 250000.50)."""
    
    def __init__(self, atributos: list[float], objetivo: float):
        if not isinstance(objetivo, (float, int)):
            raise TypeError(f"El objetivo en regresión debe ser numérico (float). Has pasado: {type(objetivo).__name__}")
            
        super().__init__(atributos)
        self.objetivo = float(objetivo)
        
    def __repr__(self):
        formato = [round(v, 2) for v in self.atributos]
        return f"RegistroRegresion(atributos={formato}, objetivo={self.objetivo})"