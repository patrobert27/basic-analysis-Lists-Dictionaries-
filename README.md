# English
## Data Processing – Large Files (Python)

### Overview
This project focuses on reading, validating, and cleaning **large data files** using Python, without relying on external libraries such as pandas for the initial processing stage.

The goal of this first step is to build a solid foundation in:
- File handling
- Data validation
- Basic data structures (`list`, `dict`)
- Clean and maintainable code organization

---

### Data Sources
The project works with three large files:

- **CSV file**
  - ~6000 rows
  - Employee-related data

- **Excel file**
  - 2 sheets:
    - `Transactions`
    - `Targets`

- **JSON file**
  - ~5500 orders
  - ~5200 audit events

These files simulate real-world datasets with non-trivial sizes.

---

### First Step / Initial Commit
In the first stage of the project, the focus is on **data cleaning and validation**.

#### What has been implemented
- Reading the CSV file using the Python standard library.
- Converting each row into a dictionary.
- Validating critical fields:
  - `age` must be between 18 and 70
  - `monthly_salary` must be greater than 0
  - `performance` must be between 1.0 and 5.0
- Separating data into:
  - A list of **valid records**
  - A list of **invalid records**, storing the `employee_id` and the reason for failure
- Organizing the logic using functions to improve readability and maintainability.

---

### Project Structure (Initial)
- Validation logic is encapsulated in dedicated functions.
- Data is stored in lists of dictionaries for easy processing in later stages.
- Error handling is implemented to prevent the program from crashing on malformed data.

---

### Next Steps
Future stages of the project will include:
- Generating metrics and aggregations
- Cross-referencing data between files
- Working with Excel multi-sheet data
- Processing nested JSON structur


# Español
## Procesamiento de Datos – Ficheros Grandes (Python)

### Descripción general
Este proyecto se centra en la lectura, validación y limpieza de **ficheros de gran tamaño** utilizando Python, sin depender de librerías externas como *pandas* en la fase inicial.

El objetivo principal de este primer paso es reforzar los fundamentos en:
- Manejo de ficheros
- Validación de datos
- Estructuras de datos básicas (`list`, `dict`)
- Organización de código limpio y mantenible

---

### Fuentes de datos
El proyecto trabaja con tres tipos de ficheros que simulan escenarios reales:

- **Archivo CSV**
  - Aproximadamente 6000 filas
  - Información de empleados

- **Archivo Excel**
  - Contiene 2 hojas:
    - `Transactions`
    - `Targets`

- **Archivo JSON**
  - Aproximadamente 5500 pedidos
  - Aproximadamente 5200 eventos de auditoría

Estos volúmenes de datos permiten practicar con conjuntos de información no triviales.

---

### Primer paso / Primer commit
En esta primera etapa, el foco está en la **limpieza y validación de datos**.

#### Funcionalidades implementadas
- Lectura del archivo CSV utilizando únicamente la librería estándar de Python.
- Conversión de cada fila en un diccionario.
- Validación de campos clave:
  - `age` debe estar entre 18 y 70
  - `monthly_salary` debe ser mayor que 0
  - `performance` debe estar entre 1.0 y 5.0
- Separación de los datos en:
  - Una lista de **registros válidos**
  - Una lista de **registros inválidos**, almacenando el `employee_id` y el motivo del error
- Uso de funciones para organizar la lógica y facilitar el mantenimiento del código.

---

### Estructura del proyecto (inicial)
- La lógica de validación está encapsulada en funciones específicas.
- Los datos se almacenan en listas de diccionarios para su posterior procesamiento.
- Se incluye manejo de errores para evitar que el programa falle ante datos mal formados.

---

### Próximos pasos
En fases posteriores se trabajará en:
- Generación de métricas y agregaciones
- Cruce de información entre distintos ficheros
- Procesamiento de archivos Excel con múltiples hojas
- Manejo de estructuras JSON anidadas
- Automatización del análisis mediante scripts

---

### Objetivo
Este proyecto forma parte de un *roadmap* personal para consolidar los fundamentos de Python y avanzar progresivamente hacia tareas más complejas de procesamiento y automatización de datos.
