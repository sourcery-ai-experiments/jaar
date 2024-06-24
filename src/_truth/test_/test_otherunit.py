from src._road.road import default_road_delimiter_if_none
from src._road.finance import default_pixel_if_none
from src._truth.other import (
    OtherUnit,
    otherunit_shop,
    otherunits_get_from_json,
    otherunit_get_from_dict,
    otherunits_get_from_dict,
)
from src._instrument.python import x_is_json, get_json_from_dict
from pytest import raises as pytest_raises


def test_OtherUnit_exists():
    # GIVEN
    bob_text = "Bob"

    # WHEN
    bob_otherunit = OtherUnit(bob_text)

    # THEN
    print(f"{bob_text}")
    assert bob_otherunit != None
    assert bob_otherunit.other_id != None
    assert bob_otherunit.other_id == bob_text
    assert bob_otherunit.credor_weight is None
    assert bob_otherunit.debtor_weight is None
    assert bob_otherunit._irrational_debtor_weight is None
    assert bob_otherunit._inallocable_debtor_weight is None
    assert bob_otherunit._truth_cred is None
    assert bob_otherunit._truth_debt is None
    assert bob_otherunit._truth_agenda_cred is None
    assert bob_otherunit._truth_agenda_debt is None
    assert bob_otherunit._credor_operational is None
    assert bob_otherunit._debtor_operational is None
    assert bob_otherunit._treasury_due_paid is None
    assert bob_otherunit._treasury_due_diff is None
    assert bob_otherunit._treasury_cred_score is None
    assert bob_otherunit._treasury_voice_rank is None
    assert bob_otherunit._treasury_voice_hx_lowest_rank is None
    assert bob_otherunit._output_truth_meld_order is None
    assert bob_otherunit._road_delimiter is None
    assert bob_otherunit._pixel is None


def test_OtherUnit_set_other_id_CorrectlySetsAttr():
    # GIVEN
    x_otherunit = OtherUnit()

    # WHEN
    bob_text = "Bob"
    x_otherunit.set_other_id(bob_text)

    # THEN
    assert x_otherunit.other_id == bob_text


