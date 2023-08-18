from src.agent.ally import AllyName, allylink_shop
from src.agent.brand import (
    Brandline,
    brandunit_shop,
    BrandName,
    brandlink_shop,
    brandlinks_get_from_json,
    brandheir_shop,
    get_from_json as brandunits_get_from_json,
)
from src.agent.x_func import x_is_json, x_get_json
from pytest import raises as pytest_raises


def test_brandName_exists():
    bikers_name = BrandName("bikers")
    assert bikers_name != None
    assert str(type(bikers_name)).find(".brand.BrandName") > 0


def test_brandunit_exists():
    # GIVEN
    swimmers = "swimmers"
    usa_road = "src,nation-states,USA"

    # WHEN
    swimmers_brand = brandunit_shop(
        name=swimmers,
        _agent_credit=0.33,
        _agent_debt=0.44,
        _agent_agenda_credit=0.66,
        _agent_agenda_debt=0.77,
        _allylinks_set_by_world_road=usa_road,
    )

    # THEN
    print(f"{swimmers}")
    assert swimmers_brand != None
    assert swimmers_brand.name != None
    assert swimmers_brand.name == swimmers
    assert swimmers_brand._agent_credit != None
    assert swimmers_brand._agent_debt != None
    assert swimmers_brand._agent_agenda_credit != None
    assert swimmers_brand._agent_agenda_debt != None
    assert swimmers_brand._allylinks_set_by_world_road == usa_road


def test_brandunit_set_name_WorksCorrectly():
    # GIVEN
    swim_text = "swimmers"
    swim_brand = brandunit_shop(name=swim_text)
    assert swim_brand.name == swim_text

    # WHEN
    water_text = "water people"
    swim_brand.set_name(name=water_text)

    # THEN
    assert swim_brand.name == water_text


def test_brandunit_set_attr_WorksCorrectly():
    # GIVEN
    swim_text = "swimmers"
    swim_brand = brandunit_shop(name=swim_text)
    assert swim_brand._allylinks_set_by_world_road is None

    # WHEN
    water_road = "src,sports,water"
    swim_brand.set_attr(_allylinks_set_by_world_road=water_road)

    # THEN
    assert swim_brand._allylinks_set_by_world_road == water_road


def test_brandunit_shop_WhenSingleAllyCorrectlyRemoves_allylinks_set_by_world_road():
    # GIVEN
    swimmers = "swimmers"
    usa_road = "src,nation-states,USA"

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        swimmers_brand = brandunit_shop(
            name=swimmers,
            _single_ally=True,
            _allylinks_set_by_world_road=usa_road,
        )
    assert (
        str(excinfo.value)
        == f"_allylinks_set_by_world_road cannot be '{usa_road}' for a single_ally BrandUnit. It must have no value."
    )


def test_brandunit_set_allylink_worksCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_ally = allylink_shop(name=todd_text, creditor_weight=13, debtor_weight=7)
    mery_ally = allylink_shop(name=mery_text, creditor_weight=23, debtor_weight=5)

    swimmers_brand = brandunit_shop(name="swimmers", _allys={})

    # WHEN
    swimmers_brand.set_allylink(todd_ally)
    swimmers_brand.set_allylink(mery_ally)

    # THEN
    swimmers_allys = {todd_ally.name: todd_ally, mery_ally.name: mery_ally}
    assert swimmers_brand._allys == swimmers_allys


def test_brandunit_del_allylink_worksCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_ally = allylink_shop(name=todd_text)
    mery_ally = allylink_shop(name=mery_text)
    swimmers_allys = {todd_ally.name: todd_ally, mery_ally.name: mery_ally}
    swimmers_brand = brandunit_shop(name="swimmers", _allys={})
    swimmers_brand.set_allylink(todd_ally)
    swimmers_brand.set_allylink(mery_ally)
    assert len(swimmers_brand._allys) == 2
    assert swimmers_brand._allys == swimmers_allys

    # WHEN
    swimmers_brand.del_allylink(name=todd_text)

    # THEN
    assert len(swimmers_brand._allys) == 1
    assert swimmers_brand._allys.get(todd_text) is None


def test_brandunit_clear_allylinks_worksCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_ally = allylink_shop(name=todd_text)
    mery_ally = allylink_shop(name=mery_text)
    swimmers_allys = {todd_ally.name: todd_ally, mery_ally.name: mery_ally}
    swimmers_brand = brandunit_shop(name="swimmers", _allys={})
    swimmers_brand.set_allylink(todd_ally)
    swimmers_brand.set_allylink(mery_ally)
    assert len(swimmers_brand._allys) == 2
    assert swimmers_brand._allys == swimmers_allys

    # WHEN
    swimmers_brand.clear_allylinks()

    # THEN
    assert len(swimmers_brand._allys) == 0
    assert swimmers_brand._allys.get(todd_text) is None


