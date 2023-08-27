from src.agent.ally import (
    AllyUnit,
    AllyName,
    allylink_shop,
    allyunit_shop,
    allylinks_get_from_json,
    allyunits_get_from_json,
    allyrings_get_from_json,
    AllyRing,
)
from src.agent.x_func import x_is_json, x_get_json
from pytest import raises as pytest_raises


def test_AllyName_exists():
    cersei_name = AllyName("Cersei")
    assert cersei_name != None
    assert str(type(cersei_name)).find(".ally.AllyName") > 0


def test_allyrings_exists():
    cersei_name = AllyName("Cersei")
    friend_link = AllyRing(name=cersei_name)
    assert friend_link.name == cersei_name


def test_allyrings_get_dict_ReturnsDictWithNecessaryDataForJSON():
    ally_name = AllyName("bob")
    ally_ring = AllyRing(name=ally_name)
    print(f"{ally_ring}")
    x_dict = ally_ring.get_dict()
    assert x_dict != None
    assert x_dict == {"name": str(ally_name)}


def test_allyrings_get_from_JSON_SimpleExampleWorks():
    marie_str = "Marie"
    marie_json_dict = {marie_str: {"name": marie_str}}
    # marie_json_dict = {marie_str: {"name": marie_str, "external_name": marie_str}}
    marie_json_str = x_get_json(dict_x=marie_json_dict)
    assert x_is_json(json_x=marie_json_str)

    marie_obj_dict = allyrings_get_from_json(allyrings_json=marie_json_str)
    assert marie_obj_dict != None

    marie_name = AllyName(marie_str)
    marie_allyring = AllyRing(name=marie_name)
    allyrings_dict = {marie_allyring.name: marie_allyring}
    assert marie_obj_dict == allyrings_dict


def test_AllyUnit_exists():
    # GIVEN
    bob_name = "bob"

    # WHEN
    bob_ally = AllyUnit(name=bob_name)

    # THEN
    print(f"{bob_name}")
    assert bob_ally != None
    assert bob_ally.name != None
    assert bob_ally.name == bob_name
    assert bob_ally.creditor_weight is None
    assert bob_ally.debtor_weight is None
    assert bob_ally._agent_credit is None
    assert bob_ally._agent_debt is None
    assert bob_ally._agent_agenda_credit is None
    assert bob_ally._agent_agenda_debt is None
    assert bob_ally._creditor_active is None
    assert bob_ally._debtor_active is None
    assert bob_ally._allyrings is None
    assert bob_ally.external_name == bob_name
    assert bob_ally._bank_tax_paid is None
    assert bob_ally._bank_tax_diff is None


def test_AllyUnit_set_empty_agent_credit_debt_to_zero_CorrectlySetsZero():
    # GIVEN
    bob_name = "bob"
    bob_ally = allyunit_shop(name=bob_name)
    assert bob_ally._agent_credit is None
    assert bob_ally._agent_debt is None
    assert bob_ally._agent_agenda_credit is None
    assert bob_ally._agent_agenda_debt is None
    assert bob_ally._agent_agenda_ratio_credit is None
    assert bob_ally._agent_agenda_ratio_debt is None

    # WHEN
    bob_ally.set_empty_agent_credit_debt_to_zero()

    # THEN
    assert bob_ally._agent_credit == 0
    assert bob_ally._agent_debt == 0
    assert bob_ally._agent_agenda_credit == 0
    assert bob_ally._agent_agenda_debt == 0
    assert bob_ally._agent_agenda_ratio_credit == 0
    assert bob_ally._agent_agenda_ratio_debt == 0

    # GIVEN
    bob_ally._agent_credit = 0.27
    bob_ally._agent_debt = 0.37
    bob_ally._agent_agenda_credit = 0.41
    bob_ally._agent_agenda_debt = 0.51
    bob_ally._agent_agenda_ratio_credit = 0.23
    bob_ally._agent_agenda_ratio_debt = 0.87
    assert bob_ally._agent_credit == 0.27
    assert bob_ally._agent_debt == 0.37
    assert bob_ally._agent_agenda_credit == 0.41
    assert bob_ally._agent_agenda_debt == 0.51
    assert bob_ally._agent_agenda_ratio_credit == 0.23
    assert bob_ally._agent_agenda_ratio_debt == 0.87

    # WHEN
    bob_ally.set_empty_agent_credit_debt_to_zero()

    # THEN
    assert bob_ally._agent_credit == 0.27
    assert bob_ally._agent_debt == 0.37
    assert bob_ally._agent_agenda_credit == 0.41
    assert bob_ally._agent_agenda_debt == 0.51
    assert bob_ally._agent_agenda_ratio_credit == 0.23
    assert bob_ally._agent_agenda_ratio_debt == 0.87


