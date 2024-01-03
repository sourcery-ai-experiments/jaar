from src._prime.meld import get_meld_weight, get_on_meld_weight_actions


def test_get_meld_weight_ReturnsCorrectObj_default():
    # GIVEN
    x_src_weight = 5
    x_src_on_meld_weight_action = "default"
    x_other_weight = 7
    x_other_on_meld_weight_action = "sum"

    # WHEN
    x_float = get_meld_weight(
        x_src_weight,
        x_src_on_meld_weight_action,
        x_other_weight,
        x_other_on_meld_weight_action,
    )

    # THEN
    assert x_float == x_src_weight


def test_get_meld_weight_ReturnsCorrectObj_ignore():
    # GIVEN
    x_src_weight = 5
    x_src_on_meld_weight_action = "default"
    x_other_weight = 7
    x_other_on_meld_weight_action = "ignore"

    # WHEN
    x_float = get_meld_weight(
        x_src_weight,
        x_src_on_meld_weight_action,
        x_other_weight,
        x_other_on_meld_weight_action,
    )

    # THEN
    assert x_float == x_src_weight + x_other_weight


def test_get_on_meld_weight_actions_ReturnsCorrectObj():
    # GIVEN / WHEN
    x_on_meld_weight_actions = get_on_meld_weight_actions()

    # THEN
    assert len(x_on_meld_weight_actions) == 5
