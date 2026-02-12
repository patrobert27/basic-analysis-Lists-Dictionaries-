from .employee import Employee

class RemoteEmployee(Employee):

    def __init__(self, row: dict[str], home_office_bonus: float = 0.0):
        # Initialize all attributes from Employee
        super().__init__(row)
        # new attribut
        self.home_office_bonus: float = float(home_office_bonus)

        # si quieres forzar que siempre sea remoto
        # self.remote = True

    def monthly_net_estimate(self, tax_rate: float = 0.21) -> float:
        """
        Calcula el neto sumando el bonus antes de aplicar impuestos
        Net estimate adding the bonus before taxes
        """

        # clamp tax_rate between 0 and 1
        # limitar tax_rate entre 0 y 1
        if tax_rate < 0:
            tax_rate = 0.0
        elif tax_rate > 1:
            tax_rate = 1.0

        # Add bonus before taxes
        gross = self.monthly_salary + self.home_office_bonus
        return round(gross * (1 - tax_rate), 2)

    def to_dict(self) -> dict:
        """
        Serializa incluyendo el bonus
        Serialize including the bonus
        """
        data = super().to_dict()
        data["home_office_bonus"] = self.home_office_bonus
        return data
