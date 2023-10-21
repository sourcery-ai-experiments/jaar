from src.agenda.party import (
    PartyUnit,
    PartyTitle,
    partylink_shop,
    partyunit_shop,
    partylinks_get_from_json,
    partyunits_get_from_json,
    partyrings_get_from_json,
    PartyRing,
)
from src.agenda.x_func import x_is_json, x_get_json
from pytest import raises as pytest_raises


def test_PartyTitle_exists():
    cersei_title = PartyTitle("Cersei")
    assert cersei_title != None
    assert str(type(cersei_title)).find(".party.PartyTitle") > 0


def test_partyrings_exists():
    cersei_title = PartyTitle("Cersei")
    friend_link = PartyRing(title=cersei_title)
    assert friend_link.title == cersei_title


def test_partyrings_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    party_title = PartyTitle("bob")
    party_ring = PartyRing(title=party_title)
    print(f"{party_ring}")

    # WHEN
    x_dict = party_ring.get_dict()

    # THEN
    assert x_dict != None
    assert x_dict == {"title": str(party_title)}


def test_partyrings_get_from_JSON_SimpleExampleWorks():
    # GIVEN
    marie_text = "Marie"
    marie_json_dict = {marie_text: {"title": marie_text}}
    marie_json_text = x_get_json(dict_x=marie_json_dict)
    assert x_is_json(json_x=marie_json_text)

    # WHEN
    marie_obj_dict = partyrings_get_from_json(partyrings_json=marie_json_text)

    # THEN
    assert marie_obj_dict != None
    marie_partyring = PartyRing(title=marie_text)
    partyrings_dict = {marie_partyring.title: marie_partyring}
    assert marie_obj_dict == partyrings_dict


def test_PartyUnit_exists():
    # GIVEN
    bob_title = "bob"

    # WHEN
    bob_party = PartyUnit(title=bob_title)

    # THEN
    print(f"{bob_title}")
    assert bob_party != None
    assert bob_party.title != None
    assert bob_party.title == bob_title
    assert bob_party.creditor_weight is None
    assert bob_party.debtor_weight is None
    assert bob_party._agenda_credit is None
    assert bob_party._agenda_debt is None
    assert bob_party._agenda_goal_credit is None
    assert bob_party._agenda_goal_debt is None
    assert bob_party._creditor_active is None
    assert bob_party._debtor_active is None
    assert bob_party._partyrings is None
    assert bob_party._bank_tax_paid is None
    assert bob_party._bank_tax_diff is None
    assert bob_party._bank_credit_score is None
    assert bob_party._bank_voice_rank is None
    assert bob_party.depotlink_type is None
    assert bob_party._output_agenda_meld_order is None


def test_PartyUnit_set_output_agenda_meld_order_CorrectlySetsAttribute():
    # GIVEN
    bob_title = "bob"
    bob_party = partyunit_shop(title=bob_title)
    assert bob_party._output_agenda_meld_order is None

    # WHEN
    x_output_agenda_meld_order = 5
    bob_party.set_output_agenda_meld_order(x_output_agenda_meld_order)

    # THEN
    assert bob_party._output_agenda_meld_order == x_output_agenda_meld_order


def test_PartyUnit_clear_output_agenda_meld_order_CorrectlySetsAttribute():
    # GIVEN
    bob_title = "bob"
    bob_party = partyunit_shop(title=bob_title)
    x_output_agenda_meld_order = 5
    bob_party.set_output_agenda_meld_order(x_output_agenda_meld_order)
    assert bob_party._output_agenda_meld_order == x_output_agenda_meld_order

    # WHEN
    bob_party.clear_output_agenda_meld_order()

    # THEN
    assert bob_party._output_agenda_meld_order is None


def test_PartyUnit_set_depotlink_type_CorrectlySetsAttributeNoNulls():
    # GIVEN
    bob_title = "bob"
    bob_party = partyunit_shop(title=bob_title)

    # WHEN
    depotlink_type_x = "assignment"
    bob_party.set_depotlink_type(
        depotlink_type=depotlink_type_x, creditor_weight=23, debtor_weight=34
    )

    # THEN
    assert bob_party.depotlink_type == depotlink_type_x
    assert bob_party.creditor_weight == 23
    assert bob_party.debtor_weight == 34


