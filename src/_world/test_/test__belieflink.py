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
    bikers_belief_id = BeliefID("bikers")

    # WHEN
    bikers_belieflink = BeliefLink(belief_id=bikers_belief_id)

    # THEN
    assert bikers_belieflink.belief_id == bikers_belief_id
    assert bikers_belieflink.credor_weight == 1.0
    assert bikers_belieflink.debtor_weight == 1.0


def test_belieflink_shop_ReturnsCorrectObj():
    # GIVEN
    bikers_belief_id = BeliefID("bikers")
    bikers_credor_weight = 3.0
    bikers_debtor_weight = 5.0

    # WHEN
    bikers_belieflink = belieflink_shop(
        belief_id=bikers_belief_id,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debtor_weight,
    )

    # THEN
    assert bikers_belieflink.credor_weight == bikers_credor_weight
    assert bikers_belieflink.debtor_weight == bikers_debtor_weight


def test_BeliefLink_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    bikers_belief_id = BeliefID("bikers")
    bikers_credor_weight = 3.0
    bikers_debtor_weight = 5.0
    bikers_link = belieflink_shop(
        belief_id=bikers_belief_id,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debtor_weight,
    )

    print(f"{bikers_link}")

    # WHEN
    biker_dict = bikers_link.get_dict()

    # THEN
    assert biker_dict != None
    assert biker_dict == {
        "belief_id": bikers_link.belief_id,
        "credor_weight": bikers_link.credor_weight,
        "debtor_weight": bikers_link.debtor_weight,
    }
