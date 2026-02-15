import json
from typing import Any

from .employees_pipeline import load_employees, filter_valid


def _load_clean_employees_json(path: str) -> list[dict[str, Any]] | None:
    """
    Try to load employees from a clean JSON file
    Returns a list of dicts if successful, otherwise None
    """
    f = None
    try:
        f = open(path, "r", encoding="utf-8")
        data = json.load(f)

        if not isinstance(data, list):
            return None

        # Basic validation: must contain employee_id and department
        for row in data[:5]:  # quick check first rows
            if not isinstance(row, dict):
                return None
            if "employee_id" not in row or "department" not in row:
                return None

        return data
    except (OSError, json.JSONDecodeError):
        return None
    finally:
        if f is not None:
            f.close()


def _build_employee_department_map(rows: list[dict[str, Any]]) -> dict[str, str]:
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


def get_employee_department_map(
    *,
    clean_json_path: str = "employees_clean.json",
    csv_path: str = "employees.csv",
) -> dict[str, str]:
    """
    Return {employee_id: department}.

    Priority:
    1) employees_clean.json (already validated)
    2) employees.csv (load + filter_valid)
    """
    clean_rows = _load_clean_employees_json(clean_json_path)
    if clean_rows is not None:
        return _build_employee_department_map(clean_rows)

    # Fallback to CSV pipeline
    rows = load_employees(csv_path)
    valid_rows, _invalid_rows = filter_valid(rows)
    return _build_employee_department_map(valid_rows)