def test_AllyUnit_reset_agent_credit_debt_MethodWorkCorrectly():
    # GIVEN
    bob_name = "bob"
    bob_ally = allyunit_shop(name=bob_name)
    bob_ally._agent_credit = 0.27
    bob_ally._agent_debt = 0.37
    bob_ally._agent_agenda_credit = 0.41
    bob_ally._agent_agenda_debt = 0.51
    bob_ally._agent_agenda_ratio_credit = 0.433
    bob_ally._agent_agenda_ratio_debt = 0.533
    assert bob_ally._agent_credit == 0.27
    assert bob_ally._agent_debt == 0.37
    assert bob_ally._agent_agenda_credit == 0.41
    assert bob_ally._agent_agenda_debt == 0.51
    assert bob_ally._agent_agenda_ratio_credit == 0.433
    assert bob_ally._agent_agenda_ratio_debt == 0.533

    # WHEN
    bob_ally.reset_agent_credit_debt()

    # THEN
    assert bob_ally._agent_credit == 0
    assert bob_ally._agent_debt == 0
    assert bob_ally._agent_agenda_credit == 0
    assert bob_ally._agent_agenda_debt == 0
    assert bob_ally._agent_agenda_ratio_credit == 0
    assert bob_ally._agent_agenda_ratio_debt == 0


def test_AllyUnit_add_agent_credit_debt_MethodWorkCorrectly():
    # GIVEN
    bob_name = "bob"
    bob_ally = allyunit_shop(name=bob_name)
    bob_ally._agent_credit = 0.4106
    bob_ally._agent_debt = 0.1106
    bob_ally._agent_agenda_credit = 0.41
    bob_ally._agent_agenda_debt = 0.51
    assert bob_ally._agent_agenda_credit == 0.41
    assert bob_ally._agent_agenda_debt == 0.51

    # WHEN
    bob_ally.add_agent_credit_debt(
        agent_credit=0.33,
        agent_debt=0.055,
        agent_agenda_credit=0.3,
        agent_agenda_debt=0.05,
    )

    # THEN
    assert bob_ally._agent_credit == 0.7406
    assert bob_ally._agent_debt == 0.1656
    assert bob_ally._agent_agenda_credit == 0.71
    assert bob_ally._agent_agenda_debt == 0.56


def test_AllyUnit_set_agent_agenda_ratio_credit_debt_MethodWorkCorrectly():
    # GIVEN
    bob_name = "bob"
    bob_ally = allyunit_shop(
        name=bob_name,
        creditor_weight=15,
        debtor_weight=7,
        _agent_credit=0.4106,
        _agent_debt=0.1106,
        _agent_agenda_credit=0.041,
        _agent_agenda_debt=0.051,
        _agent_agenda_ratio_credit=0,
        _agent_agenda_ratio_debt=0,
    )
    assert bob_ally._agent_agenda_ratio_credit == 0
    assert bob_ally._agent_agenda_ratio_debt == 0

    # WHEN
    bob_ally.set_agent_agenda_ratio_credit_debt(
        agent_agenda_ratio_credit_sum=0.2,
        agent_agenda_ratio_debt_sum=0.5,
        agent_allyunit_total_creditor_weight=20,
        agent_allyunit_total_debtor_weight=14,
    )

    # THEN
    assert bob_ally._agent_agenda_ratio_credit == 0.205
    assert bob_ally._agent_agenda_ratio_debt == 0.102

    # WHEN
    bob_ally.set_agent_agenda_ratio_credit_debt(
        agent_agenda_ratio_credit_sum=0,
        agent_agenda_ratio_debt_sum=0,
        agent_allyunit_total_creditor_weight=20,
        agent_allyunit_total_debtor_weight=14,
    )

    # THEN
    assert bob_ally._agent_agenda_ratio_credit == 0.75
    assert bob_ally._agent_agenda_ratio_debt == 0.5


