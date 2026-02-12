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

def metric_dep(row: list[dict]) -> dict:
    """
    row: lista de empleados (dicts) con al menos:
          - 'department'
          - 'monthly_salary'
    return: dict con salario medio por departamento
    """

    departments = {}  
    # {
    #   "IT": {"total_salary": 12345.0, "count": 5},
    #   "HR": {"total_salary": 6789.0, "count": 3}
    # }

    for employee in row:
        dep = (employee.get("department") or "").strip()
        salary = float(employee.get("monthly_salary") or 0)


        if dep not in departments:
            departments[dep] = {
                "total_salary": 0.0,
                "count": 0
            }

        departments[dep]["total_salary"] += salary
        departments[dep]["count"] += 1

    # calcular salario medio
    average_salary = {}

    for dep, values in departments.items():
        average_salary[dep] = round(values["total_salary"] / values["count"], 2)

    average_salary_by_dep_sorted = dict(sorted(average_salary.items(), key=lambda item: item[1], reverse=True))

    return average_salary_by_dep_sorted

def metric_city(row: list[dict]) -> dict:
    """
    row: lista de empleados (dicts) con al menos:
          - 'city'
          - 'count'
    return: 5 city con mas personas
    """
    cities = {}  
    # {
    #   "London": {"total_persons": 12345.0},
    #   "Paris": {"total_persons": 12345.0}
    # }

    for employee in row:
        city = (employee.get("city") or "").strip()

        if city not in cities:
            cities[city] = {
                "total_persons": 0,
            }

        cities[city]["total_persons"] += 1


    cities_sorted = dict(
        sorted(cities.items(), key=lambda item: item[1]["total_persons"], reverse=True)[:5]
    )


    return cities_sorted


def metric_type_wrk(row: list[dict]) -> dict:
    """
    row: lista de empleados (dicts) con al menos:
          - 'remote' o true o false
          - 'country'
    return: 5 city con mas personas
    """
    countries = {}  
    # {
    #   "Spain": {"total_persons": 12345.0, 'remote': 0, 'presencial': 0},
    #   "France": {"total_persons": 12345.0, 'remote': 0, 'presencial': 0}
    # }

    for employee in row:
        country = (employee.get("country") or "").strip()
        remote = (employee.get("remote") or "").strip().lower() #true or false
        is_remote = remote in ("true", "1", "yes", "y")

        if country not in countries:
            countries[country] = {
                "total_persons": 0,
                'remote': 0,
                'presencial': 0,
                "remote_percentage": 0.0
            }

        countries[country]["total_persons"] += 1
        if is_remote:
            countries[country]["remote"] += 1
        else:
            countries[country]["presencial"] += 1

    for country, values in countries.items():
        total = values["total_persons"]
        remote = values["remote"]

        values["remote_percentage"] = round((remote / total) * 100, 2)

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

    average_salary = metric_dep(valid_data)
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
