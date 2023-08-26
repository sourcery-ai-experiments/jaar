from src.agent.ally import AllyName, allylink_shop
from src.agent.tribe import (
    Tribeline,
    tribeunit_shop,
    TribeName,
    tribelink_shop,
    tribelinks_get_from_json,
    tribeheir_shop,
    get_from_json as tribeunits_get_from_json,
)
from src.agent.x_func import x_is_json, x_get_json
from pytest import raises as pytest_raises


def test_tribeName_exists():
    bikers_name = TribeName("bikers")
    assert bikers_name != None
    assert str(type(bikers_name)).find(".tribe.TribeName") > 0


def test_tribeunit_exists():
    # GIVEN
    swimmers = "swimmers"
    usa_road = "src,nation-states,USA"

    # WHEN
    swimmers_tribe = tribeunit_shop(
        name=swimmers,
        _agent_credit=0.33,
        _agent_debt=0.44,
        _agent_agenda_credit=0.66,
        _agent_agenda_debt=0.77,
        _allylinks_set_by_world_road=usa_road,
    )

    # THEN
    print(f"{swimmers}")
    assert swimmers_tribe != None
    assert swimmers_tribe.name != None
    assert swimmers_tribe.name == swimmers
    assert swimmers_tribe._agent_credit != None
    assert swimmers_tribe._agent_debt != None
    assert swimmers_tribe._agent_agenda_credit != None
    assert swimmers_tribe._agent_agenda_debt != None
    assert swimmers_tribe._allylinks_set_by_world_road == usa_road


def test_tribeunit_set_name_WorksCorrectly():
    # GIVEN
    swim_text = "swimmers"
    swim_tribe = tribeunit_shop(name=swim_text)
    assert swim_tribe.name == swim_text

    # WHEN
    water_text = "water people"
    swim_tribe.set_name(name=water_text)

    # THEN
    assert swim_tribe.name == water_text


def test_tribeunit_set_attr_WorksCorrectly():
    # GIVEN
    swim_text = "swimmers"
    swim_tribe = tribeunit_shop(name=swim_text)
    assert swim_tribe._allylinks_set_by_world_road is None

    # WHEN
    water_road = "src,sports,water"
    swim_tribe.set_attr(_allylinks_set_by_world_road=water_road)

    # THEN
    assert swim_tribe._allylinks_set_by_world_road == water_road


def test_tribeunit_shop_WhenSingleAllyCorrectlyRemoves_allylinks_set_by_world_road():
    # GIVEN
    swimmers = "swimmers"
    usa_road = "src,nation-states,USA"

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        swimmers_tribe = tribeunit_shop(
            name=swimmers,
            _single_ally=True,
            _allylinks_set_by_world_road=usa_road,
        )
    assert (
        str(excinfo.value)
        == f"_allylinks_set_by_world_road cannot be '{usa_road}' for a single_ally TribeUnit. It must have no value."
    )


def test_tribeunit_set_allylink_worksCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_ally = allylink_shop(name=todd_text, creditor_weight=13, debtor_weight=7)
    mery_ally = allylink_shop(name=mery_text, creditor_weight=23, debtor_weight=5)

    swimmers_tribe = tribeunit_shop(name="swimmers", _allys={})

    # WHEN
    swimmers_tribe.set_allylink(todd_ally)
    swimmers_tribe.set_allylink(mery_ally)

    # THEN
    swimmers_allys = {todd_ally.name: todd_ally, mery_ally.name: mery_ally}
    assert swimmers_tribe._allys == swimmers_allys


def test_tribeunit_del_allylink_worksCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_ally = allylink_shop(name=todd_text)
    mery_ally = allylink_shop(name=mery_text)
    swimmers_allys = {todd_ally.name: todd_ally, mery_ally.name: mery_ally}
    swimmers_tribe = tribeunit_shop(name="swimmers", _allys={})
    swimmers_tribe.set_allylink(todd_ally)
    swimmers_tribe.set_allylink(mery_ally)
    assert len(swimmers_tribe._allys) == 2
    assert swimmers_tribe._allys == swimmers_allys

    # WHEN
    swimmers_tribe.del_allylink(name=todd_text)

    # THEN
    assert len(swimmers_tribe._allys) == 1
    assert swimmers_tribe._allys.get(todd_text) is None


