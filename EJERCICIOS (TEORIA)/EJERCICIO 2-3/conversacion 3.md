# Memoria Técnica: Desarrollo Asistido por IA y Resolución de Asimetrías en Datos

## 1. Introducción
El objetivo de esta práctica es integrar dos fuentes de datos de la Universidad de Sevilla (US): un PDF con la carga docente y un directorio web (extraído mediante Web Scraping) con las sedes de cada departamento. 

El mayor reto del proyecto no fue la codificación inicial, sino la depuración de un error de asimetría de datos. Para solucionarlo, se utilizó un enfoque iterativo mediante el uso de Inteligencia Artificial (LLM), donde el intercambio de prompts y respuestas fue la clave del éxito.

## 2. Proceso de Depuración Guiado por Prompts

A continuación, se detalla el flujo de trabajo real entre el desarrollador y el asistente de IA que permitió alcanzar una tasa de éxito del 100% (0 fallos) en la fusión de datos.

### Iteración 1: El descubrimiento del problema
Tras lograr cruzar 133 de los 134 departamentos, el sistema daba un error persistente.

* **Prompt del desarrollador:** *"El código funciona casi perfecto, pero me da 1 fallo al cruzar los datos: No se encontró sede para -> DEPARTAMENTO DE CIENCIAS JURÍDICAS BÁSICAS. He intentado normalizarlo pero sigue fallando."*
* **Respuesta de la IA:** *"Es posible que el PDF tenga caracteres invisibles o saltos de línea ocultos (\xa0). Sin embargo, antes de hacer un código complejo para limpiarlo, te sugiero que vayas a la web oficial de la US y mires exactamente cómo está escrito ese departamento allí."*

### Iteración 2: El factor humano en los datos
Siguiendo el consejo de la IA, se auditó la fuente de datos original (la web de la US).

* **Prompt del desarrollador:** *"He mirado en la web y resulta que ahí se llama: CIENCIAS JURÍDICAS BÁSICAS (DERECHO ROMANO, HISTORIA DEL DERECHO Y DERECHO ECLESIÁSTICO DEL ESTADO). En el PDF solo se llama DEPARTAMENTO DE CIENCIAS JURÍDICAS BÁSICAS. Por eso no coinciden."*
* **Respuesta de la IA:** *"¡Ahí está el problema! Es una asimetría humana. Ninguna función normalizadora va a cruzar eso porque son textos distintos. Para solucionarlo sin romper tu código, vamos a hacer un mapeo manual (bypass). Inyecta esta línea en tu diccionario web:*
`diccionario_web["DEPARTAMENTO DE CIENCIAS JURÍDICAS BÁSICAS"] = "FACULTAD DE DERECHO"`*"*

### Iteración 3: El orden de ejecución
Se aplicó el parche recomendado, pero el error persistía.

* **Prompt del desarrollador:** *"He puesto el parche en el código principal, pero me sigue dando 1 fallo al ejecutarlo. ¿Qué está pasando?"*
* **Respuesta de la IA:** *"El problema es el orden de ejecución. Has puesto la inyección de datos DESPUÉS de llamar a la función `asignar_sedes()`. Estás intentando darle la tirita al paciente cuando ya se ha ido del hospital. Tienes que mover esa línea de código para que esté justo ANTES de hacer la fusión."*

### Iteración 4: El éxito total
Tras reubicar la línea de código, el programa ejecutó la fusión a la perfección.

* **Prompt del desarrollador:** *"¿Por qué me ha dado ahora 0 fallos? [Se adjunta log de consola mostrando: '✅ Fusión completada. Fallos de coincidencia documentados: 0', seguido de las estadísticas de carga docente por sede y el manejo de excepciones para sedes con un único departamento]."*
* **Respuesta de la IA:** *"¡Por dos motivos clave! Primero, porque el orden de los factores sí altera el producto: al poner el parche antes del cruce, le dimos la información a tiempo. Segundo, por el 'caballo de Troya': al inyectar la clave exacta del PDF en el diccionario de la web, la función ignoró el nombre kilométrico de internet y cruzó los datos al 100%. Has conseguido conectar a internet, raspar 134 enlaces, limpiar datos, inyectar datos faltantes y calcular estadísticas complejas. Todo con 0 fallos."*

## 3. Conclusión
El desarrollo de esta práctica evidencia que la programación asistida por IA es una herramienta fundamental para el *Data Engineering*. La interacción mediante prompts no solo sirvió para generar código, sino para razonar sobre la lógica del flujo de ejecución y entender la naturaleza imperfecta de los datos reales extraídos mediante Web Scraping.