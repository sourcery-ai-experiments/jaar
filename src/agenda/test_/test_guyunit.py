from src._road.road import default_road_delimiter_if_none
from src._road.finance import default_planck_if_none
from src.agenda.guy import (
    GuyUnit,
    guyunit_shop,
    guyunits_get_from_json,
    guyunit_get_from_dict,
    guyunits_get_from_dict,
)
from src._instrument.python import x_is_json, get_json_from_dict
from pytest import raises as pytest_raises


def test_GuyUnit_exists():
    # GIVEN
    bob_text = "Bob"

    # WHEN
    bob_guyunit = GuyUnit(bob_text)

    # THEN
    print(f"{bob_text}")
    assert bob_guyunit != None
    assert bob_guyunit.guy_id != None
    assert bob_guyunit.guy_id == bob_text
    assert bob_guyunit.credor_weight is None
    assert bob_guyunit.debtor_weight is None
    assert bob_guyunit._irrational_debtor_weight is None
    assert bob_guyunit._inallocable_debtor_weight is None
    assert bob_guyunit._agenda_cred is None
    assert bob_guyunit._agenda_debt is None
    assert bob_guyunit._agenda_intent_cred is None
    assert bob_guyunit._agenda_intent_debt is None
    assert bob_guyunit._credor_operational is None
    assert bob_guyunit._debtor_operational is None
    assert bob_guyunit._treasury_due_paid is None
    assert bob_guyunit._treasury_due_diff is None
    assert bob_guyunit._treasury_cred_score is None
    assert bob_guyunit._treasury_voice_rank is None
    assert bob_guyunit._treasury_voice_hx_lowest_rank is None
    assert bob_guyunit._output_agenda_meld_order is None
    assert bob_guyunit._road_delimiter is None
    assert bob_guyunit._planck is None


def test_GuyUnit_set_guy_id_CorrectlySetsAttr():
    # GIVEN
    x_guyunit = GuyUnit()

    # WHEN
    bob_text = "Bob"
    x_guyunit.set_guy_id(bob_text)

    # THEN
    assert x_guyunit.guy_id == bob_text