def test_PartyUnit_set_depotlink_type_CorrectlySetsAttributeWithNullsAndStartingValues():
    # GIVEN
    bob_title = "bob"
    bob_party = partyunit_shop(title=bob_title, creditor_weight=45, debtor_weight=56)

    # WHEN
    depotlink_type_x = "assignment"
    bob_party.set_depotlink_type(
        depotlink_type=depotlink_type_x, creditor_weight=None, debtor_weight=None
    )

    # THEN
    assert bob_party.depotlink_type == depotlink_type_x
    assert bob_party.creditor_weight == 45
    assert bob_party.debtor_weight == 56


def test_PartyUnit_set_depotlink_type_CorrectlySetsAttributeWithNullsAndNoStartingValues():
    # GIVEN
    bob_title = "bob"
    bob_party = partyunit_shop(title=bob_title)

    # WHEN
    depotlink_type_x = "assignment"
    bob_party.set_depotlink_type(
        depotlink_type=depotlink_type_x, creditor_weight=None, debtor_weight=None
    )

    # THEN
    assert bob_party.depotlink_type == depotlink_type_x
    assert bob_party.creditor_weight == 1
    assert bob_party.debtor_weight == 1


def test_PartyUnit_del_depotlink_type_CorrectlySetsAttributeToNone():
    # GIVEN
    bob_title = "bob"
    bob_party = partyunit_shop(title=bob_title, creditor_weight=45, debtor_weight=56)
    depotlink_type_x = "assignment"
    bob_party.set_depotlink_type(depotlink_type=depotlink_type_x)
    assert bob_party.depotlink_type == depotlink_type_x
    assert bob_party.creditor_weight == 45
    assert bob_party.debtor_weight == 56

    # WHEN
    bob_party.del_depotlink_type()

    # THEN
    assert bob_party.depotlink_type is None
    assert bob_party.creditor_weight == 45
    assert bob_party.debtor_weight == 56


def test_PartyUnit_set_depotlink_type_raisesErrorIfByTypeIsEntered():
    # GIVEN
    bad_type_text = "bad"
    bob_title = "bob"
    bob_party = partyunit_shop(title=bob_title)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_party.set_depotlink_type(depotlink_type=bad_type_text)
    assert (
        str(excinfo.value)
        == f"PartyUnit '{bob_party.title}' cannot have type '{bad_type_text}'."
    )


def test_PartyUnit_set_empty_agenda_credit_debt_to_zero_CorrectlySetsZero():
    # GIVEN
    bob_title = "bob"
    bob_party = partyunit_shop(title=bob_title)
    assert bob_party._agenda_credit is None
    assert bob_party._agenda_debt is None
    assert bob_party._agenda_goal_credit is None
    assert bob_party._agenda_goal_debt is None
    assert bob_party._agenda_goal_ratio_credit is None
    assert bob_party._agenda_goal_ratio_debt is None

    # WHEN
    bob_party.set_empty_agenda_credit_debt_to_zero()

    # THEN
    assert bob_party._agenda_credit == 0
    assert bob_party._agenda_debt == 0
    assert bob_party._agenda_goal_credit == 0
    assert bob_party._agenda_goal_debt == 0
    assert bob_party._agenda_goal_ratio_credit == 0
    assert bob_party._agenda_goal_ratio_debt == 0

    # GIVEN
    bob_party._agenda_credit = 0.27
    bob_party._agenda_debt = 0.37
    bob_party._agenda_goal_credit = 0.41
    bob_party._agenda_goal_debt = 0.51
    bob_party._agenda_goal_ratio_credit = 0.23
    bob_party._agenda_goal_ratio_debt = 0.87
    assert bob_party._agenda_credit == 0.27
    assert bob_party._agenda_debt == 0.37
    assert bob_party._agenda_goal_credit == 0.41
    assert bob_party._agenda_goal_debt == 0.51
    assert bob_party._agenda_goal_ratio_credit == 0.23
    assert bob_party._agenda_goal_ratio_debt == 0.87

    # WHEN
    bob_party.set_empty_agenda_credit_debt_to_zero()

    # THEN
    assert bob_party._agenda_credit == 0.27
    assert bob_party._agenda_debt == 0.37
    assert bob_party._agenda_goal_credit == 0.41
    assert bob_party._agenda_goal_debt == 0.51
    assert bob_party._agenda_goal_ratio_credit == 0.23
    assert bob_party._agenda_goal_ratio_debt == 0.87


