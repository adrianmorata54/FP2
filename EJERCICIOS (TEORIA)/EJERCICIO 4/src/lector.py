import pandas as pd
from jugador import Jugador
from equipo import Equipo
from liga import Liga

class LectorDatos:
    @staticmethod
    def construir_liga(ruta_archivo):
        print(f"Cargando datos desde {ruta_archivo}...")
        
        try:
            # ¡CAMBIO AQUÍ! Usamos read_excel porque el archivo es un .xls
            df = pd.read_excel(ruta_archivo) 
        except Exception as e:
            raise Exception(f"Error al leer el archivo: {e}\n(Si te pide una librería, ejecuta 'pip install xlrd' en la terminal)")
            
        liga = Liga()
        
        # Función interna para limpiar celdas vacías (NaN) del Excel
        def limpiar_num(valor):
            if pd.isna(valor): return 0
            return valor
            
        for index, fila in df.iterrows():
            temporada = str(fila['TEMPORADA'])
            nombre_equipo = str(fila['EQUIPO'])
            
            # Recogemos TODAS las columnas del dataset
            jugador = Jugador(
                nombre=fila['JUGADOR'],
                partidos=limpiar_num(fila['PJUGADOS']),
                pcompletos=limpiar_num(fila['PCOMPLETOS']),
                ptitular=limpiar_num(fila['PTITULAR']),
                psuplente=limpiar_num(fila['PSUPLENTE']),
                minutos=limpiar_num(fila['MINUTOS']),
                lesiones=limpiar_num(fila['LESIONES']),
                tarjetas=limpiar_num(fila['TARJETAS']),
                expulsiones=limpiar_num(fila['EXPULSIONES']),
                goles=limpiar_num(fila['GOLES']),
                penalties=limpiar_num(fila['PENALTIES FALLADOS'])
            )
            
            liga.agregar_registro(temporada, nombre_equipo, jugador)
            
        print("¡Construcción de objetos terminada!")
        return liga 