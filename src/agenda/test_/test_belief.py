from src.agenda.other import OtherID, otherlink_shop
from src.agenda.belief import (
    BalanceLine,
    balanceline_shop,
    BeliefUnit,
    beliefunit_shop,
    BeliefID,
    BalanceLink,
    balancelink_shop,
    balancelinks_get_from_json,
    balanceheir_shop,
    get_from_json as beliefunits_get_from_json,
    get_beliefunit_from_dict,
    get_beliefunits_from_dict,
)
from src._road.road import (
    get_default_real_id_roadnode as root_label,
    create_road,
    validate_roadnode,
    default_road_delimiter_if_none,
)
from src._instrument.python import x_is_json, get_json_from_dict
from pytest import raises as pytest_raises


def test_BeliefID_exists():
    bikers_belief_id = BeliefID("bikers")
    assert bikers_belief_id != None
    assert str(type(bikers_belief_id)).find(".belief.BeliefID") > 0


def test_BeliefUnit_exists():
    # GIVEN
    swim_text = ",swimmers"
    # WHEN
    swim_beliefunit = BeliefUnit(belief_id=swim_text)
    # THEN
    assert swim_beliefunit != None
    assert swim_beliefunit.belief_id == swim_text
    assert swim_beliefunit._other_mirror is None
    assert swim_beliefunit._others is None
    assert swim_beliefunit._agenda_cred is None
    assert swim_beliefunit._agenda_debt is None
    assert swim_beliefunit._agenda_intent_cred is None
    assert swim_beliefunit._agenda_intent_debt is None
    assert swim_beliefunit._road_delimiter is None


def test_beliefunit_shop_ReturnsCorrectObj():
    # GIVEN
    swim_text = ",swimmers"
    nation_road = create_road(root_label(), "nation-states")
    usa_road = create_road(nation_road, "USA")

    # WHEN
    swim_beliefunit = beliefunit_shop(belief_id=swim_text)

    # THEN
    print(f"{swim_text}")
    assert swim_beliefunit != None
    assert swim_beliefunit.belief_id != None
    assert swim_beliefunit.belief_id == swim_text
    assert swim_beliefunit._agenda_cred == 0
    assert swim_beliefunit._agenda_debt == 0
    assert swim_beliefunit._agenda_intent_cred == 0
    assert swim_beliefunit._agenda_intent_debt == 0
    assert swim_beliefunit._road_delimiter == default_road_delimiter_if_none()


def test_beliefunit_shop_ReturnsCorrectObj_road_delimiter():
    # GIVEN
    swim_text = "/swimmers"
    slash_text = "/"

    # WHEN
    swim_beliefunit = beliefunit_shop(belief_id=swim_text, _road_delimiter=slash_text)

    # THEN
    assert swim_beliefunit._road_delimiter == slash_text


