class FinanceUnit(float):
    """A number that can be used for financial calculations."""

    pass


def default_planck_if_none(planck: float = None) -> float:
    return planck if planck != None else 1


def trim_planck_excess(num: float, planck: float) -> float:
    return planck * int(num / planck)


def default_penny_if_none(penny: float = None) -> float:
    x_penny = penny if penny != None else 1
    return max(x_penny, 1)


def trim_penny_excess(num: float, planck: float) -> float:
    return planck * int(num / planck)


def default_money_magnitude() -> float:
    return 1000000000


def default_money_magnitude_if_none(money_magnitude: int = None) -> int:
    if money_magnitude is None:
        money_magnitude = default_money_magnitude()
    return money_magnitude
