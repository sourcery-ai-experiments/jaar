from src._world.belieflink import belieflink_shop
from src._world.char import (
    charunit_shop,
    charunits_get_from_json,
    charunit_get_from_dict,
    charunits_get_from_dict,
)
from src._instrument.python import x_is_json, get_json_from_dict
from pytest import raises as pytest_raises


def test_CharUnit_get_belieflinks_dict_ReturnObj():
    # GIVEN
    sue_text = "Sue"
    sue_credor_weight = 11
    sue_debtor_weight = 13
    run_text = ",Run"
    run_credor_weight = 17
    run_debtor_weight = 23
    sue_belieflink = belieflink_shop(sue_text, sue_credor_weight, sue_debtor_weight)
    run_belieflink = belieflink_shop(run_text, run_credor_weight, run_debtor_weight)
    sue_charunit = charunit_shop(sue_text)
    sue_charunit.set_belieflink(sue_belieflink)
    sue_charunit.set_belieflink(run_belieflink)

    # WHEN
    sue_belieflinks_dict = sue_charunit.get_belieflinks_dict()

    # THEN
    assert sue_belieflinks_dict.get(sue_text) != None
    assert sue_belieflinks_dict.get(run_text) != None
    sue_belieflink_dict = sue_belieflinks_dict.get(sue_text)
    run_belieflink_dict = sue_belieflinks_dict.get(run_text)
    assert sue_belieflink_dict == {
        "belief_id": sue_text,
        "credor_weight": sue_credor_weight,
        "debtor_weight": sue_debtor_weight,
    }
    assert run_belieflink_dict == {
        "belief_id": run_text,
        "credor_weight": run_credor_weight,
        "debtor_weight": run_debtor_weight,
    }


def test_CharUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    bob_text = "Bob"
    bob_treasury_due_paid = 0.55
    bob_treasury_due_diff = 0.66
    bob_charunit = charunit_shop(bob_text)
    bob_charunit._treasury_due_paid = bob_treasury_due_paid
    bob_charunit._treasury_due_diff = bob_treasury_due_diff
    bob_credor_operational = False
    bob_debtor_operational = True
    bob_charunit._credor_operational = bob_credor_operational
    bob_charunit._debtor_operational = bob_debtor_operational

    bob_credor_weight = 13
    bob_debtor_weight = 17
    bob_charunit.set_credor_weight(bob_credor_weight)
    bob_charunit.set_debtor_weight(bob_debtor_weight)

    bob_treasury_cred_score = 7000
    bob_treasury_voice_rank = 898
    bob_treasury_voice_hx_lowest_rank = 740
    bob_charunit._treasury_cred_score = bob_treasury_cred_score
    bob_charunit._treasury_voice_rank = bob_treasury_voice_rank
    bob_charunit._treasury_voice_hx_lowest_rank = bob_treasury_voice_hx_lowest_rank
    print(f"{bob_text}")

    bob_charunit.set_belieflink(belieflink_shop(bob_text))
    run_text = "Run"
    bob_charunit.set_belieflink(belieflink_shop(run_text))

    # WHEN
    x_dict = bob_charunit.get_dict()

    # THEN
    bl_dict = x_dict.get("_belieflinks")
    print(f"{bl_dict=}")
    assert x_dict != None
    assert x_dict == {
        "char_id": bob_text,
        "credor_weight": bob_credor_weight,
        "debtor_weight": bob_debtor_weight,
        "_belieflinks": {
            bob_text: {"belief_id": bob_text, "credor_weight": 1, "debtor_weight": 1},
            run_text: {"belief_id": run_text, "credor_weight": 1, "debtor_weight": 1},
        },
        "_credor_operational": bob_credor_operational,
        "_debtor_operational": bob_debtor_operational,
        "_treasury_due_paid": bob_treasury_due_paid,
        "_treasury_due_diff": bob_treasury_due_diff,
        "_treasury_cred_score": bob_treasury_cred_score,
        "_treasury_voice_rank": bob_treasury_voice_rank,
        "_treasury_voice_hx_lowest_rank": bob_treasury_voice_hx_lowest_rank,
    }


