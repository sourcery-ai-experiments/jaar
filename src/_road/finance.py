class FinanceUnit(float):
    """A number that can be used for financial calculations."""

    pass


def default_planck_if_none(planck: float = None) -> float:
    return planck if planck != None else 1


def get_planck_valid(num: float, planck: float) -> float:
    return planck * int(num / planck)