def test_OtherUnit_set_other_id_RaisesErrorIfParameterContains_road_delimiter():
    # GIVEN
    slash_text = "/"
    texas_text = f"Texas{slash_text}Arkansas"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        otherunit_shop(other_id=texas_text, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{texas_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_otherunit_shop_CorrectlySetsAttributes():
    # WHEN
    todd_text = "Todd"

    # WHEN
    todd_otherunit = otherunit_shop(other_id=todd_text)

    # THEN
    assert todd_otherunit._irrational_debtor_weight == 0
    assert todd_otherunit._inallocable_debtor_weight == 0
    assert todd_otherunit._truth_cred == 0
    assert todd_otherunit._truth_debt == 0
    assert todd_otherunit._truth_agenda_cred == 0
    assert todd_otherunit._truth_agenda_debt == 0
    assert todd_otherunit._truth_agenda_ratio_cred == 0
    assert todd_otherunit._truth_agenda_ratio_debt == 0
    assert todd_otherunit._road_delimiter == default_road_delimiter_if_none()
    assert todd_otherunit._pixel == default_pixel_if_none()


def test_otherunit_shop_CorrectlySetsAttributes_road_delimiter():
    # GIVEN
    slash_text = "/"

    # WHEN
    todd_otherunit = otherunit_shop("Todd", _road_delimiter=slash_text)

    # THEN
    assert todd_otherunit._road_delimiter == slash_text


def test_otherunit_shop_CorrectlySetsAttributes_pixel():
    # GIVEN
    pixel_float = 00.45

    # WHEN
    todd_otherunit = otherunit_shop("Todd", _pixel=pixel_float)

    # THEN
    assert todd_otherunit._pixel == pixel_float


def test_OtherUnit_set_pixel_CorrectlySetsAttribute():
    # GIVEN
    bob_otherunit = otherunit_shop("Bob")
    assert bob_otherunit._pixel == 1

    # WHEN
    x_pixel = 5
    bob_otherunit.set_pixel(x_pixel)

    # THEN
    assert bob_otherunit._pixel == x_pixel


def test_OtherUnit_set_output_truth_meld_order_CorrectlySetsAttribute():
    # GIVEN
    bob_otherunit = otherunit_shop("Bob")
    assert bob_otherunit._output_truth_meld_order is None

    # WHEN
    x_output_truth_meld_order = 5
    bob_otherunit.set_output_truth_meld_order(x_output_truth_meld_order)

    # THEN
    assert bob_otherunit._output_truth_meld_order == x_output_truth_meld_order


def test_OtherUnit_clear_output_truth_meld_order_CorrectlySetsAttribute():
    # GIVEN
    bob_otherunit = otherunit_shop("Bob")
    x_output_truth_meld_order = 5
    bob_otherunit.set_output_truth_meld_order(x_output_truth_meld_order)
    assert bob_otherunit._output_truth_meld_order == x_output_truth_meld_order

    # WHEN
    bob_otherunit.clear_output_truth_meld_order()

    # THEN
    assert bob_otherunit._output_truth_meld_order is None


def test_OtherUnit_set_credor_weight_CorrectlySetsAttribute():
    # GIVEN
    bob_otherunit = otherunit_shop("Bob")

    # WHEN
    x_credor_weight = 23
    bob_otherunit.set_credor_weight(x_credor_weight)

    # THEN
    assert bob_otherunit.credor_weight == x_credor_weight


def test_OtherUnit_set_credor_weight_RaisesErrorWhen_credor_weight_IsNotMultiple():
    # GIVEN
    bob_otherunit = otherunit_shop("Bob")
    x_credor_weight = 23
    bob_otherunit.set_credor_weight(x_credor_weight)
    assert bob_otherunit._pixel == 1
    assert bob_otherunit.credor_weight == x_credor_weight

    # WHEN
    new_credor_weight = 13.5
    with pytest_raises(Exception) as excinfo:
        bob_otherunit.set_credor_weight(new_credor_weight)
    assert (
        str(excinfo.value)
        == f"'{new_credor_weight}' is not divisible by pixel '{bob_otherunit._pixel}'"
    )


def test_OtherUnit_set_debtor_weight_CorrectlySetsAttribute():
    # GIVEN
    bob_otherunit = otherunit_shop("Bob")

    # WHEN
    x_debtor_weight = 23
    bob_otherunit.set_debtor_weight(x_debtor_weight)

    # THEN
    assert bob_otherunit.debtor_weight == x_debtor_weight


def test_OtherUnit_set_debtor_weight_RaisesErrorWhen_debtor_weight_IsNotMultiple():
    # GIVEN
    bob_otherunit = otherunit_shop("Bob")
    x_debtor_weight = 23
    bob_otherunit.set_debtor_weight(x_debtor_weight)
    assert bob_otherunit._pixel == 1
    assert bob_otherunit.debtor_weight == x_debtor_weight

    # WHEN
    new_debtor_weight = 13.5
    with pytest_raises(Exception) as excinfo:
        bob_otherunit.set_debtor_weight(new_debtor_weight)
    assert (
        str(excinfo.value)
        == f"'{new_debtor_weight}' is not divisible by pixel '{bob_otherunit._pixel}'"
    )


def test_OtherUnit_set_credor_debtor_weight_CorrectlySetsAttributeNoNulls():
    # GIVEN
    bob_otherunit = otherunit_shop("Bob")

    # WHEN
    bob_otherunit.set_credor_debtor_weight(credor_weight=23, debtor_weight=34)

    # THEN
    assert bob_otherunit.credor_weight == 23
    assert bob_otherunit.debtor_weight == 34


def test_OtherUnit_set_credor_debtor_weight_CorrectlySetsAttributeWithNullsAndStartingValues():
    # GIVEN
    bob_otherunit = otherunit_shop("Bob", credor_weight=45, debtor_weight=56)

    # WHEN
    bob_otherunit.set_credor_debtor_weight(credor_weight=None, debtor_weight=None)

    # THEN
    assert bob_otherunit.credor_weight == 45
    assert bob_otherunit.debtor_weight == 56


def test_OtherUnit_set_credor_debtor_weight_CorrectlySetsAttributeWithNullsAndNoStartingValues():
    # GIVEN
    bob_otherunit = otherunit_shop("Bob")

    # WHEN
    bob_otherunit.set_credor_debtor_weight(credor_weight=None, debtor_weight=None)

    # THEN
    assert bob_otherunit.credor_weight == 1
    assert bob_otherunit.debtor_weight == 1


def test_OtherUnit_add_irrational_debtor_weight_SetsAttrCorrectly():
    # GIVEN
    bob_otherunit = otherunit_shop("Bob")
    assert bob_otherunit._irrational_debtor_weight == 0

    # WHEN
    bob_int1 = 11
    bob_otherunit.add_irrational_debtor_weight(bob_int1)

    # THEN
    assert bob_otherunit._irrational_debtor_weight == bob_int1

    # WHEN
    bob_int2 = 22
    bob_otherunit.add_irrational_debtor_weight(bob_int2)

    # THEN
    assert bob_otherunit._irrational_debtor_weight == bob_int1 + bob_int2


def test_OtherUnit_add_inallocable_debtor_weight_SetsAttrCorrectly():
    # GIVEN
    bob_otherunit = otherunit_shop("Bob")
    assert bob_otherunit._inallocable_debtor_weight == 0

    # WHEN
    bob_int1 = 11
    bob_otherunit.add_inallocable_debtor_weight(bob_int1)

    # THEN
    assert bob_otherunit._inallocable_debtor_weight == bob_int1

    # WHEN
    bob_int2 = 22
    bob_otherunit.add_inallocable_debtor_weight(bob_int2)

    # THEN
    assert bob_otherunit._inallocable_debtor_weight == bob_int1 + bob_int2


def test_OtherUnit_reset_listen_calculated_attrs_SetsAttrCorrectly():
    # GIVEN
    bob_otherunit = otherunit_shop("Bob")
    bob_int1 = 11
    bob_int2 = 22
    bob_otherunit.add_irrational_debtor_weight(bob_int1)
    bob_otherunit.add_inallocable_debtor_weight(bob_int2)
    assert bob_otherunit._irrational_debtor_weight == bob_int1
    assert bob_otherunit._inallocable_debtor_weight == bob_int2

    # WHEN
    bob_otherunit.reset_listen_calculated_attrs()

    # THEN
    assert bob_otherunit._irrational_debtor_weight == 0
    assert bob_otherunit._inallocable_debtor_weight == 0


def test_OtherUnit_reset_truth_cred_debt_SetsAttrCorrectly():
    # GIVEN
    bob_otherunit = otherunit_shop("Bob")
    bob_otherunit._truth_cred = 0.27
    bob_otherunit._truth_debt = 0.37
    bob_otherunit._truth_agenda_cred = 0.41
    bob_otherunit._truth_agenda_debt = 0.51
    bob_otherunit._truth_agenda_ratio_cred = 0.433
    bob_otherunit._truth_agenda_ratio_debt = 0.533
    assert bob_otherunit._truth_cred == 0.27
    assert bob_otherunit._truth_debt == 0.37
    assert bob_otherunit._truth_agenda_cred == 0.41
    assert bob_otherunit._truth_agenda_debt == 0.51
    assert bob_otherunit._truth_agenda_ratio_cred == 0.433
    assert bob_otherunit._truth_agenda_ratio_debt == 0.533

    # WHEN
    bob_otherunit.reset_truth_cred_debt()

    # THEN
    assert bob_otherunit._truth_cred == 0
    assert bob_otherunit._truth_debt == 0
    assert bob_otherunit._truth_agenda_cred == 0
    assert bob_otherunit._truth_agenda_debt == 0
    assert bob_otherunit._truth_agenda_ratio_cred == 0
    assert bob_otherunit._truth_agenda_ratio_debt == 0


def test_OtherUnit_add_truth_cred_debt_SetsAttrCorrectly():
    # GIVEN
    bob_otherunit = otherunit_shop("Bob")
    bob_otherunit._truth_cred = 0.4106
    bob_otherunit._truth_debt = 0.1106
    bob_otherunit._truth_agenda_cred = 0.41
    bob_otherunit._truth_agenda_debt = 0.51
    assert bob_otherunit._truth_agenda_cred == 0.41
    assert bob_otherunit._truth_agenda_debt == 0.51

    # WHEN
    bob_otherunit.add_truth_cred_debt(
        truth_cred=0.33,
        truth_debt=0.055,
        truth_agenda_cred=0.3,
        truth_agenda_debt=0.05,
    )

    # THEN
    assert bob_otherunit._truth_cred == 0.7406
    assert bob_otherunit._truth_debt == 0.1656
    assert bob_otherunit._truth_agenda_cred == 0.71
    assert bob_otherunit._truth_agenda_debt == 0.56


def test_OtherUnit_set_truth_agenda_ratio_cred_debt_SetsAttrCorrectly():
    # GIVEN
    bob_otherunit = otherunit_shop("Bob", credor_weight=15, debtor_weight=7)
    bob_otherunit._truth_cred = 0.4106
    bob_otherunit._truth_debt = 0.1106
    bob_otherunit._truth_agenda_cred = 0.041
    bob_otherunit._truth_agenda_debt = 0.051
    bob_otherunit._truth_agenda_ratio_cred = 0
    bob_otherunit._truth_agenda_ratio_debt = 0
    assert bob_otherunit._truth_agenda_ratio_cred == 0
    assert bob_otherunit._truth_agenda_ratio_debt == 0

    # WHEN
    bob_otherunit.set_truth_agenda_ratio_cred_debt(
        truth_agenda_ratio_cred_sum=0.2,
        truth_agenda_ratio_debt_sum=0.5,
        truth_otherunit_total_credor_weight=20,
        truth_otherunit_total_debtor_weight=14,
    )

    # THEN
    assert bob_otherunit._truth_agenda_ratio_cred == 0.205
    assert bob_otherunit._truth_agenda_ratio_debt == 0.102

    # WHEN
    bob_otherunit.set_truth_agenda_ratio_cred_debt(
        truth_agenda_ratio_cred_sum=0,
        truth_agenda_ratio_debt_sum=0,
        truth_otherunit_total_credor_weight=20,
        truth_otherunit_total_debtor_weight=14,
    )

    # THEN
    assert bob_otherunit._truth_agenda_ratio_cred == 0.75
    assert bob_otherunit._truth_agenda_ratio_debt == 0.5


def test_OtherUnit_set_treasury_attr_SetsAttrCorrectly():
    # GIVEN
    x_truth_agenda_ratio_cred = 0.077
    x_truth_agenda_ratio_debt = 0.066

    bob_otherunit = otherunit_shop("Bob")
    bob_otherunit._truth_agenda_ratio_cred = x_truth_agenda_ratio_cred
    bob_otherunit._truth_agenda_ratio_debt = x_truth_agenda_ratio_debt
    assert bob_otherunit._truth_agenda_ratio_cred == 0.077
    assert bob_otherunit._truth_agenda_ratio_debt == 0.066
    assert bob_otherunit._treasury_due_paid is None
    assert bob_otherunit._treasury_due_diff is None
    assert bob_otherunit._treasury_cred_score is None
    assert bob_otherunit._treasury_voice_rank is None
    assert bob_otherunit._treasury_voice_hx_lowest_rank is None

    # WHEN
    x_treasury_due_paid = 0.2
    x_treasury_due_diff = 0.123
    x_treasury_cred_score = 900
    x_treasury_voice_rank = 45
    bob_otherunit.set_treasury_attr(
        _treasury_due_paid=x_treasury_due_paid,
        _treasury_due_diff=x_treasury_due_diff,
        cred_score=x_treasury_cred_score,
        voice_rank=x_treasury_voice_rank,
    )
    # THEN
    assert bob_otherunit._truth_agenda_ratio_cred == x_truth_agenda_ratio_cred
    assert bob_otherunit._truth_agenda_ratio_debt == x_truth_agenda_ratio_debt
    assert bob_otherunit._treasury_due_paid == x_treasury_due_paid
    assert bob_otherunit._treasury_due_diff == x_treasury_due_diff
    assert bob_otherunit._treasury_cred_score == x_treasury_cred_score
    assert bob_otherunit._treasury_voice_rank == x_treasury_voice_rank
    assert bob_otherunit._treasury_voice_hx_lowest_rank == x_treasury_voice_rank


def test_OtherUnit_set_treasury_attr_CorrectlyDecreasesOrIgnores_treasury_voice_hx_lowest_rank():
    # GIVEN
    x_truth_agenda_ratio_cred = 0.077
    x_truth_agenda_ratio_debt = 0.066
    bob_otherunit = otherunit_shop("Bob")
    bob_otherunit._truth_agenda_ratio_cred = x_truth_agenda_ratio_cred
    bob_otherunit._truth_agenda_ratio_debt = x_truth_agenda_ratio_debt
    x_treasury_due_paid = 0.2
    x_treasury_due_diff = 0.123
    x_treasury_cred_score = 900
    old_x_treasury_voice_rank = 45
    bob_otherunit.set_treasury_attr(
        _treasury_due_paid=x_treasury_due_paid,
        _treasury_due_diff=x_treasury_due_diff,
        cred_score=x_treasury_cred_score,
        voice_rank=old_x_treasury_voice_rank,
    )
    assert bob_otherunit._treasury_voice_hx_lowest_rank == old_x_treasury_voice_rank

    # WHEN
    new_x_treasury_voice_rank = 33
    bob_otherunit.set_treasury_attr(
        _treasury_due_paid=x_treasury_due_paid,
        _treasury_due_diff=x_treasury_due_diff,
        cred_score=x_treasury_cred_score,
        voice_rank=new_x_treasury_voice_rank,
    )
    # THEN
    assert bob_otherunit._treasury_voice_hx_lowest_rank == new_x_treasury_voice_rank

    # WHEN
    not_lower_x_treasury_voice_rank = 60
    bob_otherunit.set_treasury_attr(
        _treasury_due_paid=x_treasury_due_paid,
        _treasury_due_diff=x_treasury_due_diff,
        cred_score=x_treasury_cred_score,
        voice_rank=not_lower_x_treasury_voice_rank,
    )
    # THEN
    assert bob_otherunit._treasury_voice_hx_lowest_rank == new_x_treasury_voice_rank


def test_OtherUnit_clear_treasurying_data_SetsAttrCorrectly_Method():
    # GIVEN
    bob_otherunit = otherunit_shop("Bob")
    bob_otherunit._truth_agenda_ratio_cred = 0.355
    bob_otherunit._truth_agenda_ratio_debt = 0.066
    x_treasury_cred_score = 900
    x_treasury_voice_rank = 45
    bob_otherunit.set_treasury_attr(
        _treasury_due_paid=0.399,
        _treasury_due_diff=0.044,
        cred_score=x_treasury_cred_score,
        voice_rank=x_treasury_voice_rank,
    )
    assert bob_otherunit._treasury_due_paid == 0.399
    assert bob_otherunit._treasury_due_diff == 0.044
    assert bob_otherunit._treasury_cred_score == x_treasury_cred_score
    assert bob_otherunit._treasury_voice_rank == x_treasury_voice_rank

    # WHEN
    bob_otherunit.clear_treasurying_data()

    # THEN
    assert bob_otherunit._treasury_due_paid is None
    assert bob_otherunit._treasury_due_diff is None
    assert bob_otherunit._treasury_cred_score is None
    assert bob_otherunit._treasury_voice_rank is None


def test_OtherUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    bob_text = "Bob"
    bob_treasury_due_paid = 0.55
    bob_treasury_due_diff = 0.66
    bob_otherunit = otherunit_shop(bob_text)
    bob_otherunit._treasury_due_paid = bob_treasury_due_paid
    bob_otherunit._treasury_due_diff = bob_treasury_due_diff
    bob_credor_operational = False
    bob_debtor_operational = True
    bob_otherunit._credor_operational = bob_credor_operational
    bob_otherunit._debtor_operational = bob_debtor_operational

    bob_credor_weight = 13
    bob_debtor_weight = 17
    bob_otherunit.set_credor_weight(bob_credor_weight)
    bob_otherunit.set_debtor_weight(bob_debtor_weight)

    bob_treasury_cred_score = 7000
    bob_treasury_voice_rank = 898
    bob_treasury_voice_hx_lowest_rank = 740
    bob_otherunit._treasury_cred_score = bob_treasury_cred_score
    bob_otherunit._treasury_voice_rank = bob_treasury_voice_rank
    bob_otherunit._treasury_voice_hx_lowest_rank = bob_treasury_voice_hx_lowest_rank
    print(f"{bob_text}")

    # WHEN
    x_dict = bob_otherunit.get_dict()

    # THEN
    print(f"{x_dict=}")
    assert x_dict != None
    assert x_dict == {
        "other_id": bob_text,
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


def test_OtherUnit_get_dict_ReturnsDictWithAllAttrDataForJSON():
    # GIVEN
    bob_text = "Bob"
    bob_treasury_due_paid = 0.55
    bob_treasury_due_diff = 0.66
    bob_otherunit = otherunit_shop(bob_text)
    bob_otherunit._treasury_due_paid = bob_treasury_due_paid
    bob_otherunit._treasury_due_diff = bob_treasury_due_diff
    bob_credor_operational = False
    bob_debtor_operational = True
    bob_otherunit._credor_operational = bob_credor_operational
    bob_otherunit._debtor_operational = bob_debtor_operational

    bob_credor_weight = 13
    bob_debtor_weight = 17
    bob_otherunit.set_credor_weight(bob_credor_weight)
    bob_otherunit.set_debtor_weight(bob_debtor_weight)
    bob_irrational_debtor_weight = 87
    bob_inallocable_debtor_weight = 97
    bob_otherunit.add_irrational_debtor_weight(bob_irrational_debtor_weight)
    bob_otherunit.add_inallocable_debtor_weight(bob_inallocable_debtor_weight)

    bob_treasury_cred_score = 7000
    bob_treasury_voice_rank = 898
    bob_treasury_voice_hx_lowest_rank = 740
    bob_otherunit._treasury_cred_score = bob_treasury_cred_score
    bob_otherunit._treasury_voice_rank = bob_treasury_voice_rank
    bob_otherunit._treasury_voice_hx_lowest_rank = bob_treasury_voice_hx_lowest_rank

    bob_truth_cred = 55
    bob_truth_debt = 47
    bob_truth_agenda_cred = 51
    bob_truth_agenda_debt = 67
    bob_truth_agenda_ratio_cred = 71
    bob_truth_agenda_ratio_debt = 73
    bob_output_truth_meld_order = 79

    bob_otherunit._truth_cred = bob_truth_cred
    bob_otherunit._truth_debt = bob_truth_debt
    bob_otherunit._truth_agenda_cred = bob_truth_agenda_cred
    bob_otherunit._truth_agenda_debt = bob_truth_agenda_debt
    bob_otherunit._truth_agenda_ratio_cred = bob_truth_agenda_ratio_cred
    bob_otherunit._truth_agenda_ratio_debt = bob_truth_agenda_ratio_debt
    bob_otherunit._output_truth_meld_order = bob_output_truth_meld_order

    print(f"{bob_text}")

    # WHEN
    x_dict = bob_otherunit.get_dict(all_attrs=True)

    # THEN
    print(f"{x_dict=}")
    assert x_dict != None
    assert x_dict == {
        "other_id": bob_text,
        "credor_weight": bob_credor_weight,
        "debtor_weight": bob_debtor_weight,
        "_irrational_debtor_weight": bob_irrational_debtor_weight,
        "_inallocable_debtor_weight": bob_inallocable_debtor_weight,
        "_truth_cred": bob_truth_cred,
        "_truth_debt": bob_truth_debt,
        "_truth_agenda_cred": bob_truth_agenda_cred,
        "_truth_agenda_debt": bob_truth_agenda_debt,
        "_truth_agenda_ratio_cred": bob_truth_agenda_ratio_cred,
        "_truth_agenda_ratio_debt": bob_truth_agenda_ratio_debt,
        "_credor_operational": bob_credor_operational,
        "_debtor_operational": bob_debtor_operational,
        "_output_truth_meld_order": bob_output_truth_meld_order,
        "_treasury_due_paid": bob_treasury_due_paid,
        "_treasury_due_diff": bob_treasury_due_diff,
        "_treasury_cred_score": bob_treasury_cred_score,
        "_treasury_voice_rank": bob_treasury_voice_rank,
        "_treasury_voice_hx_lowest_rank": bob_treasury_voice_hx_lowest_rank,
    }


def test_OtherUnit_get_dict_ReturnsDictWith_irrational_missing_job_ValuesIsZerp():
    # GIVEN
    bob_text = "Bob"
    bob_otherunit = otherunit_shop(bob_text)
    assert bob_otherunit._irrational_debtor_weight == 0
    assert bob_otherunit._inallocable_debtor_weight == 0

    # WHEN
    x_dict = bob_otherunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtor_weight = "_irrational_debtor_weight"
    x_inallocable_debtor_weight = "_inallocable_debtor_weight"
    assert x_dict.get(x_irrational_debtor_weight) is None
    assert x_dict.get(x_inallocable_debtor_weight) is None
    assert len(x_dict.keys()) == 17


def test_OtherUnit_get_dict_ReturnsDictWith_irrational_missing_job_ValuesIsNumber():
    # GIVEN
    bob_text = "Bob"
    bob_otherunit = otherunit_shop(bob_text)
    bob_irrational_debtor_weight = 87
    bob_inallocable_debtor_weight = 97
    bob_otherunit.add_irrational_debtor_weight(bob_irrational_debtor_weight)
    bob_otherunit.add_inallocable_debtor_weight(bob_inallocable_debtor_weight)

    # WHEN
    x_dict = bob_otherunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtor_weight = "_irrational_debtor_weight"
    x_inallocable_debtor_weight = "_inallocable_debtor_weight"
    assert x_dict.get(x_irrational_debtor_weight) == bob_irrational_debtor_weight
    assert x_dict.get(x_inallocable_debtor_weight) == bob_inallocable_debtor_weight
    assert len(x_dict.keys()) == 19


def test_OtherUnit_get_dict_ReturnsDictWith_irrational_missing_job_ValuesIsNone():
    # GIVEN
    bob_text = "Bob"
    bob_otherunit = otherunit_shop(bob_text)
    bob_otherunit._irrational_debtor_weight = None
    bob_otherunit._inallocable_debtor_weight = None

    # WHEN
    x_dict = bob_otherunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtor_weight = "_irrational_debtor_weight"
    x_inallocable_debtor_weight = "_inallocable_debtor_weight"
    assert x_dict.get(x_irrational_debtor_weight) is None
    assert x_dict.get(x_inallocable_debtor_weight) is None
    assert len(x_dict.keys()) == 17


def test_otherunit_get_from_dict_ReturnsCorrectObjWith_road_delimiter():
    # GIVEN
    yao_text = ",Yao"
    slash_text = "/"
    before_yao_otherunit = otherunit_shop(yao_text, _road_delimiter=slash_text)
    yao_dict = before_yao_otherunit.get_dict()

    # WHEN
    after_yao_otherunit = otherunit_get_from_dict(yao_dict, slash_text)

    # THEN
    assert before_yao_otherunit == after_yao_otherunit
    assert after_yao_otherunit._road_delimiter == slash_text


def test_otherunits_get_from_dict_ReturnsCorrectObjWith_road_delimiter():
    # GIVEN
    yao_text = ",Yao"
    slash_text = "/"
    yao_otherunit = otherunit_shop(yao_text, _road_delimiter=slash_text)
    yao_dict = yao_otherunit.get_dict()
    x_otherunits_dict = {yao_text: yao_dict}

    # WHEN
    x_otherunits_objs = otherunits_get_from_dict(x_otherunits_dict, slash_text)

    # THEN
    assert x_otherunits_objs.get(yao_text) == yao_otherunit
    assert x_otherunits_objs.get(yao_text)._road_delimiter == slash_text


def test_otherunits_get_from_json_ReturnsCorrectObj_SimpleExampleWithIncompleteData():
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
            "other_id": yao_text,
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
    yao_obj_dict = otherunits_get_from_json(otherunits_json=yao_json_text)

    # THEN
    assert yao_obj_dict[yao_text] != None
    yao_otherunit = yao_obj_dict[yao_text]

    assert yao_otherunit.other_id == yao_text
    assert yao_otherunit.credor_weight == yao_credor_weight
    assert yao_otherunit.debtor_weight == yao_debtor_weight
    assert yao_otherunit._irrational_debtor_weight == yao_irrational_debtor_weight
    assert yao_otherunit._inallocable_debtor_weight == yao_inallocable_debtor_weight
    assert yao_otherunit._credor_operational == yao_credor_operational
    assert yao_otherunit._debtor_operational == yao_debtor_operational
    assert yao_otherunit._treasury_due_paid == yao_treasury_due_paid
    assert yao_otherunit._treasury_due_diff == yao_treasury_due_diff
    assert yao_otherunit._treasury_cred_score == yao_treasury_cred_score
    assert yao_otherunit._treasury_voice_rank == yao_treasury_voice_rank
    assert (
        yao_otherunit._treasury_voice_hx_lowest_rank
        == yao_treasury_voice_hx_lowest_rank
    )


def test_OtherUnit_meld_RaiseEqualother_idException():
    # GIVEN
    todd_text = "Todd"
    todd_other = otherunit_shop(other_id=todd_text)
    mery_text = "Merry"
    mery_other = otherunit_shop(other_id=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_other.meld(mery_other)
    assert (
        str(excinfo.value)
        == f"Meld fail OtherUnit='{todd_other.other_id}' not the equal as OtherUnit='{mery_other.other_id}"
    )


def test_OtherUnit_meld_CorrectlySumsWeights():
    # GIVEN
    todd_text = "Todd"
    todd_other1 = otherunit_shop(todd_text, credor_weight=7, debtor_weight=19)
    todd_other2 = otherunit_shop(todd_text, credor_weight=5, debtor_weight=3)

    todd1_irrational_debtor_weight = 44
    todd2_irrational_debtor_weight = 33
    todd_other1.add_irrational_debtor_weight(todd1_irrational_debtor_weight)
    todd_other2.add_irrational_debtor_weight(todd2_irrational_debtor_weight)
    todd1_inallocable_debtor_weight = 11
    todd2_inallocable_debtor_weight = 22
    todd_other1.add_inallocable_debtor_weight(todd1_inallocable_debtor_weight)
    todd_other2.add_inallocable_debtor_weight(todd2_inallocable_debtor_weight)

    todd_other2
    assert todd_other1.credor_weight == 7
    assert todd_other1.debtor_weight == 19
    assert todd_other1._irrational_debtor_weight == todd1_irrational_debtor_weight
    assert todd_other1._inallocable_debtor_weight == todd1_inallocable_debtor_weight

    # WHEN
    todd_other1.meld(todd_other2)

    # THEN
    assert todd_other1.credor_weight == 12
    assert todd_other1.debtor_weight == 22
    assert todd_other1._irrational_debtor_weight != todd1_irrational_debtor_weight
    assert todd_other1._inallocable_debtor_weight != todd1_inallocable_debtor_weight

    irrational_sum = todd1_irrational_debtor_weight + todd2_irrational_debtor_weight
    missing_job_sum = todd1_inallocable_debtor_weight + todd2_inallocable_debtor_weight
    assert todd_other1._irrational_debtor_weight == irrational_sum
    assert todd_other1._inallocable_debtor_weight == missing_job_sum
