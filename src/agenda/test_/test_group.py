from src.agenda.party import PartyID, partylink_shop
from src.agenda.group import (
    BalanceLine,
    balanceline_shop,
    GroupUnit,
    groupunit_shop,
    GroupBrand,
    BalanceLink,
    balancelink_shop,
    balancelinks_get_from_json,
    balanceheir_shop,
    get_from_json as groupunits_get_from_json,
)
from src._prime.road import (
    get_default_economy_root_roadnode as root_label,
    create_road,
)
from src.tools.python import x_is_json, x_get_json
from pytest import raises as pytest_raises


def test_GroupBrand_exists():
    bikers_brand = GroupBrand("bikers")
    assert bikers_brand != None
    assert str(type(bikers_brand)).find(".group.GroupBrand") > 0


def test_GroupUnit_exists():
    # GIVEN
    swim_text = "swimmers"
    # WHEN
    swim_groupunit = GroupUnit(brand=swim_text)
    # THEN
    assert swim_groupunit != None
    assert swim_groupunit.brand == swim_text
    assert swim_groupunit.uid is None
    assert swim_groupunit.single_party_id is None
    assert swim_groupunit._single_party is None
    assert swim_groupunit._partys is None
    assert swim_groupunit._agenda_credit is None
    assert swim_groupunit._agenda_debt is None
    assert swim_groupunit._agenda_intent_credit is None
    assert swim_groupunit._agenda_intent_debt is None
    assert swim_groupunit._partylinks_set_by_economy_road is None


def test_groupunit_shop_ReturnsCorrectObj():
    # GIVEN
    swimmers = "swimmers"
    nation_road = create_road(root_label(), "nation-states")
    usa_road = create_road(nation_road, "USA")

    # WHEN
    swimmers_group = groupunit_shop(
        brand=swimmers,
        _agenda_credit=0.33,
        _agenda_debt=0.44,
        _agenda_intent_credit=0.66,
        _agenda_intent_debt=0.77,
        _partylinks_set_by_economy_road=usa_road,
    )

    # THEN
    print(f"{swimmers}")
    assert swimmers_group != None
    assert swimmers_group.brand != None
    assert swimmers_group.brand == swimmers
    assert swimmers_group._agenda_credit != None
    assert swimmers_group._agenda_debt != None
    assert swimmers_group._agenda_intent_credit != None
    assert swimmers_group._agenda_intent_debt != None
    assert swimmers_group._partylinks_set_by_economy_road == usa_road


def test_GroupUnit_set_brand_WorksCorrectly():
    # GIVEN
    swim_text = "swimmers"
    swim_group = groupunit_shop(brand=swim_text)
    assert swim_group.brand == swim_text

    # WHEN
    water_text = "water people"
    swim_group.set_brand(brand=water_text)

    # THEN
    assert swim_group.brand == water_text


def test_GroupUnit_set_attr_WorksCorrectly():
    # GIVEN
    swim_text = "swimmers"
    swim_group = groupunit_shop(brand=swim_text)
    assert swim_group._partylinks_set_by_economy_road is None

    # WHEN
    sports_road = create_road(root_label(), "sports")
    water_road = create_road(sports_road, "water")
    swim_group.set_attr(_partylinks_set_by_economy_road=water_road)

    # THEN
    assert swim_group._partylinks_set_by_economy_road == water_road


def test_groupunit_shop_WhenSinglePartyCorrectlyRemoves_partylinks_set_by_economy_road():
    # GIVEN
    swimmers = "swimmers"
    nation_road = create_road(root_label(), "nation-states")
    usa_road = create_road(nation_road, "USA")

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        swimmers_group = groupunit_shop(
            brand=swimmers,
            _single_party=True,
            _partylinks_set_by_economy_road=usa_road,
        )
    assert (
        str(excinfo.value)
        == f"_partylinks_set_by_economy_road cannot be '{usa_road}' for a single_party GroupUnit. It must have no value."
    )


