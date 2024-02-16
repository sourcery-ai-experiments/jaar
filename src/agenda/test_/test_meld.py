from src.agenda.meld import (
    get_meld_weight,
    get_meld_strategys,
    MeldStrategy,
    get_meld_default,
    validate_meld_strategy,
)
from pytest import raises as pytest_raises


def test_get_meld_weight_ReturnsCorrectObj_default():
    # GIVEN
    x_src_weight = 5
    x_src_meld_strategy = MeldStrategy("default")
    x_other_weight = 7
    x_other_meld_strategy = MeldStrategy("sum")

    # WHEN
    x_float = get_meld_weight(
        x_src_weight,
        x_src_meld_strategy,
        x_other_weight,
        x_other_meld_strategy,
    )

    # THEN
    assert x_float == x_src_weight


def test_get_meld_weight_ReturnsCorrectObj_ignore():
    # GIVEN
    x_src_weight = 5
    x_src_meld_strategy = MeldStrategy("default")
    x_other_weight = 7
    x_other_meld_strategy = MeldStrategy("ignore")

    # WHEN
    x_float = get_meld_weight(
        x_src_weight,
        x_src_meld_strategy,
        x_other_weight,
        x_other_meld_strategy,
    )

    # THEN
    assert x_float == x_src_weight + x_other_weight


def test_get_meld_weight_ReturnsCorrectObj_override():
    # GIVEN
    x_src_weight = 5
    x_src_meld_strategy = MeldStrategy("default")
    x_other_weight = 7
    x_other_meld_strategy = MeldStrategy("override")

    # WHEN
    x_float = get_meld_weight(
        x_src_weight,
        x_src_meld_strategy,
        x_other_weight,
        x_other_meld_strategy,
    )

    # THEN
    assert x_float == x_other_weight


def test_get_meld_strategys_HasCorrectItems():
    # GIVEN / WHEN / THEN
    assert len(get_meld_strategys()) == 5
    assert get_meld_strategys() == {"default", "match", "sum", "accept", "override"}


def test_get_meld_default_ReturnsCorrectObj():
    assert get_meld_default() in get_meld_strategys()
    assert get_meld_default() == "default"


def test_validate_meld_strategy_CorrectlyRaisesError():
    # WHEN / THEN
    ineligible_meld_strategy = "yahoo9"
    with pytest_raises(Exception) as excinfo:
        validate_meld_strategy(meld_strategy=ineligible_meld_strategy)
    assert (
        str(excinfo.value)
        == f"'{ineligible_meld_strategy}' is ineligible meld_strategy."
    )
