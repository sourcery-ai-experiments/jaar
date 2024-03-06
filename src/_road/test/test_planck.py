from src._road.finance import default_planck_if_none, FinanceUnit
from inspect import getdoc as inspect_getdoc

# from pytest import raises as pytest_raises
# from dataclasses import dataclass


def test_FinanceUnit_exists():
    # GIVEN
    x_float = 0.045
    # WHEN
    y_financeunit = FinanceUnit(x_float)
    # THEN
    assert y_financeunit == x_float
    assert (
        inspect_getdoc(y_financeunit)
        == "A number that can be used for financial calculations."
    )


def test_default_planck_if_none_ReturnsCorrectObj():
    # GIVEN / WHEN / THEN
    assert default_planck_if_none() == 1
    assert default_planck_if_none(5) == 5
    assert default_planck_if_none(0.03) == 0.03
