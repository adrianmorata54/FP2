import pandas as pd
from jugador import Jugador
from equipo import Equipo
from temporada import Temporada
from liga import Liga

class Factoria:
    """
    Clase Factoría encargada de leer los datos en crudo, 
    validar su consistencia e instanciar toda la jerarquía de objetos.
    Lanza excepciones si los datos no cumplen las reglas de negocio.
    """
    
    @staticmethod
    def construir_liga(ruta_archivo):
        print(f"Cargando datos desde {ruta_archivo}...")
        
        try:
            df = pd.read_excel(ruta_archivo) 
        except Exception as e:
            raise Exception(f"Error al leer el archivo: {e}\n(Si te pide una librería, ejecuta 'pip install xlrd' en la terminal)")
            
        liga = Liga()
        
        def limpiar_num(valor):
            if pd.isna(valor): return 0
            return int(float(valor))  # Forzamos a entero por seguridad
            
        # =========================================================
        # PASO 1: Calcular número de equipos por temporada 
        # (Necesario para la validación de partidos máximos)
        # =========================================================
        equipos_por_temp = df.groupby('TEMPORADA')['EQUIPO'].nunique().to_dict()

        # =========================================================
        # PASO 2: Lectura, Validación y Parada en caso de error
        # =========================================================
        for index, fila in df.iterrows():
            temporada_str = str(fila['TEMPORADA']).strip()
            nombre_equipo = str(fila['EQUIPO']).strip()
            nombre_jugador = str(fila['JUGADOR']).strip()
            
            # Recogemos y limpiamos las métricas
            partidos = limpiar_num(fila['PJUGADOS'])
            pcompletos = limpiar_num(fila['PCOMPLETOS'])
            ptitular = limpiar_num(fila['PTITULAR'])
            psuplente = limpiar_num(fila['PSUPLENTE'])
            minutos = limpiar_num(fila['MINUTOS'])
            lesiones = limpiar_num(fila.get('LESIONES', 0))
            tarjetas = limpiar_num(fila['TARJETAS'])
            expulsiones = limpiar_num(fila['EXPULSIONES'])
            goles = limpiar_num(fila['GOLES'])
            penalties = limpiar_num(fila.get('PENALTIES FALLADOS', 0))

            # ---------------------------------------------------------
            # VALIDACIONES ESTRICTAS (BOLETÍN 5)
            # Si falla alguna, lanzamos un ValueError y el programa SE DETIENE.
            # ---------------------------------------------------------
            
            # Validación 1: Temporadas coherentes (ej. 2017-18 -> 17+1 = 18)
            try:
                y1, y2 = temporada_str.split('-')
                if (int(y1) + 1) % 100 != int(y2):
                    raise ValueError()
            except:
                raise ValueError(f"Error en fila {index + 2} ({nombre_jugador}): Temporada incoherente o formato inválido '{temporada_str}'.")

            # Validación 2: Cantidades positivas
            cantidades = {'Partidos': partidos, 'Completos': pcompletos, 'Titular': ptitular, 
                          'Suplente': psuplente, 'Minutos': minutos, 'Lesiones': lesiones, 
                          'Tarjetas': tarjetas, 'Expulsiones': expulsiones, 'Goles': goles, 'Penalties': penalties}
            
            for clave, valor in cantidades.items():
                if valor < 0:
                    raise ValueError(f"Error en fila {index + 2} ({nombre_jugador}): La cantidad de '{clave}' es negativa ({valor}).")
                
            # Validación 3: Partidos completos <= Partidos titular
            if pcompletos > ptitular:
                raise ValueError(f"Error en fila {index + 2} ({nombre_jugador}): Partidos completos ({pcompletos}) supera a partidos de titular ({ptitular}).")
                
            # Validación 4: Partidos jugados == Suplente + Titular
            if partidos != (psuplente + ptitular):
                raise ValueError(f"Error en fila {index + 2} ({nombre_jugador}): Partidos jugados ({partidos}) no equivale a suplente ({psuplente}) + titular ({ptitular}).")
                
            # Validación 5: Minutos <= Partidos jugados * 90
            max_minutos_posibles = partidos * 90
            if minutos > max_minutos_posibles:
                raise ValueError(f"Error en fila {index + 2} ({nombre_jugador}): Minutos jugados ({minutos}) supera el máximo matemático posible para {partidos} partidos ({max_minutos_posibles} min).")
                
            # Validación 6: Partidos jugados <= Partidos de la temporada
            num_equipos = equipos_por_temp.get(temporada_str, 0)
            max_partidos_temporada = (num_equipos - 1) * 2 if num_equipos > 1 else 0
            
            # ¡EXCEPCIÓN HISTÓRICA! La famosa "Liga del Play-off" (1986-87) tuvo 44 partidos en lugar de 34
            if temporada_str == "1986-87":
                max_partidos_temporada = 44
                
            if partidos > max_partidos_temporada:
                raise ValueError(f"Error en fila {index + 2} ({nombre_jugador}): Partidos jugados ({partidos}) supera el total de partidos posibles en la temporada {temporada_str} ({max_partidos_temporada}).")

            # ---------------------------------------------------------
            # INSTANCIACIÓN POO JERÁRQUICA
            # Solo llegamos aquí si TODAS las validaciones han sido correctas
            # ---------------------------------------------------------
            
            if temporada_str not in liga.temporadas:
                nueva_temp = Temporada(temporada_str)
                liga.agregar_temporada(nueva_temp)
                
            temporada_obj = liga.temporadas[temporada_str]
            
            if nombre_equipo not in temporada_obj.equipos:
                nuevo_eq = Equipo(nombre_equipo, temporada_str)
                temporada_obj.agregar_equipo(nuevo_eq)
                
            equipo_obj = temporada_obj.equipos[nombre_equipo]
            
            jugador_obj = Jugador(
                nombre=nombre_jugador,
                partidos=partidos,
                pcompletos=pcompletos,
                ptitular=ptitular,
                psuplente=psuplente,
                minutos=minutos,
                lesiones=lesiones,
                tarjetas=tarjetas,
                expulsiones=expulsiones,
                goles=goles,
                penalties=penalties
            )
            
            equipo_obj.agregar_jugador(jugador_obj)
            
        print("¡Construcción POO terminada con éxito! Todos los datos son válidos.")
        return liga