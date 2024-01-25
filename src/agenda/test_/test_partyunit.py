from src.agenda.party import (
    PartyUnit,
    PartyID,
    partyunit_shop,
    partyunits_get_from_json,
    get_default_depotlink_type,
)
from src.tools.python import x_is_json, x_get_json
from pytest import raises as pytest_raises


def test_PartyUnit_exists():
    # GIVEN
    bob_party_id = "Bob"

    # WHEN
    bob_party = PartyUnit(party_id=bob_party_id)

    # THEN
    print(f"{bob_party_id}")
    assert bob_party != None
    assert bob_party.party_id != None
    assert bob_party.party_id == bob_party_id
    assert bob_party.creditor_weight is None
    assert bob_party.debtor_weight is None
    assert bob_party._agenda_credit is None
    assert bob_party._agenda_debt is None
    assert bob_party._agenda_intent_credit is None
    assert bob_party._agenda_intent_debt is None
    assert bob_party._creditor_live is None
    assert bob_party._debtor_live is None
    assert bob_party._treasury_tax_paid is None
    assert bob_party._treasury_tax_diff is None
    assert bob_party._treasury_credit_score is None
    assert bob_party._treasury_voice_rank is None
    assert bob_party._treasury_voice_hx_lowest_rank is None
    assert bob_party.depotlink_type is None
    assert bob_party._output_agenda_meld_order is None


def test_partyunit_shop_CorrectlySetsAttributes():
    # WHEN
    todd_text = "Todd"

    # WHEN
    todd_partyunit = partyunit_shop(party_id=todd_text)

    # THEN
    assert todd_partyunit._agenda_credit == 0
    assert todd_partyunit._agenda_debt == 0
    assert todd_partyunit._agenda_intent_credit == 0
    assert todd_partyunit._agenda_intent_debt == 0
    assert todd_partyunit._agenda_intent_ratio_credit == 0
    assert todd_partyunit._agenda_intent_ratio_debt == 0


def test_PartyUnit_set_output_agenda_meld_order_CorrectlySetsAttribute():
    # GIVEN
    bob_party_id = "Bob"
    bob_party = partyunit_shop(party_id=bob_party_id)
    assert bob_party._output_agenda_meld_order is None

    # WHEN
    x_output_agenda_meld_order = 5
    bob_party.set_output_agenda_meld_order(x_output_agenda_meld_order)

    # THEN
    assert bob_party._output_agenda_meld_order == x_output_agenda_meld_order


def test_PartyUnit_clear_output_agenda_meld_order_CorrectlySetsAttribute():
    # GIVEN
    bob_party_id = "Bob"
    bob_party = partyunit_shop(party_id=bob_party_id)
    x_output_agenda_meld_order = 5
    bob_party.set_output_agenda_meld_order(x_output_agenda_meld_order)
    assert bob_party._output_agenda_meld_order == x_output_agenda_meld_order

    # WHEN
    bob_party.clear_output_agenda_meld_order()

    # THEN
    assert bob_party._output_agenda_meld_order is None


def test_PartyUnit_set_depotlink_type_CorrectlySetsAttributeNoNulls():
    # GIVEN
    bob_party_id = "Bob"
    bob_party = partyunit_shop(party_id=bob_party_id)

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
    bob_party_id = "Bob"
    bob_party = partyunit_shop(
        party_id=bob_party_id, creditor_weight=45, debtor_weight=56
    )

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
    bob_party_id = "Bob"
    bob_party = partyunit_shop(party_id=bob_party_id)

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
    bob_party_id = "Bob"
    bob_party = partyunit_shop(
        party_id=bob_party_id, creditor_weight=45, debtor_weight=56
    )
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
    unacceptable_type_text = "unacceptable"
    bob_party_id = "Bob"
    bob_party = partyunit_shop(party_id=bob_party_id)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob_party.set_depotlink_type(depotlink_type=unacceptable_type_text)
    assert (
        str(excinfo.value)
        == f"PartyUnit '{bob_party.party_id}' cannot have type '{unacceptable_type_text}'."
    )


def test_get_default_depotlink_type_ReturnsCorrectObj():
    # GIVEN / WHEN
    assert get_default_depotlink_type() == "assignment"


