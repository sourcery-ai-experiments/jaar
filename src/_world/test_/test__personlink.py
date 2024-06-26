from src._world.person import personlink_shop, personlinks_get_from_json
from src._instrument.python import x_is_json, get_json_from_dict
from pytest import raises as pytest_raises


def test_PersonLink_exists():
    # GIVEN
    yao_text = "Yao"

    # WHEN
    yao_personlink = personlink_shop(yao_text)

    # THEN
    assert yao_personlink.person_id == yao_text
    assert yao_personlink.credor_weight == 1.0
    assert yao_personlink.debtor_weight == 1.0

    # WHEN
    bikers_credor_weight = 3.0
    bikers_debtor_weight = 5.0
    yao_personlink = personlink_shop(
        person_id=yao_text,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debtor_weight,
        _world_cred=0.7,
        _world_debt=0.51,
        _world_agenda_cred=0.66,
        _world_agenda_debt=0.55,
    )

    # THEN
    assert yao_personlink.credor_weight == bikers_credor_weight
    assert yao_personlink.debtor_weight == bikers_debtor_weight
    assert yao_personlink._world_cred != None
    assert yao_personlink._world_cred == 0.7
    assert yao_personlink._world_debt == 0.51
    assert yao_personlink._world_agenda_cred == 0.66
    assert yao_personlink._world_agenda_debt == 0.55


def test_personlink_shop_set_world_cred_debt_SetsAttrCorrectly():
    # GIVEN
    yao_text = "Yao"
    bikers_credor_weight = 3.0
    personlinks_sum_credor_weight = 60
    belief_world_cred = 0.5
    belief_world_agenda_cred = 0.98

    bikers_debtor_weight = 13.0
    personlinks_sum_debtor_weight = 26.0
    belief_world_debt = 0.9
    belief_world_agenda_debt = 0.5151

    yao_personlink = personlink_shop(
        person_id=yao_text,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debtor_weight,
    )
    assert yao_personlink._world_cred is None
    assert yao_personlink._world_debt is None
    assert yao_personlink._world_agenda_cred is None
    assert yao_personlink._world_agenda_debt is None

    # WHEN
    yao_personlink.set_world_cred_debt(
        personlinks_credor_weight_sum=personlinks_sum_credor_weight,
        personlinks_debtor_weight_sum=personlinks_sum_debtor_weight,
        belief_world_cred=belief_world_cred,
        belief_world_debt=belief_world_debt,
        belief_world_agenda_cred=belief_world_agenda_cred,
        belief_world_agenda_debt=belief_world_agenda_debt,
    )

    # THEN
    assert yao_personlink._world_cred == 0.025
    assert yao_personlink._world_debt == 0.45
    assert yao_personlink._world_agenda_cred == 0.049
    assert yao_personlink._world_agenda_debt == 0.25755


def test_personlink_shop_reset_world_cred_debt():
    # GIVEN
    yao_text = "Yao"
    yao_personlink = personlink_shop(yao_text, _world_cred=0.04, _world_debt=0.7)
    print(f"{yao_text=}")

    assert yao_personlink._world_cred != None
    assert yao_personlink._world_debt != None

    # WHEN
    yao_personlink.reset_world_cred_debt()

    # THEN
    assert yao_personlink._world_cred == 0
    assert yao_personlink._world_debt == 0


def test_PersonLink_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    yao_text = "Yao"
    yao_personlink = personlink_shop(yao_text, credor_weight=12, debtor_weight=19)
    print(f"{yao_personlink}")

    # WHEN
    biker_dict = yao_personlink.get_dict()

    # THEN
    assert biker_dict != None
    assert biker_dict == {
        "person_id": yao_text,
        "credor_weight": 12,
        "debtor_weight": 19,
    }


def test_PersonLink_get_from_JSON_ReturnsCorrectObj_SimpleExample():
    # GIVEN
    yao_text = "Yao"
    yao_json_dict = {
        yao_text: {"person_id": yao_text, "credor_weight": 12, "debtor_weight": 19}
    }
    yao_json_text = get_json_from_dict(dict_x=yao_json_dict)
    assert x_is_json(json_x=yao_json_text)

    # WHEN
    yao_obj_dict = personlinks_get_from_json(personlinks_json=yao_json_text)

    # THEN
    assert yao_obj_dict != None

    yao_personlink = personlink_shop(yao_text, credor_weight=12, debtor_weight=19)
    personlinks_dict = {yao_personlink.person_id: yao_personlink}
    assert yao_obj_dict == personlinks_dict


def test_PersonLink_meld_RaiseEqualperson_idException():
    # GIVEN
    todd_text = "Todd"
    todd_personlink = personlink_shop(todd_text)
    mery_text = "Merry"
    mery_personlink = personlink_shop(mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_personlink.meld(mery_personlink)
    assert (
        str(excinfo.value)
        == f"Meld fail PersonLink='{todd_personlink.person_id}' not the equal as PersonLink='{mery_personlink.person_id}"
    )


def test_PersonLink_meld_CorrectlySumsWeights():
    # GIVEN
    todd_text = "Todd"
    todd_personlink1 = personlink_shop(todd_text, credor_weight=12, debtor_weight=19)
    todd_personlink2 = personlink_shop(todd_text, credor_weight=33, debtor_weight=3)
    assert todd_personlink1.credor_weight == 12
    assert todd_personlink1.debtor_weight == 19

    # WHEN
    todd_personlink1.meld(todd_personlink2)

    # THEN
    assert todd_personlink1.credor_weight == 45
    assert todd_personlink1.debtor_weight == 22