def test_CharUnit_get_dict_ReturnsDictWithAllAttrDataForJSON():
    # GIVEN
    bob_text = "Bob"
    bob_treasury_due_paid = 0.55
    bob_treasury_due_diff = 0.66
    bob_charunit = charunit_shop(bob_text)
    bob_charunit._treasury_due_paid = bob_treasury_due_paid
    bob_charunit._treasury_due_diff = bob_treasury_due_diff
    bob_credor_operational = False
    bob_debtor_operational = True
    bob_charunit._credor_operational = bob_credor_operational
    bob_charunit._debtor_operational = bob_debtor_operational

    bob_credor_weight = 13
    bob_debtor_weight = 17
    bob_charunit.set_credor_weight(bob_credor_weight)
    bob_charunit.set_debtor_weight(bob_debtor_weight)
    bob_irrational_debtor_weight = 87
    bob_inallocable_debtor_weight = 97
    bob_charunit.add_irrational_debtor_weight(bob_irrational_debtor_weight)
    bob_charunit.add_inallocable_debtor_weight(bob_inallocable_debtor_weight)

    bob_treasury_cred_score = 7000
    bob_treasury_voice_rank = 898
    bob_treasury_voice_hx_lowest_rank = 740
    bob_charunit._treasury_cred_score = bob_treasury_cred_score
    bob_charunit._treasury_voice_rank = bob_treasury_voice_rank
    bob_charunit._treasury_voice_hx_lowest_rank = bob_treasury_voice_hx_lowest_rank

    bob_world_cred = 55
    bob_world_debt = 47
    bob_world_agenda_cred = 51
    bob_world_agenda_debt = 67
    bob_world_agenda_ratio_cred = 71
    bob_world_agenda_ratio_debt = 73
    bob_output_world_meld_order = 79

    bob_charunit._world_cred = bob_world_cred
    bob_charunit._world_debt = bob_world_debt
    bob_charunit._world_agenda_cred = bob_world_agenda_cred
    bob_charunit._world_agenda_debt = bob_world_agenda_debt
    bob_charunit._world_agenda_ratio_cred = bob_world_agenda_ratio_cred
    bob_charunit._world_agenda_ratio_debt = bob_world_agenda_ratio_debt
    bob_charunit._output_world_meld_order = bob_output_world_meld_order

    bob_charunit.set_belieflink(belieflink_shop(bob_text))
    run_text = "Run"
    bob_charunit.set_belieflink(belieflink_shop(run_text))

    print(f"{bob_text}")

    # WHEN
    x_dict = bob_charunit.get_dict(all_attrs=True)

    # THEN
    print(f"{x_dict=}")
    assert x_dict != None
    assert x_dict == {
        "char_id": bob_text,
        "credor_weight": bob_credor_weight,
        "debtor_weight": bob_debtor_weight,
        "_belieflinks": bob_charunit.get_belieflinks_dict(),
        "_irrational_debtor_weight": bob_irrational_debtor_weight,
        "_inallocable_debtor_weight": bob_inallocable_debtor_weight,
        "_world_cred": bob_world_cred,
        "_world_debt": bob_world_debt,
        "_world_agenda_cred": bob_world_agenda_cred,
        "_world_agenda_debt": bob_world_agenda_debt,
        "_world_agenda_ratio_cred": bob_world_agenda_ratio_cred,
        "_world_agenda_ratio_debt": bob_world_agenda_ratio_debt,
        "_credor_operational": bob_credor_operational,
        "_debtor_operational": bob_debtor_operational,
        "_output_world_meld_order": bob_output_world_meld_order,
        "_treasury_due_paid": bob_treasury_due_paid,
        "_treasury_due_diff": bob_treasury_due_diff,
        "_treasury_cred_score": bob_treasury_cred_score,
        "_treasury_voice_rank": bob_treasury_voice_rank,
        "_treasury_voice_hx_lowest_rank": bob_treasury_voice_hx_lowest_rank,
    }