def test_GuyUnit_set_guy_id_RaisesErrorIfParameterContains_road_delimiter():
    # GIVEN
    slash_text = "/"
    texas_text = f"Texas{slash_text}Arkansas"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        guyunit_shop(guy_id=texas_text, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{texas_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_guyunit_shop_CorrectlySetsAttributes():
    # WHEN
    todd_text = "Todd"

    # WHEN
    todd_guyunit = guyunit_shop(guy_id=todd_text)

    # THEN
    assert todd_guyunit._irrational_debtor_weight == 0
    assert todd_guyunit._inallocable_debtor_weight == 0
    assert todd_guyunit._agenda_cred == 0
    assert todd_guyunit._agenda_debt == 0
    assert todd_guyunit._agenda_intent_cred == 0
    assert todd_guyunit._agenda_intent_debt == 0
    assert todd_guyunit._agenda_intent_ratio_cred == 0
    assert todd_guyunit._agenda_intent_ratio_debt == 0
    assert todd_guyunit._road_delimiter == default_road_delimiter_if_none()
    assert todd_guyunit._planck == default_planck_if_none()


def test_guyunit_shop_CorrectlySetsAttributes_road_delimiter():
    # GIVEN
    slash_text = "/"

    # WHEN
    todd_guyunit = guyunit_shop("Todd", _road_delimiter=slash_text)

    # THEN
    assert todd_guyunit._road_delimiter == slash_text


def test_guyunit_shop_CorrectlySetsAttributes_planck():
    # GIVEN
    plank_float = 00.45

    # WHEN
    todd_guyunit = guyunit_shop("Todd", _planck=plank_float)

    # THEN
    assert todd_guyunit._planck == plank_float


def test_GuyUnit_set_planck_CorrectlySetsAttribute():
    # GIVEN
    bob_guyunit = guyunit_shop("Bob")
    assert bob_guyunit._planck == 1

    # WHEN
    x_planck = 5
    bob_guyunit.set_planck(x_planck)

    # THEN
    assert bob_guyunit._planck == x_planck


def test_GuyUnit_set_output_agenda_meld_order_CorrectlySetsAttribute():
    # GIVEN
    bob_guyunit = guyunit_shop("Bob")
    assert bob_guyunit._output_agenda_meld_order is None

    # WHEN
    x_output_agenda_meld_order = 5
    bob_guyunit.set_output_agenda_meld_order(x_output_agenda_meld_order)

    # THEN
    assert bob_guyunit._output_agenda_meld_order == x_output_agenda_meld_order


def test_GuyUnit_clear_output_agenda_meld_order_CorrectlySetsAttribute():
    # GIVEN
    bob_guyunit = guyunit_shop("Bob")
    x_output_agenda_meld_order = 5
    bob_guyunit.set_output_agenda_meld_order(x_output_agenda_meld_order)
    assert bob_guyunit._output_agenda_meld_order == x_output_agenda_meld_order

    # WHEN
    bob_guyunit.clear_output_agenda_meld_order()

    # THEN
    assert bob_guyunit._output_agenda_meld_order is None


def test_GuyUnit_set_credor_weight_CorrectlySetsAttribute():
    # GIVEN
    bob_guyunit = guyunit_shop("Bob")

    # WHEN
    x_credor_weight = 23
    bob_guyunit.set_credor_weight(x_credor_weight)

    # THEN
    assert bob_guyunit.credor_weight == x_credor_weight


def test_GuyUnit_set_credor_weight_RaisesErrorWhen_credor_weight_IsNotMultiple():
    # GIVEN
    bob_guyunit = guyunit_shop("Bob")
    x_credor_weight = 23
    bob_guyunit.set_credor_weight(x_credor_weight)
    assert bob_guyunit._planck == 1
    assert bob_guyunit.credor_weight == x_credor_weight

    # WHEN
    new_credor_weight = 13.5
    with pytest_raises(Exception) as excinfo:
        bob_guyunit.set_credor_weight(new_credor_weight)
    assert (
        str(excinfo.value)
        == f"'{new_credor_weight}' is not divisible by planck '{bob_guyunit._planck}'"
    )


def test_GuyUnit_set_debtor_weight_CorrectlySetsAttribute():
    # GIVEN
    bob_guyunit = guyunit_shop("Bob")

    # WHEN
    x_debtor_weight = 23
    bob_guyunit.set_debtor_weight(x_debtor_weight)

    # THEN
    assert bob_guyunit.debtor_weight == x_debtor_weight


def test_GuyUnit_set_debtor_weight_RaisesErrorWhen_debtor_weight_IsNotMultiple():
    # GIVEN
    bob_guyunit = guyunit_shop("Bob")
    x_debtor_weight = 23
    bob_guyunit.set_debtor_weight(x_debtor_weight)
    assert bob_guyunit._planck == 1
    assert bob_guyunit.debtor_weight == x_debtor_weight

    # WHEN
    new_debtor_weight = 13.5
    with pytest_raises(Exception) as excinfo:
        bob_guyunit.set_debtor_weight(new_debtor_weight)
    assert (
        str(excinfo.value)
        == f"'{new_debtor_weight}' is not divisible by planck '{bob_guyunit._planck}'"
    )


def test_GuyUnit_set_credor_debtor_weight_CorrectlySetsAttributeNoNulls():
    # GIVEN
    bob_guyunit = guyunit_shop("Bob")

    # WHEN
    bob_guyunit.set_credor_debtor_weight(credor_weight=23, debtor_weight=34)

    # THEN
    assert bob_guyunit.credor_weight == 23
    assert bob_guyunit.debtor_weight == 34


def test_GuyUnit_set_credor_debtor_weight_CorrectlySetsAttributeWithNullsAndStartingValues():
    # GIVEN
    bob_guyunit = guyunit_shop("Bob", credor_weight=45, debtor_weight=56)

    # WHEN
    bob_guyunit.set_credor_debtor_weight(credor_weight=None, debtor_weight=None)

    # THEN
    assert bob_guyunit.credor_weight == 45
    assert bob_guyunit.debtor_weight == 56


def test_GuyUnit_set_credor_debtor_weight_CorrectlySetsAttributeWithNullsAndNoStartingValues():
    # GIVEN
    bob_guyunit = guyunit_shop("Bob")

    # WHEN
    bob_guyunit.set_credor_debtor_weight(credor_weight=None, debtor_weight=None)

    # THEN
    assert bob_guyunit.credor_weight == 1
    assert bob_guyunit.debtor_weight == 1


def test_GuyUnit_add_irrational_debtor_weight_SetsAttrCorrectly():
    # GIVEN
    bob_guyunit = guyunit_shop("Bob")
    assert bob_guyunit._irrational_debtor_weight == 0

    # WHEN
    bob_int1 = 11
    bob_guyunit.add_irrational_debtor_weight(bob_int1)

    # THEN
    assert bob_guyunit._irrational_debtor_weight == bob_int1

    # WHEN
    bob_int2 = 22
    bob_guyunit.add_irrational_debtor_weight(bob_int2)

    # THEN
    assert bob_guyunit._irrational_debtor_weight == bob_int1 + bob_int2


def test_GuyUnit_add_inallocable_debtor_weight_SetsAttrCorrectly():
    # GIVEN
    bob_guyunit = guyunit_shop("Bob")
    assert bob_guyunit._inallocable_debtor_weight == 0

    # WHEN
    bob_int1 = 11
    bob_guyunit.add_inallocable_debtor_weight(bob_int1)

    # THEN
    assert bob_guyunit._inallocable_debtor_weight == bob_int1

    # WHEN
    bob_int2 = 22
    bob_guyunit.add_inallocable_debtor_weight(bob_int2)

    # THEN
    assert bob_guyunit._inallocable_debtor_weight == bob_int1 + bob_int2


def test_GuyUnit_reset_listen_calculated_attrs_SetsAttrCorrectly():
    # GIVEN
    bob_guyunit = guyunit_shop("Bob")
    bob_int1 = 11
    bob_int2 = 22
    bob_guyunit.add_irrational_debtor_weight(bob_int1)
    bob_guyunit.add_inallocable_debtor_weight(bob_int2)
    assert bob_guyunit._irrational_debtor_weight == bob_int1
    assert bob_guyunit._inallocable_debtor_weight == bob_int2

    # WHEN
    bob_guyunit.reset_listen_calculated_attrs()

    # THEN
    assert bob_guyunit._irrational_debtor_weight == 0
    assert bob_guyunit._inallocable_debtor_weight == 0


def test_GuyUnit_reset_agenda_cred_debt_SetsAttrCorrectly():
    # GIVEN
    bob_guyunit = guyunit_shop("Bob")
    bob_guyunit._agenda_cred = 0.27
    bob_guyunit._agenda_debt = 0.37
    bob_guyunit._agenda_intent_cred = 0.41
    bob_guyunit._agenda_intent_debt = 0.51
    bob_guyunit._agenda_intent_ratio_cred = 0.433
    bob_guyunit._agenda_intent_ratio_debt = 0.533
    assert bob_guyunit._agenda_cred == 0.27
    assert bob_guyunit._agenda_debt == 0.37
    assert bob_guyunit._agenda_intent_cred == 0.41
    assert bob_guyunit._agenda_intent_debt == 0.51
    assert bob_guyunit._agenda_intent_ratio_cred == 0.433
    assert bob_guyunit._agenda_intent_ratio_debt == 0.533

    # WHEN
    bob_guyunit.reset_agenda_cred_debt()

    # THEN
    assert bob_guyunit._agenda_cred == 0
    assert bob_guyunit._agenda_debt == 0
    assert bob_guyunit._agenda_intent_cred == 0
    assert bob_guyunit._agenda_intent_debt == 0
    assert bob_guyunit._agenda_intent_ratio_cred == 0
    assert bob_guyunit._agenda_intent_ratio_debt == 0


def test_GuyUnit_add_agenda_cred_debt_SetsAttrCorrectly():
    # GIVEN
    bob_guyunit = guyunit_shop("Bob")
    bob_guyunit._agenda_cred = 0.4106
    bob_guyunit._agenda_debt = 0.1106
    bob_guyunit._agenda_intent_cred = 0.41
    bob_guyunit._agenda_intent_debt = 0.51
    assert bob_guyunit._agenda_intent_cred == 0.41
    assert bob_guyunit._agenda_intent_debt == 0.51

    # WHEN
    bob_guyunit.add_agenda_cred_debt(
        agenda_cred=0.33,
        agenda_debt=0.055,
        agenda_intent_cred=0.3,
        agenda_intent_debt=0.05,
    )

    # THEN
    assert bob_guyunit._agenda_cred == 0.7406
    assert bob_guyunit._agenda_debt == 0.1656
    assert bob_guyunit._agenda_intent_cred == 0.71
    assert bob_guyunit._agenda_intent_debt == 0.56


def test_GuyUnit_set_agenda_intent_ratio_cred_debt_SetsAttrCorrectly():
    # GIVEN
    bob_guyunit = guyunit_shop("Bob", credor_weight=15, debtor_weight=7)
    bob_guyunit._agenda_cred = 0.4106
    bob_guyunit._agenda_debt = 0.1106
    bob_guyunit._agenda_intent_cred = 0.041
    bob_guyunit._agenda_intent_debt = 0.051
    bob_guyunit._agenda_intent_ratio_cred = 0
    bob_guyunit._agenda_intent_ratio_debt = 0
    assert bob_guyunit._agenda_intent_ratio_cred == 0
    assert bob_guyunit._agenda_intent_ratio_debt == 0

    # WHEN
    bob_guyunit.set_agenda_intent_ratio_cred_debt(
        agenda_intent_ratio_cred_sum=0.2,
        agenda_intent_ratio_debt_sum=0.5,
        agenda_guyunit_total_credor_weight=20,
        agenda_guyunit_total_debtor_weight=14,
    )

    # THEN
    assert bob_guyunit._agenda_intent_ratio_cred == 0.205
    assert bob_guyunit._agenda_intent_ratio_debt == 0.102

    # WHEN
    bob_guyunit.set_agenda_intent_ratio_cred_debt(
        agenda_intent_ratio_cred_sum=0,
        agenda_intent_ratio_debt_sum=0,
        agenda_guyunit_total_credor_weight=20,
        agenda_guyunit_total_debtor_weight=14,
    )

    # THEN
    assert bob_guyunit._agenda_intent_ratio_cred == 0.75
    assert bob_guyunit._agenda_intent_ratio_debt == 0.5


def test_GuyUnit_set_treasury_attr_SetsAttrCorrectly():
    # GIVEN
    x_agenda_intent_ratio_cred = 0.077
    x_agenda_intent_ratio_debt = 0.066

    bob_guyunit = guyunit_shop("Bob")
    bob_guyunit._agenda_intent_ratio_cred = x_agenda_intent_ratio_cred
    bob_guyunit._agenda_intent_ratio_debt = x_agenda_intent_ratio_debt
    assert bob_guyunit._agenda_intent_ratio_cred == 0.077
    assert bob_guyunit._agenda_intent_ratio_debt == 0.066
    assert bob_guyunit._treasury_due_paid is None
    assert bob_guyunit._treasury_due_diff is None
    assert bob_guyunit._treasury_cred_score is None
    assert bob_guyunit._treasury_voice_rank is None
    assert bob_guyunit._treasury_voice_hx_lowest_rank is None

    # WHEN
    x_due_paid = 0.2
    x_due_diff = 0.123
    x_treasury_cred_score = 900
    x_treasury_voice_rank = 45
    bob_guyunit.set_treasury_attr(
        due_paid=x_due_paid,
        due_diff=x_due_diff,
        cred_score=x_treasury_cred_score,
        voice_rank=x_treasury_voice_rank,
    )
    # THEN
    assert bob_guyunit._agenda_intent_ratio_cred == x_agenda_intent_ratio_cred
    assert bob_guyunit._agenda_intent_ratio_debt == x_agenda_intent_ratio_debt
    assert bob_guyunit._treasury_due_paid == x_due_paid
    assert bob_guyunit._treasury_due_diff == x_due_diff
    assert bob_guyunit._treasury_cred_score == x_treasury_cred_score
    assert bob_guyunit._treasury_voice_rank == x_treasury_voice_rank
    assert bob_guyunit._treasury_voice_hx_lowest_rank == x_treasury_voice_rank


def test_GuyUnit_set_treasury_attr_CorrectlyDecreasesOrIgnores_treasury_voice_hx_lowest_rank():
    # GIVEN
    x_agenda_intent_ratio_cred = 0.077
    x_agenda_intent_ratio_debt = 0.066
    bob_guyunit = guyunit_shop("Bob")
    bob_guyunit._agenda_intent_ratio_cred = x_agenda_intent_ratio_cred
    bob_guyunit._agenda_intent_ratio_debt = x_agenda_intent_ratio_debt
    x_due_paid = 0.2
    x_due_diff = 0.123
    x_treasury_cred_score = 900
    old_x_treasury_voice_rank = 45
    bob_guyunit.set_treasury_attr(
        due_paid=x_due_paid,
        due_diff=x_due_diff,
        cred_score=x_treasury_cred_score,
        voice_rank=old_x_treasury_voice_rank,
    )
    assert bob_guyunit._treasury_voice_hx_lowest_rank == old_x_treasury_voice_rank

    # WHEN
    new_x_treasury_voice_rank = 33
    bob_guyunit.set_treasury_attr(
        due_paid=x_due_paid,
        due_diff=x_due_diff,
        cred_score=x_treasury_cred_score,
        voice_rank=new_x_treasury_voice_rank,
    )
    # THEN
    assert bob_guyunit._treasury_voice_hx_lowest_rank == new_x_treasury_voice_rank

    # WHEN
    not_lower_x_treasury_voice_rank = 60
    bob_guyunit.set_treasury_attr(
        due_paid=x_due_paid,
        due_diff=x_due_diff,
        cred_score=x_treasury_cred_score,
        voice_rank=not_lower_x_treasury_voice_rank,
    )
    # THEN
    assert bob_guyunit._treasury_voice_hx_lowest_rank == new_x_treasury_voice_rank


def test_GuyUnit_clear_treasurying_data_SetsAttrCorrectly_Method():
    # GIVEN
    bob_guyunit = guyunit_shop("Bob")
    bob_guyunit._agenda_intent_ratio_cred = 0.355
    bob_guyunit._agenda_intent_ratio_debt = 0.066
    x_treasury_cred_score = 900
    x_treasury_voice_rank = 45
    bob_guyunit.set_treasury_attr(
        due_paid=0.399,
        due_diff=0.044,
        cred_score=x_treasury_cred_score,
        voice_rank=x_treasury_voice_rank,
    )
    assert bob_guyunit._treasury_due_paid == 0.399
    assert bob_guyunit._treasury_due_diff == 0.044
    assert bob_guyunit._treasury_cred_score == x_treasury_cred_score
    assert bob_guyunit._treasury_voice_rank == x_treasury_voice_rank

    # WHEN
    bob_guyunit.clear_treasurying_data()

    # THEN
    assert bob_guyunit._treasury_due_paid is None
    assert bob_guyunit._treasury_due_diff is None
    assert bob_guyunit._treasury_cred_score is None
    assert bob_guyunit._treasury_voice_rank is None


def test_GuyUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    bob_text = "Bob"
    bob_treasury_due_paid = 0.55
    bob_treasury_due_diff = 0.66
    bob_guyunit = guyunit_shop(bob_text)
    bob_guyunit._treasury_due_paid = bob_treasury_due_paid
    bob_guyunit._treasury_due_diff = bob_treasury_due_diff
    bob_credor_operational = False
    bob_debtor_operational = True
    bob_guyunit._credor_operational = bob_credor_operational
    bob_guyunit._debtor_operational = bob_debtor_operational

    bob_credor_weight = 13
    bob_debtor_weight = 17
    bob_guyunit.set_credor_weight(bob_credor_weight)
    bob_guyunit.set_debtor_weight(bob_debtor_weight)

    bob_treasury_cred_score = 7000
    bob_treasury_voice_rank = 898
    bob_treasury_voice_hx_lowest_rank = 740
    bob_guyunit._treasury_cred_score = bob_treasury_cred_score
    bob_guyunit._treasury_voice_rank = bob_treasury_voice_rank
    bob_guyunit._treasury_voice_hx_lowest_rank = bob_treasury_voice_hx_lowest_rank
    print(f"{bob_text}")

    # WHEN
    x_dict = bob_guyunit.get_dict()

    # THEN
    print(f"{x_dict=}")
    assert x_dict != None
    assert x_dict == {
        "guy_id": bob_text,
        "credor_weight": bob_credor_weight,
        "debtor_weight": bob_debtor_weight,
        "_credor_operational": bob_credor_operational,
        "_debtor_operational": bob_debtor_operational,
        "_treasury_due_paid": bob_treasury_due_paid,
        "_treasury_due_diff": bob_treasury_due_diff,
        "_treasury_cred_score": bob_treasury_cred_score,
        "_treasury_voice_rank": bob_treasury_voice_rank,
        "_treasury_voice_hx_lowest_rank": bob_treasury_voice_hx_lowest_rank,
    }


def test_GuyUnit_get_dict_ReturnsDictWithAllAttrDataForJSON():
    # GIVEN
    bob_text = "Bob"
    bob_treasury_due_paid = 0.55
    bob_treasury_due_diff = 0.66
    bob_guyunit = guyunit_shop(bob_text)
    bob_guyunit._treasury_due_paid = bob_treasury_due_paid
    bob_guyunit._treasury_due_diff = bob_treasury_due_diff
    bob_credor_operational = False
    bob_debtor_operational = True
    bob_guyunit._credor_operational = bob_credor_operational
    bob_guyunit._debtor_operational = bob_debtor_operational

    bob_credor_weight = 13
    bob_debtor_weight = 17
    bob_guyunit.set_credor_weight(bob_credor_weight)
    bob_guyunit.set_debtor_weight(bob_debtor_weight)
    bob_irrational_debtor_weight = 87
    bob_inallocable_debtor_weight = 97
    bob_guyunit.add_irrational_debtor_weight(bob_irrational_debtor_weight)
    bob_guyunit.add_inallocable_debtor_weight(bob_inallocable_debtor_weight)

    bob_treasury_cred_score = 7000
    bob_treasury_voice_rank = 898
    bob_treasury_voice_hx_lowest_rank = 740
    bob_guyunit._treasury_cred_score = bob_treasury_cred_score
    bob_guyunit._treasury_voice_rank = bob_treasury_voice_rank
    bob_guyunit._treasury_voice_hx_lowest_rank = bob_treasury_voice_hx_lowest_rank

    bob_agenda_cred = 55
    bob_agenda_debt = 47
    bob_agenda_intent_cred = 51
    bob_agenda_intent_debt = 67
    bob_agenda_intent_ratio_cred = 71
    bob_agenda_intent_ratio_debt = 73
    bob_output_agenda_meld_order = 79

    bob_guyunit._agenda_cred = bob_agenda_cred
    bob_guyunit._agenda_debt = bob_agenda_debt
    bob_guyunit._agenda_intent_cred = bob_agenda_intent_cred
    bob_guyunit._agenda_intent_debt = bob_agenda_intent_debt
    bob_guyunit._agenda_intent_ratio_cred = bob_agenda_intent_ratio_cred
    bob_guyunit._agenda_intent_ratio_debt = bob_agenda_intent_ratio_debt
    bob_guyunit._output_agenda_meld_order = bob_output_agenda_meld_order

    print(f"{bob_text}")

    # WHEN
    x_dict = bob_guyunit.get_dict(all_attrs=True)

    # THEN
    print(f"{x_dict=}")
    assert x_dict != None
    assert x_dict == {
        "guy_id": bob_text,
        "credor_weight": bob_credor_weight,
        "debtor_weight": bob_debtor_weight,
        "_irrational_debtor_weight": bob_irrational_debtor_weight,
        "_inallocable_debtor_weight": bob_inallocable_debtor_weight,
        "_agenda_cred": bob_agenda_cred,
        "_agenda_debt": bob_agenda_debt,
        "_agenda_intent_cred": bob_agenda_intent_cred,
        "_agenda_intent_debt": bob_agenda_intent_debt,
        "_agenda_intent_ratio_cred": bob_agenda_intent_ratio_cred,
        "_agenda_intent_ratio_debt": bob_agenda_intent_ratio_debt,
        "_credor_operational": bob_credor_operational,
        "_debtor_operational": bob_debtor_operational,
        "_output_agenda_meld_order": bob_output_agenda_meld_order,
        "_treasury_due_paid": bob_treasury_due_paid,
        "_treasury_due_diff": bob_treasury_due_diff,
        "_treasury_cred_score": bob_treasury_cred_score,
        "_treasury_voice_rank": bob_treasury_voice_rank,
        "_treasury_voice_hx_lowest_rank": bob_treasury_voice_hx_lowest_rank,
    }


def test_GuyUnit_get_dict_ReturnsDictWith_irrational_missing_job_ValuesIsZerp():
    # GIVEN
    bob_text = "Bob"
    bob_guyunit = guyunit_shop(bob_text)
    assert bob_guyunit._irrational_debtor_weight == 0
    assert bob_guyunit._inallocable_debtor_weight == 0

    # WHEN
    x_dict = bob_guyunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtor_weight = "_irrational_debtor_weight"
    x_inallocable_debtor_weight = "_inallocable_debtor_weight"
    assert x_dict.get(x_irrational_debtor_weight) is None
    assert x_dict.get(x_inallocable_debtor_weight) is None
    assert len(x_dict.keys()) == 17


def test_GuyUnit_get_dict_ReturnsDictWith_irrational_missing_job_ValuesIsNumber():
    # GIVEN
    bob_text = "Bob"
    bob_guyunit = guyunit_shop(bob_text)
    bob_irrational_debtor_weight = 87
    bob_inallocable_debtor_weight = 97
    bob_guyunit.add_irrational_debtor_weight(bob_irrational_debtor_weight)
    bob_guyunit.add_inallocable_debtor_weight(bob_inallocable_debtor_weight)

    # WHEN
    x_dict = bob_guyunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtor_weight = "_irrational_debtor_weight"
    x_inallocable_debtor_weight = "_inallocable_debtor_weight"
    assert x_dict.get(x_irrational_debtor_weight) == bob_irrational_debtor_weight
    assert x_dict.get(x_inallocable_debtor_weight) == bob_inallocable_debtor_weight
    assert len(x_dict.keys()) == 19


def test_GuyUnit_get_dict_ReturnsDictWith_irrational_missing_job_ValuesIsNone():
    # GIVEN
    bob_text = "Bob"
    bob_guyunit = guyunit_shop(bob_text)
    bob_guyunit._irrational_debtor_weight = None
    bob_guyunit._inallocable_debtor_weight = None

    # WHEN
    x_dict = bob_guyunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtor_weight = "_irrational_debtor_weight"
    x_inallocable_debtor_weight = "_inallocable_debtor_weight"
    assert x_dict.get(x_irrational_debtor_weight) is None
    assert x_dict.get(x_inallocable_debtor_weight) is None
    assert len(x_dict.keys()) == 17


def test_guyunit_get_from_dict_ReturnsCorrectObjWith_road_delimiter():
    # GIVEN
    yao_text = ",Yao"
    slash_text = "/"
    before_yao_guyunit = guyunit_shop(yao_text, _road_delimiter=slash_text)
    yao_dict = before_yao_guyunit.get_dict()

    # WHEN
    after_yao_guyunit = guyunit_get_from_dict(yao_dict, slash_text)

    # THEN
    assert before_yao_guyunit == after_yao_guyunit
    assert after_yao_guyunit._road_delimiter == slash_text


def test_guyunits_get_from_dict_ReturnsCorrectObjWith_road_delimiter():
    # GIVEN
    yao_text = ",Yao"
    slash_text = "/"
    yao_guyunit = guyunit_shop(yao_text, _road_delimiter=slash_text)
    yao_dict = yao_guyunit.get_dict()
    x_guyunits_dict = {yao_text: yao_dict}

    # WHEN
    x_guyunits_objs = guyunits_get_from_dict(x_guyunits_dict, slash_text)

    # THEN
    assert x_guyunits_objs.get(yao_text) == yao_guyunit
    assert x_guyunits_objs.get(yao_text)._road_delimiter == slash_text


def test_guyunits_get_from_json_ReturnsCorrectObj_SimpleExampleWithIncompleteData():
    # GIVEN
    yao_text = "Yao"
    yao_credor_weight = 13
    yao_debtor_weight = 17
    yao_irrational_debtor_weight = 87
    yao_inallocable_debtor_weight = 97
    yao_credor_operational = False
    yao_debtor_operational = True
    yao_treasury_due_paid = 0.55
    yao_treasury_due_diff = 0.66
    yao_treasury_cred_score = 7000
    yao_treasury_voice_rank = 898
    yao_treasury_voice_hx_lowest_rank = 740
    yao_json_dict = {
        yao_text: {
            "guy_id": yao_text,
            "credor_weight": yao_credor_weight,
            "debtor_weight": yao_debtor_weight,
            "_irrational_debtor_weight": yao_irrational_debtor_weight,
            "_inallocable_debtor_weight": yao_inallocable_debtor_weight,
            "_credor_operational": yao_credor_operational,
            "_debtor_operational": yao_debtor_operational,
            "_treasury_due_paid": yao_treasury_due_paid,
            "_treasury_due_diff": yao_treasury_due_diff,
            "_treasury_cred_score": yao_treasury_cred_score,
            "_treasury_voice_rank": yao_treasury_voice_rank,
            "_treasury_voice_hx_lowest_rank": yao_treasury_voice_hx_lowest_rank,
        }
    }
    yao_json_text = get_json_from_dict(dict_x=yao_json_dict)
    assert x_is_json(json_x=yao_json_text)

    # WHEN
    yao_obj_dict = guyunits_get_from_json(guyunits_json=yao_json_text)

    # THEN
    assert yao_obj_dict[yao_text] != None
    yao_guyunit = yao_obj_dict[yao_text]

    assert yao_guyunit.guy_id == yao_text
    assert yao_guyunit.credor_weight == yao_credor_weight
    assert yao_guyunit.debtor_weight == yao_debtor_weight
    assert yao_guyunit._irrational_debtor_weight == yao_irrational_debtor_weight
    assert yao_guyunit._inallocable_debtor_weight == yao_inallocable_debtor_weight
    assert yao_guyunit._credor_operational == yao_credor_operational
    assert yao_guyunit._debtor_operational == yao_debtor_operational
    assert yao_guyunit._treasury_due_paid == yao_treasury_due_paid
    assert yao_guyunit._treasury_due_diff == yao_treasury_due_diff
    assert yao_guyunit._treasury_cred_score == yao_treasury_cred_score
    assert yao_guyunit._treasury_voice_rank == yao_treasury_voice_rank
    assert (
        yao_guyunit._treasury_voice_hx_lowest_rank == yao_treasury_voice_hx_lowest_rank
    )


def test_GuyUnit_meld_RaiseSameguy_idException():
    # GIVEN
    todd_text = "Todd"
    todd_guy = guyunit_shop(guy_id=todd_text)
    mery_text = "Merry"
    mery_guy = guyunit_shop(guy_id=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_guy.meld(mery_guy)
    assert (
        str(excinfo.value)
        == f"Meld fail GuyUnit='{todd_guy.guy_id}' not the same as GuyUnit='{mery_guy.guy_id}"
    )


def test_GuyUnit_meld_CorrectlySumsWeights():
    # GIVEN
    todd_text = "Todd"
    todd_guy1 = guyunit_shop(todd_text, credor_weight=7, debtor_weight=19)
    todd_guy2 = guyunit_shop(todd_text, credor_weight=5, debtor_weight=3)

    todd1_irrational_debtor_weight = 44
    todd2_irrational_debtor_weight = 33
    todd_guy1.add_irrational_debtor_weight(todd1_irrational_debtor_weight)
    todd_guy2.add_irrational_debtor_weight(todd2_irrational_debtor_weight)
    todd1_inallocable_debtor_weight = 11
    todd2_inallocable_debtor_weight = 22
    todd_guy1.add_inallocable_debtor_weight(todd1_inallocable_debtor_weight)
    todd_guy2.add_inallocable_debtor_weight(todd2_inallocable_debtor_weight)

    todd_guy2
    assert todd_guy1.credor_weight == 7
    assert todd_guy1.debtor_weight == 19
    assert todd_guy1._irrational_debtor_weight == todd1_irrational_debtor_weight
    assert todd_guy1._inallocable_debtor_weight == todd1_inallocable_debtor_weight

    # WHEN
    todd_guy1.meld(todd_guy2)

    # THEN
    assert todd_guy1.credor_weight == 12
    assert todd_guy1.debtor_weight == 22
    assert todd_guy1._irrational_debtor_weight != todd1_irrational_debtor_weight
    assert todd_guy1._inallocable_debtor_weight != todd1_inallocable_debtor_weight

    irrational_sum = todd1_irrational_debtor_weight + todd2_irrational_debtor_weight
    missing_job_sum = todd1_inallocable_debtor_weight + todd2_inallocable_debtor_weight
    assert todd_guy1._irrational_debtor_weight == irrational_sum
    assert todd_guy1._inallocable_debtor_weight == missing_job_sum