def test_PartyUnit_reset_agenda_credit_debt_MethodWorkCorrectly():
    # GIVEN
    bob_party_id = "Bob"
    bob_party = partyunit_shop(party_id=bob_party_id)
    bob_party._agenda_credit = 0.27
    bob_party._agenda_debt = 0.37
    bob_party._agenda_intent_credit = 0.41
    bob_party._agenda_intent_debt = 0.51
    bob_party._agenda_intent_ratio_credit = 0.433
    bob_party._agenda_intent_ratio_debt = 0.533
    assert bob_party._agenda_credit == 0.27
    assert bob_party._agenda_debt == 0.37
    assert bob_party._agenda_intent_credit == 0.41
    assert bob_party._agenda_intent_debt == 0.51
    assert bob_party._agenda_intent_ratio_credit == 0.433
    assert bob_party._agenda_intent_ratio_debt == 0.533

    # WHEN
    bob_party.reset_agenda_credit_debt()

    # THEN
    assert bob_party._agenda_credit == 0
    assert bob_party._agenda_debt == 0
    assert bob_party._agenda_intent_credit == 0
    assert bob_party._agenda_intent_debt == 0
    assert bob_party._agenda_intent_ratio_credit == 0
    assert bob_party._agenda_intent_ratio_debt == 0


def test_PartyUnit_add_agenda_credit_debt_MethodWorkCorrectly():
    # GIVEN
    bob_party_id = "Bob"
    bob_party = partyunit_shop(party_id=bob_party_id)
    bob_party._agenda_credit = 0.4106
    bob_party._agenda_debt = 0.1106
    bob_party._agenda_intent_credit = 0.41
    bob_party._agenda_intent_debt = 0.51
    assert bob_party._agenda_intent_credit == 0.41
    assert bob_party._agenda_intent_debt == 0.51

    # WHEN
    bob_party.add_agenda_credit_debt(
        agenda_credit=0.33,
        agenda_debt=0.055,
        agenda_intent_credit=0.3,
        agenda_intent_debt=0.05,
    )

    # THEN
    assert bob_party._agenda_credit == 0.7406
    assert bob_party._agenda_debt == 0.1656
    assert bob_party._agenda_intent_credit == 0.71
    assert bob_party._agenda_intent_debt == 0.56


def test_PartyUnit_set_agenda_intent_ratio_credit_debt_MethodWorkCorrectly():
    # GIVEN
    bob_party_id = "Bob"
    bob_party = partyunit_shop(
        party_id=bob_party_id,
        creditor_weight=15,
        debtor_weight=7,
        _agenda_credit=0.4106,
        _agenda_debt=0.1106,
        _agenda_intent_credit=0.041,
        _agenda_intent_debt=0.051,
        _agenda_intent_ratio_credit=0,
        _agenda_intent_ratio_debt=0,
    )
    assert bob_party._agenda_intent_ratio_credit == 0
    assert bob_party._agenda_intent_ratio_debt == 0

    # WHEN
    bob_party.set_agenda_intent_ratio_credit_debt(
        agenda_intent_ratio_credit_sum=0.2,
        agenda_intent_ratio_debt_sum=0.5,
        agenda_partyunit_total_creditor_weight=20,
        agenda_partyunit_total_debtor_weight=14,
    )

    # THEN
    assert bob_party._agenda_intent_ratio_credit == 0.205
    assert bob_party._agenda_intent_ratio_debt == 0.102

    # WHEN
    bob_party.set_agenda_intent_ratio_credit_debt(
        agenda_intent_ratio_credit_sum=0,
        agenda_intent_ratio_debt_sum=0,
        agenda_partyunit_total_creditor_weight=20,
        agenda_partyunit_total_debtor_weight=14,
    )

    # THEN
    assert bob_party._agenda_intent_ratio_credit == 0.75
    assert bob_party._agenda_intent_ratio_debt == 0.5


def test_PartyUnit_set_treasurying_data_MethodWorkCorrectly():
    # GIVEN
    bob_party_id = "Bob"
    x_agenda_intent_ratio_credit = 0.077
    x_agenda_intent_ratio_debt = 0.066

    bob_party = partyunit_shop(
        party_id=bob_party_id,
        _agenda_intent_ratio_credit=x_agenda_intent_ratio_credit,
        _agenda_intent_ratio_debt=x_agenda_intent_ratio_debt,
    )
    assert bob_party._agenda_intent_ratio_credit == 0.077
    assert bob_party._agenda_intent_ratio_debt == 0.066
    assert bob_party._treasury_tax_paid is None
    assert bob_party._treasury_tax_diff is None
    assert bob_party._treasury_credit_score is None
    assert bob_party._treasury_voice_rank is None
    assert bob_party._treasury_voice_hx_lowest_rank is None

    # WHEN
    x_tax_paid = 0.2
    x_tax_diff = 0.123
    x_treasury_credit_score = 900
    x_treasury_voice_rank = 45
    bob_party.set_treasurying_data(
        tax_paid=x_tax_paid,
        tax_diff=x_tax_diff,
        credit_score=x_treasury_credit_score,
        voice_rank=x_treasury_voice_rank,
    )
    # THEN
    assert bob_party._agenda_intent_ratio_credit == x_agenda_intent_ratio_credit
    assert bob_party._agenda_intent_ratio_debt == x_agenda_intent_ratio_debt
    assert bob_party._treasury_tax_paid == x_tax_paid
    assert bob_party._treasury_tax_diff == x_tax_diff
    assert bob_party._treasury_credit_score == x_treasury_credit_score
    assert bob_party._treasury_voice_rank == x_treasury_voice_rank
    assert bob_party._treasury_voice_hx_lowest_rank == x_treasury_voice_rank


