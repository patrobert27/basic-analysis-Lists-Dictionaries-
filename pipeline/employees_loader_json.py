import json
from typing import Any

from .employees_pipeline import load_employees, filter_valid



"""
load_clean_employees_json
BAsicamente dice ¿Existe employees_clean.json?
¿Está bien formado? o ¿Tiene employee_id y department?
Si todo está bien devuelve la lista de empleados, 
en cambio si algo falla devuelve None
"""
def load_clean_employees_json(path: str) -> list[dict[str, Any]] | None:
    """
    Try to load employees from a clean JSON file
    Returns a list of dicts if successful, otherwise None
    """
    f = None
    try:
        f = open(path, "r", encoding="utf-8")
        data = json.load(f)

        # Si el contenido del JSON NO es una lista con [{},{}], entonces no es válido
        if not isinstance(data, list):
            return None

        # Basic and fast validation must contain employee_id and department
        for row in data[:5]:  # quick check first 5 rows
            if not isinstance(row, dict):
                return None
            if "employee_id" not in row or "department" not in row:
                return None

        return data
    except (OSError, json.JSONDecodeError):
        return None
    except Exception as e:
        return e
    finally:
        if f is not None:
            f.close()

"""
build_employee_department_map

Recibe una lista de empleados en formato list[dict], por ejemplo:

[
  {"employee_id": "1", "department": "IT"},
  {"employee_id": "2", "department": "Sales"},
  {"employee_id": "3", "department": "HR"}
]

Y transforma esa lista en un diccionario más eficiente para búsquedas rápidas:

{
  "employee_id": "department"
  "1": "IT",
  "2": "Sales",
  "3": "HR"
}

Esto nos permite hacer un "join" más adelante con Transactions.
Por ejemplo, si tenemos una transacción con employee_id = "2",
podemos obtener su departamento inmediatamente con:

    department = employee_map["2"]

En resumen:
Convierte list[dict] → dict[employee_id -> department]
para facilitar cruces de información.
"""

def build_employee_department_map(rows: list[dict[str, Any]]) -> dict[str, str]:
    """
    Build {employee_id: department} from employee rows.
    """
    mapping: dict[str, str] = {}

    for row in rows:
        employee_id = (row.get("employee_id") or "").strip()
        department = (row.get("department") or "").strip()

        if employee_id:
            mapping[employee_id] = department

    return mapping

"""
get_employee_department_map

Devuelve un diccionario en formato:

    {employee_id: department}

Primero intenta cargar los empleados desde el archivo
"employees_clean.json", que ya contiene datos validados.

Si el JSON no existe o no es válido, entonces:
- Carga el archivo CSV original.
- Filtra los empleados válidos usando el pipeline.
- Construye el diccionario a partir de esos datos.

De esta forma, siempre obtenemos el mapping
employee_id → department de manera segura,
usando datos limpios si están disponibles,
o reconstruyéndolos automáticamente si no.
"""

def get_employee_department_map(
    *, # Si o si se tiene que llamar o clean... o csv... y indicar
    clean_json_path: str = "employees_clean.json",
    csv_path: str = "employees.csv",
) -> dict[str, str]:
    """
    Return {employee_id: department}.

    Priority:
    1) employees_clean.json (already validated)
    2) employees.csv (load + filter_valid)
    """
    clean_rows = load_clean_employees_json(clean_json_path)
    if clean_rows is not None:
        return build_employee_department_map(clean_rows)

    # Fallback to CSV pipeline
    rows = load_employees(csv_path)
    valid_rows, _invalid_rows = filter_valid(rows)
    return build_employee_department_map(valid_rows)