def test_PartyUnit_reset_agenda_credit_debt_MethodWorkCorrectly():
    # GIVEN
    bob_title = "bob"
    bob_party = partyunit_shop(title=bob_title)
    bob_party._agenda_credit = 0.27
    bob_party._agenda_debt = 0.37
    bob_party._agenda_goal_credit = 0.41
    bob_party._agenda_goal_debt = 0.51
    bob_party._agenda_goal_ratio_credit = 0.433
    bob_party._agenda_goal_ratio_debt = 0.533
    assert bob_party._agenda_credit == 0.27
    assert bob_party._agenda_debt == 0.37
    assert bob_party._agenda_goal_credit == 0.41
    assert bob_party._agenda_goal_debt == 0.51
    assert bob_party._agenda_goal_ratio_credit == 0.433
    assert bob_party._agenda_goal_ratio_debt == 0.533

    # WHEN
    bob_party.reset_agenda_credit_debt()

    # THEN
    assert bob_party._agenda_credit == 0
    assert bob_party._agenda_debt == 0
    assert bob_party._agenda_goal_credit == 0
    assert bob_party._agenda_goal_debt == 0
    assert bob_party._agenda_goal_ratio_credit == 0
    assert bob_party._agenda_goal_ratio_debt == 0


def test_PartyUnit_add_agenda_credit_debt_MethodWorkCorrectly():
    # GIVEN
    bob_title = "bob"
    bob_party = partyunit_shop(title=bob_title)
    bob_party._agenda_credit = 0.4106
    bob_party._agenda_debt = 0.1106
    bob_party._agenda_goal_credit = 0.41
    bob_party._agenda_goal_debt = 0.51
    assert bob_party._agenda_goal_credit == 0.41
    assert bob_party._agenda_goal_debt == 0.51

    # WHEN
    bob_party.add_agenda_credit_debt(
        agenda_credit=0.33,
        agenda_debt=0.055,
        agenda_goal_credit=0.3,
        agenda_goal_debt=0.05,
    )

    # THEN
    assert bob_party._agenda_credit == 0.7406
    assert bob_party._agenda_debt == 0.1656
    assert bob_party._agenda_goal_credit == 0.71
    assert bob_party._agenda_goal_debt == 0.56


def test_PartyUnit_set_agenda_goal_ratio_credit_debt_MethodWorkCorrectly():
    # GIVEN
    bob_title = "bob"
    bob_party = partyunit_shop(
        title=bob_title,
        creditor_weight=15,
        debtor_weight=7,
        _agenda_credit=0.4106,
        _agenda_debt=0.1106,
        _agenda_goal_credit=0.041,
        _agenda_goal_debt=0.051,
        _agenda_goal_ratio_credit=0,
        _agenda_goal_ratio_debt=0,
    )
    assert bob_party._agenda_goal_ratio_credit == 0
    assert bob_party._agenda_goal_ratio_debt == 0

    # WHEN
    bob_party.set_agenda_goal_ratio_credit_debt(
        agenda_goal_ratio_credit_sum=0.2,
        agenda_goal_ratio_debt_sum=0.5,
        agenda_partyunit_total_creditor_weight=20,
        agenda_partyunit_total_debtor_weight=14,
    )

    # THEN
    assert bob_party._agenda_goal_ratio_credit == 0.205
    assert bob_party._agenda_goal_ratio_debt == 0.102

    # WHEN
    bob_party.set_agenda_goal_ratio_credit_debt(
        agenda_goal_ratio_credit_sum=0,
        agenda_goal_ratio_debt_sum=0,
        agenda_partyunit_total_creditor_weight=20,
        agenda_partyunit_total_debtor_weight=14,
    )

    # THEN
    assert bob_party._agenda_goal_ratio_credit == 0.75
    assert bob_party._agenda_goal_ratio_debt == 0.5


