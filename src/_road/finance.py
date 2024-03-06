class FinanceUnit(float):
    """A number that can be used for financial calculations."""

    pass


def default_planck_if_none(planck: str = None) -> str:
    return planck if planck != None else 1
