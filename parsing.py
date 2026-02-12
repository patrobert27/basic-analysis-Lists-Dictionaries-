import csv
import json


def is_float(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False

def load_employees(path: str) -> list[dict]:
    rows: list[dict] = []

    f = None

    try:
        f = open(path, "r", encoding="utf-8", newline="")

        # Esto convierte el CSV a dicts
        # This transform the CSV to a dinc
        reader = csv.DictReader(f)

        for row in reader:
            rows.append(row)
        return rows

    except FileNotFoundError:
        print("I don't find the file")
        return []
    except csv.Error as e:
        print(f"CSV format error: {e}")
        return []
    finally:
        if f is not None:
            f.close()



def validate_employee(row: dict) -> tuple[bool, str | None]:
    # Validar el id
    # Validate employee_id
    emp_id = row.get("employee_id", "").strip()
    if not emp_id.isdigit():
        return False, "invalid employee_id"

    # Validar la edad
    # Validate age
    age_str = row.get("age", "").strip()
    if not age_str.isdigit():
        return False, "age is not an integer" # No es un numero entero
    age = int(age_str)
    if not (18 <= age <= 70):
        return False, "age out of allowed range (18-70)" # No esta en el rango

    # Validar salario mensual
    # Validate monthly salary
    salary_str = row.get("monthly_salary", "").strip()
    if not is_float(salary_str):
        return False, "monthly_salary is not a number" # No es un numero
    monthly_salary = float(salary_str)
    if monthly_salary <= 0:
        return False, "monthly_salary must be greater than 0" # No es mayor a 0

    # Validar puntos
    # Validate performance score
    perf_str = row.get("performance", "").strip()
    if not is_float(perf_str):
        return False, "performance is not a number"
    performance = float(perf_str)
    if not (1.0 <= performance <= 5.0):
        return False, "performance out of allowed range (1.0-5.0)"

    # All validations passed
    return True, None

def filter_valid(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    Split rows into valid and invalid
    Separa filas válidas e inválidas con motivo del error

    Invalid rows are returned as dicts with:
    Filas invalidas se devuelven en un diccionarrio asi:
    - employee_id
    - reason

    Args:
        rows: List of employee rows.

    Returns:
        (valid_rows, invalid_rows_with_reason)
        (filas_validas, filas_invalidas_con_motivo)
    """
    valid: list[dict] = []
    invalid: list[dict] = []

    for row in rows:
        ok, reason = validate_employee(row)
        if ok:
            valid.append(row)
        else:
            invalid.append(
                {
                    "employee_id": (row.get("employee_id") or "").strip(),
                    "reason": reason,
                }
            )

    return valid, invalid


def group_by(rows: list[dict], key: str) -> dict[str, list[dict]]:
    """Agrupa filas por el valor de una clave.
       Groups rows by the value of a key."""
    groups: dict[str, list[dict]] = {}
    for row in rows:
        k = (row.get(key) or "").strip()
        groups.setdefault(k, []).append(row)
    return groups


def aggregate_salary(rows: list[dict]) -> dict[str, float]:
    """
    row: lista de empleados (dicts) con al menos:
          - 'department'
          - 'monthly_salary'
    return: dict con salario medio por departamento
    """

    groups = group_by(rows, "department") 
    #{
    #   "IT": [emp1, emp2, emp3],
    #   "HR": [emp4, emp5]
    #}

    average_salary: dict[str, float] = {}

    for dep, dep_rows in groups.items():
        total_salary = 0.0
        for emp in dep_rows:
            total_salary += float(emp.get("monthly_salary") or 0)

        if dep_rows:
            average_salary[dep] = round(total_salary / len(dep_rows), 2)
        else:
            average_salary[dep] = 0.0


    return dict(sorted(average_salary.items(), key=lambda item: item[1], reverse=True))

def metric_city(rows: list[dict]) -> dict[str, int]:
    """
    Top 5 ciudades con más empleados.
    """

    groups = group_by(rows, "city")

    city_counts = {}

    for city, city_rows in groups.items():
        city_counts[city] = len(city_rows)

    cities_sorted = dict(
        sorted(city_counts.items(), key=lambda item: item[1], reverse=True)[:5]
    )

    return cities_sorted



def metric_type_wrk(rows: list[dict]) -> dict:
    """
    % de empleados remotos por país.
    """

    groups = group_by(rows, "country")

    countries = {}

    for country, country_rows in groups.items():
        total = len(country_rows)
        remote_count = 0

        for r in country_rows:
            remote = (r.get("remote") or "").strip().lower()
            if remote in ("true", "1", "yes", "y"):
                remote_count += 1

        countries[country] = {
            "total_persons": total,
            "remote": remote_count,
            "presencial": total - remote_count,
            "remote_percentage": round((remote_count / total) * 100, 2) if total else 0.0
        }

    return countries

def duplicate_name_hire(rows: list[dict]) -> set[str]:
    seen: set[tuple[str, str]] = set()
    duplicate_ids: set[str] = set()

    for row in rows:
        # if exsist -> return value
        # else -> return None "", for don't obtain a error
        name = (row.get("name") or "").strip()
        hire_date = (row.get("hire_date") or "").strip()
        employee_id = (row.get("employee_id") or "").strip()

        key = (name, hire_date)

        if key in seen:
            # este es un duplicado (segunda vez o más)
            if employee_id:
                duplicate_ids.add(employee_id)
        else:
            seen.add(key)

    return duplicate_ids

def save_clean_json(rows: list[dict], path: str) -> None:
    #save the data in a JSON
    j = None
    try:
        j = open(path, "w", encoding="utf-8")
        json.dump(rows, j, ensure_ascii=False, indent=2)

    except OSError as e:
        print("Error writing file:", e)

    finally:
        if j is not None:
            j.close()


def main() -> None:

    try:
        rows = load_employees("employees.csv")

        if not rows:
            return

    except FileNotFoundError:
        print("File not found")
        return
    except csv.Error as e:
        print(f"CSV format error: {e}")
        return

    valid_data, invalid_data = filter_valid(rows)

    average_salary = aggregate_salary(valid_data)
    top_cities = metric_city(valid_data)
    percentage = metric_type_wrk(valid_data)
    duplicate = duplicate_name_hire(valid_data)

    try:
        save_clean_json(valid_data, "employees_clean.json")
    except OSError as e:
        print("Error writing file:", e)
        return

    print("=== SUMMARY ===")
    print(f"Valid rows: {len(valid_data)}")
    print(f"Invalid rows: {len(invalid_data)}")
    print("-------------------")
    print(f"Average salary by department: {average_salary}")
    print("-------------------")
    print(f"Top 5 cities: {top_cities}")
    print("-------------------")
    print(f"Remote % by country: {percentage}")
    print("-------------------")
    print(f"Duplicate IDs: {duplicate}")

if __name__ == "__main__":
    main()