def test_tribeunit_clear_allylinks_worksCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_ally = allylink_shop(name=todd_text)
    mery_ally = allylink_shop(name=mery_text)
    swimmers_allys = {todd_ally.name: todd_ally, mery_ally.name: mery_ally}
    swimmers_tribe = tribeunit_shop(name="swimmers", _allys={})
    swimmers_tribe.set_allylink(todd_ally)
    swimmers_tribe.set_allylink(mery_ally)
    assert len(swimmers_tribe._allys) == 2
    assert swimmers_tribe._allys == swimmers_allys

    # WHEN
    swimmers_tribe.clear_allylinks()

    # THEN
    assert len(swimmers_tribe._allys) == 0
    assert swimmers_tribe._allys.get(todd_text) is None


def test_Tribeunit_reset_agent_importance_WorkCorrectly():
    # GIVEN
    maria_name = "maria"
    maria_tribe = tribeunit_shop(
        name=maria_name,
        _agent_credit=0.33,
        _agent_debt=0.44,
        _agent_agenda_credit=0.13,
        _agent_agenda_debt=0.23,
    )
    print(f"{maria_tribe}")
    assert maria_tribe._agent_credit == 0.33
    assert maria_tribe._agent_debt == 0.44
    assert maria_tribe._agent_agenda_credit == 0.13
    assert maria_tribe._agent_agenda_debt == 0.23

    # WHEN
    maria_tribe.reset_agent_credit_debt()

    # THEN
    assert maria_tribe._agent_credit == 0
    assert maria_tribe._agent_debt == 0
    assert maria_tribe._agent_agenda_credit == 0
    assert maria_tribe._agent_agenda_debt == 0


def test_Tribeunit_reset_agent_importance_reset_allylinks():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_ally = allylink_shop(
        name=todd_text,
        _agent_credit=0.13,
        _agent_debt=0.7,
        _agent_agenda_credit=0.53,
        _agent_agenda_debt=0.77,
    )
    mery_ally = allylink_shop(
        name=mery_text,
        _agent_credit=0.23,
        _agent_debt=0.5,
        _agent_agenda_credit=0.54,
        _agent_agenda_debt=0.57,
    )
    bikers_allys = {todd_ally.name: todd_ally, mery_ally.name: mery_ally}
    bikers_name = "bikers"
    bikers_tribe = tribeunit_shop(
        name=bikers_name,
        _allys={},
        _agent_credit=0.33,
        _agent_debt=0.44,
        _agent_agenda_credit=0.1,
        _agent_agenda_debt=0.2,
    )
    bikers_tribe.set_allylink(allylink=todd_ally)
    bikers_tribe.set_allylink(allylink=mery_ally)
    print(f"{bikers_tribe}")
    biker_allylink_todd = bikers_tribe._allys.get(todd_text)
    assert biker_allylink_todd._agent_credit == 0.13
    assert biker_allylink_todd._agent_debt == 0.7
    assert biker_allylink_todd._agent_agenda_credit == 0.53
    assert biker_allylink_todd._agent_agenda_debt == 0.77

    biker_allylink_mery = bikers_tribe._allys.get(mery_text)
    assert biker_allylink_mery._agent_credit == 0.23
    assert biker_allylink_mery._agent_debt == 0.5
    assert biker_allylink_mery._agent_agenda_credit == 0.54
    assert biker_allylink_mery._agent_agenda_debt == 0.57

    # WHEN
    bikers_tribe.reset_agent_credit_debt()

    # THEN
    assert biker_allylink_todd._agent_credit == 0
    assert biker_allylink_todd._agent_debt == 0
    assert biker_allylink_todd._agent_agenda_credit == 0
    assert biker_allylink_todd._agent_agenda_debt == 0
    assert biker_allylink_mery._agent_credit == 0
    assert biker_allylink_mery._agent_debt == 0
    assert biker_allylink_mery._agent_agenda_credit == 0
    assert biker_allylink_mery._agent_agenda_debt == 0


def test_TribeUnit_allylink_meld_BaseScenarioWorks():
    # GIVEN
    todd_ally = allylink_shop(name="Todd")
    merry_ally = allylink_shop(name="Merry")
    x1_name = "bikers"
    x1_tribe = tribeunit_shop(name=x1_name, _allys={})
    x1_tribe.set_allylink(allylink=todd_ally)
    x1_tribe.set_allylink(allylink=merry_ally)

    x2_tribe = tribeunit_shop(name=x1_name, _allys={})

    # WHEN
    x1_tribe.meld(other_tribe=x2_tribe)
    print(f"{x1_tribe.name=} {x2_tribe.name=}")

    # THEN
    assert len(x1_tribe._allys) == 2


