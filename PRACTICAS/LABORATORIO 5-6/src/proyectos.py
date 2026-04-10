
# =====================================================================
# 1. CLASE BASE: Proyecto
# =====================================================================
class Proyecto:
    """
    Clase base (el molde principal). 
    Representa CUALQUIER proyecto que se presenta, ya sea concedido o denegado.
    Contiene solo la información más básica.
    """
    
    def __init__(self, referencia, area, entidad_solicitante, comunidad_autonoma):
        
        self.referencia = referencia
        self.area = area
        self.entidad_solicitante = entidad_solicitante
        self.comunidad_autonoma = comunidad_autonoma
        
        # Por defecto, asumimos que un proyecto NO está concedido. 
        self.concedido = False 


# =====================================================================
# 2. PRIMERA HERENCIA: ProyectoConcedido
# =====================================================================
class ProyectoConcedido(Proyecto):
    """
    Esta clase HEREDA de Proyecto.
    Sirve para los proyectos que SÍ consiguieron dinero.
    Tiene todos los datos de Proyecto + datos económicos.
    """
    
    # Este constructor pide los 4 datos básicos + todos los datos de dinero nuevos
    def __init__(self, referencia, area, entidad_solicitante, comunidad_autonoma, 
                 costes_directos, costes_indirectos, anticipo, subvencion, 
                 anualidades, num_contratos=0):
        
        super().__init__(referencia, area, entidad_solicitante, comunidad_autonoma)
        
        # Como este molde es exclusivo para proyectos concedidos, cambiamos 
        # el atributo que heredamos de la clase padre de False a True.
        self.concedido = True
        
        # Guardamos los nuevos datos económicos exclusivos de esta clase
        self.costes_directos = costes_directos
        self.costes_indirectos = costes_indirectos
        self.anticipo = anticipo
        self.subvencion = subvencion
        self.anualidades = anualidades # Esto será una lista con 4 números (los 4 años)
        
        # Evaluamos si tiene contrato: si el número de contratos es mayor que 0, 
        # esto guardará True. Si es 0, guardará False.
        self.contratado_predoctoral = num_contratos > 0
        
        # VALIDACIÓN: El PDF pide comprobar que los costes cuadran con las ayudas.
        # Usamos round(numero, 2) para redondear a 2 decimales y evitar los típicos
        # fallos matemáticos internos de Python con los decimales largos.
        suma_costes = round(self.costes_directos + self.costes_indirectos, 2)
        suma_ayudas = round(self.anticipo + self.subvencion, 2)
        
        # Si las matemáticas no cuadran, imprimimos un aviso por pantalla
        if suma_costes != suma_ayudas:
            print(f"Aviso en {self.referencia}: Costes ({suma_costes}) no coincide con Ayudas ({suma_ayudas}).")

    @property
    def presupuesto(self):
        """Devuelve la suma de los costes directos e indirectos (El presupuesto total)."""
        return self.costes_directos + self.costes_indirectos


# =====================================================================
# 3. SEGUNDA HERENCIA: ProyectoContrato
# =====================================================================
class ProyectoContrato(ProyectoConcedido):
    """
    Esta clase es la más especializada. HEREDA de ProyectoConcedido.
    Sirve para proyectos que fueron aprobados (tienen dinero) y que ADEMÁS 
    tienen asignado un contrato predoctoral (por lo que tienen un Título).
    """
    
    # Este constructor pide la avalancha de datos anterior + el "titulo_proyecto"
    def __init__(self, referencia, area, entidad_solicitante, comunidad_autonoma, 
                 costes_directos, costes_indirectos, anticipo, subvencion, 
                 anualidades, titulo_proyecto, num_contratos=1):
        
        super().__init__(referencia, area, entidad_solicitante, comunidad_autonoma, 
                         costes_directos, costes_indirectos, anticipo, subvencion, 
                         anualidades, num_contratos)
        
        # Aunque la clase padre ya calculaba esto, aquí lo forzamos a True 
        # para estar seguros, ya que si usamos esta clase es porque SÍ hay contrato.
        self.contratado_predoctoral = True
        
        # Guardamos el dato exclusivo de esta clase: el título de la investigación
        self.titulo_proyecto = titulo_proyecto