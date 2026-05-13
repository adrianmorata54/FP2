class Linea:
    """
    Representa una línea individual de la red de Metro.
    """

    def __init__(self, nombre: str, escircular: bool = False):
        """
        Inicializa una nueva Línea.
        """
        self.nombre = nombre
        self.escircular = escircular

    def __eq__(self, otro) -> bool:
        """
        Define cómo comparar dos objetos Linea.
        Dos líneas son iguales estrictamente si tienen el mismo nombre.
        """
        if isinstance(otro, Linea):
            return self.nombre == otro.nombre
        return False

    def __hash__(self) -> int:
        """
        Hace que el objeto sea 'hasheable'.
        Al basar el hash en el nombre, garantizamos que líneas con el mismo 
        nombre generen el mismo identificador interno.
        """
        return hash(self.nombre)
        
    def __repr__(self) -> str:
        """
        Representación en texto para cuando imprimamos el objeto por pantalla 
        (muy útil para depurar errores).
        """
        tipo = "Circular" if self.escircular else "Lineal"
        return f"Linea({self.nombre} - {tipo})"