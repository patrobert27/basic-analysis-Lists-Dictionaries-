from pipeline.parsing import (
    load_employees,
    filter_valid,
    save_clean_json,
)

from domain.operations import (
    to_employee_objects,
    split_remote_onsite,
    best_value_top,
)


def main() -> None:
    # -------------------------
    # Load + validate pipeline
    # -------------------------
    rows = load_employees("employees.csv")

    if not rows:
        print("No data loaded")
        return

    valid_data, invalid_data = filter_valid(rows)

    print("=== PIPELINE ===")
    print("Valid rows:", len(valid_data))
    print("Invalid rows:", len(invalid_data))

    save_clean_json(valid_data, "employees_clean.json")

    # -------------------------
    # Reto C — Domain Model
    # -------------------------
    print("\n=== DOMAIN MODEL ===")

    # Convert rows → objects
    employees = to_employee_objects(valid_data, bonus=150.0)

    # Split remote / onsite
    remote, onsite = split_remote_onsite(employees)

    print("Remote employees:", len(remote))
    print("Onsite employees:", len(onsite))

    # Ranking best value
    ranking = best_value_top(employees, limit=15)

    print("\nTop 15 best value employees:")
    for i, e in enumerate(ranking, start=1):
        score = e.performance / e.monthly_salary if e.monthly_salary else 0
        print(f"{i}. {e.name} → score={score:.6f}")


if __name__ == "__main__":
    main()
