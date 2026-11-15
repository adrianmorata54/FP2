# FP2 · Fundamentos de Programación 2

Repositorio con los **boletines de teoría**, las **prácticas de laboratorio** y la **práctica de examen** de la asignatura *Fundamentos de Programación 2* (Grado en Ingeniería Informática · Inteligencia Artificial, curso 2025/26).

Todo el código está escrito en **Python** y sigue una metodología de **programación orientada a objetos**: clases, herencia, clases abstractas (`ABC`), factorías, igualdad/hash de objetos y estructuras de datos (listas, tuplas, diccionarios) aplicadas a problemas reales y de Inteligencia Artificial.

> **Autor:** _[tu nombre]_

---

## Índice

- [Estructura del repositorio](#estructura-del-repositorio)
- [Ejercicios de teoría (boletines)](#ejercicios-de-teoría-boletines)
- [Prácticas de laboratorio](#prácticas-de-laboratorio)
- [Notas](#notas)

---

## Estructura del repositorio

```text
FP2/
├── EJERCICIOS (TEORIA)/
│   ├── EJERCICIO 1/            # Boletín 1
│   ├── EJERCICIO 2-3/          # Boletines 2 y 3
│   ├── EJERCICIO 4-5/          # Boletines 4 y 5
│   ├── EJERCICIO 6/            # Boletín 6
│   ├── EJERCICIO 7/            # Boletín 7
│   ├── EJERCICIO 8/            # Boletín 8
│   ├── EJERCICIO 9/            # Boletín 9
│   └── PRÁCTICA EXAMEN/        # Ejercicios de preparación del examen final
└── PRÁCTICAS/
    ├── LABORATORIO 1-3/        # Clasificadores y regresores (ML desde cero)
    ├── LABORATORIO 5-6/        # Agencia Estatal de Investigación
    ├── LABORATORIO 7-8/        # Optimización heurística de funciones
    ├── LABORATORIO 9/          # Predicción de series temporales
    └── LABORATORIO 10/         # Series diferencias y detección de anomalías
```

Cada ejercicio mantiene la misma organización interna:

```text
EJERCICIO X/
├── Boletin X.(pdf|docx)    # Enunciado
├── datos/                  # Ficheros de entrada (CSV, Excel, PDF...)
└── src/                    # Código fuente (main.py como punto de entrada)
```

---

## Ejercicios de teoría (boletines)

| Boletín | Tema | Conceptos principales |
|:-------:|------|-----------------------|
| **1** | Alumnos, profesores y asignaturas | Clases, herencia (`Persona` → `Alumno`/`Profesor`), lectura de CSV |
| **2** | Departamentos de la Universidad de Sevilla | Lectura de datos desde un PDF "sucio", clase contenedora `Universidad`, carga docente real |
| **3** | Sedes de los departamentos | Obtención de datos de la web, diccionarios, departamentos con mayor/menor carga por sede |
| **4** | Estadísticas de La Liga (1928-29 a 2017-18) | Lectura de Excel, consultas sobre jugadores, equipos y temporadas |
| **5** | Estadísticas de La Liga (diseño POO correcto) | Clases `Jugador`, `Equipo`, `Temporada` y `Liga`, propiedades derivadas |
| **6** | Elecciones generales 2023 (Congreso) | Diseño OO de circunscripciones, comunidades y partidos; comprobación de sumas; gráficos de sectores y barras |
| **7** | Nomenclátor de nombres de pila (INE) | Frecuencias por década, propiedades derivadas, exportación a Excel |
| **8** | Metro de Madrid como grafo | Clases `Líneas` y `Estaciones`, conversión entre ambas visiones, igualdad vs. identidad, líneas circulares, conectividad |
| **9** | Metro de Madrid (diseño con 4 clases) | `Linea`, `Estacion`, `Lineas`, `Estaciones`; objetos *hasheables* y `__eq__` |

---

## Prácticas de laboratorio

### Laboratorios 1-3 · Clasificadores y regresores
Construcción desde cero de un pequeño framework de **aprendizaje supervisado**:

- `Registro`, `RegistroClasificacion`, `RegistroRegresion`
- `DataSet` (abstracta), `DataSetClasificacion`, `DataSetRegresion`
- Factoría universal para cargar datasets (Iris, Wine, Diabetes, Boston Housing, Breast Cancer, Concrete...)
- **Modelos:** k-NN (clasificación y regresión), clasificador por centroides, regresión lineal múltiple
- **Preprocesado:** normalización Max-Min, estandarización Z-Score, filtro de varianza
- **Validación:** métricas para clasificación y regresión, selección de atributos
- `lab4_concurso.py`: script de entrega del concurso del Laboratorio 4

### Laboratorios 5-6 · Agencia Estatal de Investigación
Análisis de los resultados de una convocatoria de proyectos de investigación (2024) a partir de ficheros Excel:

- Clases `Proyecto`, `ProyectoConcedido` y `ProyectoContrato`
- Gestores de proyectos con estadísticas por Comunidad Autónoma (tasas de éxito, financiación por habitante...)

### Laboratorios 7-8 · Optimización heurística de funciones
Algoritmos de **búsqueda local de trayectoria única** para minimizar funciones de caja negra, con parametrización dinámica y visualización del avance de la optimización.

- Incluye la función de Schwefel como ejercicio voluntario.
- La carpeta `dist/` contiene el módulo de retos ofuscado con **PyArmor** proporcionado por el profesorado.

### Laboratorio 9 · Predicción de series temporales
Planteamiento de la predicción de series temporales como un problema de **regresión** reutilizando el framework de los laboratorios anteriores (`Regresor_kNN`, `Regresor_kNN_Ponderado`, `Regresor_kNN_Correlacion`, regresión lineal).

### Laboratorio 10 · Series diferencias y detección de anomalías
- Predicción sobre la **serie de diferencias** y comparación de MAE con la serie original.
- **Detección de anomalías** en datos de sensórica de un proceso industrial (20 variables medidas cada minuto) con `GestorAnomalias`.
- Se incluyen las gráficas generadas y el Excel de resultados.

---


> Ejecuta siempre desde la carpeta `src` del ejercicio: los módulos se importan entre sí y los ficheros de datos se buscan en la carpeta `datos/` correspondiente.

---

## Notas

- Los enunciados originales (PDF/DOCX) se incluyen junto a cada ejercicio como referencia.
- Los ficheros de datos pertenecen a sus respectivas fuentes (INE, Ministerio del Interior, Agencia Estatal de Investigación, Metro de Madrid, repositorio UCI, etc.) y se incluyen únicamente con fines educativos.
- Los módulos ofuscados con PyArmor (`LABORATORIO 7-8/dist/`) forman parte del material de la asignatura y están ligados a una plataforma concreta (runtime `.pyd` de Windows).
- Proyecto de carácter **académico**.