def test_PartyUnit_set_banking_data_MethodWorkCorrectly():
    # GIVEN
    bob_title = "bob"
    x_agenda_goal_ratio_credit = 0.077
    x_agenda_goal_ratio_debt = 0.066

    bob_party = partyunit_shop(
        title=bob_title,
        _agenda_goal_ratio_credit=x_agenda_goal_ratio_credit,
        _agenda_goal_ratio_debt=x_agenda_goal_ratio_debt,
    )
    assert bob_party._agenda_goal_ratio_credit == 0.077
    assert bob_party._agenda_goal_ratio_debt == 0.066
    assert bob_party._bank_tax_paid is None
    assert bob_party._bank_tax_diff is None
    assert bob_party._bank_credit_score is None
    assert bob_party._bank_voice_rank is None

    # WHEN
    x_tax_paid = 0.2
    x_tax_diff = 0.123
    x_bank_credit_score = 900
    x_bank_voice_rank = 45
    bob_party.set_banking_data(
        tax_paid=x_tax_paid,
        tax_diff=x_tax_diff,
        credit_score=x_bank_credit_score,
        voice_rank=x_bank_voice_rank,
    )
    # THEN
    assert bob_party._agenda_goal_ratio_credit == x_agenda_goal_ratio_credit
    assert bob_party._agenda_goal_ratio_debt == x_agenda_goal_ratio_debt
    assert bob_party._bank_tax_paid == x_tax_paid
    assert bob_party._bank_tax_diff == x_tax_diff
    assert bob_party._bank_credit_score == x_bank_credit_score
    assert bob_party._bank_voice_rank == x_bank_voice_rank


def test_PartyUnit_clear_banking_data_MethodWorkCorrectly():
    # GIVEN
    bob_title = "bob"
    bob_party = partyunit_shop(
        title=bob_title,
        _agenda_goal_ratio_credit=0.355,
        _agenda_goal_ratio_debt=0.066,
    )
    x_bank_credit_score = 900
    x_bank_voice_rank = 45
    bob_party.set_banking_data(
        tax_paid=0.399,
        tax_diff=0.044,
        credit_score=x_bank_credit_score,
        voice_rank=x_bank_voice_rank,
    )
    assert bob_party._bank_tax_paid == 0.399
    assert bob_party._bank_tax_diff == 0.044
    assert bob_party._bank_credit_score == x_bank_credit_score
    assert bob_party._bank_voice_rank == x_bank_voice_rank

    # WHEN
    bob_party.clear_banking_data()

    # THEN
    assert bob_party._bank_tax_paid is None
    assert bob_party._bank_tax_diff is None
    assert bob_party._bank_credit_score is None
    assert bob_party._bank_voice_rank is None


def test_PartyUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    glen_text = "glen"
    glen_ring = PartyRing(title=glen_text)
    party_rings = {glen_ring.title: glen_ring}
    bob_text = "bob"
    bank_tax_paid = 0.55
    bank_tax_diff = 0.66
    depotlink_type = "assignment"
    bob_party = partyunit_shop(
        title=bob_text,
        uid=652,
        creditor_weight=13,
        debtor_weight=17,
        _creditor_active=False,
        _debtor_active=True,
        _partyrings=party_rings,
        _bank_tax_paid=bank_tax_paid,
        _bank_tax_diff=bank_tax_diff,
        depotlink_type=depotlink_type,
    )
    print(f"{bob_text}")

    # WHEN
    x_dict = bob_party.get_dict()

    # THEN
    print(f"{x_dict=}")
    assert x_dict != None
    assert x_dict == {
        "title": bob_text,
        "uid": 652,
        "creditor_weight": 13,
        "debtor_weight": 17,
        "_creditor_active": False,
        "_debtor_active": True,
        "_partyrings": {"glen": {"title": "glen"}},
        "_bank_tax_paid": bank_tax_paid,
        "_bank_tax_diff": bank_tax_diff,
        "depotlink_type": depotlink_type,
    }


def test_PartyUnisshop_get_from_JSON_SimpleExampleWorks():
    cersei_title = PartyTitle("Cersei")
    party_rings = {cersei_title: {"title": cersei_title}}
    marie_text = "Marie"
    bank_tax_paid = 0.55
    bank_tax_diff = 0.66
    depotlink_type = "assignment"
    marie_json_dict = {
        marie_text: {
            "title": marie_text,
            "uid": 103,
            "creditor_weight": 17,
            "debtor_weight": 17,
            "_creditor_active": False,
            "_debtor_active": True,
            "_partyrings": party_rings,
            "_bank_tax_paid": bank_tax_paid,
            "_bank_tax_diff": bank_tax_diff,
            "depotlink_type": depotlink_type,
        }
    }
    marie_json_text = x_get_json(dict_x=marie_json_dict)
    assert x_is_json(json_x=marie_json_text)


