from pipeline.employees_loader_json import get_employee_department_map


def main() -> None:
    emp_map = get_employee_department_map(
        clean_json_path="employees_clean.json",
        csv_path="employees.csv",
    )

    print("Employee map size:", len(emp_map))


if __name__ == "__main__":
    main()