def test_GroupUnit_set_partylink_worksCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_party = partylink_shop(party_id=todd_text, creditor_weight=13, debtor_weight=7)
    mery_party = partylink_shop(party_id=mery_text, creditor_weight=23, debtor_weight=5)

    swimmers_group = groupunit_shop(brand="swimmers", _partys={})

    # WHEN
    swimmers_group.set_partylink(todd_party)
    swimmers_group.set_partylink(mery_party)

    # THEN
    swimmers_partys = {todd_party.party_id: todd_party, mery_party.party_id: mery_party}
    assert swimmers_group._partys == swimmers_partys


def test_GroupUnit_get_partylink_worksCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    swimmers_group = groupunit_shop(brand="swimmers", _partys={})
    swimmers_group.set_partylink(partylink_shop(todd_text, 13, 7))
    swimmers_group.set_partylink(partylink_shop(mery_text, 23, 5))

    # WHEN / THEN
    assert swimmers_group.get_partylink(todd_text) != None
    assert swimmers_group.get_partylink(mery_text) != None
    assert swimmers_group.get_partylink("todd") is None


def test_GroupUnit_partylink_exists_worksCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    swimmers_group = groupunit_shop(brand="swimmers", _partys={})
    swimmers_group.set_partylink(partylink_shop(todd_text, 13, 7))
    swimmers_group.set_partylink(partylink_shop(mery_text, 23, 5))

    # WHEN / THEN
    assert swimmers_group.partylink_exists(todd_text)
    assert swimmers_group.partylink_exists(mery_text)
    assert swimmers_group.partylink_exists("todd") == False


def test_GroupUnit_del_partylink_worksCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_party = partylink_shop(party_id=todd_text)
    mery_party = partylink_shop(party_id=mery_text)
    swimmers_partys = {todd_party.party_id: todd_party, mery_party.party_id: mery_party}
    swimmers_group = groupunit_shop(brand="swimmers", _partys={})
    swimmers_group.set_partylink(todd_party)
    swimmers_group.set_partylink(mery_party)
    assert len(swimmers_group._partys) == 2
    assert swimmers_group._partys == swimmers_partys

    # WHEN
    swimmers_group.del_partylink(party_id=todd_text)

    # THEN
    assert len(swimmers_group._partys) == 1
    assert swimmers_group._partys.get(todd_text) is None


def test_GroupUnit_clear_partylinks_worksCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_party = partylink_shop(party_id=todd_text)
    mery_party = partylink_shop(party_id=mery_text)
    swimmers_partys = {todd_party.party_id: todd_party, mery_party.party_id: mery_party}
    swimmers_group = groupunit_shop(brand="swimmers", _partys={})
    swimmers_group.set_partylink(todd_party)
    swimmers_group.set_partylink(mery_party)
    assert len(swimmers_group._partys) == 2
    assert swimmers_group._partys == swimmers_partys

    # WHEN
    swimmers_group.clear_partylinks()

    # THEN
    assert len(swimmers_group._partys) == 0
    assert swimmers_group._partys.get(todd_text) is None


def test_GroupUnit_reset_agenda_importance_WorkCorrectly():
    # GIVEN
    maria_brand = "maria"
    maria_group = groupunit_shop(
        brand=maria_brand,
        _agenda_credit=0.33,
        _agenda_debt=0.44,
        _agenda_intent_credit=0.13,
        _agenda_intent_debt=0.23,
    )
    print(f"{maria_group}")
    assert maria_group._agenda_credit == 0.33
    assert maria_group._agenda_debt == 0.44
    assert maria_group._agenda_intent_credit == 0.13
    assert maria_group._agenda_intent_debt == 0.23

    # WHEN
    maria_group.reset_agenda_credit_debt()

    # THEN
    assert maria_group._agenda_credit == 0
    assert maria_group._agenda_debt == 0
    assert maria_group._agenda_intent_credit == 0
    assert maria_group._agenda_intent_debt == 0


