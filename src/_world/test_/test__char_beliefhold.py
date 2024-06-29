from src._world.beliefhold import BeliefID, BeliefHold, beliefhold_shop
from src._world.char import (
    charunit_shop,
)
from pytest import raises as pytest_raises


def test_CharUnit_set_beliefhold_CorrectlySetsAttr():
    # GIVEN
    run_text = ",run"
    fly_text = ",fly"
    run_beliefhold = beliefhold_shop(run_text, credor_weight=13, debtor_weight=7)
    fly_beliefhold = beliefhold_shop(fly_text, credor_weight=23, debtor_weight=5)
    yao_char = charunit_shop("Yao")
    assert yao_char._beliefholds == {}

    # WHEN
    yao_char.set_beliefhold(run_beliefhold)
    yao_char.set_beliefhold(fly_beliefhold)

    # THEN
    yao_beliefholds = {
        run_beliefhold.belief_id: run_beliefhold,
        fly_beliefhold.belief_id: fly_beliefhold,
    }
    assert yao_char._beliefholds == yao_beliefholds


def test_CharUnit_get_beliefhold_ReturnsCorrectObj():
    # GIVEN
    run_text = ",run"
    fly_text = ",fly"
    yao_char = charunit_shop("Yao")
    yao_char.set_beliefhold(beliefhold_shop(run_text, 13, 7))
    yao_char.set_beliefhold(beliefhold_shop(fly_text, 23, 5))

    # WHEN / THEN
    assert yao_char.get_beliefhold(run_text) != None
    assert yao_char.get_beliefhold(fly_text) != None
    climb_text = ",climbers"
    assert yao_char.get_beliefhold(climb_text) is None


def test_beliefhold_exists_ReturnsCorrectObj():
    # GIVEN
    run_text = ",run"
    fly_text = ",fly"
    yao_char = charunit_shop("Yao")
    yao_char.set_beliefhold(beliefhold_shop(run_text, 13, 7))
    yao_char.set_beliefhold(beliefhold_shop(fly_text, 23, 5))

    # WHEN / THEN
    assert yao_char.beliefhold_exists(run_text)
    assert yao_char.beliefhold_exists(fly_text)
    climb_text = ",climbers"
    assert yao_char.beliefhold_exists(climb_text) is False


def test_CharUnit_del_beliefhold_SetsAttrCorrectly():
    # GIVEN
    run_text = ",run"
    fly_text = ",fly"
    run_beliefhold = beliefhold_shop(run_text)
    fly_beliefhold = beliefhold_shop(fly_text)
    yao_beliefholds = {
        run_beliefhold.belief_id: run_beliefhold,
        fly_beliefhold.belief_id: fly_beliefhold,
    }
    yao_char = charunit_shop("Yao")
    yao_char.set_beliefhold(run_beliefhold)
    yao_char.set_beliefhold(fly_beliefhold)
    assert len(yao_char._beliefholds) == 2
    assert yao_char._beliefholds == yao_beliefholds

    # WHEN
    yao_char.delete_beliefhold(run_text)

    # THEN
    assert len(yao_char._beliefholds) == 1
    assert yao_char._beliefholds.get(run_text) is None


def test_CharUnit_clear_beliefholds_SetsAttrCorrectly():
    # GIVEN
    run_text = ",run"
    fly_text = ",fly"
    run_beliefhold = beliefhold_shop(run_text)
    fly_beliefhold = beliefhold_shop(fly_text)
    yao_beliefholds = {
        run_beliefhold.belief_id: run_beliefhold,
        fly_beliefhold.belief_id: fly_beliefhold,
    }
    yao_char = charunit_shop("Yao")
    yao_char.set_beliefhold(run_beliefhold)
    yao_char.set_beliefhold(fly_beliefhold)
    assert len(yao_char._beliefholds) == 2
    assert yao_char._beliefholds == yao_beliefholds

    # WHEN
    yao_char.clear_beliefholds()

    # THEN
    assert len(yao_char._beliefholds) == 0
    assert yao_char._beliefholds.get(run_text) is None