def test_Brandunit_reset_agent_importance_WorkCorrectly():
    # GIVEN
    maria_name = "maria"
    maria_brand = brandunit_shop(
        name=maria_name,
        _agent_credit=0.33,
        _agent_debt=0.44,
        _agent_agenda_credit=0.13,
        _agent_agenda_debt=0.23,
    )
    print(f"{maria_brand}")
    assert maria_brand._agent_credit == 0.33
    assert maria_brand._agent_debt == 0.44
    assert maria_brand._agent_agenda_credit == 0.13
    assert maria_brand._agent_agenda_debt == 0.23

    # WHEN
    maria_brand.reset_agent_credit_debt()

    # THEN
    assert maria_brand._agent_credit == 0
    assert maria_brand._agent_debt == 0
    assert maria_brand._agent_agenda_credit == 0
    assert maria_brand._agent_agenda_debt == 0


def test_Brandunit_reset_agent_importance_reset_allylinks():
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
    bikers_brand = brandunit_shop(
        name=bikers_name,
        _allys={},
        _agent_credit=0.33,
        _agent_debt=0.44,
        _agent_agenda_credit=0.1,
        _agent_agenda_debt=0.2,
    )
    bikers_brand.set_allylink(allylink=todd_ally)
    bikers_brand.set_allylink(allylink=mery_ally)
    print(f"{bikers_brand}")
    biker_allylink_todd = bikers_brand._allys.get(todd_text)
    assert biker_allylink_todd._agent_credit == 0.13
    assert biker_allylink_todd._agent_debt == 0.7
    assert biker_allylink_todd._agent_agenda_credit == 0.53
    assert biker_allylink_todd._agent_agenda_debt == 0.77

    biker_allylink_mery = bikers_brand._allys.get(mery_text)
    assert biker_allylink_mery._agent_credit == 0.23
    assert biker_allylink_mery._agent_debt == 0.5
    assert biker_allylink_mery._agent_agenda_credit == 0.54
    assert biker_allylink_mery._agent_agenda_debt == 0.57

    # WHEN
    bikers_brand.reset_agent_credit_debt()

    # THEN
    assert biker_allylink_todd._agent_credit == 0
    assert biker_allylink_todd._agent_debt == 0
    assert biker_allylink_todd._agent_agenda_credit == 0
    assert biker_allylink_todd._agent_agenda_debt == 0
    assert biker_allylink_mery._agent_credit == 0
    assert biker_allylink_mery._agent_debt == 0
    assert biker_allylink_mery._agent_agenda_credit == 0
    assert biker_allylink_mery._agent_agenda_debt == 0


def test_BrandUnit_allylink_meld_BaseScenarioWorks():
    # GIVEN
    todd_ally = allylink_shop(name="Todd")
    merry_ally = allylink_shop(name="Merry")
    x1_name = "bikers"
    x1_brand = brandunit_shop(name=x1_name, _allys={})
    x1_brand.set_allylink(allylink=todd_ally)
    x1_brand.set_allylink(allylink=merry_ally)

    x2_brand = brandunit_shop(name=x1_name, _allys={})

    # WHEN
    x1_brand.meld(other_brand=x2_brand)
    print(f"{x1_brand.name=} {x2_brand.name=}")

    # THEN
    assert len(x1_brand._allys) == 2


def test_BrandUnit_allylink_meld_GainScenarioWorks():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_ally = allylink_shop(name=todd_text, creditor_weight=13, debtor_weight=7)
    mery_ally = allylink_shop(name=mery_text, creditor_weight=23, debtor_weight=5)
    x1_name = "bikers"
    x1_brand = brandunit_shop(name=x1_name, _allys={})

    x2_brand = brandunit_shop(name=x1_name, _allys={})
    x2_brand.set_allylink(allylink=todd_ally)
    x2_brand.set_allylink(allylink=mery_ally)

    # WHEN
    x1_brand.meld(other_brand=x2_brand)

    # THEN
    assert len(x1_brand._allys) == 2
    assert x1_brand._allys.get(todd_text) != None


