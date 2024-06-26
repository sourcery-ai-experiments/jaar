from src._road.road import default_road_delimiter_if_none
from src._road.finance import default_pixel_if_none
from src._world.person import (
    PersonUnit,
    personunit_shop,
    personunits_get_from_json,
    personunit_get_from_dict,
    personunits_get_from_dict,
)
from src._instrument.python import x_is_json, get_json_from_dict
from pytest import raises as pytest_raises


def test_PersonUnit_exists():
    # GIVEN
    bob_text = "Bob"

    # WHEN
    bob_personunit = PersonUnit(bob_text)

    # THEN
    print(f"{bob_text}")
    assert bob_personunit != None
    assert bob_personunit.person_id != None
    assert bob_personunit.person_id == bob_text
    assert bob_personunit.credor_weight is None
    assert bob_personunit.debtor_weight is None
    # calculated fields
    assert bob_personunit._belieflinks is None
    assert bob_personunit._irrational_debtor_weight is None
    assert bob_personunit._inallocable_debtor_weight is None
    assert bob_personunit._world_cred is None
    assert bob_personunit._world_debt is None
    assert bob_personunit._world_agenda_cred is None
    assert bob_personunit._world_agenda_debt is None
    assert bob_personunit._credor_operational is None
    assert bob_personunit._debtor_operational is None
    assert bob_personunit._treasury_due_paid is None
    assert bob_personunit._treasury_due_diff is None
    assert bob_personunit._treasury_cred_score is None
    assert bob_personunit._treasury_voice_rank is None
    assert bob_personunit._treasury_voice_hx_lowest_rank is None
    assert bob_personunit._output_world_meld_order is None
    assert bob_personunit._road_delimiter is None
    assert bob_personunit._pixel is None


def test_PersonUnit_set_person_id_CorrectlySetsAttr():
    # GIVEN
    x_personunit = PersonUnit()

    # WHEN
    bob_text = "Bob"
    x_personunit.set_person_id(bob_text)

    # THEN
    assert x_personunit.person_id == bob_text


