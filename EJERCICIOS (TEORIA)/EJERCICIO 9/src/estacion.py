class Estacion:
    """
    Representa una estación individual de la red de Metro.
    """

    def __init__(self, nombre: str, latitud: float = None, longitud: float = None):
        """
        Inicializa una nueva Estación.
        Las coordenadas son opcionales al principio, ya que podemos 
        buscarlas o actualizarlas más adelante usando nuestra API.
        """
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud

    def __eq__(self, otro) -> bool:
        """
        Define cómo comparar dos objetos Estacion.
        Condición: 'dos estaciones son iguales si tienen el mismo nombre'.
        """
        if isinstance(otro, Estacion):
            return self.nombre == otro.nombre
        return False

    def __hash__(self) -> int:
        """
        Hace que el objeto sea 'hasheable'.
        Al igual que con Linea, basamos el hash en el nombre para poder usar 
        objetos Estacion como claves en nuestro grafo_estaciones.
        """
        return hash(self.nombre)
        
    def __repr__(self) -> str:
        """
        Representación visual del objeto por consola.
        Si tiene coordenadas las muestra, si no, solo el nombre.
        """
        if self.latitud is not None and self.longitud is not None:
            return f"Estacion({self.nombre} [{self.latitud:.4f}, {self.longitud:.4f}])"
        return f"Estacion({self.nombre})"