def test_CharUnit_get_dict_ReturnsDictWith_irrational_missing_job_ValuesIsZerp():
    # GIVEN
    bob_text = "Bob"
    bob_charunit = charunit_shop(bob_text)
    assert bob_charunit._irrational_debtor_weight == 0
    assert bob_charunit._inallocable_debtor_weight == 0

    # WHEN
    x_dict = bob_charunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtor_weight = "_irrational_debtor_weight"
    x_inallocable_debtor_weight = "_inallocable_debtor_weight"
    assert x_dict.get(x_irrational_debtor_weight) is None
    assert x_dict.get(x_inallocable_debtor_weight) is None
    assert len(x_dict.keys()) == 18


def test_CharUnit_get_dict_ReturnsDictWith_irrational_missing_job_ValuesIsNumber():
    # GIVEN
    bob_text = "Bob"
    bob_charunit = charunit_shop(bob_text)
    bob_irrational_debtor_weight = 87
    bob_inallocable_debtor_weight = 97
    bob_charunit.add_irrational_debtor_weight(bob_irrational_debtor_weight)
    bob_charunit.add_inallocable_debtor_weight(bob_inallocable_debtor_weight)

    # WHEN
    x_dict = bob_charunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtor_weight = "_irrational_debtor_weight"
    x_inallocable_debtor_weight = "_inallocable_debtor_weight"
    assert x_dict.get(x_irrational_debtor_weight) == bob_irrational_debtor_weight
    assert x_dict.get(x_inallocable_debtor_weight) == bob_inallocable_debtor_weight
    assert len(x_dict.keys()) == 20


def test_CharUnit_get_dict_ReturnsDictWith_irrational_missing_job_ValuesIsNone():
    # GIVEN
    bob_text = "Bob"
    bob_charunit = charunit_shop(bob_text)
    bob_charunit._irrational_debtor_weight = None
    bob_charunit._inallocable_debtor_weight = None

    # WHEN
    x_dict = bob_charunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtor_weight = "_irrational_debtor_weight"
    x_inallocable_debtor_weight = "_inallocable_debtor_weight"
    assert x_dict.get(x_irrational_debtor_weight) is None
    assert x_dict.get(x_inallocable_debtor_weight) is None
    assert len(x_dict.keys()) == 18


def test_charunit_get_from_dict_ReturnsCorrectObjWith_road_delimiter():
    # GIVEN
    yao_text = ",Yao"
    slash_text = "/"
    before_yao_charunit = charunit_shop(yao_text, _road_delimiter=slash_text)
    yao_dict = before_yao_charunit.get_dict()

    # WHEN
    after_yao_charunit = charunit_get_from_dict(yao_dict, slash_text)

    # THEN
    assert before_yao_charunit == after_yao_charunit
    assert after_yao_charunit._road_delimiter == slash_text


def test_charunit_get_from_dict_Returns_belieflinks():
    # GIVEN
    yao_text = ",Yao"
    slash_text = "/"
    before_yao_charunit = charunit_shop(yao_text, _road_delimiter=slash_text)
    bob_text = "Bob"
    zia_text = "Zia"
    before_yao_charunit.set_belieflink(belieflink_shop(bob_text))
    before_yao_charunit.set_belieflink(belieflink_shop(zia_text))
    yao_dict = before_yao_charunit.get_dict()

    # WHEN
    after_yao_charunit = charunit_get_from_dict(yao_dict, slash_text)

    # THEN
    assert before_yao_charunit == after_yao_charunit
    assert after_yao_charunit._road_delimiter == slash_text


def test_charunits_get_from_dict_ReturnsCorrectObjWith_road_delimiter():
    # GIVEN
    yao_text = ",Yao"
    slash_text = "/"
    yao_charunit = charunit_shop(yao_text, _road_delimiter=slash_text)
    yao_dict = yao_charunit.get_dict()
    x_charunits_dict = {yao_text: yao_dict}

    # WHEN
    x_charunits_objs = charunits_get_from_dict(x_charunits_dict, slash_text)

    # THEN
    assert x_charunits_objs.get(yao_text) == yao_charunit
    assert x_charunits_objs.get(yao_text)._road_delimiter == slash_text