def test_GroupUnit_reset_agenda_importance_reset_partylinks():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_party = partylink_shop(
        party_id=todd_text,
        _agenda_credit=0.13,
        _agenda_debt=0.7,
        _agenda_intent_credit=0.53,
        _agenda_intent_debt=0.77,
    )
    mery_party = partylink_shop(
        party_id=mery_text,
        _agenda_credit=0.23,
        _agenda_debt=0.5,
        _agenda_intent_credit=0.54,
        _agenda_intent_debt=0.57,
    )
    bikers_partys = {todd_party.party_id: todd_party, mery_party.party_id: mery_party}
    bikers_brand = "bikers"
    bikers_group = groupunit_shop(
        brand=bikers_brand,
        _partys={},
        _agenda_credit=0.33,
        _agenda_debt=0.44,
        _agenda_intent_credit=0.1,
        _agenda_intent_debt=0.2,
    )
    bikers_group.set_partylink(partylink=todd_party)
    bikers_group.set_partylink(partylink=mery_party)
    print(f"{bikers_group}")
    biker_partylink_todd = bikers_group._partys.get(todd_text)
    assert biker_partylink_todd._agenda_credit == 0.13
    assert biker_partylink_todd._agenda_debt == 0.7
    assert biker_partylink_todd._agenda_intent_credit == 0.53
    assert biker_partylink_todd._agenda_intent_debt == 0.77

    biker_partylink_mery = bikers_group._partys.get(mery_text)
    assert biker_partylink_mery._agenda_credit == 0.23
    assert biker_partylink_mery._agenda_debt == 0.5
    assert biker_partylink_mery._agenda_intent_credit == 0.54
    assert biker_partylink_mery._agenda_intent_debt == 0.57

    # WHEN
    bikers_group.reset_agenda_credit_debt()

    # THEN
    assert biker_partylink_todd._agenda_credit == 0
    assert biker_partylink_todd._agenda_debt == 0
    assert biker_partylink_todd._agenda_intent_credit == 0
    assert biker_partylink_todd._agenda_intent_debt == 0
    assert biker_partylink_mery._agenda_credit == 0
    assert biker_partylink_mery._agenda_debt == 0
    assert biker_partylink_mery._agenda_intent_credit == 0
    assert biker_partylink_mery._agenda_intent_debt == 0


def test_GroupUnit_partylink_meld_BaseScenarioWorks():
    # GIVEN
    todd_party = partylink_shop(party_id="Todd")
    merry_party = partylink_shop(party_id="Merry")
    x1_brand = "bikers"
    x1_group = groupunit_shop(brand=x1_brand, _partys={})
    x1_group.set_partylink(partylink=todd_party)
    x1_group.set_partylink(partylink=merry_party)

    x2_group = groupunit_shop(brand=x1_brand, _partys={})

    # WHEN
    x1_group.meld(other_group=x2_group)
    print(f"{x1_group.brand=} {x2_group.brand=}")

    # THEN
    assert len(x1_group._partys) == 2


def test_GroupUnit_partylink_meld_GainScenarioWorks():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_party = partylink_shop(party_id=todd_text, creditor_weight=13, debtor_weight=7)
    mery_party = partylink_shop(party_id=mery_text, creditor_weight=23, debtor_weight=5)
    x1_brand = "bikers"
    x1_group = groupunit_shop(brand=x1_brand, _partys={})

    x2_group = groupunit_shop(brand=x1_brand, _partys={})
    x2_group.set_partylink(partylink=todd_party)
    x2_group.set_partylink(partylink=mery_party)

    # WHEN
    x1_group.meld(other_group=x2_group)

    # THEN
    assert len(x1_group._partys) == 2
    assert x1_group._partys.get(todd_text) != None