def test_PersonUnit_set_person_id_RaisesErrorIfParameterContains_road_delimiter():
    # GIVEN
    slash_text = "/"
    texas_text = f"Texas{slash_text}Arkansas"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        personunit_shop(person_id=texas_text, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{texas_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_personunit_shop_CorrectlySetsAttributes():
    # WHEN
    todd_text = "Todd"

    # WHEN
    todd_personunit = personunit_shop(person_id=todd_text)

    # THEN
    assert todd_personunit.person_id == todd_text
    assert todd_personunit.credor_weight == 1
    assert todd_personunit.debtor_weight == 1
    # calculated fields
    assert todd_personunit._belieflinks == {}
    assert todd_personunit._irrational_debtor_weight == 0
    assert todd_personunit._inallocable_debtor_weight == 0
    assert todd_personunit._world_cred == 0
    assert todd_personunit._world_debt == 0
    assert todd_personunit._world_agenda_cred == 0
    assert todd_personunit._world_agenda_debt == 0
    assert todd_personunit._world_agenda_ratio_cred == 0
    assert todd_personunit._world_agenda_ratio_debt == 0
    assert todd_personunit._road_delimiter == default_road_delimiter_if_none()
    assert todd_personunit._pixel == default_pixel_if_none()


def test_personunit_shop_CorrectlySetsAttributes_road_delimiter():
    # GIVEN
    slash_text = "/"

    # WHEN
    todd_personunit = personunit_shop("Todd", _road_delimiter=slash_text)

    # THEN
    assert todd_personunit._road_delimiter == slash_text


def test_personunit_shop_CorrectlySetsAttributes_pixel():
    # GIVEN
    pixel_float = 00.45

    # WHEN
    todd_personunit = personunit_shop("Todd", _pixel=pixel_float)

    # THEN
    assert todd_personunit._pixel == pixel_float


def test_PersonUnit_set_pixel_CorrectlySetsAttribute():
    # GIVEN
    bob_personunit = personunit_shop("Bob")
    assert bob_personunit._pixel == 1

    # WHEN
    x_pixel = 5
    bob_personunit.set_pixel(x_pixel)

    # THEN
    assert bob_personunit._pixel == x_pixel


def test_PersonUnit_set_output_world_meld_order_CorrectlySetsAttribute():
    # GIVEN
    bob_personunit = personunit_shop("Bob")
    assert bob_personunit._output_world_meld_order is None

    # WHEN
    x_output_world_meld_order = 5
    bob_personunit.set_output_world_meld_order(x_output_world_meld_order)

    # THEN
    assert bob_personunit._output_world_meld_order == x_output_world_meld_order


def test_PersonUnit_clear_output_world_meld_order_CorrectlySetsAttribute():
    # GIVEN
    bob_personunit = personunit_shop("Bob")
    x_output_world_meld_order = 5
    bob_personunit.set_output_world_meld_order(x_output_world_meld_order)
    assert bob_personunit._output_world_meld_order == x_output_world_meld_order

    # WHEN
    bob_personunit.clear_output_world_meld_order()

    # THEN
    assert bob_personunit._output_world_meld_order is None


def test_PersonUnit_set_credor_weight_CorrectlySetsAttribute():
    # GIVEN
    bob_personunit = personunit_shop("Bob")

    # WHEN
    x_credor_weight = 23
    bob_personunit.set_credor_weight(x_credor_weight)

    # THEN
    assert bob_personunit.credor_weight == x_credor_weight


def test_PersonUnit_set_credor_weight_RaisesErrorWhen_credor_weight_IsNotMultiple():
    # GIVEN
    bob_personunit = personunit_shop("Bob")
    x_credor_weight = 23
    bob_personunit.set_credor_weight(x_credor_weight)
    assert bob_personunit._pixel == 1
    assert bob_personunit.credor_weight == x_credor_weight

    # WHEN
    new_credor_weight = 13.5
    with pytest_raises(Exception) as excinfo:
        bob_personunit.set_credor_weight(new_credor_weight)
    assert (
        str(excinfo.value)
        == f"'{new_credor_weight}' is not divisible by pixel '{bob_personunit._pixel}'"
    )


def test_PersonUnit_set_debtor_weight_CorrectlySetsAttribute():
    # GIVEN
    bob_personunit = personunit_shop("Bob")

    # WHEN
    x_debtor_weight = 23
    bob_personunit.set_debtor_weight(x_debtor_weight)

    # THEN
    assert bob_personunit.debtor_weight == x_debtor_weight


def test_PersonUnit_set_debtor_weight_RaisesErrorWhen_debtor_weight_IsNotMultiple():
    # GIVEN
    bob_personunit = personunit_shop("Bob")
    x_debtor_weight = 23
    bob_personunit.set_debtor_weight(x_debtor_weight)
    assert bob_personunit._pixel == 1
    assert bob_personunit.debtor_weight == x_debtor_weight

    # WHEN
    new_debtor_weight = 13.5
    with pytest_raises(Exception) as excinfo:
        bob_personunit.set_debtor_weight(new_debtor_weight)
    assert (
        str(excinfo.value)
        == f"'{new_debtor_weight}' is not divisible by pixel '{bob_personunit._pixel}'"
    )


def test_PersonUnit_set_credor_debtor_weight_CorrectlySetsAttributeNoNulls():
    # GIVEN
    bob_personunit = personunit_shop("Bob")

    # WHEN
    bob_personunit.set_credor_debtor_weight(credor_weight=23, debtor_weight=34)

    # THEN
    assert bob_personunit.credor_weight == 23
    assert bob_personunit.debtor_weight == 34


def test_PersonUnit_set_credor_debtor_weight_CorrectlySetsAttributeWithNullsAndStartingValues():
    # GIVEN
    bob_personunit = personunit_shop("Bob", credor_weight=45, debtor_weight=56)

    # WHEN
    bob_personunit.set_credor_debtor_weight(credor_weight=None, debtor_weight=None)

    # THEN
    assert bob_personunit.credor_weight == 45
    assert bob_personunit.debtor_weight == 56


def test_PersonUnit_set_credor_debtor_weight_CorrectlySetsAttributeWithNullsAndNoStartingValues():
    # GIVEN
    bob_personunit = personunit_shop("Bob")

    # WHEN
    bob_personunit.set_credor_debtor_weight(credor_weight=None, debtor_weight=None)

    # THEN
    assert bob_personunit.credor_weight == 1
    assert bob_personunit.debtor_weight == 1


def test_PersonUnit_add_irrational_debtor_weight_SetsAttrCorrectly():
    # GIVEN
    bob_personunit = personunit_shop("Bob")
    assert bob_personunit._irrational_debtor_weight == 0

    # WHEN
    bob_int1 = 11
    bob_personunit.add_irrational_debtor_weight(bob_int1)

    # THEN
    assert bob_personunit._irrational_debtor_weight == bob_int1

    # WHEN
    bob_int2 = 22
    bob_personunit.add_irrational_debtor_weight(bob_int2)

    # THEN
    assert bob_personunit._irrational_debtor_weight == bob_int1 + bob_int2


def test_PersonUnit_add_inallocable_debtor_weight_SetsAttrCorrectly():
    # GIVEN
    bob_personunit = personunit_shop("Bob")
    assert bob_personunit._inallocable_debtor_weight == 0

    # WHEN
    bob_int1 = 11
    bob_personunit.add_inallocable_debtor_weight(bob_int1)

    # THEN
    assert bob_personunit._inallocable_debtor_weight == bob_int1

    # WHEN
    bob_int2 = 22
    bob_personunit.add_inallocable_debtor_weight(bob_int2)

    # THEN
    assert bob_personunit._inallocable_debtor_weight == bob_int1 + bob_int2


def test_PersonUnit_reset_listen_calculated_attrs_SetsAttrCorrectly():
    # GIVEN
    bob_personunit = personunit_shop("Bob")
    bob_int1 = 11
    bob_int2 = 22
    bob_personunit.add_irrational_debtor_weight(bob_int1)
    bob_personunit.add_inallocable_debtor_weight(bob_int2)
    assert bob_personunit._irrational_debtor_weight == bob_int1
    assert bob_personunit._inallocable_debtor_weight == bob_int2

    # WHEN
    bob_personunit.reset_listen_calculated_attrs()

    # THEN
    assert bob_personunit._irrational_debtor_weight == 0
    assert bob_personunit._inallocable_debtor_weight == 0


def test_PersonUnit_reset_world_cred_debt_SetsAttrCorrectly():
    # GIVEN
    bob_personunit = personunit_shop("Bob")
    bob_personunit._world_cred = 0.27
    bob_personunit._world_debt = 0.37
    bob_personunit._world_agenda_cred = 0.41
    bob_personunit._world_agenda_debt = 0.51
    bob_personunit._world_agenda_ratio_cred = 0.433
    bob_personunit._world_agenda_ratio_debt = 0.533
    assert bob_personunit._world_cred == 0.27
    assert bob_personunit._world_debt == 0.37
    assert bob_personunit._world_agenda_cred == 0.41
    assert bob_personunit._world_agenda_debt == 0.51
    assert bob_personunit._world_agenda_ratio_cred == 0.433
    assert bob_personunit._world_agenda_ratio_debt == 0.533

    # WHEN
    bob_personunit.reset_world_cred_debt()

    # THEN
    assert bob_personunit._world_cred == 0
    assert bob_personunit._world_debt == 0
    assert bob_personunit._world_agenda_cred == 0
    assert bob_personunit._world_agenda_debt == 0
    assert bob_personunit._world_agenda_ratio_cred == 0
    assert bob_personunit._world_agenda_ratio_debt == 0


def test_PersonUnit_add_world_cred_debt_SetsAttrCorrectly():
    # GIVEN
    bob_personunit = personunit_shop("Bob")
    bob_personunit._world_cred = 0.4106
    bob_personunit._world_debt = 0.1106
    bob_personunit._world_agenda_cred = 0.41
    bob_personunit._world_agenda_debt = 0.51
    assert bob_personunit._world_agenda_cred == 0.41
    assert bob_personunit._world_agenda_debt == 0.51

    # WHEN
    bob_personunit.add_world_cred_debt(
        world_cred=0.33,
        world_debt=0.055,
        world_agenda_cred=0.3,
        world_agenda_debt=0.05,
    )

    # THEN
    assert bob_personunit._world_cred == 0.7406
    assert bob_personunit._world_debt == 0.1656
    assert bob_personunit._world_agenda_cred == 0.71
    assert bob_personunit._world_agenda_debt == 0.56


def test_PersonUnit_set_world_agenda_ratio_cred_debt_SetsAttrCorrectly():
    # GIVEN
    bob_personunit = personunit_shop("Bob", credor_weight=15, debtor_weight=7)
    bob_personunit._world_cred = 0.4106
    bob_personunit._world_debt = 0.1106
    bob_personunit._world_agenda_cred = 0.041
    bob_personunit._world_agenda_debt = 0.051
    bob_personunit._world_agenda_ratio_cred = 0
    bob_personunit._world_agenda_ratio_debt = 0
    assert bob_personunit._world_agenda_ratio_cred == 0
    assert bob_personunit._world_agenda_ratio_debt == 0

    # WHEN
    bob_personunit.set_world_agenda_ratio_cred_debt(
        world_agenda_ratio_cred_sum=0.2,
        world_agenda_ratio_debt_sum=0.5,
        world_personunit_total_credor_weight=20,
        world_personunit_total_debtor_weight=14,
    )

    # THEN
    assert bob_personunit._world_agenda_ratio_cred == 0.205
    assert bob_personunit._world_agenda_ratio_debt == 0.102

    # WHEN
    bob_personunit.set_world_agenda_ratio_cred_debt(
        world_agenda_ratio_cred_sum=0,
        world_agenda_ratio_debt_sum=0,
        world_personunit_total_credor_weight=20,
        world_personunit_total_debtor_weight=14,
    )

    # THEN
    assert bob_personunit._world_agenda_ratio_cred == 0.75
    assert bob_personunit._world_agenda_ratio_debt == 0.5


def test_PersonUnit_set_treasury_attr_SetsAttrCorrectly():
    # GIVEN
    x_world_agenda_ratio_cred = 0.077
    x_world_agenda_ratio_debt = 0.066

    bob_personunit = personunit_shop("Bob")
    bob_personunit._world_agenda_ratio_cred = x_world_agenda_ratio_cred
    bob_personunit._world_agenda_ratio_debt = x_world_agenda_ratio_debt
    assert bob_personunit._world_agenda_ratio_cred == 0.077
    assert bob_personunit._world_agenda_ratio_debt == 0.066
    assert bob_personunit._treasury_due_paid is None
    assert bob_personunit._treasury_due_diff is None
    assert bob_personunit._treasury_cred_score is None
    assert bob_personunit._treasury_voice_rank is None
    assert bob_personunit._treasury_voice_hx_lowest_rank is None

    # WHEN
    x_treasury_due_paid = 0.2
    x_treasury_due_diff = 0.123
    x_treasury_cred_score = 900
    x_treasury_voice_rank = 45
    bob_personunit.set_treasury_attr(
        _treasury_due_paid=x_treasury_due_paid,
        _treasury_due_diff=x_treasury_due_diff,
        cred_score=x_treasury_cred_score,
        voice_rank=x_treasury_voice_rank,
    )
    # THEN
    assert bob_personunit._world_agenda_ratio_cred == x_world_agenda_ratio_cred
    assert bob_personunit._world_agenda_ratio_debt == x_world_agenda_ratio_debt
    assert bob_personunit._treasury_due_paid == x_treasury_due_paid
    assert bob_personunit._treasury_due_diff == x_treasury_due_diff
    assert bob_personunit._treasury_cred_score == x_treasury_cred_score
    assert bob_personunit._treasury_voice_rank == x_treasury_voice_rank
    assert bob_personunit._treasury_voice_hx_lowest_rank == x_treasury_voice_rank


def test_PersonUnit_set_treasury_attr_CorrectlyDecreasesOrIgnores_treasury_voice_hx_lowest_rank():
    # GIVEN
    x_world_agenda_ratio_cred = 0.077
    x_world_agenda_ratio_debt = 0.066
    bob_personunit = personunit_shop("Bob")
    bob_personunit._world_agenda_ratio_cred = x_world_agenda_ratio_cred
    bob_personunit._world_agenda_ratio_debt = x_world_agenda_ratio_debt
    x_treasury_due_paid = 0.2
    x_treasury_due_diff = 0.123
    x_treasury_cred_score = 900
    old_x_treasury_voice_rank = 45
    bob_personunit.set_treasury_attr(
        _treasury_due_paid=x_treasury_due_paid,
        _treasury_due_diff=x_treasury_due_diff,
        cred_score=x_treasury_cred_score,
        voice_rank=old_x_treasury_voice_rank,
    )
    assert bob_personunit._treasury_voice_hx_lowest_rank == old_x_treasury_voice_rank

    # WHEN
    new_x_treasury_voice_rank = 33
    bob_personunit.set_treasury_attr(
        _treasury_due_paid=x_treasury_due_paid,
        _treasury_due_diff=x_treasury_due_diff,
        cred_score=x_treasury_cred_score,
        voice_rank=new_x_treasury_voice_rank,
    )
    # THEN
    assert bob_personunit._treasury_voice_hx_lowest_rank == new_x_treasury_voice_rank

    # WHEN
    not_lower_x_treasury_voice_rank = 60
    bob_personunit.set_treasury_attr(
        _treasury_due_paid=x_treasury_due_paid,
        _treasury_due_diff=x_treasury_due_diff,
        cred_score=x_treasury_cred_score,
        voice_rank=not_lower_x_treasury_voice_rank,
    )
    # THEN
    assert bob_personunit._treasury_voice_hx_lowest_rank == new_x_treasury_voice_rank


def test_PersonUnit_clear_treasurying_data_SetsAttrCorrectly_Method():
    # GIVEN
    bob_personunit = personunit_shop("Bob")
    bob_personunit._world_agenda_ratio_cred = 0.355
    bob_personunit._world_agenda_ratio_debt = 0.066
    x_treasury_cred_score = 900
    x_treasury_voice_rank = 45
    bob_personunit.set_treasury_attr(
        _treasury_due_paid=0.399,
        _treasury_due_diff=0.044,
        cred_score=x_treasury_cred_score,
        voice_rank=x_treasury_voice_rank,
    )
    assert bob_personunit._treasury_due_paid == 0.399
    assert bob_personunit._treasury_due_diff == 0.044
    assert bob_personunit._treasury_cred_score == x_treasury_cred_score
    assert bob_personunit._treasury_voice_rank == x_treasury_voice_rank

    # WHEN
    bob_personunit.clear_treasurying_data()

    # THEN
    assert bob_personunit._treasury_due_paid is None
    assert bob_personunit._treasury_due_diff is None
    assert bob_personunit._treasury_cred_score is None
    assert bob_personunit._treasury_voice_rank is None
