class FinanceUnit(float):
    """A number that can be used for financial calculations."""

    pass


def default_planck_if_none(planck: float = None) -> float:
    return planck if planck != None else 1


def trim_planck_excess(num: float, planck: float) -> float:
    return planck * int(num / planck)
