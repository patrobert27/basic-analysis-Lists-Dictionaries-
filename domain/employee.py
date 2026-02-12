from .person import Person
from datetime import date, datetime

class Employee(Person):

    def __init__(self, row):
        self.employee_id: str = self._to_str(row.get("employee_id"))
        self.name: str = self._to_str(row.get("name"))
        self.department: str = self._to_str(row.get("department"))
        self.city: str = self._to_str(row.get("city"))
        self.country: str = self._to_str(row.get("country"))

        self.age: int = self._to_int(row.get("age"), default=0)
        self.monthly_salary: float = self._to_float(row.get("monthly_salary"), default=0.0)
        self.performance: float = self._to_float(row.get("performance"), default=0.0)

        self.hire_date: date | None = self._to_date(row.get("hire_date"))
        self.remote: bool = self._to_bool(row.get("remote"))

    # -------------------------
    # Business methods / Métodos
    # -------------------------

    def tenure_years(self) -> float:
        """
        ES: Años en la empresa desde hire_date (aprox. usando 365.25).
        EN: Years at the company since hire_date (approx. using 365.25).
        """
        if self.hire_date is None:
            return 0.0

        days = (date.today() - self.hire_date).days
        if days <= 0:
            return 0.0

        return round(days / 365.25, 2)

    def monthly_net_estimate(self, tax_rate: float = 0.21) -> float:
        """
        ES: Estimación simple del neto mensual: salary * (1 - tax_rate).
        EN: Simple monthly net estimate: salary * (1 - tax_rate).
        """
        # clamp tax_rate to [0, 1]
        if tax_rate < 0:
            tax_rate = 0.0
        elif tax_rate > 1:
            tax_rate = 1.0

        return round(self.monthly_salary * (1.0 - tax_rate), 2)

    def to_dict(self) -> dict[str]:
        """
        ES: Convierte el objeto a dict (serializable).
        EN: Convert the object to a serializable dict.
        """
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "age": self.age,
            "department": self.department,
            "city": self.city,
            "country": self.country,
            "monthly_salary": self.monthly_salary,
            "performance": self.performance,
            "hire_date": self.hire_date.isoformat() if self.hire_date else None,
            "remote": self.remote,
        }

    # parsing / Helpers

    @staticmethod
    def _to_str(value) -> str:
        return ("" if value is None else str(value)).strip()

    @staticmethod
    def _to_int(value, default: int = 0) -> int:
        string = Employee._to_str(value)
        try:
            return int(string)
        except ValueError:
            return default

    @staticmethod
    def _to_float(value, default: float = 0.0) -> float:
        string = Employee._to_str(value)
        try:
            return float(string)
        except ValueError:
            return default

    @staticmethod
    def _to_bool(value) -> bool:
        string = Employee._to_str(value).lower()
        return string in ("true", "1", "yes", "y", "t")

    @staticmethod
    def _to_date(value) -> date | None:
        string = Employee._to_str(value)
        if not string:
            return None

        # Common formats: YYYY-MM-DD, YYYY/MM/DD, DD/MM/YYYY
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y"):
            try:
                return datetime.strptime(string, fmt).date()
            except ValueError:
                continue

        return None