def test_PartyUnisshop_get_from_JSON_SimpleExampleWorksWithIncompleteData():
    # GIVEN
    cersei_title = PartyTitle("Cersei")
    party_rings = {cersei_title: {"title": None}}
    marie_text = "Marie"
    bank_tax_paid = 0.55
    bank_tax_diff = 0.66
    depotlink_type_x = "assignment"
    marie_json_dict = {
        marie_text: {
            "title": marie_text,
            "uid": 103,
            "creditor_weight": 17,
            "debtor_weight": 15,
            "_creditor_active": False,
            "_debtor_active": True,
            "_bank_tax_paid": bank_tax_paid,
            "_bank_tax_diff": bank_tax_diff,
            "depotlink_type": depotlink_type_x,
        }
    }

    # WHEN
    marie_json_text = x_get_json(dict_x=marie_json_dict)

    # THEN
    assert x_is_json(json_x=marie_json_text)

    marie_obj_dict = partyunits_get_from_json(partyunits_json=marie_json_text)
    assert marie_obj_dict[marie_text] != None
    assert marie_obj_dict[marie_text].creditor_weight == 17
    assert marie_obj_dict[marie_text].debtor_weight == 15
    assert marie_obj_dict[marie_text]._creditor_active == False
    assert marie_obj_dict[marie_text]._debtor_active == True
    assert marie_obj_dict[marie_text]._bank_tax_paid == 0.55
    assert marie_obj_dict[marie_text]._bank_tax_diff == 0.66
    assert marie_obj_dict[marie_text].depotlink_type == depotlink_type_x
    # assert marie_obj_dict[marie_text]._partyrings == party_rings


def test_PartyLink_exists():
    # GIVEN
    bikers_title = PartyTitle("Marie")

    # WHEN
    party_link_x = partylink_shop(title=bikers_title)

    # THEN
    assert party_link_x.title == bikers_title
    assert party_link_x.creditor_weight == 1.0
    assert party_link_x.debtor_weight == 1.0

    # WHEN
    bikers_creditor_weight = 3.0
    bikers_debtor_weight = 5.0
    party_link_x = partylink_shop(
        title=bikers_title,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debtor_weight,
        _agenda_credit=0.7,
        _agenda_debt=0.51,
        _agenda_goal_credit=0.66,
        _agenda_goal_debt=0.55,
    )

    # THEN
    assert party_link_x.creditor_weight == bikers_creditor_weight
    assert party_link_x.debtor_weight == bikers_debtor_weight
    assert party_link_x._agenda_credit != None
    assert party_link_x._agenda_credit == 0.7
    assert party_link_x._agenda_debt == 0.51
    assert party_link_x._agenda_goal_credit == 0.66
    assert party_link_x._agenda_goal_debt == 0.55


def test_partylink_shop_set_agenda_credit_debt_CorrectlyWorks():
    # GIVEN
    bikers_title = PartyTitle("Marie")
    bikers_creditor_weight = 3.0
    partylinks_sum_creditor_weight = 60
    group_agenda_credit = 0.5
    group_agenda_goal_credit = 0.98

    bikers_debtor_weight = 13.0
    partylinks_sum_debtor_weight = 26.0
    group_agenda_debt = 0.9
    group_agenda_goal_debt = 0.5151

    party_link_x = partylink_shop(
        title=bikers_title,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debtor_weight,
    )
    assert party_link_x._agenda_credit is None
    assert party_link_x._agenda_debt is None
    assert party_link_x._agenda_goal_credit is None
    assert party_link_x._agenda_goal_debt is None

    # WHEN
    party_link_x.set_agenda_credit_debt(
        partylinks_creditor_weight_sum=partylinks_sum_creditor_weight,
        partylinks_debtor_weight_sum=partylinks_sum_debtor_weight,
        group_agenda_credit=group_agenda_credit,
        group_agenda_debt=group_agenda_debt,
        group_agenda_goal_credit=group_agenda_goal_credit,
        group_agenda_goal_debt=group_agenda_goal_debt,
    )

    # THEN
    assert party_link_x._agenda_credit == 0.025
    assert party_link_x._agenda_debt == 0.45
    assert party_link_x._agenda_goal_credit == 0.049
    assert party_link_x._agenda_goal_debt == 0.25755


