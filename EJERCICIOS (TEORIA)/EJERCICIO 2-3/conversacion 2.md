# 📑 BITÁCORA DE INGENIERÍA: EVOLUCIÓN DEL ALGORITMO DE LECTURA

**Proyecto:** Análisis de Carga Docente (Universidad de Sevilla)
**Objetivo:** Extracción robusta de datos desde `departamentos.pdf` (134 registros).

---

### 1️⃣ PLANTEAMIENTO INICIAL Y ARQUITECTURA
**👤 USUARIO (Prompt):**
> "La lectura del pdf vamos a adaptarla en una clase llamada Factoria, que sea capaz de leer el pdf y podamos crear en el main un objeto de tipo Universidad, el cual es una clase que tambien me puedes definir ya. Esta clase Universidad tendrá como atributos una lista de Departamentos y un nombre, y como funciones, las siguientes: la primera consiste en que dado un numero n, nos diga los n departamentos con mayor carga docente real; y la segunda será que dado un número n, sepamos cuales son los n departamentos con menos carga docente real."

**🤖 RESPUESTA TÉCNICA:**
Se diseñó la arquitectura orientada a objetos (Clases `Universidad` y `Factoria`). Para la lectura, se propuso la librería estándar **`tabula-py`** en modo **`lattice=True`**, asumiendo una estructura de tabla estándar con bordes definidos (rejilla).
`[ESTADO: 🟡 PROPUESTA INICIAL]`

---

### 2️⃣ INSPECCIÓN VISUAL Y REAJUSTE
**👤 USUARIO (Prompt):**
> "Aqui tienes el pdf con el que estamos trabajando, yo creo que separa titulo de la columna con el contenido pero las columnas entre si no tienen lineas de separacion."

**🤖 RESPUESTA TÉCNICA:**
Tras confirmar la ausencia de líneas divisorias negras, se modificó la estrategia a **`stream=True`**. Este modo deja de buscar bordes físicos y pasa a calcular los "ríos" de espacio en blanco vertical para inferir la separación virtual de las columnas.
`[ESTADO: 🟡 ADAPTACIÓN VISUAL]`

---

### 3️⃣ ERROR CRÍTICO DE ENTORNO
**👤 USUARIO (Prompt):**
> "He ejecutado el main y me ha salido esto: `Failed to import jpype dependencies. No module named 'jpype'`. Se ha cargado la Universidad de Sevilla con 0 departamentos."

**🤖 DIAGNÓSTICO:**
Fallo en el puente Python-Java. La librería `tabula` es un *wrapper* que requiere una instalación perfecta de **Java (JRE)** en el sistema operativo. La dependencia falló al intentar arrancar la Máquina Virtual de Java (JVM), devolviendo objetos vacíos.
`[ESTADO: 💥 FALLO DE DEPENDENCIAS]`

---

### 4️⃣ BLOQUEO DEL SISTEMA (DEADLOCK)
**👤 USUARIO (Prompt):**
> "Lo he ejecutado y no ha avanzado la consola de este mensaje: `Intentando leer PDF con Tabula...`"

**🤖 DECISIÓN DE INGENIERÍA:**
Ante el bloqueo indefinido (*Deadlock*) de la JVM, se decidió **abandonar `tabula`**. Se migró a **`pdfplumber`**, una librería nativa de Python.
* **Ventaja:** Elimina la dependencia de Java.
* **Resultado:** El código se vuelve portable y no se congela.
`[ESTADO: 🛑 CAMBIO DE LIBRERÍA]`

---

### 5️⃣ SOLUCIÓN FINAL ROBUSTA (REGEX)
**👤 USUARIO (Prompt):**
> "Vale, pero necesito que la lectura sea robusta."

**🤖 IMPLEMENTACIÓN FINAL:**
Para garantizar la robustez sin depender de la alineación visual (que fallaba por milímetros), se implementó **Análisis Sintáctico con Expresiones Regulares**.
1.  **Lectura:** Se extrae el texto plano línea a línea.
2.  **Patrón:** Si la línea contiene "DEPARTAMENTO", se usa `re.findall` para extraer la secuencia numérica.
3.  **Asignación:** Se toma el primer número como ETC y el último como Experimentalidad, ignorando el formato visual.
`[ESTADO: 🚀 SOLUCIÓN IMPLEMENTADA]`

---

### 6️⃣ VALIDACIÓN DEL SISTEMA
**👤 USUARIO (Prompt):**
> "Vale, ahora si ha leido bien el pdf."

**🏁 CONCLUSIÓN:**
El sistema evolucionó desde una lectura visual frágil (dependiente de Java) a una extracción lógica basada en patrones de texto (**Python Puro + Regex**), logrando procesar el 100% de los registros correctamente.
`[ESTADO: ✅ ÉXITO]`