

# =====================================================================
# 1. GESTOR GENERAL: Todos los proyectos
# =====================================================================
class Gestor_Proyecto:
    """
    Clase contenedor para almacenar objetos de la clase base 'Proyecto'.
    Aquí guardaremos absolutamente todos los registros (7092 en total),
    tanto los que han sido concedidos como los denegados.
    """
    
    def __init__(self):
        self.lista_proyectos = []
        
    # Método para encapsular la inserción de datos
    def añadir(self, proyecto):
        """Añade un objeto Proyecto al final de la lista interna."""
        self.lista_proyectos.append(proyecto)

    # Método para consultar información sin tocar la lista directamente
    def total(self):
        """Devuelve el número total de proyectos almacenados."""
        return len(self.lista_proyectos)


# =====================================================================
# 2. GESTOR ESPECÍFICO: Proyectos Concedidos
# =====================================================================
class Gestor_ProyectoConcedido:
    """
    Clase contenedor exclusiva para objetos de tipo 'ProyectoConcedido'.
    Aunque el código es idéntico al de arriba, el PDF pide clases separadas
    por claridad conceptual (aquí solo irán los 3252 proyectos aprobados).
    """
    
    def __init__(self):
        self.lista_proyectos = []
        
    def añadir(self, proyecto):
        self.lista_proyectos.append(proyecto)
        
    def total(self):
        """Devuelve el número total de proyectos concedidos almacenados."""
        return len(self.lista_proyectos)


# =====================================================================
# 3. GESTOR SÚPER ESPECÍFICO: Proyectos con Contrato
# =====================================================================
class Gestor_ProyectoContrato:
    """
    Clase contenedor exclusiva para objetos de tipo 'ProyectoContrato'.
    Aquí solo guardaremos la "élite": los 1149 proyectos aprobados 
    que además tienen un contrato predoctoral.
    """
    
    def __init__(self):
        self.lista_proyectos = []
        
    def añadir(self, proyecto):
        self.lista_proyectos.append(proyecto)
        
    def total(self):
        """Devuelve el número total de proyectos con contrato almacenados."""
        return len(self.lista_proyectos)