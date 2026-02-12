# English
## Data Processing – Large Files (Python)

### Overview
This project focuses on reading, validating, and cleaning **large data files** using Python, without relying on external libraries such as *pandas* in the initial stage.

The main goal of this first phase is to strengthen the fundamentals of:

- File handling
- Data validation
- Basic data structures (`list`, `dict`)
- Clean and maintainable code organization
- Classes and abstraction
- Other core language concepts

---

### Data Sources
The project works with three types of files that simulate real-world scenarios:

- **CSV file `employees.csv`**
  - Approximately 6000 rows
  - Employee information

- **Excel file `sales.xlsx`**
  - Contains 2 sheets:
    - `Transactions`
    - `Targets`

- **JSON file `company_data.json`**
  - Approximately 5500 orders
  - Approximately 5200 audit events

These data volumes allow working with non-trivial datasets.

---

### First Step / First Commit
In this initial stage, the focus is on **data cleaning and validation**.

#### Implemented Features

**First version in the `main` branch:**

- Reading the CSV file using only Python’s standard library.
- Converting each row into a dictionary.
- Validation of key fields:
  - `age` must be between 18 and 70.
  - `monthly_salary` must be greater than 0.
  - `performance` must be between 1.0 and 5.0.
- Separation of data into:
  - A list of **valid records**.
  - A list of **invalid records**, storing the `employee_id` and the error reason.
- Use of functions to organize logic and improve code maintainability.

**Second version in the `pipeline-funcional` branch:**

- Implementation of a functional pipeline for data loading, validation, and processing.
- Clear separation of responsibilities through independent functions.

---

### Errors and Fixes During Development

- Initially, data was accessed directly using:

  ```python
  country = employee["country"]

This may cause errors if fields are null or incorrectly formatted.

- It was corrected by using a safer access approach:
  ```python
  country = (employee.get("country") or "").strip()

This prevents errors when data is missing and improves code robustness.

---

### Next Steps
In later stages, the project will include:
- Generating metrics and aggregations
- Cross-referencing data between different files
- Processing Excel files with multiple sheets
- Handling nested JSON structures
- Automating analysis through scripts

---

### Objetivo
This project is part of a personal *roadmap* to consolidate Python fundamentals and progressively move toward more complex data processing and automation tasks.


# Español
## Procesamiento de Datos – Ficheros Grandes (Python)

### Descripción general
Este proyecto se centra en la lectura, validación y limpieza de **ficheros de gran tamaño** utilizando Python, sin depender de librerías externas como *pandas* en la fase inicial.

El objetivo principal de esta primera etapa es reforzar los fundamentos en:

- Manejo de ficheros
- Validación de datos
- Estructuras de datos básicas (`list`, `dict`)
- Organización de código limpio y mantenible
- Clases y abstracción
- Otros conceptos fundamentales del lenguaje

---

### Fuentes de datos
El proyecto trabaja con tres tipos de ficheros que simulan escenarios reales:

- **Archivo CSV `employees.csv`**
  - Aproximadamente 6000 filas
  - Información de empleados

- **Archivo Excel `sales.xlsx`**
  - Contiene 2 hojas:
    - `Transactions`
    - `Targets`

- **Archivo JSON `company_data.json`**
  - Aproximadamente 5500 pedidos
  - Aproximadamente 5200 eventos de auditoría

Estos volúmenes de datos permiten practicar con conjuntos de información no triviales.

---

### Primer paso / Primer commit
En esta primera etapa, el foco está en la **limpieza y validación de datos**.

#### Funcionalidades implementadas

**Primera versión en la rama `main`:**

- Lectura del archivo CSV utilizando únicamente la librería estándar de Python.
- Conversión de cada fila en un diccionario.
- Validación de campos clave:
  - `age` debe estar entre 18 y 70.
  - `monthly_salary` debe ser mayor que 0.
  - `performance` debe estar entre 1.0 y 5.0.
- Separación de los datos en:
  - Una lista de **registros válidos**.
  - Una lista de **registros inválidos**, almacenando el `employee_id` y el motivo del error.
- Uso de funciones para organizar la lógica y facilitar el mantenimiento del código.

**Segunda versión en la rama `pipeline-funcional`:**

- Implementación de un pipeline funcional para la carga, validación y procesamiento de datos.
- Separación clara de responsabilidades mediante funciones independientes.

---

### Errores y correcciones durante el proyecto

- Inicialmente se accedía a los datos directamente con:
  ```python
  country = employee["country"]

Esto puede provocar errores si existen campos nulos o mal formateados.

- Se corrigió utilizando un acceso más seguro:
  ```python
    country = (employee.get("country") or "").strip()

lo que evita errores cuando faltan datos y mejora la robustez del código.

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
