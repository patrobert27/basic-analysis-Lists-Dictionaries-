from .employee import Employee
from .remote_employee import RemoteEmployee


def to_employee_objects(rows: list[dict[str]], bonus: float = 0.0) -> list[Employee]:
    """
    Convert CSV rows into Employee or RemoteEmployee objects
    """
    employees: list[Employee] = []

    for row in rows:
        remote = (row.get("remote") or "").strip().lower()

        if remote in ("true", "1", "yes", "y"):
            employees.append(RemoteEmployee(row, home_office_bonus=bonus))
        else:
            employees.append(Employee(row))

    return employees


def split_remote_onsite(employees: list[Employee]) -> tuple[list[Employee], list[Employee]]:
    """
    Split employees into remote and onsite lists
    """
    remote: list[Employee] = []
    onsite: list[Employee] = []

    for e in employees:
        if getattr(e, "remote", False):
            remote.append(e)
        else:
            onsite.append(e)

    return remote, onsite


def best_value_top(employees: list[Employee], limit: int = 15) -> list[Employee]:
    """
    Best value ranking = performance / monthly_salary
    Returns top N employees
    """
    scored: list[tuple[float, Employee]] = []

    for e in employees:
        if e.monthly_salary > 0:
            score = e.performance / e.monthly_salary
            scored.append((score, e))

    scored.sort(key=lambda x: x[0], reverse=True)

    return [emp for _, emp in scored[:limit]]