def test_AllyUnit_set_banking_data_MethodWorkCorrectly():
    # GIVEN
    bob_name = "bob"
    bob_ally = allyunit_shop(
        name=bob_name,
        _agent_agenda_ratio_credit=0.077,
        _agent_agenda_ratio_debt=0.066,
    )
    assert bob_ally._agent_agenda_ratio_credit == 0.077
    assert bob_ally._agent_agenda_ratio_debt == 0.066
    assert bob_ally._bank_tax_paid is None
    assert bob_ally._bank_tax_diff is None

    # WHEN
    tax_paid_v1 = 0.2
    tax_diff = 0.123
    bob_ally.set_banking_data(tax_paid=tax_paid_v1, tax_diff=tax_diff)
    # THEN
    assert bob_ally._agent_agenda_ratio_credit == 0.077
    assert bob_ally._agent_agenda_ratio_debt == 0.066
    assert bob_ally._bank_tax_paid == tax_paid_v1
    assert bob_ally._bank_tax_diff == tax_diff

    # tax_paid_v2 = 0.3

    # # WHEN / Then
    # with pytest_raises(Exception) as excinfo:
    #     bob_ally.set_banking_data(tax_paid=tax_paid_v2, tax_diff=tax_diff)
    # assert (
    #     str(excinfo.value)
    #     == f"AllyUnit.set_banking_data fail: tax_paid={tax_paid_v2} + tax_diff={tax_diff} not equal to _agent_agenda_ratio_credit={bob_ally._agent_agenda_ratio_credit}"
    # )


def test_AllyUnit_clear_banking_data_MethodWorkCorrectly():
    # GIVEN
    bob_name = "bob"
    bob_ally = allyunit_shop(
        name=bob_name,
        _agent_agenda_ratio_credit=0.355,
        _agent_agenda_ratio_debt=0.066,
    )
    bob_ally.set_banking_data(tax_paid=0.399, tax_diff=0.044)
    assert bob_ally._bank_tax_paid == 0.399
    assert bob_ally._bank_tax_diff == 0.044

    # WHEN
    bob_ally.clear_banking_data()

    # THEN
    assert bob_ally._bank_tax_paid is None
    assert bob_ally._bank_tax_diff is None


def test_AllyUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    glen_str = "glen"
    glen_ring = AllyRing(name=glen_str)
    ally_rings = {glen_ring.name: glen_ring}
    bob_str = "bob"
    bank_tax_paid = 0.55
    bank_tax_diff = 0.66
    bob_ally = allyunit_shop(
        name=bob_str,
        uid=652,
        creditor_weight=13,
        debtor_weight=17,
        _creditor_active=False,
        _debtor_active=True,
        _allyrings=ally_rings,
        _bank_tax_paid=bank_tax_paid,
        _bank_tax_diff=bank_tax_diff,
    )
    print(f"{bob_str}")
    x_dict = bob_ally.get_dict()
    print(f"{x_dict=}")
    assert x_dict != None
    assert x_dict == {
        "name": bob_str,
        "uid": 652,
        "creditor_weight": 13,
        "debtor_weight": 17,
        "_creditor_active": False,
        "_debtor_active": True,
        "_allyrings": {"glen": {"name": "glen"}},
        "external_name": bob_str,
        "_bank_tax_paid": bank_tax_paid,
        "_bank_tax_diff": bank_tax_diff,
    }


def test_AllyUnisshop_get_from_JSON_SimpleExampleWorks():
    cersei_name = AllyName("Cersei")
    cersei_external = "Cersei Lan"
    ally_rings = {cersei_name: {"name": cersei_name}}
    marie_str = "Marie"
    bank_tax_paid = 0.55
    bank_tax_diff = 0.66
    marie_json_dict = {
        marie_str: {
            "name": marie_str,
            "uid": 103,
            "creditor_weight": 17,
            "debtor_weight": 17,
            "_creditor_active": False,
            "_debtor_active": True,
            "_allyrings": ally_rings,
            "external_name": cersei_external,
            "_bank_tax_paid": bank_tax_paid,
            "_bank_tax_diff": bank_tax_diff,
        }
    }
    marie_json_str = x_get_json(dict_x=marie_json_dict)
    assert x_is_json(json_x=marie_json_str)