def test_BeliefUnit_set_belief_id_RaisesErrorIfParameterContains_road_delimiter_And_other_mirror_True():
    # GIVEN
    slash_text = "/"
    bob_text = f"Bob{slash_text}Texas"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        beliefunit_shop(bob_text, _other_mirror=True, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{bob_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_BeliefUnit_set_belief_id_RaisesErrorIfParameterDoesNotContain_road_delimiter_other_mirror_False():
    # GIVEN
    comma_text = ","
    texas_text = f"Texas{comma_text}Arkansas"

    # WHEN / THEN
    slash_text = "/"
    with pytest_raises(Exception) as excinfo:
        beliefunit_shop(belief_id=texas_text, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{texas_text}' needs to not be a RoadNode. Must contain delimiter: '{slash_text}'"
    )


def test_BeliefUnit_set_belief_id_SetsAttrCorrectly():
    # GIVEN
    swim_text = ",swimmers"
    swim_belief = beliefunit_shop(belief_id=swim_text)
    assert swim_belief.belief_id == swim_text

    # WHEN
    water_text = ",water people"
    swim_belief.set_belief_id(belief_id=water_text)

    # THEN
    assert swim_belief.belief_id == water_text


def test_BeliefUnit_set_otherlink_CorrectlySetsAttr():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_other = otherlink_shop(other_id=todd_text, credor_weight=13, debtor_weight=7)
    mery_other = otherlink_shop(other_id=mery_text, credor_weight=23, debtor_weight=5)

    swimmers_belief = beliefunit_shop(belief_id=",swimmers", _others={})

    # WHEN
    swimmers_belief.set_otherlink(todd_other)
    swimmers_belief.set_otherlink(mery_other)

    # THEN
    swimmers_others = {todd_other.other_id: todd_other, mery_other.other_id: mery_other}
    assert swimmers_belief._others == swimmers_others


def test_BeliefUnit_get_otherlink_ReturnsCorrectObj():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    swimmers_belief = beliefunit_shop(belief_id=",swimmers", _others={})
    swimmers_belief.set_otherlink(otherlink_shop(todd_text, 13, 7))
    swimmers_belief.set_otherlink(otherlink_shop(mery_text, 23, 5))

    # WHEN / THEN
    assert swimmers_belief.get_otherlink(todd_text) != None
    assert swimmers_belief.get_otherlink(mery_text) != None
    assert swimmers_belief.get_otherlink("todd") is None


def test_BeliefUnit_edit_otherlink_CorrectlySetsAttr():
    # GIVEN
    todd_text = "Todd"
    old_todd_credor_weight = 13
    todd_debtor_weight = 7
    swimmers_belief = beliefunit_shop(belief_id=",swimmers")
    swimmers_belief.set_otherlink(
        otherlink_shop(todd_text, old_todd_credor_weight, todd_debtor_weight)
    )
    todd_otherlink = swimmers_belief.get_otherlink(todd_text)
    assert todd_otherlink.credor_weight == old_todd_credor_weight

    # WHEN
    new_todd_credor_weight = 17
    swimmers_belief.edit_otherlink(
        other_id=todd_text, credor_weight=new_todd_credor_weight
    )

    # THEN
    assert todd_otherlink.credor_weight == new_todd_credor_weight


def test_otherlink_exists_ReturnsCorrectObj():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    swimmers_belief = beliefunit_shop(belief_id=",swimmers", _others={})
    swimmers_belief.set_otherlink(otherlink_shop(todd_text, 13, 7))
    swimmers_belief.set_otherlink(otherlink_shop(mery_text, 23, 5))

    # WHEN / THEN
    assert swimmers_belief.otherlink_exists(todd_text)
    assert swimmers_belief.otherlink_exists(mery_text)
    assert swimmers_belief.otherlink_exists("todd") is False


def test_BeliefUnit_del_otherlink_SetsAttrCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_other = otherlink_shop(other_id=todd_text)
    mery_other = otherlink_shop(other_id=mery_text)
    swimmers_others = {todd_other.other_id: todd_other, mery_other.other_id: mery_other}
    swimmers_belief = beliefunit_shop(belief_id=",swimmers", _others={})
    swimmers_belief.set_otherlink(todd_other)
    swimmers_belief.set_otherlink(mery_other)
    assert len(swimmers_belief._others) == 2
    assert swimmers_belief._others == swimmers_others

    # WHEN
    swimmers_belief.del_otherlink(other_id=todd_text)

    # THEN
    assert len(swimmers_belief._others) == 1
    assert swimmers_belief._others.get(todd_text) is None


def test_BeliefUnit_clear_otherlinks_SetsAttrCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_other = otherlink_shop(other_id=todd_text)
    mery_other = otherlink_shop(other_id=mery_text)
    swimmers_others = {todd_other.other_id: todd_other, mery_other.other_id: mery_other}
    swimmers_belief = beliefunit_shop(belief_id=",swimmers", _others={})
    swimmers_belief.set_otherlink(todd_other)
    swimmers_belief.set_otherlink(mery_other)
    assert len(swimmers_belief._others) == 2
    assert swimmers_belief._others == swimmers_others

    # WHEN
    swimmers_belief.clear_otherlinks()

    # THEN
    assert len(swimmers_belief._others) == 0
    assert swimmers_belief._others.get(todd_text) is None


def test_BeliefUnit_reset_agenda_importance_SetsAttrCorrectly():
    # GIVEN
    maria_belief_id = "maria"
    maria_beliefunit = beliefunit_shop(belief_id=maria_belief_id, _other_mirror=True)
    maria_beliefunit._agenda_cred = 0.33
    maria_beliefunit._agenda_debt = 0.44
    maria_beliefunit._agenda_intent_cred = 0.13
    maria_beliefunit._agenda_intent_debt = 0.23
    print(f"{maria_beliefunit}")
    assert maria_beliefunit._agenda_cred == 0.33
    assert maria_beliefunit._agenda_debt == 0.44
    assert maria_beliefunit._agenda_intent_cred == 0.13
    assert maria_beliefunit._agenda_intent_debt == 0.23

    # WHEN
    maria_beliefunit.reset_agenda_cred_debt()

    # THEN
    assert maria_beliefunit._agenda_cred == 0
    assert maria_beliefunit._agenda_debt == 0
    assert maria_beliefunit._agenda_intent_cred == 0
    assert maria_beliefunit._agenda_intent_debt == 0


def test_BeliefUnit_reset_agenda_importance_reset_otherlinks():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_other = otherlink_shop(
        other_id=todd_text,
        _agenda_cred=0.13,
        _agenda_debt=0.7,
        _agenda_intent_cred=0.53,
        _agenda_intent_debt=0.77,
    )
    mery_other = otherlink_shop(
        other_id=mery_text,
        _agenda_cred=0.23,
        _agenda_debt=0.5,
        _agenda_intent_cred=0.54,
        _agenda_intent_debt=0.57,
    )
    bikers_others = {todd_other.other_id: todd_other, mery_other.other_id: mery_other}
    bikers_belief_id = ",bikers"
    bikers_beliefunit = beliefunit_shop(belief_id=bikers_belief_id)
    bikers_beliefunit._agenda_cred = (0.33,)
    bikers_beliefunit._agenda_debt = (0.44,)
    bikers_beliefunit._agenda_intent_cred = (0.1,)
    bikers_beliefunit._agenda_intent_debt = (0.2,)
    bikers_beliefunit.set_otherlink(otherlink=todd_other)
    bikers_beliefunit.set_otherlink(otherlink=mery_other)
    print(f"{bikers_beliefunit}")
    biker_otherlink_todd = bikers_beliefunit._others.get(todd_text)
    assert biker_otherlink_todd._agenda_cred == 0.13
    assert biker_otherlink_todd._agenda_debt == 0.7
    assert biker_otherlink_todd._agenda_intent_cred == 0.53
    assert biker_otherlink_todd._agenda_intent_debt == 0.77

    biker_otherlink_mery = bikers_beliefunit._others.get(mery_text)
    assert biker_otherlink_mery._agenda_cred == 0.23
    assert biker_otherlink_mery._agenda_debt == 0.5
    assert biker_otherlink_mery._agenda_intent_cred == 0.54
    assert biker_otherlink_mery._agenda_intent_debt == 0.57

    # WHEN
    bikers_beliefunit.reset_agenda_cred_debt()

    # THEN
    assert biker_otherlink_todd._agenda_cred == 0
    assert biker_otherlink_todd._agenda_debt == 0
    assert biker_otherlink_todd._agenda_intent_cred == 0
    assert biker_otherlink_todd._agenda_intent_debt == 0
    assert biker_otherlink_mery._agenda_cred == 0
    assert biker_otherlink_mery._agenda_debt == 0
    assert biker_otherlink_mery._agenda_intent_cred == 0
    assert biker_otherlink_mery._agenda_intent_debt == 0


def test_otherlink_meld_ReturnsCorrectObj_BaseScenario():
    # GIVEN
    todd_other = otherlink_shop(other_id="Todd")
    merry_other = otherlink_shop(other_id="Merry")
    bikers_belief_id = ",bikers"
    bikers_belief = beliefunit_shop(belief_id=bikers_belief_id, _others={})
    bikers_belief.set_otherlink(otherlink=todd_other)
    bikers_belief.set_otherlink(otherlink=merry_other)

    x2_belief = beliefunit_shop(belief_id=bikers_belief_id, _others={})

    # WHEN
    bikers_belief.meld(exterior_belief=x2_belief)
    print(f"{bikers_belief.belief_id=} {x2_belief.belief_id=}")

    # THEN
    assert len(bikers_belief._others) == 2


def test_otherlink_meld_ReturnsCorrectObj_GainScenario():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_other = otherlink_shop(other_id=todd_text, credor_weight=13, debtor_weight=7)
    mery_other = otherlink_shop(other_id=mery_text, credor_weight=23, debtor_weight=5)
    bikers_belief_id = ",bikers"
    bikers_belief = beliefunit_shop(belief_id=bikers_belief_id, _others={})

    x2_belief = beliefunit_shop(belief_id=bikers_belief_id, _others={})
    x2_belief.set_otherlink(otherlink=todd_other)
    x2_belief.set_otherlink(otherlink=mery_other)

    # WHEN
    bikers_belief.meld(exterior_belief=x2_belief)

    # THEN
    assert len(bikers_belief._others) == 2
    assert bikers_belief._others.get(todd_text) != None


def test_BeliefUnit_meld_RaiseSameother_idException():
    # GIVEN
    todd_text = "Todd"
    todd_belief = beliefunit_shop(belief_id=todd_text, _other_mirror=True)
    mery_text = "Merry"
    mery_belief = beliefunit_shop(belief_id=mery_text, _other_mirror=True)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_belief.meld(mery_belief)
    assert (
        str(excinfo.value)
        == f"Meld fail BeliefUnit {todd_belief.belief_id} .belief_id='{todd_belief.belief_id}' not the same as .belief_id='{mery_belief.belief_id}"
    )


def test_BeliefUnit_get_dict_ReturnsDictWithAttrsCorrectlySet():
    # GIVEN
    todd_text = "Todd"
    todd_belief = beliefunit_shop(belief_id=todd_text, _other_mirror=True)
    sue_text = "Sue"
    todd_belief.set_otherlink(otherlink_shop(other_id=sue_text))

    assert todd_belief.belief_id == todd_text
    assert todd_belief._other_mirror
    assert len(todd_belief._others) == 1

    # WHEN
    todd_dict = todd_belief.get_dict()

    # THEN
    assert todd_dict["belief_id"] == todd_text
    assert todd_dict["_other_mirror"]
    assert len(todd_dict["_others"]) == 1


def test_BeliefUnit_get_dict_ReturnsDictWithAttrsCorrectlyEmpty():
    # GIVEN
    swim_text = ",Swimmers"
    swim_belief = beliefunit_shop(belief_id=swim_text)
    assert swim_belief._other_mirror is False
    assert swim_belief._others == {}

    # WHEN
    swim_dict = swim_belief.get_dict()

    # THEN
    assert swim_dict.get("_other_mirror") is None
    assert swim_dict.get("_others") is None


def test_BeliefUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    swim_text = ",swimmers"

    # WHEN
    swimmers_belief = beliefunit_shop(belief_id=swim_text)
    print(f"{swim_text}")

    # THEN
    ee_dict = swimmers_belief.get_dict()
    assert ee_dict != None
    # assert ee_dict == {"belief_id": swimmers}
    assert ee_dict == {"belief_id": swim_text}

    # GIVEN
    sue_text = "Marie"
    marie_otherlink = otherlink_shop(
        other_id=sue_text, credor_weight=29, debtor_weight=3
    )
    otherlinks_dict = {marie_otherlink.other_id: marie_otherlink}
    marie_json_dict = {
        sue_text: {
            "other_id": sue_text,
            "credor_weight": 29,
            "debtor_weight": 3,
        }
    }

    teacher_text = ",teachers"
    swim_road = "swim"
    teachers_belief = beliefunit_shop(
        belief_id=teacher_text,
        _others=otherlinks_dict,
    )

    # WHEN
    teachers_dict = teachers_belief.get_dict()

    # THEN
    print(f"{marie_json_dict=}")
    assert teachers_dict == {
        "belief_id": teacher_text,
        "_others": marie_json_dict,
    }


def test_beliefunit_get_from_dict_CorrectlyReturnsBeliefUnitWith_road_delimiter():
    # GIVEN
    slash_text = "/"
    teacher_text = f"{slash_text}teachers"
    before_teacher_beliefunit = beliefunit_shop(
        teacher_text, _road_delimiter=slash_text
    )
    teacher_dict = before_teacher_beliefunit.get_dict()

    # WHEN
    print(f"{teacher_dict=}")
    after_teacher_beliefunit = get_beliefunit_from_dict(teacher_dict, slash_text)

    # THEN
    assert after_teacher_beliefunit == before_teacher_beliefunit


def test_BeliefUnit_get_from_JSON_ReturnsCorrectObj_SimpleExample():
    # GIVEN
    sue_text = "Sue"
    marie_otherlink = otherlink_shop(
        other_id=sue_text, credor_weight=29, debtor_weight=3
    )
    otherlinks_dict = {marie_otherlink.other_id: marie_otherlink}

    teacher_text = ",teachers"
    swim_road = "swim"
    teacher_belief = beliefunit_shop(belief_id=teacher_text, _others=otherlinks_dict)
    teacher_dict = teacher_belief.get_dict()
    beliefs_dict = {teacher_text: teacher_dict}

    teachers_json = get_json_from_dict(dict_x=beliefs_dict)
    assert teachers_json != None
    assert x_is_json(json_x=teachers_json)

    # WHEN
    beliefunits_obj_dict = beliefunits_get_from_json(beliefunits_json=teachers_json)

    # THEN
    assert beliefunits_obj_dict != None
    teachers_obj_check_dict = {teacher_belief.belief_id: teacher_belief}
    print(f"    {beliefunits_obj_dict=}")
    print(f"{teachers_obj_check_dict=}")
    assert beliefunits_obj_dict == teachers_obj_check_dict


def test_BeliefUnit_get_beliefunits_from_dict_ReturnsCorrectObjWith_road_delimiter():
    # GIVEN
    slash_text = "/"
    teacher_text = f"{slash_text}teachers"
    teacher_beliefunit = beliefunit_shop(teacher_text, _road_delimiter=slash_text)
    teacher_dict = teacher_beliefunit.get_dict()

    teacher_dict = teacher_beliefunit.get_dict()
    beliefunits_dict = {teacher_text: teacher_dict}

    # WHEN
    x_beliefunits = get_beliefunits_from_dict(beliefunits_dict, slash_text)

    # THEN
    assert x_beliefunits != None
    teachers_obj_check_dict = {teacher_beliefunit.belief_id: teacher_beliefunit}
    print(f"{teachers_obj_check_dict=}")
    assert x_beliefunits == teachers_obj_check_dict


def test_BalanceLink_exists():
    # GIVEN
    bikers_belief_id = BeliefID("bikers")

    # WHEN
    bikers_balancelink = BalanceLink(belief_id=bikers_belief_id)

    # THEN
    assert bikers_balancelink.belief_id == bikers_belief_id
    assert bikers_balancelink.credor_weight == 1.0
    assert bikers_balancelink.debtor_weight == 1.0


def test_balancelink_shop_ReturnsCorrectObj():
    # GIVEN
    bikers_belief_id = BeliefID("bikers")
    bikers_credor_weight = 3.0
    bikers_debtor_weight = 5.0

    # WHEN
    bikers_balancelink = balancelink_shop(
        belief_id=bikers_belief_id,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debtor_weight,
    )

    # THEN
    assert bikers_balancelink.credor_weight == bikers_credor_weight
    assert bikers_balancelink.debtor_weight == bikers_debtor_weight


def test_BalanceHeir_set_agenda_importance_CorrectlySetsAttr():
    # GIVEN
    bikers_belief_id = BeliefID("bikers")
    bikers_credor_weight = 3.0
    bikers_debt_weight = 6.0
    balancelinks_sum_credor_weight = 60
    balancelinks_sum_debtor_weight = 60
    idea_agenda_importance = 1
    belief_heir_x = balanceheir_shop(
        belief_id=bikers_belief_id,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debt_weight,
    )

    # WHEN
    belief_heir_x.set_agenda_cred_debt(
        idea_agenda_importance=idea_agenda_importance,
        balanceheirs_credor_weight_sum=balancelinks_sum_credor_weight,
        balanceheirs_debtor_weight_sum=balancelinks_sum_debtor_weight,
    )

    # THEN
    assert belief_heir_x._agenda_cred == 0.05
    assert belief_heir_x._agenda_debt == 0.1


def test_BalanceLink_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    bikers_belief_id = BeliefID("bikers")
    bikers_credor_weight = 3.0
    bikers_debtor_weight = 5.0
    bikers_link = balancelink_shop(
        belief_id=bikers_belief_id,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debtor_weight,
    )

    print(f"{bikers_link}")

    # WHEN
    biker_dict = bikers_link.get_dict()

    # THEN
    assert biker_dict != None
    assert biker_dict == {
        "belief_id": bikers_link.belief_id,
        "credor_weight": bikers_link.credor_weight,
        "debtor_weight": bikers_link.debtor_weight,
    }


def test_balancelinks_get_from_JSON_ReturnsCorrectObj_SimpleExample():
    # GIVEN
    teacher_text = "teachers"
    teacher_balancelink = balancelink_shop(
        belief_id=teacher_text, credor_weight=103, debtor_weight=155
    )
    teacher_dict = teacher_balancelink.get_dict()
    balancelinks_dict = {teacher_balancelink.belief_id: teacher_dict}

    teachers_json = get_json_from_dict(dict_x=balancelinks_dict)
    assert teachers_json != None
    assert x_is_json(json_x=teachers_json)

    # WHEN
    balancelinks_obj_dict = balancelinks_get_from_json(balancelinks_json=teachers_json)

    # THEN
    assert balancelinks_obj_dict != None
    teachers_obj_check_dict = {teacher_balancelink.belief_id: teacher_balancelink}
    print(f"    {balancelinks_obj_dict=}")
    print(f"{teachers_obj_check_dict=}")
    assert balancelinks_obj_dict == teachers_obj_check_dict


def test_BalanceLine_exists():
    # GIVEN
    bikers_belief_id = BeliefID("bikers")
    bikers_agenda_cred = 0.33
    bikers_agenda_debt = 0.55

    # WHEN
    bikers_balanceline = BalanceLine(
        belief_id=bikers_belief_id,
        _agenda_cred=bikers_agenda_cred,
        _agenda_debt=bikers_agenda_debt,
    )

    # THEN
    assert bikers_balanceline.belief_id == bikers_belief_id
    assert bikers_balanceline._agenda_cred == bikers_agenda_cred
    assert bikers_balanceline._agenda_debt == bikers_agenda_debt


def test_balanceline_shop_ReturnsCorrectObj_exists():
    # GIVEN
    bikers_belief_id = BeliefID("bikers")
    bikers_belief_id = bikers_belief_id
    bikers_agenda_cred = 0.33
    bikers_agenda_debt = 0.55

    # WHEN
    biker_balanceline = balanceline_shop(
        belief_id=bikers_belief_id,
        _agenda_cred=bikers_agenda_cred,
        _agenda_debt=bikers_agenda_debt,
    )

    assert biker_balanceline != None
    assert biker_balanceline.belief_id == bikers_belief_id
    assert biker_balanceline._agenda_cred == bikers_agenda_cred
    assert biker_balanceline._agenda_debt == bikers_agenda_debt


def test_BalanceLine_add_agenda_cred_debt_CorrectlyModifiesAttr():
    # GIVEN
    bikers_belief_id = BeliefID("bikers")
    bikers_balanceline = balanceline_shop(
        belief_id=bikers_belief_id, _agenda_cred=0.33, _agenda_debt=0.55
    )
    assert bikers_balanceline.belief_id == bikers_belief_id
    assert bikers_balanceline._agenda_cred == 0.33
    assert bikers_balanceline._agenda_debt == 0.55

    # WHEN
    bikers_balanceline.add_agenda_cred_debt(agenda_cred=0.11, agenda_debt=0.2)

    # THEN
    assert bikers_balanceline._agenda_cred == 0.44
    assert bikers_balanceline._agenda_debt == 0.75
