from pipeline.employees_loader_json import get_employee_department_map
from pipeline.sales_loader import load_transactions, load_targets


def main() -> None:
    emp_map = get_employee_department_map(
        clean_json_path="employees_clean.json",
        csv_path="employees.csv",
    )

    print("Employee map size:", len(emp_map))

    transactions = load_transactions("sales.xlsx")
    print(transactions[:2])
    targets = load_targets("sales.xlsx")
    print(targets[:2])


if __name__ == "__main__":
    main()
