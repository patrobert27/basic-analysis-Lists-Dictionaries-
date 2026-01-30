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

if __name__ == "__main__":
    main()
