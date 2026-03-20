import os
import pandas as pd
from factoria import FactoriaUniversal
from modelos import Clasificador_kNN, Regresor_kNN
from preprocesado import NormalizadorMaxMin, NormalizadorZ_Score
from validacion import ValidacionClasificacion, ValidacionRegresion
from dataset import DataSetRegresion
from registro import RegistroRegresion

# ==============================================================================
# 🏆 SCRIPT DEFINITIVO DE ENTREGA - CONCURSO LAB 4 🏆
# ==============================================================================

def ejecutar_solucion_final():
    print("======================================================")
    print("   🚀 INICIANDO EJECUCIÓN OPTIMIZADA - CONCURSO LAB 4")
    print("======================================================\n")

    # --------------------------------------------------------------------------
    # 🛠️ RUTAS ABSOLUTAS DINÁMICAS
    # --------------------------------------------------------------------------
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    ruta_datos = os.path.abspath(os.path.join(directorio_actual, "..", "datos"))
    
    ruta_wdbc = os.path.join(ruta_datos, "wdbc.data")
    ruta_concrete = os.path.join(ruta_datos, "Concrete_Data.xls")

    print(f"[INFO] Buscando carpeta de datos en: {ruta_datos}\n")

    # --------------------------------------------------------------------------
    # 1. CLASIFICACIÓN (Cáncer - WDBC)
    # --------------------------------------------------------------------------
    print(f"[INFO] Cargando Clasificación desde: {ruta_wdbc}...")
    
    try:
        # Cargamos y ELIMINAMOS el ID del paciente para no meter ruido
        ds_wdbc_bruto = FactoriaUniversal.crear_dataset_clasificacion(ruta_wdbc, indice_objetivo=1)
        dataset_wdbc = ds_wdbc_bruto.eliminar_atributos([0])
        
        print(f"✅ ¡Éxito! Se han cargado y limpiado {len(dataset_wdbc.registros)} pacientes del WDBC.")
        
        # Pesos ganadores (98.24%)
        pesos_wdbc = [
            2.0229, 1.0928, 1.2099, 1.1382, 1.7445, 1.9285, 2.5584, 2.3458, 2.3926, 1.9179, 
            0.9515, 1.1415, 1.8654, 1.9383, 0.9526, 1.1654, 1.5095, 2.287, 0.9504, 1.7277, 
            1.2995, 1.4505, 0.2806, 1.7814, 2.0305, 0.6688, 0.7301, 0.6822, 1.0694, 1.5698
        ]
        
        modelo_clasificacion = Clasificador_kNN(k=3, distancia="ponderada", pesos=pesos_wdbc)
        validador_clasificacion = ValidacionClasificacion()
        
        resultados_wdbc = validador_clasificacion.validacion_cruzada(
            modelo=modelo_clasificacion, 
            dataset=dataset_wdbc, 
            m_bolsas=5, 
            normalizador=NormalizadorMaxMin(), 
            shuffle=False
        )
        
        print("★" * 60)
        print(f"🥇 RESULTADO CLASIFICACIÓN (WDBC)")
        print(f"   Parámetros    : k=3 | Norm: Max-Min | Dist: Ponderada")
        print(f"   Accuracy Final: {resultados_wdbc.get('Accuracy', 0):.2f}%")
        print("★" * 60 + "\n")
            
    except Exception as e:
        print(f"❌ ERROR INESPERADO en Clasificación: {e}")

    # --------------------------------------------------------------------------
    # 2. REGRESIÓN (Hormigón - Concrete)
    # --------------------------------------------------------------------------
    print(f"[INFO] Cargando Regresión desde: {ruta_concrete}...")
    
    try:
        # Lectura robusta mediante Pandas para lidiar con el archivo Excel (.xls)
        try:
            df = pd.read_excel(ruta_concrete)
        except:
            df = pd.read_csv(ruta_concrete)
            
        df = df.apply(pd.to_numeric, errors='coerce').dropna()
        
        dataset_concrete = DataSetRegresion()
        dataset_concrete.set_cabeceras(df.columns.tolist())
        
        for fila in df.values.tolist():
            atributos = fila[:-1]
            objetivo = fila[-1]
            dataset_concrete.agregar_registro(RegistroRegresion(atributos, objetivo))
            
        print(f"✅ ¡Éxito! Se han cargado {len(dataset_concrete.registros)} registros de Concrete.")
        
        # Pesos ganadores con hiper-precisión (47.4133)
        pesos_concrete = [
            0.44442150038934314, 0.14801365055221993, 0.0018797915556658714, 
            0.42971486857733476, 0.898581554223812, 0.0, 0.033613410419959244, 3.4304310676649763
        ]
        
        modelo_regresion = Regresor_kNN(k=3, distancia="ponderada", pesos=pesos_concrete)
        validador_regresion = ValidacionRegresion()
        
        resultados_concrete = validador_regresion.validacion_cruzada(
            modelo=modelo_regresion, 
            dataset=dataset_concrete, 
            m_bolsas=5, 
            normalizador=NormalizadorZ_Score(), 
            shuffle=False
        )
        
        print("★" * 60)
        print(f"🥇 RESULTADO REGRESIÓN (CONCRETE)")
        print(f"   Parámetros: k=3 | Norm: Z-Score | Dist: Ponderada")
        print(f"   MSE Final : {resultados_concrete.get('MSE', 0):.4f}")
        print("★" * 60 + "\n")
            
    except Exception as e:
        print(f"❌ ERROR INESPERADO en Regresión: {e}")

if __name__ == "__main__":
    ejecutar_solucion_final()