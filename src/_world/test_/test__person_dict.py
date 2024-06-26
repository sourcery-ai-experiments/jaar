from src._world.belieflink import belieflink_shop
from src._world.person import (
    personunit_shop,
    personunits_get_from_json,
    personunit_get_from_dict,
    personunits_get_from_dict,
)
from src._instrument.python import x_is_json, get_json_from_dict
from pytest import raises as pytest_raises


def test_PersonUnit_get_belieflinks_dict_ReturnObj():
    # GIVEN
    sue_text = "Sue"
    sue_credor_weight = 11
    sue_debtor_weight = 13
    run_text = ",Run"
    run_credor_weight = 17
    run_debtor_weight = 23
    sue_belieflink = belieflink_shop(sue_text, sue_credor_weight, sue_debtor_weight)
    run_belieflink = belieflink_shop(run_text, run_credor_weight, run_debtor_weight)
    sue_personunit = personunit_shop(sue_text)
    sue_personunit.set_belieflink(sue_belieflink)
    sue_personunit.set_belieflink(run_belieflink)

    # WHEN
    sue_belieflinks_dict = sue_personunit.get_belieflinks_dict()

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


def test_PersonUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    bob_text = "Bob"
    bob_treasury_due_paid = 0.55
    bob_treasury_due_diff = 0.66
    bob_personunit = personunit_shop(bob_text)
    bob_personunit._treasury_due_paid = bob_treasury_due_paid
    bob_personunit._treasury_due_diff = bob_treasury_due_diff
    bob_credor_operational = False
    bob_debtor_operational = True
    bob_personunit._credor_operational = bob_credor_operational
    bob_personunit._debtor_operational = bob_debtor_operational

    bob_credor_weight = 13
    bob_debtor_weight = 17
    bob_personunit.set_credor_weight(bob_credor_weight)
    bob_personunit.set_debtor_weight(bob_debtor_weight)

    bob_treasury_cred_score = 7000
    bob_treasury_voice_rank = 898
    bob_treasury_voice_hx_lowest_rank = 740
    bob_personunit._treasury_cred_score = bob_treasury_cred_score
    bob_personunit._treasury_voice_rank = bob_treasury_voice_rank
    bob_personunit._treasury_voice_hx_lowest_rank = bob_treasury_voice_hx_lowest_rank
    print(f"{bob_text}")

    # WHEN
    x_dict = bob_personunit.get_dict()

    # THEN
    print(f"{x_dict=}")
    assert x_dict != None
    assert x_dict == {
        "person_id": bob_text,
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


def test_PersonUnit_get_dict_ReturnsDictWithAllAttrDataForJSON():
    # GIVEN
    bob_text = "Bob"
    bob_treasury_due_paid = 0.55
    bob_treasury_due_diff = 0.66
    bob_personunit = personunit_shop(bob_text)
    bob_personunit._treasury_due_paid = bob_treasury_due_paid
    bob_personunit._treasury_due_diff = bob_treasury_due_diff
    bob_credor_operational = False
    bob_debtor_operational = True
    bob_personunit._credor_operational = bob_credor_operational
    bob_personunit._debtor_operational = bob_debtor_operational

    bob_credor_weight = 13
    bob_debtor_weight = 17
    bob_personunit.set_credor_weight(bob_credor_weight)
    bob_personunit.set_debtor_weight(bob_debtor_weight)
    bob_irrational_debtor_weight = 87
    bob_inallocable_debtor_weight = 97
    bob_personunit.add_irrational_debtor_weight(bob_irrational_debtor_weight)
    bob_personunit.add_inallocable_debtor_weight(bob_inallocable_debtor_weight)

    bob_treasury_cred_score = 7000
    bob_treasury_voice_rank = 898
    bob_treasury_voice_hx_lowest_rank = 740
    bob_personunit._treasury_cred_score = bob_treasury_cred_score
    bob_personunit._treasury_voice_rank = bob_treasury_voice_rank
    bob_personunit._treasury_voice_hx_lowest_rank = bob_treasury_voice_hx_lowest_rank

    bob_world_cred = 55
    bob_world_debt = 47
    bob_world_agenda_cred = 51
    bob_world_agenda_debt = 67
    bob_world_agenda_ratio_cred = 71
    bob_world_agenda_ratio_debt = 73
    bob_output_world_meld_order = 79

    bob_personunit._world_cred = bob_world_cred
    bob_personunit._world_debt = bob_world_debt
    bob_personunit._world_agenda_cred = bob_world_agenda_cred
    bob_personunit._world_agenda_debt = bob_world_agenda_debt
    bob_personunit._world_agenda_ratio_cred = bob_world_agenda_ratio_cred
    bob_personunit._world_agenda_ratio_debt = bob_world_agenda_ratio_debt
    bob_personunit._output_world_meld_order = bob_output_world_meld_order

    print(f"{bob_text}")

    # WHEN
    x_dict = bob_personunit.get_dict(all_attrs=True)

    # THEN
    print(f"{x_dict=}")
    assert x_dict != None
    assert x_dict == {
        "person_id": bob_text,
        "credor_weight": bob_credor_weight,
        "debtor_weight": bob_debtor_weight,
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


def test_PersonUnit_get_dict_ReturnsDictWith_irrational_missing_job_ValuesIsZerp():
    # GIVEN
    bob_text = "Bob"
    bob_personunit = personunit_shop(bob_text)
    assert bob_personunit._irrational_debtor_weight == 0
    assert bob_personunit._inallocable_debtor_weight == 0

    # WHEN
    x_dict = bob_personunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtor_weight = "_irrational_debtor_weight"
    x_inallocable_debtor_weight = "_inallocable_debtor_weight"
    assert x_dict.get(x_irrational_debtor_weight) is None
    assert x_dict.get(x_inallocable_debtor_weight) is None
    assert len(x_dict.keys()) == 17


def test_PersonUnit_get_dict_ReturnsDictWith_irrational_missing_job_ValuesIsNumber():
    # GIVEN
    bob_text = "Bob"
    bob_personunit = personunit_shop(bob_text)
    bob_irrational_debtor_weight = 87
    bob_inallocable_debtor_weight = 97
    bob_personunit.add_irrational_debtor_weight(bob_irrational_debtor_weight)
    bob_personunit.add_inallocable_debtor_weight(bob_inallocable_debtor_weight)

    # WHEN
    x_dict = bob_personunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtor_weight = "_irrational_debtor_weight"
    x_inallocable_debtor_weight = "_inallocable_debtor_weight"
    assert x_dict.get(x_irrational_debtor_weight) == bob_irrational_debtor_weight
    assert x_dict.get(x_inallocable_debtor_weight) == bob_inallocable_debtor_weight
    assert len(x_dict.keys()) == 19


def test_PersonUnit_get_dict_ReturnsDictWith_irrational_missing_job_ValuesIsNone():
    # GIVEN
    bob_text = "Bob"
    bob_personunit = personunit_shop(bob_text)
    bob_personunit._irrational_debtor_weight = None
    bob_personunit._inallocable_debtor_weight = None

    # WHEN
    x_dict = bob_personunit.get_dict(all_attrs=True)

    # THEN
    x_irrational_debtor_weight = "_irrational_debtor_weight"
    x_inallocable_debtor_weight = "_inallocable_debtor_weight"
    assert x_dict.get(x_irrational_debtor_weight) is None
    assert x_dict.get(x_inallocable_debtor_weight) is None
    assert len(x_dict.keys()) == 17


def test_personunit_get_from_dict_ReturnsCorrectObjWith_road_delimiter():
    # GIVEN
    yao_text = ",Yao"
    slash_text = "/"
    before_yao_personunit = personunit_shop(yao_text, _road_delimiter=slash_text)
    yao_dict = before_yao_personunit.get_dict()

    # WHEN
    after_yao_personunit = personunit_get_from_dict(yao_dict, slash_text)

    # THEN
    assert before_yao_personunit == after_yao_personunit
    assert after_yao_personunit._road_delimiter == slash_text


def test_personunits_get_from_dict_ReturnsCorrectObjWith_road_delimiter():
    # GIVEN
    yao_text = ",Yao"
    slash_text = "/"
    yao_personunit = personunit_shop(yao_text, _road_delimiter=slash_text)
    yao_dict = yao_personunit.get_dict()
    x_personunits_dict = {yao_text: yao_dict}

    # WHEN
    x_personunits_objs = personunits_get_from_dict(x_personunits_dict, slash_text)

    # THEN
    assert x_personunits_objs.get(yao_text) == yao_personunit
    assert x_personunits_objs.get(yao_text)._road_delimiter == slash_text


def test_personunits_get_from_json_ReturnsCorrectObj_SimpleExampleWithIncompleteData():
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
            "person_id": yao_text,
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
    yao_obj_dict = personunits_get_from_json(personunits_json=yao_json_text)

    # THEN
    assert yao_obj_dict[yao_text] != None
    yao_personunit = yao_obj_dict[yao_text]

    assert yao_personunit.person_id == yao_text
    assert yao_personunit.credor_weight == yao_credor_weight
    assert yao_personunit.debtor_weight == yao_debtor_weight
    assert yao_personunit._irrational_debtor_weight == yao_irrational_debtor_weight
    assert yao_personunit._inallocable_debtor_weight == yao_inallocable_debtor_weight
    assert yao_personunit._credor_operational == yao_credor_operational
    assert yao_personunit._debtor_operational == yao_debtor_operational
    assert yao_personunit._treasury_due_paid == yao_treasury_due_paid
    assert yao_personunit._treasury_due_diff == yao_treasury_due_diff
    assert yao_personunit._treasury_cred_score == yao_treasury_cred_score
    assert yao_personunit._treasury_voice_rank == yao_treasury_voice_rank
    assert (
        yao_personunit._treasury_voice_hx_lowest_rank
        == yao_treasury_voice_hx_lowest_rank
    )


def test_PersonUnit_meld_RaiseEqualperson_idException():
    # GIVEN
    todd_text = "Todd"
    todd_person = personunit_shop(person_id=todd_text)
    mery_text = "Merry"
    mery_person = personunit_shop(person_id=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_person.meld(mery_person)
    assert (
        str(excinfo.value)
        == f"Meld fail PersonUnit='{todd_person.person_id}' not the equal as PersonUnit='{mery_person.person_id}"
    )


def test_PersonUnit_meld_CorrectlySumsWeights():
    # GIVEN
    todd_text = "Todd"
    todd_person1 = personunit_shop(todd_text, credor_weight=7, debtor_weight=19)
    todd_person2 = personunit_shop(todd_text, credor_weight=5, debtor_weight=3)

    todd1_irrational_debtor_weight = 44
    todd2_irrational_debtor_weight = 33
    todd_person1.add_irrational_debtor_weight(todd1_irrational_debtor_weight)
    todd_person2.add_irrational_debtor_weight(todd2_irrational_debtor_weight)
    todd1_inallocable_debtor_weight = 11
    todd2_inallocable_debtor_weight = 22
    todd_person1.add_inallocable_debtor_weight(todd1_inallocable_debtor_weight)
    todd_person2.add_inallocable_debtor_weight(todd2_inallocable_debtor_weight)

    todd_person2
    assert todd_person1.credor_weight == 7
    assert todd_person1.debtor_weight == 19
    assert todd_person1._irrational_debtor_weight == todd1_irrational_debtor_weight
    assert todd_person1._inallocable_debtor_weight == todd1_inallocable_debtor_weight

    # WHEN
    todd_person1.meld(todd_person2)

    # THEN
    assert todd_person1.credor_weight == 12
    assert todd_person1.debtor_weight == 22
    assert todd_person1._irrational_debtor_weight != todd1_irrational_debtor_weight
    assert todd_person1._inallocable_debtor_weight != todd1_inallocable_debtor_weight

    irrational_sum = todd1_irrational_debtor_weight + todd2_irrational_debtor_weight
    missing_job_sum = todd1_inallocable_debtor_weight + todd2_inallocable_debtor_weight
    assert todd_person1._irrational_debtor_weight == irrational_sum
    assert todd_person1._inallocable_debtor_weight == missing_job_sum
