from src.agenda.party import (
    PartyUnit,
    PartyHandle,
    partylink_shop,
    partyunit_shop,
    partylinks_get_from_json,
    partyunits_get_from_json,
    partyrings_get_from_json,
    PartyRing,
)
from src.agenda.x_func import x_is_json, x_get_json
from pytest import raises as pytest_raises


def test_PartyHandle_exists():
    cersei_handle = PartyHandle("Cersei")
    assert cersei_handle != None
    assert str(type(cersei_handle)).find(".party.PartyHandle") > 0


def test_partyrings_exists():
    cersei_handle = PartyHandle("Cersei")
    friend_link = PartyRing(handle=cersei_handle)
    assert friend_link.handle == cersei_handle


def test_partyrings_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    party_handle = PartyHandle("bob")
    party_ring = PartyRing(handle=party_handle)
    print(f"{party_ring}")

    # WHEN
    x_dict = party_ring.get_dict()

    # THEN
    assert x_dict != None
    assert x_dict == {"handle": str(party_handle)}


def test_partyrings_get_from_JSON_SimpleExampleWorks():
    # GIVEN
    yao_text = "Yao"
    yao_json_dict = {yao_text: {"handle": yao_text}}
    yao_json_text = x_get_json(dict_x=yao_json_dict)
    assert x_is_json(json_x=yao_json_text)

    # WHEN
    yao_obj_dict = partyrings_get_from_json(partyrings_json=yao_json_text)

    # THEN
    assert yao_obj_dict != None
    yao_partyring = PartyRing(handle=yao_text)
    partyrings_dict = {yao_partyring.handle: yao_partyring}
    assert yao_obj_dict == partyrings_dict


def test_PartyUnit_exists():
    # GIVEN
    bob_handle = "bob"

    # WHEN
    bob_party = PartyUnit(handle=bob_handle)

    # THEN
    print(f"{bob_handle}")
    assert bob_party != None
    assert bob_party.handle != None
    assert bob_party.handle == bob_handle
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
    assert bob_party._bank_voice_hx_lowest_rank is None
    assert bob_party.depotlink_type is None
    assert bob_party._output_agenda_meld_order is None


def test_PartyUnit_set_output_agenda_meld_order_CorrectlySetsAttribute():
    # GIVEN
    bob_handle = "bob"
    bob_party = partyunit_shop(handle=bob_handle)
    assert bob_party._output_agenda_meld_order is None

    # WHEN
    x_output_agenda_meld_order = 5
    bob_party.set_output_agenda_meld_order(x_output_agenda_meld_order)

    # THEN
    assert bob_party._output_agenda_meld_order == x_output_agenda_meld_order


def test_PartyUnit_clear_output_agenda_meld_order_CorrectlySetsAttribute():
    # GIVEN
    bob_handle = "bob"
    bob_party = partyunit_shop(handle=bob_handle)
    x_output_agenda_meld_order = 5
    bob_party.set_output_agenda_meld_order(x_output_agenda_meld_order)
    assert bob_party._output_agenda_meld_order == x_output_agenda_meld_order

    # WHEN
    bob_party.clear_output_agenda_meld_order()

    # THEN
    assert bob_party._output_agenda_meld_order is None


def test_PartyUnit_set_depotlink_type_CorrectlySetsAttributeNoNulls():
    # GIVEN
    bob_handle = "bob"
    bob_party = partyunit_shop(handle=bob_handle)

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
    bob_handle = "bob"
    bob_party = partyunit_shop(handle=bob_handle, creditor_weight=45, debtor_weight=56)

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
    bob_handle = "bob"
    bob_party = partyunit_shop(handle=bob_handle)

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
    bob_handle = "bob"
    bob_party = partyunit_shop(handle=bob_handle, creditor_weight=45, debtor_weight=56)
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
    bob_handle = "bob"
    bob_party = partyunit_shop(handle=bob_handle)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_party.set_depotlink_type(depotlink_type=bad_type_text)
    assert (
        str(excinfo.value)
        == f"PartyUnit '{bob_party.handle}' cannot have type '{bad_type_text}'."
    )


