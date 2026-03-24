import pandas as pd
from nacion import Nacion
from comunidad_autonoma import ComunidadAutonoma
from circunscripcion import Circunscripcion
from partido import Partido

class FactoriaElecciones:
    @staticmethod
    def cargar_datos(ruta_archivo='EJERCICIOS (TEORIA)\EJERCICIO 6\datos\PROV_02_202307_1.xlsx'):
        nacion = Nacion("España")
        errores_integridad = 0
        
        try:
            print("⏳ Leyendo archivo y validando integridad de datos...")
            if ruta_archivo.endswith('.csv'):
                df = pd.read_csv(ruta_archivo, header=None, dtype=str)
            else:
                df = pd.read_excel(ruta_archivo, header=None, dtype=str)

            df = df.fillna('')
            nombres_partidos = df.iloc[3].values
            
            for index in range(6, len(df)):
                row = df.iloc[index].values
                
                nombre_ccaa = str(row[0]).strip()
                if not nombre_ccaa: 
                    continue
                    
                codigo_prov = int(row[1]) if row[1] else 0
                nombre_prov = str(row[2]).strip()
                
                # --- EXTRACCIÓN DE TODOS LOS DATOS ---
                poblacion = int(row[3]) if row[3] else 0
                num_mesas = int(row[4]) if row[4] else 0
                
                censo_ine = int(row[5]) if row[5] else 0
                censo_cera = int(row[6]) if row[6] else 0
                censo_total = int(row[7]) if row[7] else 0
                
                votantes_ine = int(row[8]) if row[8] else 0
                votantes_cera = int(row[9]) if row[9] else 0
                votantes_totales = int(row[10]) if row[10] else 0
                
                votos_validos = int(row[11]) if row[11] else 0
                votos_candidaturas = int(row[12]) if row[12] else 0
                votos_blancos = int(row[13]) if row[13] else 0
                votos_nulos = int(row[14]) if row[14] else 0

                # ==========================================
                # 🛡️ COMPROBACIONES DE COHERENCIA DEL EXCEL
                # ==========================================
                if censo_total != (censo_ine + censo_cera):
                    print(f"⚠️ Aviso en {nombre_prov}: Censo Total ({censo_total}) != INE ({censo_ine}) + CERA ({censo_cera})")
                    errores_integridad += 1
                    
                if votantes_totales != (votantes_ine + votantes_cera):
                    print(f"⚠️ Aviso en {nombre_prov}: Votantes Totales ({votantes_totales}) != INE ({votantes_ine}) + CERA ({votantes_cera})")
                    errores_integridad += 1
                    
                if votantes_totales != (votos_validos + votos_nulos):
                    print(f"⚠️ Aviso en {nombre_prov}: Votantes ({votantes_totales}) != Válidos ({votos_validos}) + Nulos ({votos_nulos})")
                    errores_integridad += 1
                    
                if votos_validos != (votos_candidaturas + votos_blancos):
                    print(f"⚠️ Aviso en {nombre_prov}: Votos Válidos ({votos_validos}) != Candidaturas ({votos_candidaturas}) + Blancos ({votos_blancos})")
                    errores_integridad += 1
                # ==========================================

                # --- CREACIÓN DE OBJETOS ---
                if nombre_ccaa not in nacion.comunidades:
                    nacion.agregar_comunidad(ComunidadAutonoma(nombre_ccaa))
                ccaa = nacion.comunidades[nombre_ccaa]
                
                circ = Circunscripcion(
                    nombre_prov, codigo_prov, poblacion, num_mesas, 
                    censo_ine, censo_cera, censo_total, 
                    votantes_ine, votantes_cera, votantes_totales, 
                    votos_validos, votos_candidaturas, votos_blancos, votos_nulos
                )
                
                # --- LECTURA DE PARTIDOS ---
                for i in range(15, len(row) - 1, 2):
                    nombre_partido = str(nombres_partidos[i]).strip()
                    if not nombre_partido:
                        continue
                        
                    votos_partido = int(row[i]) if row[i] else 0
                    escanos_partido = int(row[i+1]) if row[i+1] else 0
                    
                    if votos_partido > 0 or escanos_partido > 0:
                        partido = Partido(nombre_partido, votos_partido, escanos_partido)
                        circ.agregar_partido(partido)
                        
                # 🛡️ COMPROBACIÓN FINAL DE PARTIDOS
                if not circ.chequear_sumas():
                    suma_calculada = sum(p.votos for p in circ.partidos)
                    print(f"⚠️ Aviso en {nombre_prov}: Suma de votos de partidos ({suma_calculada}) no coincide con la columna Votos a Candidaturas ({circ.votos_candidaturas})")
                    errores_integridad += 1

                ccaa.agregar_circunscripcion(circ)
                
            if errores_integridad == 0:
                print("✅ Lectura finalizada. Los datos son 100% coherentes y exactos matemáticamente.")
            else:
                print(f"⚠️ Lectura finalizada, pero se detectaron {errores_integridad} incoherencias internas en el Excel.")
                
            return nacion
            
        except FileNotFoundError:
            print(f"❌ Error: No se ha encontrado el archivo '{ruta_archivo}'.")
            return None
        except Exception as e:
            print(f"❌ Error crítico al procesar el archivo: {e}")
            return None