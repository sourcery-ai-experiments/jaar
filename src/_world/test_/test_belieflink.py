from src._world.person import (
    PersonID,
    belieflink_shop,
    belieflinks_get_from_json,
)
from src._instrument.python import x_is_json, get_json_from_dict
from pytest import raises as pytest_raises


def test_BeliefLink_exists():
    # GIVEN
    bikers_person_id = PersonID("Yao")

    # WHEN
    x_belieflink = belieflink_shop(person_id=bikers_person_id)

    # THEN
    assert x_belieflink.person_id == bikers_person_id
    assert x_belieflink.credor_weight == 1.0
    assert x_belieflink.debtor_weight == 1.0

    # WHEN
    bikers_credor_weight = 3.0
    bikers_debtor_weight = 5.0
    x_belieflink = belieflink_shop(
        person_id=bikers_person_id,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debtor_weight,
        _world_cred=0.7,
        _world_debt=0.51,
        _world_agenda_cred=0.66,
        _world_agenda_debt=0.55,
    )

    # THEN
    assert x_belieflink.credor_weight == bikers_credor_weight
    assert x_belieflink.debtor_weight == bikers_debtor_weight
    assert x_belieflink._world_cred != None
    assert x_belieflink._world_cred == 0.7
    assert x_belieflink._world_debt == 0.51
    assert x_belieflink._world_agenda_cred == 0.66
    assert x_belieflink._world_agenda_debt == 0.55


def test_belieflink_shop_set_world_cred_debt_SetsAttrCorrectly():
    # GIVEN
    bikers_person_id = PersonID("Yao")
    bikers_credor_weight = 3.0
    belieflinks_sum_credor_weight = 60
    belief_world_cred = 0.5
    belief_world_agenda_cred = 0.98

    bikers_debtor_weight = 13.0
    belieflinks_sum_debtor_weight = 26.0
    belief_world_debt = 0.9
    belief_world_agenda_debt = 0.5151

    x_belieflink = belieflink_shop(
        person_id=bikers_person_id,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debtor_weight,
    )
    assert x_belieflink._world_cred is None
    assert x_belieflink._world_debt is None
    assert x_belieflink._world_agenda_cred is None
    assert x_belieflink._world_agenda_debt is None

    # WHEN
    x_belieflink.set_world_cred_debt(
        belieflinks_credor_weight_sum=belieflinks_sum_credor_weight,
        belieflinks_debtor_weight_sum=belieflinks_sum_debtor_weight,
        belief_world_cred=belief_world_cred,
        belief_world_debt=belief_world_debt,
        belief_world_agenda_cred=belief_world_agenda_cred,
        belief_world_agenda_debt=belief_world_agenda_debt,
    )

    # THEN
    assert x_belieflink._world_cred == 0.025
    assert x_belieflink._world_debt == 0.45
    assert x_belieflink._world_agenda_cred == 0.049
    assert x_belieflink._world_agenda_debt == 0.25755


def test_belieflink_shop_reset_world_cred_debt():
    # GIVEN
    biker_person_id = "maria"
    biker_person = belieflink_shop(
        person_id=biker_person_id, _world_cred=0.04, _world_debt=0.7
    )
    print(f"{biker_person}")

    assert biker_person._world_cred != None
    assert biker_person._world_debt != None

    # WHEN
    biker_person.reset_world_cred_debt()

    # THEN
    assert biker_person._world_cred == 0
    assert biker_person._world_debt == 0


def test_belieflink_shop_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    str_person_id = "Yao"
    biker_person_id = PersonID(str_person_id)
    biker_person_link = belieflink_shop(
        person_id=biker_person_id, credor_weight=12, debtor_weight=19
    )
    print(f"{biker_person_link}")

    # WHEN
    biker_dict = biker_person_link.get_dict()

    # THEN
    assert biker_dict != None
    assert biker_dict == {
        "person_id": biker_person_id,
        "credor_weight": 12,
        "debtor_weight": 19,
    }


def test_belieflink_get_from_JSON_ReturnsCorrectObj_SimpleExample():
    # GIVEN
    yao_text = "Yao"
    yao_json_dict = {
        yao_text: {"person_id": yao_text, "credor_weight": 12, "debtor_weight": 19}
    }
    yao_json_text = get_json_from_dict(dict_x=yao_json_dict)
    assert x_is_json(json_x=yao_json_text)

    # WHEN
    yao_obj_dict = belieflinks_get_from_json(belieflinks_json=yao_json_text)

    # THEN
    assert yao_obj_dict != None

    yao_person_id = PersonID(yao_text)
    yao_belieflink = belieflink_shop(
        person_id=yao_person_id, credor_weight=12, debtor_weight=19
    )
    belieflinks_dict = {yao_belieflink.person_id: yao_belieflink}
    assert yao_obj_dict == belieflinks_dict


def test_belieflink_meld_RaiseEqualperson_idException():
    # GIVEN
    todd_text = "Todd"
    todd_person = belieflink_shop(person_id=todd_text)
    mery_text = "Merry"
    mery_person = belieflink_shop(person_id=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_person.meld(mery_person)
    assert (
        str(excinfo.value)
        == f"Meld fail BeliefLink='{todd_person.person_id}' not the equal as BeliefLink='{mery_person.person_id}"
    )


def test_belieflink_meld_CorrectlySumsWeights():
    # GIVEN
    todd_text = "Todd"
    todd_person1 = belieflink_shop(
        person_id=todd_text, credor_weight=12, debtor_weight=19
    )
    todd_person2 = belieflink_shop(
        person_id=todd_text, credor_weight=33, debtor_weight=3
    )
    assert todd_person1.credor_weight == 12
    assert todd_person1.debtor_weight == 19

    # WHEN
    todd_person1.meld(todd_person2)

    # THEN
    assert todd_person1.credor_weight == 45
    assert todd_person1.debtor_weight == 22
