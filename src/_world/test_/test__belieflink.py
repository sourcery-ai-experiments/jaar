from src._world.belieflink import BeliefCore, BeliefID, belieflink_shop, BeliefLink


def test_BeliefID_exists():
    bikers_belief_id = BeliefID("bikers")
    assert bikers_belief_id != None
    assert str(type(bikers_belief_id)).find(".belieflink.BeliefID") > 0


def test_BeliefUnit_exists():
    # GIVEN
    swim_text = ",swimmers"
    # WHEN
    swim_beliefunit = BeliefCore(belief_id=swim_text)
    # THEN
    assert swim_beliefunit != None
    assert swim_beliefunit.belief_id == swim_text


def test_BeliefLink_exists():
    # GIVEN
    swim_text = "swim"

    # WHEN
    swim_belieflink = BeliefLink(belief_id=swim_text)

    # THEN
    assert swim_belieflink.belief_id == swim_text
    assert swim_belieflink.credor_weight == 1.0
    assert swim_belieflink.debtor_weight == 1.0


def test_belieflink_shop_ReturnsCorrectObj():
    # GIVEN
    swim_text = "swim"
    swim_credor_weight = 3.0
    swim_debtor_weight = 5.0

    # WHEN
    swim_belieflink = belieflink_shop(
        belief_id=swim_text,
        credor_weight=swim_credor_weight,
        debtor_weight=swim_debtor_weight,
    )

    # THEN
    assert swim_belieflink.credor_weight == swim_credor_weight
    assert swim_belieflink.debtor_weight == swim_debtor_weight


def test_BeliefLink_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    swim_text = "swim"
    swim_credor_weight = 3.0
    swim_debtor_weight = 5.0
    swimlink = belieflink_shop(
        belief_id=swim_text,
        credor_weight=swim_credor_weight,
        debtor_weight=swim_debtor_weight,
    )

    print(f"{swimlink}")

    # WHEN
    biker_dict = swimlink.get_dict()

    # THEN
    assert biker_dict != None
    assert biker_dict == {
        "belief_id": swimlink.belief_id,
        "credor_weight": swimlink.credor_weight,
        "debtor_weight": swimlink.debtor_weight,
    }
