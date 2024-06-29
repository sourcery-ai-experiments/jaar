from src._world.beliefhold import (
    BeliefCore,
    BeliefID,
    beliefhold_shop,
    BeliefHold,
    beliefhold_get_from_dict,
    beliefholds_get_from_dict,
)


def test_BeliefID_exists():
    bikers_belief_id = BeliefID("bikers")
    assert bikers_belief_id != None
    assert str(type(bikers_belief_id)).find(".beliefhold.BeliefID") > 0


def test_BeliefUnit_exists():
    # GIVEN
    swim_text = ",swimmers"
    # WHEN
    swim_beliefunit = BeliefCore(belief_id=swim_text)
    # THEN
    assert swim_beliefunit != None
    assert swim_beliefunit.belief_id == swim_text


def test_BeliefHold_exists():
    # GIVEN
    swim_text = "swim"

    # WHEN
    swim_beliefhold = BeliefHold(belief_id=swim_text)

    # THEN
    assert swim_beliefhold.belief_id == swim_text
    assert swim_beliefhold.credor_weight == 1.0
    assert swim_beliefhold.debtor_weight == 1.0


def test_beliefhold_shop_ReturnsCorrectObj():
    # GIVEN
    swim_text = "swim"
    swim_credor_weight = 3.0
    swim_debtor_weight = 5.0

    # WHEN
    swim_beliefhold = beliefhold_shop(
        belief_id=swim_text,
        credor_weight=swim_credor_weight,
        debtor_weight=swim_debtor_weight,
    )

    # THEN
    assert swim_beliefhold.credor_weight == swim_credor_weight
    assert swim_beliefhold.debtor_weight == swim_debtor_weight


def test_BeliefHold_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    swim_text = "swim"
    swim_credor_weight = 3.0
    swim_debtor_weight = 5.0
    swim_beliefhold = beliefhold_shop(
        belief_id=swim_text,
        credor_weight=swim_credor_weight,
        debtor_weight=swim_debtor_weight,
    )

    print(f"{swim_beliefhold}")

    # WHEN
    swim_dict = swim_beliefhold.get_dict()

    # THEN
    assert swim_dict != None
    assert swim_dict == {
        "belief_id": swim_beliefhold.belief_id,
        "credor_weight": swim_beliefhold.credor_weight,
        "debtor_weight": swim_beliefhold.debtor_weight,
    }


def test_beliefhold_get_from_dict_ReturnsObj():
    # GIVEN
    swim_text = "swim"
    swim_credor_weight = 3.0
    swim_debtor_weight = 5.0
    before_swim_beliefhold = beliefhold_shop(
        belief_id=swim_text,
        credor_weight=swim_credor_weight,
        debtor_weight=swim_debtor_weight,
    )
    swim_beliefhold_dict = before_swim_beliefhold.get_dict()

    # WHEN
    after_swim_beliefhold = beliefhold_get_from_dict(swim_beliefhold_dict)

    # THEN
    assert before_swim_beliefhold == after_swim_beliefhold
    assert after_swim_beliefhold.belief_id == swim_text


def test_beliefholds_get_from_dict_ReturnsObj():
    # GIVEN
    swim_text = "swim"
    swim_credor_weight = 3.0
    swim_debtor_weight = 5.0
    before_swim_beliefhold = beliefhold_shop(
        belief_id=swim_text,
        credor_weight=swim_credor_weight,
        debtor_weight=swim_debtor_weight,
    )
    before_swim_beliefholds_objs = {swim_text: before_swim_beliefhold}
    swim_beliefholds_dict = {swim_text: before_swim_beliefhold.get_dict()}

    # WHEN
    after_swim_beliefholds_objs = beliefholds_get_from_dict(swim_beliefholds_dict)

    # THEN
    assert before_swim_beliefholds_objs == after_swim_beliefholds_objs
    assert after_swim_beliefholds_objs.get(swim_text) == before_swim_beliefhold