def test_PartyUnit_set_treasurying_data_CorrectlyDecreasesOrIgnores_treasury_voice_hx_lowest_rank():
    # GIVEN
    bob_party_id = "Bob"
    x_agenda_intent_ratio_credit = 0.077
    x_agenda_intent_ratio_debt = 0.066
    bob_party = partyunit_shop(
        party_id=bob_party_id,
        _agenda_intent_ratio_credit=x_agenda_intent_ratio_credit,
        _agenda_intent_ratio_debt=x_agenda_intent_ratio_debt,
    )
    x_tax_paid = 0.2
    x_tax_diff = 0.123
    x_treasury_credit_score = 900
    old_x_treasury_voice_rank = 45
    bob_party.set_treasurying_data(
        tax_paid=x_tax_paid,
        tax_diff=x_tax_diff,
        credit_score=x_treasury_credit_score,
        voice_rank=old_x_treasury_voice_rank,
    )
    assert bob_party._treasury_voice_hx_lowest_rank == old_x_treasury_voice_rank

    # WHEN
    new_x_treasury_voice_rank = 33
    bob_party.set_treasurying_data(
        tax_paid=x_tax_paid,
        tax_diff=x_tax_diff,
        credit_score=x_treasury_credit_score,
        voice_rank=new_x_treasury_voice_rank,
    )
    # THEN
    assert bob_party._treasury_voice_hx_lowest_rank == new_x_treasury_voice_rank

    # WHEN
    not_lower_x_treasury_voice_rank = 60
    bob_party.set_treasurying_data(
        tax_paid=x_tax_paid,
        tax_diff=x_tax_diff,
        credit_score=x_treasury_credit_score,
        voice_rank=not_lower_x_treasury_voice_rank,
    )
    # THEN
    assert bob_party._treasury_voice_hx_lowest_rank == new_x_treasury_voice_rank


def test_PartyUnit_clear_treasurying_data_MethodWorkCorrectly():
    # GIVEN
    bob_party_id = "Bob"
    bob_party = partyunit_shop(
        party_id=bob_party_id,
        _agenda_intent_ratio_credit=0.355,
        _agenda_intent_ratio_debt=0.066,
    )
    x_treasury_credit_score = 900
    x_treasury_voice_rank = 45
    bob_party.set_treasurying_data(
        tax_paid=0.399,
        tax_diff=0.044,
        credit_score=x_treasury_credit_score,
        voice_rank=x_treasury_voice_rank,
    )
    assert bob_party._treasury_tax_paid == 0.399
    assert bob_party._treasury_tax_diff == 0.044
    assert bob_party._treasury_credit_score == x_treasury_credit_score
    assert bob_party._treasury_voice_rank == x_treasury_voice_rank

    # WHEN
    bob_party.clear_treasurying_data()

    # THEN
    assert bob_party._treasury_tax_paid is None
    assert bob_party._treasury_tax_diff is None
    assert bob_party._treasury_credit_score is None
    assert bob_party._treasury_voice_rank is None


def test_PartyUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    glen_text = "glen"
    bob_text = "Bob"
    bob_treasury_tax_paid = 0.55
    bob_treasury_tax_diff = 0.66
    depotlink_type = "assignment"
    bob_party = partyunit_shop(
        party_id=bob_text,
        _treasury_tax_paid=bob_treasury_tax_paid,
        _treasury_tax_diff=bob_treasury_tax_diff,
        depotlink_type=depotlink_type,
    )
    bob_uid = 4321
    bob_party.uid = bob_uid

    bob_creditor_live = False
    bob_debtor_live = True
    bob_party._creditor_live = bob_creditor_live
    bob_party._debtor_live = bob_debtor_live

    bob_creditor_weight = 13
    bob_debtor_weight = 17
    bob_party.creditor_weight = bob_creditor_weight
    bob_party.debtor_weight = bob_debtor_weight

    bob_treasury_credit_score = 7000
    bob_treasury_voice_rank = 898
    bob_treasury_voice_hx_lowest_rank = 740
    bob_party._treasury_credit_score = bob_treasury_credit_score
    bob_party._treasury_voice_rank = bob_treasury_voice_rank
    bob_party._treasury_voice_hx_lowest_rank = bob_treasury_voice_hx_lowest_rank
    print(f"{bob_text}")

    # WHEN
    x_dict = bob_party.get_dict()

    # THEN
    print(f"{x_dict=}")
    assert x_dict != None
    assert x_dict == {
        "party_id": bob_text,
        "uid": bob_uid,
        "creditor_weight": bob_creditor_weight,
        "debtor_weight": bob_debtor_weight,
        "_creditor_live": bob_creditor_live,
        "_debtor_live": bob_debtor_live,
        "_treasury_tax_paid": bob_treasury_tax_paid,
        "_treasury_tax_diff": bob_treasury_tax_diff,
        "_treasury_credit_score": bob_treasury_credit_score,
        "_treasury_voice_rank": bob_treasury_voice_rank,
        "_treasury_voice_hx_lowest_rank": bob_treasury_voice_hx_lowest_rank,
        "depotlink_type": depotlink_type,
    }


