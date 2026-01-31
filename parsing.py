import csv

FILE_PATH = "employees.csv"

def is_float(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False

def validate_employee(data: dict) -> tuple[bool, str | None]:
    # Validar el id
    # Validate employee_id
    emp_id = data.get("employee_id", "").strip()
    if not emp_id.isdigit():
        return False, "invalid employee_id"

    # Validar la edad
    # Validate age
    age_str = data.get("age", "").strip()
    if not age_str.isdigit():
        return False, "age is not an integer" # No es un numero entero
    age = int(age_str)
    if not (18 <= age <= 70):
        return False, "age out of allowed range (18-70)" # No esta en el rango

    # Validar salario mensual
    # Validate monthly salary
    salary_str = data.get("monthly_salary", "").strip()
    if not is_float(salary_str):
        return False, "monthly_salary is not a number" # No es un numero
    monthly_salary = float(salary_str)
    if monthly_salary <= 0:
        return False, "monthly_salary must be greater than 0" # No es mayor a 0

    # Validar puntos
    # Validate performance score
    perf_str = data.get("performance", "").strip()
    if not is_float(perf_str):
        return False, "performance is not a number"
    performance = float(perf_str)
    if not (1.0 <= performance <= 5.0):
        return False, "performance out of allowed range (1.0-5.0)"

    # All validations passed
    return True, None


def metric_dep(data: list[dict]) -> dict:
    """
    data: lista de empleados (dicts) con al menos:
          - 'department'
          - 'monthly_salary'
    return: dict con salario medio por departamento
    """

    departments = {}  
    # {
    #   "IT": {"total_salary": 12345.0, "count": 5},
    #   "HR": {"total_salary": 6789.0, "count": 3}
    # }

    for employee in data:
        dep = employee["department"]
        salary = float(employee["monthly_salary"])

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

def metric_city(data: list[dict]) -> dict:
    """
    data: lista de empleados (dicts) con al menos:
          - 'city'
          - 'count'
    return: 5 city con mas personas
    """
    cities = {}  
    # {
    #   "London": {"total_persons": 12345.0},
    #   "Paris": {"total_persons": 12345.0}
    # }

    for employee in data:
        city = employee["city"]

        if city not in cities:
            cities[city] = {
                "total_persons": 0,
            }

        cities[city]["total_persons"] += 1


    cities_sorted = dict(sorted(cities.items(), key=lambda item: item[0], reverse=True) [:5])


    return cities_sorted


def metric_type_wrk(data: list[dict]) -> dict:
    """
    data: lista de empleados (dicts) con al menos:
          - 'remote' o true o false
          - 'country'
    return: 5 city con mas personas
    """
    countries = {}  
    # {
    #   "Spain": {"total_persons": 12345.0, 'remote': 0, 'presencial': 0},
    #   "France": {"total_persons": 12345.0, 'remote': 0, 'presencial': 0}
    # }

    for employee in data:
        country = employee["country"]
        remote = employee["remote"]

        if country not in countries:
            countries[country] = {
                "total_persons": 0,
                'remote': 0,
                'presencial': 0,
                "remote_percentage": 0.0
            }

        countries[country]["total_persons"] += 1
        if remote:
            countries[country]["remote"] += 1
        else:
            countries[country]["presencial"] += 1

    for country, values in countries.items():
        total = values["total_persons"]
        remote = values["remote"]

        values["remote_percentage"] = round((remote / total) * 100, 2)

    return countries



def main() -> None:
    valid_data: list[dict] = []
    invalid_data: list[dict] = []  # {"employee_id": ..., "reason": ...}

    try:
        f = open(FILE_PATH, "r", encoding="utf-8", newline="")

        # Esto convierte el CSV a dicts
        # This transform the CSV to a dinc
        reader = csv.DictReader(f)

        for row in reader:
            ok, reason = validate_employee(row)

            if ok:
                valid_data.append(row)
            else:
                invalid_data.append({
                    "employee_id": row.get("employee_id"),
                    "reason": reason
                })

        if valid_data:
            average_salary = metric_dep(valid_data)
            top_cities = metric_city(valid_data)
            percentage = metric_type_wrk(valid_data)

    except FileNotFoundError:
        print("I don't find the file")
        return
    except csv.Error as e:
        print(f"CSV format error: {e}")
        return
    finally:
        f.close()

    print("=== RESUMEN ===")
    print(f"Valid rows: {len(valid_data)}")
    print(f"Invalid rows: {len(invalid_data)}")
    print(f"Average: {average_salary}")
    print("-------------------")
    print(f"Cities: {top_cities}")
    print("-------------------")
    print(f"Porcentage %: {percentage}")

if __name__ == "__main__":
    main()