def test_PartyUnit_set_empty_agenda_credit_debt_to_zero_CorrectlySetsZero():
    # GIVEN
    bob_handle = "bob"
    bob_party = partyunit_shop(handle=bob_handle)
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
    bob_handle = "bob"
    bob_party = partyunit_shop(handle=bob_handle)
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
    bob_handle = "bob"
    bob_party = partyunit_shop(handle=bob_handle)
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
    bob_handle = "bob"
    bob_party = partyunit_shop(
        handle=bob_handle,
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
    bob_handle = "bob"
    x_agenda_goal_ratio_credit = 0.077
    x_agenda_goal_ratio_debt = 0.066

    bob_party = partyunit_shop(
        handle=bob_handle,
        _agenda_goal_ratio_credit=x_agenda_goal_ratio_credit,
        _agenda_goal_ratio_debt=x_agenda_goal_ratio_debt,
    )
    assert bob_party._agenda_goal_ratio_credit == 0.077
    assert bob_party._agenda_goal_ratio_debt == 0.066
    assert bob_party._bank_tax_paid is None
    assert bob_party._bank_tax_diff is None
    assert bob_party._bank_credit_score is None
    assert bob_party._bank_voice_rank is None
    assert bob_party._bank_voice_hx_lowest_rank is None

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
    assert bob_party._bank_voice_hx_lowest_rank == x_bank_voice_rank


def test_PartyUnit_set_banking_data_CorrectlyDecreasesOrIgnores_bank_voice_hx_lowest_rank():
    # GIVEN
    bob_handle = "bob"
    x_agenda_goal_ratio_credit = 0.077
    x_agenda_goal_ratio_debt = 0.066
    bob_party = partyunit_shop(
        handle=bob_handle,
        _agenda_goal_ratio_credit=x_agenda_goal_ratio_credit,
        _agenda_goal_ratio_debt=x_agenda_goal_ratio_debt,
    )
    x_tax_paid = 0.2
    x_tax_diff = 0.123
    x_bank_credit_score = 900
    old_x_bank_voice_rank = 45
    bob_party.set_banking_data(
        tax_paid=x_tax_paid,
        tax_diff=x_tax_diff,
        credit_score=x_bank_credit_score,
        voice_rank=old_x_bank_voice_rank,
    )
    assert bob_party._bank_voice_hx_lowest_rank == old_x_bank_voice_rank

    # WHEN
    new_x_bank_voice_rank = 33
    bob_party.set_banking_data(
        tax_paid=x_tax_paid,
        tax_diff=x_tax_diff,
        credit_score=x_bank_credit_score,
        voice_rank=new_x_bank_voice_rank,
    )
    # THEN
    assert bob_party._bank_voice_hx_lowest_rank == new_x_bank_voice_rank

    # WHEN
    not_lower_x_bank_voice_rank = 60
    bob_party.set_banking_data(
        tax_paid=x_tax_paid,
        tax_diff=x_tax_diff,
        credit_score=x_bank_credit_score,
        voice_rank=not_lower_x_bank_voice_rank,
    )
    # THEN
    assert bob_party._bank_voice_hx_lowest_rank == new_x_bank_voice_rank


def test_PartyUnit_clear_banking_data_MethodWorkCorrectly():
    # GIVEN
    bob_handle = "bob"
    bob_party = partyunit_shop(
        handle=bob_handle,
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
    glen_ring = PartyRing(handle=glen_text)
    bob_party_rings = {glen_ring.handle: glen_ring}
    bob_text = "bob"
    bob_bank_tax_paid = 0.55
    bob_bank_tax_diff = 0.66
    depotlink_type = "assignment"
    bob_party = partyunit_shop(
        handle=bob_text,
        _partyrings=bob_party_rings,
        _bank_tax_paid=bob_bank_tax_paid,
        _bank_tax_diff=bob_bank_tax_diff,
        depotlink_type=depotlink_type,
    )
    bob_uid = 4321
    bob_party.uid = bob_uid

    bob_creditor_active = False
    bob_debtor_active = True
    bob_party._creditor_active = bob_creditor_active
    bob_party._debtor_active = bob_debtor_active

    bob_creditor_weight = 13
    bob_debtor_weight = 17
    bob_party.creditor_weight = bob_creditor_weight
    bob_party.debtor_weight = bob_debtor_weight

    bob_bank_credit_score = 7000
    bob_bank_voice_rank = 898
    bob_bank_voice_hx_lowest_rank = 740
    bob_party._bank_credit_score = bob_bank_credit_score
    bob_party._bank_voice_rank = bob_bank_voice_rank
    bob_party._bank_voice_hx_lowest_rank = bob_bank_voice_hx_lowest_rank
    print(f"{bob_text}")

    # WHEN
    x_dict = bob_party.get_dict()

    # THEN
    print(f"{x_dict=}")
    assert x_dict != None
    assert x_dict == {
        "handle": bob_text,
        "uid": bob_uid,
        "creditor_weight": bob_creditor_weight,
        "debtor_weight": bob_debtor_weight,
        "_creditor_active": bob_creditor_active,
        "_debtor_active": bob_debtor_active,
        "_partyrings": {"glen": {"handle": "glen"}},
        "_bank_tax_paid": bob_bank_tax_paid,
        "_bank_tax_diff": bob_bank_tax_diff,
        "_bank_credit_score": bob_bank_credit_score,
        "_bank_voice_rank": bob_bank_voice_rank,
        "_bank_voice_hx_lowest_rank": bob_bank_voice_hx_lowest_rank,
        "depotlink_type": depotlink_type,
    }


def test_PartyUnisshop_get_from_JSON_SimpleExampleWorks():
    cersei_handle = PartyHandle("Cersei")
    yao_party_rings = {cersei_handle: {"handle": cersei_handle}}
    yao_text = "Yao"
    yao_uid = 239
    yao_creditor_weight = 13
    yao_debtor_weight = 17
    yao_creditor_active = False
    yao_debtor_active = True
    yao_bank_tax_paid = 0.55
    yao_bank_tax_diff = 0.66
    yao_depotlink_type = "assignment"
    yao_bank_credit_score = 7000
    yao_bank_voice_rank = 898
    yao_bank_voice_hx_lowest_rank = 740
    yao_json_dict = {
        yao_text: {
            "handle": yao_text,
            "uid": yao_uid,
            "creditor_weight": yao_creditor_weight,
            "debtor_weight": yao_debtor_weight,
            "_creditor_active": yao_creditor_active,
            "_debtor_active": yao_debtor_active,
            "_partyrings": yao_party_rings,
            "_bank_tax_paid": yao_bank_tax_paid,
            "_bank_tax_diff": yao_bank_tax_diff,
            "_bank_credit_score": yao_bank_credit_score,
            "_bank_voice_rank": yao_bank_voice_rank,
            "_bank_voice_hx_lowest_rank": yao_bank_voice_hx_lowest_rank,
            "depotlink_type": yao_depotlink_type,
        }
    }
    yao_json_text = x_get_json(dict_x=yao_json_dict)
    assert x_is_json(json_x=yao_json_text)


def test_PartyUnisshop_get_from_JSON_SimpleExampleWorksWithIncompleteData():
    # GIVEN
    cersei_handle = PartyHandle("Cersei")
    yao_party_rings = {cersei_handle: {"handle": cersei_handle}}
    yao_text = "Yao"
    yao_uid = 239
    yao_creditor_weight = 13
    yao_debtor_weight = 17
    yao_creditor_active = False
    yao_debtor_active = True
    yao_bank_tax_paid = 0.55
    yao_bank_tax_diff = 0.66
    yao_depotlink_type = "assignment"
    yao_bank_credit_score = 7000
    yao_bank_voice_rank = 898
    yao_bank_voice_hx_lowest_rank = 740
    yao_json_dict = {
        yao_text: {
            "handle": yao_text,
            "uid": yao_uid,
            "creditor_weight": yao_creditor_weight,
            "debtor_weight": yao_debtor_weight,
            "_creditor_active": yao_creditor_active,
            "_debtor_active": yao_debtor_active,
            "_partyrings": yao_party_rings,
            "_bank_tax_paid": yao_bank_tax_paid,
            "_bank_tax_diff": yao_bank_tax_diff,
            "_bank_credit_score": yao_bank_credit_score,
            "_bank_voice_rank": yao_bank_voice_rank,
            "_bank_voice_hx_lowest_rank": yao_bank_voice_hx_lowest_rank,
            "depotlink_type": yao_depotlink_type,
        }
    }

    # WHEN
    yao_json_text = x_get_json(dict_x=yao_json_dict)

    # THEN
    assert x_is_json(json_x=yao_json_text)

    yao_obj_dict = partyunits_get_from_json(partyunits_json=yao_json_text)
    assert yao_obj_dict[yao_text] != None
    yao_partyunit = yao_obj_dict[yao_text]

    assert yao_partyunit.handle == yao_text
    assert yao_partyunit.uid == yao_uid
    assert yao_partyunit.creditor_weight == yao_creditor_weight
    assert yao_partyunit.debtor_weight == yao_debtor_weight
    assert yao_partyunit._creditor_active == yao_creditor_active
    assert yao_partyunit._debtor_active == yao_debtor_active
    # assert yao_partyunit._party_rings == yao_party_rings
    assert yao_partyunit._bank_tax_paid == yao_bank_tax_paid
    assert yao_partyunit._bank_tax_diff == yao_bank_tax_diff
    assert yao_partyunit._bank_credit_score == yao_bank_credit_score
    assert yao_partyunit._bank_voice_rank == yao_bank_voice_rank
    assert yao_partyunit._bank_voice_hx_lowest_rank == yao_bank_voice_hx_lowest_rank
    assert yao_partyunit.depotlink_type == yao_depotlink_type

    # assert yao_obj_dict[yao_text]._partyrings == party_rings


def test_PartyLink_exists():
    # GIVEN
    bikers_handle = PartyHandle("Yao")

    # WHEN
    party_link_x = partylink_shop(handle=bikers_handle)

    # THEN
    assert party_link_x.handle == bikers_handle
    assert party_link_x.creditor_weight == 1.0
    assert party_link_x.debtor_weight == 1.0

    # WHEN
    bikers_creditor_weight = 3.0
    bikers_debtor_weight = 5.0
    party_link_x = partylink_shop(
        handle=bikers_handle,
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
    bikers_handle = PartyHandle("Yao")
    bikers_creditor_weight = 3.0
    partylinks_sum_creditor_weight = 60
    group_agenda_credit = 0.5
    group_agenda_goal_credit = 0.98

    bikers_debtor_weight = 13.0
    partylinks_sum_debtor_weight = 26.0
    group_agenda_debt = 0.9
    group_agenda_goal_debt = 0.5151

    party_link_x = partylink_shop(
        handle=bikers_handle,
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
    biker_handle = "maria"
    biker_party = partylink_shop(
        handle=biker_handle, _agenda_credit=0.04, _agenda_debt=0.7
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
    str_handle = "Yao"
    biker_handle = PartyHandle(str_handle)
    biker_party_link = partylink_shop(
        handle=biker_handle, creditor_weight=12, debtor_weight=19
    )
    print(f"{biker_party_link}")

    # WHEN
    biker_dict = biker_party_link.get_dict()

    # THEN
    assert biker_dict != None
    assert biker_dict == {
        "handle": biker_handle,
        "creditor_weight": 12,
        "debtor_weight": 19,
    }


def test_partylink_get_from_JSON_SimpleExampleWorks():
    # GIVEN
    yao_text = "Yao"
    yao_json_dict = {
        yao_text: {"handle": yao_text, "creditor_weight": 12, "debtor_weight": 19}
    }
    yao_json_text = x_get_json(dict_x=yao_json_dict)
    assert x_is_json(json_x=yao_json_text)

    # WHEN
    yao_obj_dict = partylinks_get_from_json(partylinks_json=yao_json_text)

    # THEN
    assert yao_obj_dict != None

    yao_handle = PartyHandle(yao_text)
    yao_partylink = partylink_shop(
        handle=yao_handle, creditor_weight=12, debtor_weight=19
    )
    partylinks_dict = {yao_partylink.handle: yao_partylink}
    assert yao_obj_dict == partylinks_dict


def test_partylink_meld_RaiseSameHandleException():
    # GIVEN
    todd_text = "Todd"
    todd_party = partylink_shop(handle=todd_text)
    mery_text = "Merry"
    mery_party = partylink_shop(handle=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_party.meld(mery_party)
    assert (
        str(excinfo.value)
        == f"Meld fail PartyLink='{todd_party.handle}' not the same as PartyLink='{mery_party.handle}"
    )


def test_partylink_meld_CorrectlySumsWeights():
    # GIVEN
    todd_text = "Todd"
    todd_party1 = partylink_shop(handle=todd_text, creditor_weight=12, debtor_weight=19)
    todd_party2 = partylink_shop(handle=todd_text, creditor_weight=33, debtor_weight=3)
    assert todd_party1.creditor_weight == 12
    assert todd_party1.debtor_weight == 19

    # WHEN
    todd_party1.meld(todd_party2)

    # THEN
    assert todd_party1.creditor_weight == 45
    assert todd_party1.debtor_weight == 22


def test_partyunit_meld_RaiseSameHandleException():
    # GIVEN
    todd_text = "Todd"
    todd_party = partyunit_shop(handle=todd_text)
    mery_text = "Merry"
    mery_party = partyunit_shop(handle=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_party.meld(mery_party)
    assert (
        str(excinfo.value)
        == f"Meld fail PartyUnit='{todd_party.handle}' not the same as PartyUnit='{mery_party.handle}"
    )


def test_partyunit_meld_CorrectlySumsWeights():
    # GIVEN
    todd_text = "Todd"
    todd_party1 = partyunit_shop(handle=todd_text, creditor_weight=7, debtor_weight=19)
    todd_party2 = partyunit_shop(handle=todd_text, creditor_weight=5, debtor_weight=3)
    assert todd_party1.creditor_weight == 7
    assert todd_party1.debtor_weight == 19

    # WHEN
    todd_party1.meld(todd_party2)

    # THEN
    assert todd_party1.creditor_weight == 12
    assert todd_party1.debtor_weight == 22
