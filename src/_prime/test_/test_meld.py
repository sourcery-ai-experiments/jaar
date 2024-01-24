from src._prime.meld import get_meld_weight, get_meld_strategys


def test_get_meld_weight_ReturnsCorrectObj_default():
    # GIVEN
    x_src_weight = 5
    x_src_meld_strategy = "default"
    x_other_weight = 7
    x_other_meld_strategy = "sum"

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
    x_src_meld_strategy = "default"
    x_other_weight = 7
    x_other_meld_strategy = "ignore"

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
    x_src_meld_strategy = "default"
    x_other_weight = 7
    x_other_meld_strategy = "override"

    # WHEN
    x_float = get_meld_weight(
        x_src_weight,
        x_src_meld_strategy,
        x_other_weight,
        x_other_meld_strategy,
    )

    # THEN
    assert x_float == x_other_weight


def test_get_meld_strategys_ReturnsCorrectObj():
    # GIVEN / WHEN
    x_meld_strategys = get_meld_strategys()

    # THEN
    assert len(x_meld_strategys) == 5
