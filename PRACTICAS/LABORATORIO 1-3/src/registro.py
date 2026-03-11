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
        # Validación: No puedes comparar un punto 3D con uno 2D.
        if len(self.atributos) != len(otro.atributos):
            raise ValueError("Los registros deben tener la misma dimensión para calcular la distancia.")
            
        # MAGIA PYTHONICA: zip()
        # zip() empareja los atributos del registro actual (a) con los del otro (b).
        # Hacemos la suma de: (a - b)^2
        suma_cuadrados = sum((a - b) ** 2 for a, b in zip(self.atributos, otro.atributos))
        return math.sqrt(suma_cuadrados)

    def distancia_manhattan(self, otro: 'Registro') -> float:
        """Calcula la distancia moviéndose en ángulos rectos (como un taxi en Nueva York)."""
        if len(self.atributos) != len(otro.atributos):
            raise ValueError("Los registros deben tener la misma dimensión para calcular la distancia.")        
            
        # Suma de los valores absolutos de las diferencias: |a - b|
        return sum(abs(a - b) for a, b in zip(self.atributos, otro.atributos))

    def distancia_ponderada(self, otro: 'Registro', pesos: list[float]) -> float:
        """Calcula la distancia dando más importancia (peso) a unas variables que a otras."""
        if len(self.atributos) != len(otro.atributos):
            raise ValueError("Los registros deben tener la misma dimensión para calcular la distancia.")
            
        # zip() ahora empareja tres cosas: atributo actual (a), atributo del otro (b) y el peso (w)
        return sum(w * ((a - b) ** 2) for a, b, w in zip(self.atributos, otro.atributos, pesos))

    def calcula_distancia(self, otro: 'Registro', tipo: str = "euclídea", pesos: list[float] = None) -> float:
        """Método 'enrutador'. Recibe el tipo de distancia en texto y llama a la función adecuada."""
        tipo = tipo.lower() # Pasamos a minúsculas para evitar errores si el usuario escribe "Euclídea"
        
        if len(self.atributos) != len(otro.atributos):
            raise ValueError("Los registros deben tener la misma dimensión para calcular la distancia.")
            
        if tipo == "manhattan":
            return self.distancia_manhattan(otro)
        elif tipo == "ponderada":
            if pesos is None:
                raise ValueError("Se requieren pesos para calcular la distancia ponderada.")
            return self.distancia_ponderada(otro, pesos)
        else:
            # Por defecto, o si escriben "euclidea", usamos esta
            return self.distancia_euclidea(otro)

    def normalizar(self, minimos: list[float], maximos: list[float]) -> 'Registro':
        """
        Escala todos los valores para que estén entre 0 y 1.
        Fórmula: x' = (x - min) / (max - min)
        """
        nuevos_atributos = []
        for x, min_val, max_val in zip(self.atributos, minimos, maximos):
            # Prevención de división por cero (si todos los valores de una columna son idénticos)
            if max_val == min_val:
                valor_norm = 0.0
            else:
                valor_norm = (x - min_val) / (max_val - min_val)
            nuevos_atributos.append(valor_norm)
        
        # EL TRUCO DE LA INSTANCIACIÓN DINÁMICA:
        # Si este método lo llama un RegistroClasificacion, debe devolver un RegistroClasificacion.
        # Si lo llama un RegistroRegresion, debe devolver un RegistroRegresion.
        # hasattr() comprueba si el objeto tiene la variable 'objetivo'.
        if hasattr(self, 'objetivo'):
            # self.__class__ crea un objeto de la misma clase que hizo la llamada
            return self.__class__(nuevos_atributos, self.objetivo)
        else:
            return self.__class__(nuevos_atributos)

    def k_vecinos(self, registros: list['Registro'], k: int, tipo_distancia: str = "euclídea", pesos: list[float] = None) -> list[int]:
        """
        Calcula la distancia de ESTE registro contra TODOS los de la lista,
        los ordena de más cercano a más lejano, y devuelve las posiciones (índices) de los 'k' ganadores.
        """
        distancias_con_indices = []
        
        # enumerate() nos da la posición en la lista (indice) y el dato (registro)
        for indice, registro in enumerate(registros):
            # IDENTIDAD vs IGUALDAD: 'is' comprueba si son exactamente el mismo objeto en memoria.
            # Evitamos que un paciente se compare consigo mismo y diga "¡soy mi mejor vecino!".
            if registro is self:
                continue
                
            dist = self.calcula_distancia(registro, tipo_distancia, pesos)
            
            # Guardamos una tupla: (la distancia calculada, la posición en la lista original)
            distancias_con_indices.append((dist, indice))
            
        # .sort() ordena la lista. Le decimos mediante una función lambda (anónima) 
        # que ordene fijándose exclusivamente en la posición 0 de la tupla (la distancia).
        distancias_con_indices.sort(key=lambda item: item[0])
        
        # Extraemos solo los índices (ignorando ya la distancia) de los primeros 'k' elementos [:k]
        return [indice for dist, indice in distancias_con_indices[:k]]

    def __str__(self):
        # Función auxiliar para imprimir el registro de forma legible, redondeando a 2 decimales
        formato_atributos = [round(v, 2) for v in self.atributos]
        return f"Registro{formato_atributos}"


# ==============================================================================
# CLASES HIJAS (Añaden el concepto de "Etiqueta" o "Variable Objetivo")
# ==============================================================================

class RegistroClasificacion(Registro):
    """Para problemas donde predecimos categorías (ej: 'Enfermo', 'Sano')."""
    
    def __init__(self, atributos: list[float], objetivo: str):
        # Programación defensiva: Forzamos que la etiqueta sea un texto
        if not isinstance(objetivo, str):
            raise TypeError(f"El objetivo en clasificación debe ser texto (str). Has pasado: {type(objetivo).__name__}")
            
        # Inicializamos la parte matemática llamando al padre
        super().__init__(atributos)
        # Añadimos la etiqueta
        self.objetivo = objetivo
        
    def __repr__(self):
        # __repr__ es como __str__ pero se usa cuando imprimimos listas enteras de objetos
        formato = [round(v, 2) for v in self.atributos]
        return f"RegistroClasificacion(atributos={formato}, objetivo='{self.objetivo}')"


class RegistroRegresion(Registro):
    """Para problemas donde predecimos números exactos (ej: Precio de una casa: 250000.50)."""
    
    def __init__(self, atributos: list[float], objetivo: float):
        # Programación defensiva: Forzamos que la etiqueta sea un número
        if not isinstance(objetivo, (float, int)):
            raise TypeError(f"El objetivo en regresión debe ser numérico (float). Has pasado: {type(objetivo).__name__}")
            
        super().__init__(atributos)
        # Lo forzamos a float por si el usuario pasó un int (ej: 5 -> 5.0)
        self.objetivo = float(objetivo)
        
    def __repr__(self):
        formato = [round(v, 2) for v in self.atributos]
        return f"RegistroRegresion(atributos={formato}, objetivo={self.objetivo})"