def test_partyunits_get_from_json_SimpleExampleWorksWithIncompleteData():
    # GIVEN
    cersei_party_id = PartyID("Cersei")
    yao_text = "Yao"
    yao_uid = 239
    yao_creditor_weight = 13
    yao_debtor_weight = 17
    yao_creditor_live = False
    yao_debtor_live = True
    yao_treasury_tax_paid = 0.55
    yao_treasury_tax_diff = 0.66
    yao_depotlink_type = "assignment"
    yao_treasury_credit_score = 7000
    yao_treasury_voice_rank = 898
    yao_treasury_voice_hx_lowest_rank = 740
    yao_json_dict = {
        yao_text: {
            "party_id": yao_text,
            "uid": yao_uid,
            "creditor_weight": yao_creditor_weight,
            "debtor_weight": yao_debtor_weight,
            "_creditor_live": yao_creditor_live,
            "_debtor_live": yao_debtor_live,
            "_treasury_tax_paid": yao_treasury_tax_paid,
            "_treasury_tax_diff": yao_treasury_tax_diff,
            "_treasury_credit_score": yao_treasury_credit_score,
            "_treasury_voice_rank": yao_treasury_voice_rank,
            "_treasury_voice_hx_lowest_rank": yao_treasury_voice_hx_lowest_rank,
            "depotlink_type": yao_depotlink_type,
        }
    }
    yao_json_text = x_get_json(dict_x=yao_json_dict)
    assert x_is_json(json_x=yao_json_text)

    # WHEN
    yao_obj_dict = partyunits_get_from_json(partyunits_json=yao_json_text)

    # THEN
    assert yao_obj_dict[yao_text] != None
    yao_partyunit = yao_obj_dict[yao_text]

    assert yao_partyunit.party_id == yao_text
    assert yao_partyunit.uid == yao_uid
    assert yao_partyunit.creditor_weight == yao_creditor_weight
    assert yao_partyunit.debtor_weight == yao_debtor_weight
    assert yao_partyunit._creditor_live == yao_creditor_live
    assert yao_partyunit._debtor_live == yao_debtor_live
    assert yao_partyunit._treasury_tax_paid == yao_treasury_tax_paid
    assert yao_partyunit._treasury_tax_diff == yao_treasury_tax_diff
    assert yao_partyunit._treasury_credit_score == yao_treasury_credit_score
    assert yao_partyunit._treasury_voice_rank == yao_treasury_voice_rank
    assert (
        yao_partyunit._treasury_voice_hx_lowest_rank
        == yao_treasury_voice_hx_lowest_rank
    )
    assert yao_partyunit.depotlink_type == yao_depotlink_type


def test_PartyUnit_meld_RaiseSameparty_idException():
    # GIVEN
    todd_text = "Todd"
    todd_party = partyunit_shop(party_id=todd_text)
    mery_text = "Merry"
    mery_party = partyunit_shop(party_id=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_party.meld(mery_party)
    assert (
        str(excinfo.value)
        == f"Meld fail PartyUnit='{todd_party.party_id}' not the same as PartyUnit='{mery_party.party_id}"
    )


def test_PartyUnit_meld_CorrectlySumsWeights():
    # GIVEN
    todd_text = "Todd"
    todd_party1 = partyunit_shop(
        party_id=todd_text, creditor_weight=7, debtor_weight=19
    )
    todd_party2 = partyunit_shop(party_id=todd_text, creditor_weight=5, debtor_weight=3)
    assert todd_party1.creditor_weight == 7
    assert todd_party1.debtor_weight == 19

    # WHEN
    todd_party1.meld(todd_party2)

    # THEN
    assert todd_party1.creditor_weight == 12
    assert todd_party1.debtor_weight == 22