def test_partylink_shop_reset_agenda_credit_debt():
    # GIVEN
    biker_title = "maria"
    biker_party = partylink_shop(
        title=biker_title, _agenda_credit=0.04, _agenda_debt=0.7
    )
    print(f"{biker_party}")

    assert biker_party._agenda_credit != None
    assert biker_party._agenda_debt != None

    # WHEN
    biker_party.reset_agenda_credit_debt()

    # THEN
    assert biker_party._agenda_credit == 0
    assert biker_party._agenda_debt == 0


def test_partylink_shop_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    str_title = "Marie"
    biker_title = PartyTitle(str_title)
    biker_party_link = partylink_shop(
        title=biker_title, creditor_weight=12, debtor_weight=19
    )
    print(f"{biker_party_link}")

    # WHEN
    biker_dict = biker_party_link.get_dict()

    # THEN
    assert biker_dict != None
    assert biker_dict == {
        "title": biker_title,
        "creditor_weight": 12,
        "debtor_weight": 19,
    }


def test_partylink_get_from_JSON_SimpleExampleWorks():
    # GIVEN
    marie_text = "Marie"
    marie_json_dict = {
        marie_text: {"title": marie_text, "creditor_weight": 12, "debtor_weight": 19}
    }
    marie_json_text = x_get_json(dict_x=marie_json_dict)
    assert x_is_json(json_x=marie_json_text)

    # WHEN
    marie_obj_dict = partylinks_get_from_json(partylinks_json=marie_json_text)

    # THEN
    assert marie_obj_dict != None

    marie_title = PartyTitle(marie_text)
    marie_partylink = partylink_shop(
        title=marie_title, creditor_weight=12, debtor_weight=19
    )
    partylinks_dict = {marie_partylink.title: marie_partylink}
    assert marie_obj_dict == partylinks_dict


def test_partylink_meld_RaiseSameTitleException():
    # GIVEN
    todd_text = "Todd"
    todd_party = partylink_shop(title=todd_text)
    mery_text = "Merry"
    mery_party = partylink_shop(title=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_party.meld(mery_party)
    assert (
        str(excinfo.value)
        == f"Meld fail PartyLink='{todd_party.title}' not the same as PartyLink='{mery_party.title}"
    )


def test_partylink_meld_CorrectlySumsWeights():
    # GIVEN
    todd_text = "Todd"
    todd_party1 = partylink_shop(title=todd_text, creditor_weight=12, debtor_weight=19)
    todd_party2 = partylink_shop(title=todd_text, creditor_weight=33, debtor_weight=3)
    assert todd_party1.creditor_weight == 12
    assert todd_party1.debtor_weight == 19

    # WHEN
    todd_party1.meld(todd_party2)

    # THEN
    assert todd_party1.creditor_weight == 45
    assert todd_party1.debtor_weight == 22


def test_partyunit_meld_RaiseSameTitleException():
    # GIVEN
    todd_text = "Todd"
    todd_party = partyunit_shop(title=todd_text)
    mery_text = "Merry"
    mery_party = partyunit_shop(title=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_party.meld(mery_party)
    assert (
        str(excinfo.value)
        == f"Meld fail PartyUnit='{todd_party.title}' not the same as PartyUnit='{mery_party.title}"
    )


def test_partyunit_meld_CorrectlySumsWeights():
    # GIVEN
    todd_text = "Todd"
    todd_party1 = partyunit_shop(title=todd_text, creditor_weight=7, debtor_weight=19)
    todd_party2 = partyunit_shop(title=todd_text, creditor_weight=5, debtor_weight=3)
    assert todd_party1.creditor_weight == 7
    assert todd_party1.debtor_weight == 19

    # WHEN
    todd_party1.meld(todd_party2)

    # THEN
    assert todd_party1.creditor_weight == 12
    assert todd_party1.debtor_weight == 22
