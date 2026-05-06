import numpy as np
import retos_optimizacion as reto

class Funcion_8(reto._BaseOpt):
    def __init__(self):
        shift_vectors = [0.0] * 10
        super().__init__(shift_vectors)

    def evaluar(self, x):
        z = self._preparar_x(x)
        z = z - self._shift
        
        # Evaluamos la sumatoria de z * sen(sqrt(|z|))
        sum_term = np.sum(z * np.sin(np.sqrt(np.abs(z))))
        return float(418.9828872724338 * self._dims - sum_term)

class Funcion_8_modificada(reto._BaseOpt):
    def __init__(self):
        # Aplicamos la "trampa" para mover el mínimo a [1.0]*10
        shift_vectors = [-419.9687] * 10
        super().__init__(shift_vectors)

    def evaluar(self, x):
        z = self._preparar_x(x)
        z = z - self._shift
        
        # Evaluamos la sumatoria de z * sen(sqrt(|z|))
        sum_term = np.sum(z * np.sin(np.sqrt(np.abs(z))))
        return float(418.9828872724338 * self._dims - sum_term)