def test_charunits_get_from_json_ReturnsCorrectObj_SimpleExampleWithIncompleteData():
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
            "char_id": yao_text,
            "credor_weight": yao_credor_weight,
            "debtor_weight": yao_debtor_weight,
            "_belieflinks": {},
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
    yao_obj_dict = charunits_get_from_json(charunits_json=yao_json_text)

    # THEN
    assert yao_obj_dict[yao_text] != None
    yao_charunit = yao_obj_dict[yao_text]

    assert yao_charunit.char_id == yao_text
    assert yao_charunit.credor_weight == yao_credor_weight
    assert yao_charunit.debtor_weight == yao_debtor_weight
    assert yao_charunit._irrational_debtor_weight == yao_irrational_debtor_weight
    assert yao_charunit._inallocable_debtor_weight == yao_inallocable_debtor_weight
    assert yao_charunit._credor_operational == yao_credor_operational
    assert yao_charunit._debtor_operational == yao_debtor_operational
    assert yao_charunit._treasury_due_paid == yao_treasury_due_paid
    assert yao_charunit._treasury_due_diff == yao_treasury_due_diff
    assert yao_charunit._treasury_cred_score == yao_treasury_cred_score
    assert yao_charunit._treasury_voice_rank == yao_treasury_voice_rank
    assert (
        yao_charunit._treasury_voice_hx_lowest_rank == yao_treasury_voice_hx_lowest_rank
    )


def test_CharUnit_meld_RaiseEqualchar_idException():
    # GIVEN
    todd_text = "Todd"
    todd_char = charunit_shop(char_id=todd_text)
    mery_text = "Merry"
    mery_char = charunit_shop(char_id=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_char.meld(mery_char)
    assert (
        str(excinfo.value)
        == f"Meld fail CharUnit='{todd_char.char_id}' not the equal as CharUnit='{mery_char.char_id}"
    )


def test_CharUnit_meld_CorrectlySumsWeights():
    # GIVEN
    todd_text = "Todd"
    todd_char1 = charunit_shop(todd_text, credor_weight=7, debtor_weight=19)
    todd_char2 = charunit_shop(todd_text, credor_weight=5, debtor_weight=3)

    todd1_irrational_debtor_weight = 44
    todd2_irrational_debtor_weight = 33
    todd_char1.add_irrational_debtor_weight(todd1_irrational_debtor_weight)
    todd_char2.add_irrational_debtor_weight(todd2_irrational_debtor_weight)
    todd1_inallocable_debtor_weight = 11
    todd2_inallocable_debtor_weight = 22
    todd_char1.add_inallocable_debtor_weight(todd1_inallocable_debtor_weight)
    todd_char2.add_inallocable_debtor_weight(todd2_inallocable_debtor_weight)

    todd_char2
    assert todd_char1.credor_weight == 7
    assert todd_char1.debtor_weight == 19
    assert todd_char1._irrational_debtor_weight == todd1_irrational_debtor_weight
    assert todd_char1._inallocable_debtor_weight == todd1_inallocable_debtor_weight

    # WHEN
    todd_char1.meld(todd_char2)

    # THEN
    assert todd_char1.credor_weight == 12
    assert todd_char1.debtor_weight == 22
    assert todd_char1._irrational_debtor_weight != todd1_irrational_debtor_weight
    assert todd_char1._inallocable_debtor_weight != todd1_inallocable_debtor_weight

    irrational_sum = todd1_irrational_debtor_weight + todd2_irrational_debtor_weight
    missing_job_sum = todd1_inallocable_debtor_weight + todd2_inallocable_debtor_weight
    assert todd_char1._irrational_debtor_weight == irrational_sum
    assert todd_char1._inallocable_debtor_weight == missing_job_sum