def test_AllyUnisshop_get_from_JSON_SimpleExampleWorksWithIncompleteData():
    # GIVEN
    cersei_name = AllyName("Cersei")
    ally_rings = {cersei_name: {"name": None}}
    marie_text = "Marie"
    bank_tax_paid = 0.55
    bank_tax_diff = 0.66
    marie_json_dict = {
        marie_text: {
            "name": marie_text,
            "uid": 103,
            "creditor_weight": 17,
            "debtor_weight": 15,
            "_creditor_active": False,
            "_debtor_active": True,
            "_bank_tax_paid": bank_tax_paid,
            "_bank_tax_diff": bank_tax_diff,
        }
    }

    # WHEN
    marie_json_str = x_get_json(dict_x=marie_json_dict)

    # THEN
    assert x_is_json(json_x=marie_json_str)

    marie_obj_dict = allyunits_get_from_json(allyunits_json=marie_json_str)
    assert marie_obj_dict[marie_text] != None
    assert marie_obj_dict[marie_text].creditor_weight == 17
    assert marie_obj_dict[marie_text].debtor_weight == 15
    assert marie_obj_dict[marie_text]._creditor_active == False
    assert marie_obj_dict[marie_text]._debtor_active == True
    assert marie_obj_dict[marie_text]._bank_tax_paid == 0.55
    assert marie_obj_dict[marie_text]._bank_tax_diff == 0.66
    # assert marie_obj_dict[marie_text]._allyrings == ally_rings


def test_AllyLink_exists():
    # GIVEN
    bikers_name = AllyName("Marie")

    # WHEN
    ally_link_x = allylink_shop(name=bikers_name)

    # THEN
    assert ally_link_x.name == bikers_name
    assert ally_link_x.creditor_weight == 1.0
    assert ally_link_x.debtor_weight == 1.0

    # WHEN
    bikers_creditor_weight = 3.0
    bikers_debtor_weight = 5.0
    ally_link_x = allylink_shop(
        name=bikers_name,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debtor_weight,
        _agent_credit=0.7,
        _agent_debt=0.51,
        _agent_agenda_credit=0.66,
        _agent_agenda_debt=0.55,
    )

    # THEN
    assert ally_link_x.creditor_weight == bikers_creditor_weight
    assert ally_link_x.debtor_weight == bikers_debtor_weight
    assert ally_link_x._agent_credit != None
    assert ally_link_x._agent_credit == 0.7
    assert ally_link_x._agent_debt == 0.51
    assert ally_link_x._agent_agenda_credit == 0.66
    assert ally_link_x._agent_agenda_debt == 0.55


def test_allylink_shop_set_agent_credit_debt_CorrectlyWorks():
    # GIVEN
    bikers_name = AllyName("Marie")
    bikers_creditor_weight = 3.0
    allylinks_sum_creditor_weight = 60
    group_agent_credit = 0.5
    group_agent_agenda_credit = 0.98

    bikers_debtor_weight = 13.0
    allylinks_sum_debtor_weight = 26.0
    group_agent_debt = 0.9
    group_agent_agenda_debt = 0.5151

    ally_link_x = allylink_shop(
        name=bikers_name,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debtor_weight,
    )
    assert ally_link_x._agent_credit is None
    assert ally_link_x._agent_debt is None
    assert ally_link_x._agent_agenda_credit is None
    assert ally_link_x._agent_agenda_debt is None

    # WHEN
    ally_link_x.set_agent_credit_debt(
        allylinks_creditor_weight_sum=allylinks_sum_creditor_weight,
        allylinks_debtor_weight_sum=allylinks_sum_debtor_weight,
        group_agent_credit=group_agent_credit,
        group_agent_debt=group_agent_debt,
        group_agent_agenda_credit=group_agent_agenda_credit,
        group_agent_agenda_debt=group_agent_agenda_debt,
    )

    # THEN
    assert ally_link_x._agent_credit == 0.025
    assert ally_link_x._agent_debt == 0.45
    assert ally_link_x._agent_agenda_credit == 0.049
    assert ally_link_x._agent_agenda_debt == 0.25755