def test_BrandUnit_meld_RaiseSameNameException():
    # GIVEN
    todd_text = "Todd"
    todd_brand = brandunit_shop(name=todd_text)
    mery_text = "Merry"
    mery_brand = brandunit_shop(name=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_brand.meld(mery_brand)
    assert (
        str(excinfo.value)
        == f"Meld fail BrandUnit {todd_brand.name} .name='{todd_brand.name}' not the same as .name='{mery_brand.name}"
    )


def test_BrandUnit_meld_RaiseSameUIDException():
    # GIVEN
    todd_text = "Todd"
    todd3_brand = brandunit_shop(name=todd_text, uid=3)
    todd5_brand = brandunit_shop(name=todd_text, uid=5)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd3_brand.meld(todd5_brand)
    assert (
        str(excinfo.value)
        == f"Meld fail BrandUnit {todd3_brand.name} .uid='{todd3_brand.uid}' not the same as .uid='{todd5_brand.uid}"
    )


def test_brandUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    swimmers = "swimmers"

    # WHEN
    swimmers_brand = brandunit_shop(name=swimmers)
    print(f"{swimmers}")

    # THEN
    ee_dict = swimmers_brand.get_dict()
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
    teachers_brand = brandunit_shop(
        name=str_teacher, _allys=allylinks_dict, _allylinks_set_by_world_road=swim_road
    )

    # WHEN
    teachers_dict = teachers_brand.get_dict()

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


def test_brandunit_get_from_JSON_SimpleExampleWorks():
    # GIVEN
    str_name = "Marie"
    marie_name = AllyName(str_name)
    marie_allylink = allylink_shop(name=marie_name, creditor_weight=29, debtor_weight=3)
    allylinks_dict = {marie_allylink.name: marie_allylink}

    str_teacher = "teachers"
    swim_road = "road_str"
    teacher_brand = brandunit_shop(
        name=str_teacher, _allys=allylinks_dict, _allylinks_set_by_world_road=swim_road
    )
    teacher_dict = teacher_brand.get_dict()
    _allylinks_set_by_world_road_text = "_allylinks_set_by_world_road"
    print(f"{teacher_dict.get(_allylinks_set_by_world_road_text)=}")
    brands_dict = {"teachers": teacher_dict}

    teachers_json = x_get_json(dict_x=brands_dict)
    print(f"{teachers_json.find(_allylinks_set_by_world_road_text)=}")
    assert teachers_json != None
    assert x_is_json(json_x=teachers_json)

    # WHEN
    brandunits_obj_dict = brandunits_get_from_json(brandunits_json=teachers_json)

    # THEN
    assert brandunits_obj_dict != None
    teachers_obj_check_dict = {teacher_brand.name: teacher_brand}
    print(f"    {brandunits_obj_dict=}")
    allylinks_set_by_world_road_text = "_allylinks_set_by_world_road"
    print(f"{teachers_obj_check_dict.get(allylinks_set_by_world_road_text)=}")
    print(f"{teachers_obj_check_dict=}")
    assert brandunits_obj_dict == teachers_obj_check_dict


def test_brankLink_exists():
    # GIVEN
    bikers_name = BrandName("bikers")

    # WHEN
    brand_link_x = brandlink_shop(name=bikers_name)

    # THEN
    assert brand_link_x.name == bikers_name
    assert brand_link_x.creditor_weight == 1.0
    assert brand_link_x.debtor_weight == 1.0

    # WHEN
    bikers_creditor_weight = 3.0
    bikers_debtor_weight = 5.0

    brand_link_x = brandlink_shop(
        name=bikers_name,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debtor_weight,
    )

    # THEN
    assert brand_link_x.creditor_weight == 3.0
    assert brand_link_x.debtor_weight == 5.0


def test_brankLink_set_agent_importanceCorrectly():
    # GIVEN
    bikers_name = BrandName("bikers")
    bikers_creditor_weight = 3.0
    bikers_debt_weight = 6.0
    brandlinks_sum_creditor_weight = 60
    brandlinks_sum_debtor_weight = 60
    idea_agent_importance = 1
    brand_heir_x = brandheir_shop(
        name=bikers_name,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debt_weight,
    )

    # WHEN
    brand_heir_x.set_agent_credit_debt(
        idea_agent_importance=idea_agent_importance,
        brandheirs_creditor_weight_sum=brandlinks_sum_creditor_weight,
        brandheirs_debtor_weight_sum=brandlinks_sum_debtor_weight,
    )

    # THEN
    assert brand_heir_x._agent_credit == 0.05
    assert brand_heir_x._agent_debt == 0.1


def test_brandlink_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    bikers_name = BrandName("bikers")
    bikers_creditor_weight = 3.0
    bikers_debtor_weight = 5.0
    bikers_link = brandlink_shop(
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


def test_brandlinks_get_from_JSON_SimpleExampleWorks():
    # GIVEN
    str_teacher = "teachers"
    teacher_brandlink = brandlink_shop(
        name=str_teacher, creditor_weight=103, debtor_weight=155
    )
    teacher_dict = teacher_brandlink.get_dict()
    brandlinks_dict = {teacher_brandlink.name: teacher_dict}

    teachers_json = x_get_json(dict_x=brandlinks_dict)
    assert teachers_json != None
    assert x_is_json(json_x=teachers_json)

    # WHEN
    brandlinks_obj_dict = brandlinks_get_from_json(brandlinks_json=teachers_json)

    # THEN
    assert brandlinks_obj_dict != None
    teachers_obj_check_dict = {teacher_brandlink.name: teacher_brandlink}
    print(f"    {brandlinks_obj_dict=}")
    print(f"{teachers_obj_check_dict=}")
    assert brandlinks_obj_dict == teachers_obj_check_dict


def test_Brandline_exists():
    # GIVEN
    bikers_name = BrandName("bikers")
    brandline_x = Brandline(name=bikers_name, _agent_credit=0.33, _agent_debt=0.55)
    assert brandline_x.name == bikers_name
    assert brandline_x._agent_credit == 0.33
    assert brandline_x._agent_debt == 0.55

    # WHEN
    brandline_x.add_agent_credit_debt(agent_credit=0.11, agent_debt=0.2)

    # THEN
    assert brandline_x._agent_credit == 0.44
    assert brandline_x._agent_debt == 0.75