def test_GroupUnit_meld_RaiseSameparty_idException():
    # GIVEN
    todd_text = "Todd"
    todd_group = groupunit_shop(brand=todd_text)
    mery_text = "Merry"
    mery_group = groupunit_shop(brand=mery_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_group.meld(mery_group)
    assert (
        str(excinfo.value)
        == f"Meld fail GroupUnit {todd_group.brand} .brand='{todd_group.brand}' not the same as .brand='{mery_group.brand}"
    )


def test_GroupUnit_meld_RaiseSameUIDException():
    # GIVEN
    todd_text = "Todd"
    todd3_group = groupunit_shop(brand=todd_text, uid=3)
    todd5_group = groupunit_shop(brand=todd_text, uid=5)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd3_group.meld(todd5_group)
    assert (
        str(excinfo.value)
        == f"Meld fail GroupUnit {todd3_group.brand} .uid='{todd3_group.uid}' not the same as .uid='{todd5_group.uid}"
    )


def test_GroupUnit_get_dict_ReturnsDictWithAttrsCorrectlySet():
    # GIVEN
    todd_text = "Todd"
    todd_uid = 33
    todd_party_id = 55
    todd_group = groupunit_shop(
        brand=todd_text, uid=todd_uid, single_party_id=todd_party_id, _single_party=True
    )
    sue_text = "Sue"
    todd_group.set_partylink(partylink_shop(party_id=sue_text))
    x_partylinks_set_by_economy_road = 44
    todd_group.set_attr(x_partylinks_set_by_economy_road)

    assert todd_group.brand == todd_text
    assert todd_group.uid == todd_uid
    assert todd_group.single_party_id == todd_party_id
    assert todd_group._single_party
    assert len(todd_group._partys) == 1
    assert (
        todd_group._partylinks_set_by_economy_road == x_partylinks_set_by_economy_road
    )

    # WHEN
    todd_dict = todd_group.get_dict()

    # THEN
    assert todd_dict["brand"] == todd_text
    assert todd_dict["uid"] == todd_uid
    assert todd_dict["single_party_id"] == todd_party_id
    assert todd_dict["_single_party"]
    assert len(todd_dict["_partys"]) == 1
    assert (
        todd_dict["_partylinks_set_by_economy_road"] == x_partylinks_set_by_economy_road
    )


def test_GroupUnit_get_dict_ReturnsDictWithAttrsCorrectlyEmpty():
    # GIVEN
    todd_text = "Todd"
    todd_group = groupunit_shop(brand=todd_text)
    assert todd_group.uid is None
    assert todd_group.single_party_id is None
    assert todd_group._single_party is False
    assert todd_group._partys == {}
    assert todd_group._partylinks_set_by_economy_road is None

    # WHEN
    todd_dict = todd_group.get_dict()

    # THEN
    assert todd_dict.get("uid") is None
    assert todd_dict.get("single_party_id") is None
    assert todd_dict.get("_single_party") is None
    assert todd_dict.get("_partys") is None
    assert todd_dict.get("_partylinks_set_by_economy_road") is None


def test_GroupUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    swimmers = "swimmers"

    # WHEN
    swimmers_group = groupunit_shop(brand=swimmers)
    print(f"{swimmers}")

    # THEN
    ee_dict = swimmers_group.get_dict()
    assert ee_dict != None
    # assert ee_dict == {"brand": swimmers, "uid": 2}
    assert ee_dict == {"brand": swimmers}

    # GIVEN
    sue_text = "Marie"
    marie_partylink = partylink_shop(
        party_id=sue_text, creditor_weight=29, debtor_weight=3
    )
    partylinks_dict = {marie_partylink.party_id: marie_partylink}
    marie_json_dict = {
        sue_text: {
            "party_id": sue_text,
            "creditor_weight": 29,
            "debtor_weight": 3,
        }
    }

    teacher_text = "teachers"
    teacher_uid = 55
    swim_road = "swim"
    teachers_group = groupunit_shop(
        brand=teacher_text,
        uid=teacher_uid,
        _partys=partylinks_dict,
        _partylinks_set_by_economy_road=swim_road,
    )

    # WHEN
    teachers_dict = teachers_group.get_dict()

    # THEN
    print(f"{marie_json_dict=}")
    assert teachers_dict == {
        "brand": teacher_text,
        "uid": teacher_uid,
        "_partys": marie_json_dict,
        "_partylinks_set_by_economy_road": swim_road,
    }


def test_GroupUnit_get_from_JSON_SimpleExampleWorks():
    # GIVEN
    sue_text = "Sue"
    marie_partylink = partylink_shop(
        party_id=sue_text, creditor_weight=29, debtor_weight=3
    )
    partylinks_dict = {marie_partylink.party_id: marie_partylink}

    teacher_text = "teachers"
    swim_road = "swim"
    teacher_group = groupunit_shop(
        brand=teacher_text,
        _partys=partylinks_dict,
        _partylinks_set_by_economy_road=swim_road,
    )
    teacher_dict = teacher_group.get_dict()
    _partylinks_set_by_economy_road_text = "_partylinks_set_by_economy_road"
    print(f"{teacher_dict.get(_partylinks_set_by_economy_road_text)=}")
    groups_dict = {"teachers": teacher_dict}

    teachers_json = x_get_json(dict_x=groups_dict)
    print(f"{teachers_json.find(_partylinks_set_by_economy_road_text)=}")
    assert teachers_json != None
    assert x_is_json(json_x=teachers_json)

    # WHEN
    groupunits_obj_dict = groupunits_get_from_json(groupunits_json=teachers_json)

    # THEN
    assert groupunits_obj_dict != None
    teachers_obj_check_dict = {teacher_group.brand: teacher_group}
    print(f"    {groupunits_obj_dict=}")
    partylinks_set_by_economy_road_text = "_partylinks_set_by_economy_road"
    print(f"{teachers_obj_check_dict.get(partylinks_set_by_economy_road_text)=}")
    print(f"{teachers_obj_check_dict=}")
    assert groupunits_obj_dict == teachers_obj_check_dict


def test_BalanceLink_exists():
    # GIVEN
    bikers_brand = GroupBrand("bikers")

    # WHEN
    bikers_balancelink = BalanceLink(brand=bikers_brand)

    # THEN
    assert bikers_balancelink.brand == bikers_brand
    assert bikers_balancelink.creditor_weight == 1.0
    assert bikers_balancelink.debtor_weight == 1.0


def test_balancelink_shop_ReturnsCorrectObj():
    # GIVEN
    bikers_brand = GroupBrand("bikers")
    bikers_creditor_weight = 3.0
    bikers_debtor_weight = 5.0

    # WHEN
    bikers_balancelink = balancelink_shop(
        brand=bikers_brand,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debtor_weight,
    )

    # THEN
    assert bikers_balancelink.creditor_weight == bikers_creditor_weight
    assert bikers_balancelink.debtor_weight == bikers_debtor_weight


def test_BalanceHeir_set_agenda_importance_CorrectlySetsAttr():
    # GIVEN
    bikers_brand = GroupBrand("bikers")
    bikers_creditor_weight = 3.0
    bikers_debt_weight = 6.0
    balancelinks_sum_creditor_weight = 60
    balancelinks_sum_debtor_weight = 60
    idea_agenda_importance = 1
    group_heir_x = balanceheir_shop(
        brand=bikers_brand,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debt_weight,
    )

    # WHEN
    group_heir_x.set_agenda_credit_debt(
        idea_agenda_importance=idea_agenda_importance,
        balanceheirs_creditor_weight_sum=balancelinks_sum_creditor_weight,
        balanceheirs_debtor_weight_sum=balancelinks_sum_debtor_weight,
    )

    # THEN
    assert group_heir_x._agenda_credit == 0.05
    assert group_heir_x._agenda_debt == 0.1


def test_BalanceLink_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    bikers_brand = GroupBrand("bikers")
    bikers_creditor_weight = 3.0
    bikers_debtor_weight = 5.0
    bikers_link = balancelink_shop(
        brand=bikers_brand,
        creditor_weight=bikers_creditor_weight,
        debtor_weight=bikers_debtor_weight,
    )

    print(f"{bikers_link}")

    # WHEN
    biker_dict = bikers_link.get_dict()

    # THEN
    assert biker_dict != None
    assert biker_dict == {
        "brand": bikers_link.brand,
        "creditor_weight": bikers_link.creditor_weight,
        "debtor_weight": bikers_link.debtor_weight,
    }


def test_balancelinks_get_from_JSON_SimpleExampleWorks():
    # GIVEN
    teacher_text = "teachers"
    teacher_balancelink = balancelink_shop(
        brand=teacher_text, creditor_weight=103, debtor_weight=155
    )
    teacher_dict = teacher_balancelink.get_dict()
    balancelinks_dict = {teacher_balancelink.brand: teacher_dict}

    teachers_json = x_get_json(dict_x=balancelinks_dict)
    assert teachers_json != None
    assert x_is_json(json_x=teachers_json)

    # WHEN
    balancelinks_obj_dict = balancelinks_get_from_json(balancelinks_json=teachers_json)

    # THEN
    assert balancelinks_obj_dict != None
    teachers_obj_check_dict = {teacher_balancelink.brand: teacher_balancelink}
    print(f"    {balancelinks_obj_dict=}")
    print(f"{teachers_obj_check_dict=}")
    assert balancelinks_obj_dict == teachers_obj_check_dict


def test_BalanceLine_exists():
    # GIVEN
    bikers_brand = GroupBrand("bikers")
    bikers_agenda_credit = 0.33
    bikers_agenda_debt = 0.55

    # WHEN
    bikers_balanceline = BalanceLine(
        brand=bikers_brand,
        _agenda_credit=bikers_agenda_credit,
        _agenda_debt=bikers_agenda_debt,
    )

    # THEN
    assert bikers_balanceline.brand == bikers_brand
    assert bikers_balanceline._agenda_credit == bikers_agenda_credit
    assert bikers_balanceline._agenda_debt == bikers_agenda_debt


def test_balanceline_shop_ReturnsCorrectObj_exists():
    # GIVEN
    bikers_brand = GroupBrand("bikers")
    bikers_brand = bikers_brand
    bikers_agenda_credit = 0.33
    bikers_agenda_debt = 0.55

    # WHEN
    biker_balanceline = balanceline_shop(
        brand=bikers_brand,
        _agenda_credit=bikers_agenda_credit,
        _agenda_debt=bikers_agenda_debt,
    )

    assert biker_balanceline != None
    assert biker_balanceline.brand == bikers_brand
    assert biker_balanceline._agenda_credit == bikers_agenda_credit
    assert biker_balanceline._agenda_debt == bikers_agenda_debt


def test_BalanceLine_add_agenda_credit_debt_CorrectlyChangesAttr():
    # GIVEN
    bikers_brand = GroupBrand("bikers")
    bikers_balanceline = balanceline_shop(
        brand=bikers_brand, _agenda_credit=0.33, _agenda_debt=0.55
    )
    assert bikers_balanceline.brand == bikers_brand
    assert bikers_balanceline._agenda_credit == 0.33
    assert bikers_balanceline._agenda_debt == 0.55

    # WHEN
    bikers_balanceline.add_agenda_credit_debt(agenda_credit=0.11, agenda_debt=0.2)

    # THEN
    assert bikers_balanceline._agenda_credit == 0.44
    assert bikers_balanceline._agenda_debt == 0.75