def test_allylink_shop_reset_agent_credit_debt():
    # GIVEN
    biker_name = "maria"
    biker_ally = allylink_shop(name=biker_name, _agent_credit=0.04, _agent_debt=0.7)
    print(f"{biker_ally}")

    assert biker_ally._agent_credit != None
    assert biker_ally._agent_debt != None

    # WHEN
    biker_ally.reset_agent_credit_debt()

    # THEN
    assert biker_ally._agent_credit == 0
    assert biker_ally._agent_debt == 0


def test_allylink_shop_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    str_name = "Marie"
    biker_name = AllyName(str_name)
    biker_ally_link = allylink_shop(
        name=biker_name, creditor_weight=12, debtor_weight=19
    )
    print(f"{biker_ally_link}")

    # WHEN
    biker_dict = biker_ally_link.get_dict()

    # THEN
    assert biker_dict != None
    assert biker_dict == {
        "name": biker_name,
        "creditor_weight": 12,
        "debtor_weight": 19,
    }


def test_allylink_get_from_JSON_SimpleExampleWorks():
    # GIVEN
    marie_str = "Marie"
    marie_json_dict = {
        marie_str: {"name": marie_str, "creditor_weight": 12, "debtor_weight": 19}
    }
    marie_json_str = x_get_json(dict_x=marie_json_dict)
    assert x_is_json(json_x=marie_json_str)

    # WHEN
    marie_obj_dict = allylinks_get_from_json(allylinks_json=marie_json_str)

    # THEN
    assert marie_obj_dict != None

    marie_name = AllyName(marie_str)
    marie_allylink = allylink_shop(
        name=marie_name, creditor_weight=12, debtor_weight=19
    )
    allylinks_dict = {marie_allylink.name: marie_allylink}
    assert marie_obj_dict == allylinks_dict


def test_allylink_meld_RaiseSameNameException():
    # GIVEN
    todd_text = "Todd"
    todd_ally = allylink_shop(name=todd_text)
    mery_text = "Merry"
    mery_ally = allylink_shop(name=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_ally.meld(mery_ally)
    assert (
        str(excinfo.value)
        == f"Meld fail AllyLink='{todd_ally.name}' not the same as AllyLink='{mery_ally.name}"
    )


def test_allylink_meld_CorrectlySumsWeights():
    # GIVEN
    todd_text = "Todd"
    todd_ally1 = allylink_shop(name=todd_text, creditor_weight=12, debtor_weight=19)
    todd_ally2 = allylink_shop(name=todd_text, creditor_weight=33, debtor_weight=3)
    assert todd_ally1.creditor_weight == 12
    assert todd_ally1.debtor_weight == 19

    # WHEN
    todd_ally1.meld(todd_ally2)

    # THEN
    assert todd_ally1.creditor_weight == 45
    assert todd_ally1.debtor_weight == 22


def test_allyunit_meld_RaiseSameNameException():
    # GIVEN
    todd_text = "Todd"
    todd_ally = allyunit_shop(name=todd_text)
    mery_text = "Merry"
    mery_ally = allyunit_shop(name=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_ally.meld(mery_ally)
    assert (
        str(excinfo.value)
        == f"Meld fail AllyUnit='{todd_ally.name}' not the same as AllyUnit='{mery_ally.name}"
    )


def test_allyunit_meld_CorrectlySumsWeights():
    # GIVEN
    todd_text = "Todd"
    todd_ally1 = allyunit_shop(name=todd_text, creditor_weight=7, debtor_weight=19)
    todd_ally2 = allyunit_shop(name=todd_text, creditor_weight=5, debtor_weight=3)
    assert todd_ally1.creditor_weight == 7
    assert todd_ally1.debtor_weight == 19

    # WHEN
    todd_ally1.meld(todd_ally2)

    # THEN
    assert todd_ally1.creditor_weight == 12
    assert todd_ally1.debtor_weight == 22
