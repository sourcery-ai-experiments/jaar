from src.agenda.guy import (
    GuyID,
    guylink_shop,
    guylinks_get_from_json,
)
from src._instrument.python import x_is_json, get_json_from_dict
from pytest import raises as pytest_raises


def test_GuyLink_exists():
    # GIVEN
    bikers_guy_id = GuyID("Yao")

    # WHEN
    x_guylink = guylink_shop(guy_id=bikers_guy_id)

    # THEN
    assert x_guylink.guy_id == bikers_guy_id
    assert x_guylink.credor_weight == 1.0
    assert x_guylink.debtor_weight == 1.0

    # WHEN
    bikers_credor_weight = 3.0
    bikers_debtor_weight = 5.0
    x_guylink = guylink_shop(
        guy_id=bikers_guy_id,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debtor_weight,
        _agenda_cred=0.7,
        _agenda_debt=0.51,
        _agenda_intent_cred=0.66,
        _agenda_intent_debt=0.55,
    )

    # THEN
    assert x_guylink.credor_weight == bikers_credor_weight
    assert x_guylink.debtor_weight == bikers_debtor_weight
    assert x_guylink._agenda_cred != None
    assert x_guylink._agenda_cred == 0.7
    assert x_guylink._agenda_debt == 0.51
    assert x_guylink._agenda_intent_cred == 0.66
    assert x_guylink._agenda_intent_debt == 0.55


def test_guylink_shop_set_agenda_cred_debt_SetsAttrCorrectly():
    # GIVEN
    bikers_guy_id = GuyID("Yao")
    bikers_credor_weight = 3.0
    guylinks_sum_credor_weight = 60
    belief_agenda_cred = 0.5
    belief_agenda_intent_cred = 0.98

    bikers_debtor_weight = 13.0
    guylinks_sum_debtor_weight = 26.0
    belief_agenda_debt = 0.9
    belief_agenda_intent_debt = 0.5151

    x_guylink = guylink_shop(
        guy_id=bikers_guy_id,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debtor_weight,
    )
    assert x_guylink._agenda_cred is None
    assert x_guylink._agenda_debt is None
    assert x_guylink._agenda_intent_cred is None
    assert x_guylink._agenda_intent_debt is None

    # WHEN
    x_guylink.set_agenda_cred_debt(
        guylinks_credor_weight_sum=guylinks_sum_credor_weight,
        guylinks_debtor_weight_sum=guylinks_sum_debtor_weight,
        belief_agenda_cred=belief_agenda_cred,
        belief_agenda_debt=belief_agenda_debt,
        belief_agenda_intent_cred=belief_agenda_intent_cred,
        belief_agenda_intent_debt=belief_agenda_intent_debt,
    )

    # THEN
    assert x_guylink._agenda_cred == 0.025
    assert x_guylink._agenda_debt == 0.45
    assert x_guylink._agenda_intent_cred == 0.049
    assert x_guylink._agenda_intent_debt == 0.25755


def test_guylink_shop_reset_agenda_cred_debt():
    # GIVEN
    biker_guy_id = "maria"
    biker_guy = guylink_shop(guy_id=biker_guy_id, _agenda_cred=0.04, _agenda_debt=0.7)
    print(f"{biker_guy}")

    assert biker_guy._agenda_cred != None
    assert biker_guy._agenda_debt != None

    # WHEN
    biker_guy.reset_agenda_cred_debt()

    # THEN
    assert biker_guy._agenda_cred == 0
    assert biker_guy._agenda_debt == 0


def test_guylink_shop_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    str_guy_id = "Yao"
    biker_guy_id = GuyID(str_guy_id)
    biker_guy_link = guylink_shop(
        guy_id=biker_guy_id, credor_weight=12, debtor_weight=19
    )
    print(f"{biker_guy_link}")

    # WHEN
    biker_dict = biker_guy_link.get_dict()

    # THEN
    assert biker_dict != None
    assert biker_dict == {
        "guy_id": biker_guy_id,
        "credor_weight": 12,
        "debtor_weight": 19,
    }


def test_guylink_get_from_JSON_ReturnsCorrectObj_SimpleExample():
    # GIVEN
    yao_text = "Yao"
    yao_json_dict = {
        yao_text: {"guy_id": yao_text, "credor_weight": 12, "debtor_weight": 19}
    }
    yao_json_text = get_json_from_dict(dict_x=yao_json_dict)
    assert x_is_json(json_x=yao_json_text)

    # WHEN
    yao_obj_dict = guylinks_get_from_json(guylinks_json=yao_json_text)

    # THEN
    assert yao_obj_dict != None

    yao_guy_id = GuyID(yao_text)
    yao_guylink = guylink_shop(guy_id=yao_guy_id, credor_weight=12, debtor_weight=19)
    guylinks_dict = {yao_guylink.guy_id: yao_guylink}
    assert yao_obj_dict == guylinks_dict


def test_guylink_meld_RaiseSameguy_idException():
    # GIVEN
    todd_text = "Todd"
    todd_guy = guylink_shop(guy_id=todd_text)
    mery_text = "Merry"
    mery_guy = guylink_shop(guy_id=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_guy.meld(mery_guy)
    assert (
        str(excinfo.value)
        == f"Meld fail GuyLink='{todd_guy.guy_id}' not the same as GuyLink='{mery_guy.guy_id}"
    )


def test_guylink_meld_CorrectlySumsWeights():
    # GIVEN
    todd_text = "Todd"
    todd_guy1 = guylink_shop(guy_id=todd_text, credor_weight=12, debtor_weight=19)
    todd_guy2 = guylink_shop(guy_id=todd_text, credor_weight=33, debtor_weight=3)
    assert todd_guy1.credor_weight == 12
    assert todd_guy1.debtor_weight == 19

    # WHEN
    todd_guy1.meld(todd_guy2)

    # THEN
    assert todd_guy1.credor_weight == 45
    assert todd_guy1.debtor_weight == 22