def test_TribeUnit_allylink_meld_GainScenarioWorks():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_ally = allylink_shop(name=todd_text, creditor_weight=13, debtor_weight=7)
    mery_ally = allylink_shop(name=mery_text, creditor_weight=23, debtor_weight=5)
    x1_name = "bikers"
    x1_tribe = tribeunit_shop(name=x1_name, _allys={})

    x2_tribe = tribeunit_shop(name=x1_name, _allys={})
    x2_tribe.set_allylink(allylink=todd_ally)
    x2_tribe.set_allylink(allylink=mery_ally)

    # WHEN
    x1_tribe.meld(other_tribe=x2_tribe)

    # THEN
    assert len(x1_tribe._allys) == 2
    assert x1_tribe._allys.get(todd_text) != None


def test_TribeUnit_meld_RaiseSameNameException():
    # GIVEN
    todd_text = "Todd"
    todd_tribe = tribeunit_shop(name=todd_text)
    mery_text = "Merry"
    mery_tribe = tribeunit_shop(name=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_tribe.meld(mery_tribe)
    assert (
        str(excinfo.value)
        == f"Meld fail TribeUnit {todd_tribe.name} .name='{todd_tribe.name}' not the same as .name='{mery_tribe.name}"
    )


def test_TribeUnit_meld_RaiseSameUIDException():
    # GIVEN
    todd_text = "Todd"
    todd3_tribe = tribeunit_shop(name=todd_text, uid=3)
    todd5_tribe = tribeunit_shop(name=todd_text, uid=5)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd3_tribe.meld(todd5_tribe)
    assert (
        str(excinfo.value)
        == f"Meld fail TribeUnit {todd3_tribe.name} .uid='{todd3_tribe.uid}' not the same as .uid='{todd5_tribe.uid}"
    )


def test_tribeUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    swimmers = "swimmers"

    # WHEN
    swimmers_tribe = tribeunit_shop(name=swimmers)
    print(f"{swimmers}")

    # THEN
    ee_dict = swimmers_tribe.get_dict()
    assert ee_dict != None
    # assert ee_dict == {"name": swimmers, "uid": 2}
    assert ee_dict == {
        "name": swimmers,
        "uid": None,
        "single_member_ally_id": None,
        "_single_ally": False,
        "_allys": {},
        "_allylinks_set_by_world_road": None,
    }

    # GIVEN
    str_name = "Marie"
    marie_name = AllyName(str_name)
    marie_allylink = allylink_shop(name=marie_name, creditor_weight=29, debtor_weight=3)
    allylinks_dict = {marie_allylink.name: marie_allylink}
    marie_json_dict = {
        marie_name: {"name": marie_name, "creditor_weight": 29, "debtor_weight": 3}
    }

    str_teacher = "teachers"
    swim_road = "road_str"
    teachers_tribe = tribeunit_shop(
        name=str_teacher, _allys=allylinks_dict, _allylinks_set_by_world_road=swim_road
    )

    # WHEN
    teachers_dict = teachers_tribe.get_dict()

    # THEN
    print(f"{marie_json_dict=}")
    assert teachers_dict == {
        "name": str_teacher,
        "uid": None,
        "single_member_ally_id": None,
        "_single_ally": False,
        "_allys": marie_json_dict,
        "_allylinks_set_by_world_road": swim_road,
    }


def test_tribeunit_get_from_JSON_SimpleExampleWorks():
    # GIVEN
    str_name = "Marie"
    marie_name = AllyName(str_name)
    marie_allylink = allylink_shop(name=marie_name, creditor_weight=29, debtor_weight=3)
    allylinks_dict = {marie_allylink.name: marie_allylink}

    str_teacher = "teachers"
    swim_road = "road_str"
    teacher_tribe = tribeunit_shop(
        name=str_teacher, _allys=allylinks_dict, _allylinks_set_by_world_road=swim_road
    )
    teacher_dict = teacher_tribe.get_dict()
    _allylinks_set_by_world_road_text = "_allylinks_set_by_world_road"
    print(f"{teacher_dict.get(_allylinks_set_by_world_road_text)=}")
    tribes_dict = {"teachers": teacher_dict}

    teachers_json = x_get_json(dict_x=tribes_dict)
    print(f"{teachers_json.find(_allylinks_set_by_world_road_text)=}")
    assert teachers_json != None
    assert x_is_json(json_x=teachers_json)

    # WHEN
    tribeunits_obj_dict = tribeunits_get_from_json(tribeunits_json=teachers_json)

    # THEN
    assert tribeunits_obj_dict != None
    teachers_obj_check_dict = {teacher_tribe.name: teacher_tribe}
    print(f"    {tribeunits_obj_dict=}")
    allylinks_set_by_world_road_text = "_allylinks_set_by_world_road"
    print(f"{teachers_obj_check_dict.get(allylinks_set_by_world_road_text)=}")
    print(f"{teachers_obj_check_dict=}")
    assert tribeunits_obj_dict == teachers_obj_check_dict


def test_brankLink_exists():
    # GIVEN
    bikers_name = TribeName("bikers")

    # WHEN
    tribe_link_x = tribelink_shop(name=bikers_name)

    # THEN
    assert tribe_link_x.name == bikers_name
    assert tribe_link_x.creditor_weight == 1.0
    assert tribe_link_x.debtor_weight == 1.0

    # WHEN
    bikers_creditor_weight = 3.0
    bikers_debtor_weight = 5.0

    tribe_link_x = tribelink_shop(
        name=bikers_name,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debtor_weight,
    )

    # THEN
    assert tribe_link_x.creditor_weight == 3.0
    assert tribe_link_x.debtor_weight == 5.0


def test_brankLink_set_agent_importanceCorrectly():
    # GIVEN
    bikers_name = TribeName("bikers")
    bikers_creditor_weight = 3.0
    bikers_debt_weight = 6.0
    tribelinks_sum_creditor_weight = 60
    tribelinks_sum_debtor_weight = 60
    idea_agent_importance = 1
    tribe_heir_x = tribeheir_shop(
        name=bikers_name,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debt_weight,
    )

    # WHEN
    tribe_heir_x.set_agent_credit_debt(
        idea_agent_importance=idea_agent_importance,
        tribeheirs_creditor_weight_sum=tribelinks_sum_creditor_weight,
        tribeheirs_debtor_weight_sum=tribelinks_sum_debtor_weight,
    )

    # THEN
    assert tribe_heir_x._agent_credit == 0.05
    assert tribe_heir_x._agent_debt == 0.1


def test_tribelink_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    bikers_name = TribeName("bikers")
    bikers_creditor_weight = 3.0
    bikers_debtor_weight = 5.0
    bikers_link = tribelink_shop(
        name=bikers_name,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debtor_weight,
    )

    print(f"{bikers_link}")

    # WHEN
    biker_dict = bikers_link.get_dict()

    # THEN
    assert biker_dict != None
    assert biker_dict == {
        "name": bikers_link.name,
        "creditor_weight": bikers_link.creditor_weight,
        "debtor_weight": bikers_link.debtor_weight,
    }


def test_tribelinks_get_from_JSON_SimpleExampleWorks():
    # GIVEN
    str_teacher = "teachers"
    teacher_tribelink = tribelink_shop(
        name=str_teacher, creditor_weight=103, debtor_weight=155
    )
    teacher_dict = teacher_tribelink.get_dict()
    tribelinks_dict = {teacher_tribelink.name: teacher_dict}

    teachers_json = x_get_json(dict_x=tribelinks_dict)
    assert teachers_json != None
    assert x_is_json(json_x=teachers_json)

    # WHEN
    tribelinks_obj_dict = tribelinks_get_from_json(tribelinks_json=teachers_json)

    # THEN
    assert tribelinks_obj_dict != None
    teachers_obj_check_dict = {teacher_tribelink.name: teacher_tribelink}
    print(f"    {tribelinks_obj_dict=}")
    print(f"{teachers_obj_check_dict=}")
    assert tribelinks_obj_dict == teachers_obj_check_dict


def test_Tribeline_exists():
    # GIVEN
    bikers_name = TribeName("bikers")
    tribeline_x = Tribeline(name=bikers_name, _agent_credit=0.33, _agent_debt=0.55)
    assert tribeline_x.name == bikers_name
    assert tribeline_x._agent_credit == 0.33
    assert tribeline_x._agent_debt == 0.55

    # WHEN
    tribeline_x.add_agent_credit_debt(agent_credit=0.11, agent_debt=0.2)

    # THEN
    assert tribeline_x._agent_credit == 0.44
    assert tribeline_x._agent_debt == 0.75
