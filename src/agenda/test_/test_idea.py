from src.agenda.party import PartyID, partylink_shop
from src.agenda.idea import (
    BalanceLine,
    balanceline_shop,
    IdeaUnit,
    ideaunit_shop,
    IdeaID,
    BalanceLink,
    balancelink_shop,
    balancelinks_get_from_json,
    balanceheir_shop,
    get_from_json as ideaunits_get_from_json,
    get_ideaunit_from_dict,
    get_ideaunits_from_dict,
)
from src._road.road import (
    get_default_real_id_roadnode as root_label,
    create_road,
    validate_roadnode,
    default_road_delimiter_if_none,
)
from src._instrument.python import x_is_json, get_json_from_dict
from pytest import raises as pytest_raises


def test_IdeaID_exists():
    bikers_idea_id = IdeaID("bikers")
    assert bikers_idea_id != None
    assert str(type(bikers_idea_id)).find(".idea.IdeaID") > 0


def test_IdeaUnit_exists():
    # GIVEN
    swim_text = ",swimmers"
    # WHEN
    swim_ideaunit = IdeaUnit(idea_id=swim_text)
    # THEN
    assert swim_ideaunit != None
    assert swim_ideaunit.idea_id == swim_text
    assert swim_ideaunit._party_mirror is None
    assert swim_ideaunit._partys is None
    assert swim_ideaunit._agenda_cred is None
    assert swim_ideaunit._agenda_debt is None
    assert swim_ideaunit._agenda_intent_cred is None
    assert swim_ideaunit._agenda_intent_debt is None
    assert swim_ideaunit._road_delimiter is None


def test_ideaunit_shop_ReturnsCorrectObj():
    # GIVEN
    swim_text = ",swimmers"
    nation_road = create_road(root_label(), "nation-states")
    usa_road = create_road(nation_road, "USA")

    # WHEN
    swim_ideaunit = ideaunit_shop(idea_id=swim_text)

    # THEN
    print(f"{swim_text}")
    assert swim_ideaunit != None
    assert swim_ideaunit.idea_id != None
    assert swim_ideaunit.idea_id == swim_text
    assert swim_ideaunit._agenda_cred == 0
    assert swim_ideaunit._agenda_debt == 0
    assert swim_ideaunit._agenda_intent_cred == 0
    assert swim_ideaunit._agenda_intent_debt == 0
    assert swim_ideaunit._road_delimiter == default_road_delimiter_if_none()


def test_ideaunit_shop_ReturnsCorrectObj_road_delimiter():
    # GIVEN
    swim_text = "/swimmers"
    slash_text = "/"

    # WHEN
    swim_ideaunit = ideaunit_shop(idea_id=swim_text, _road_delimiter=slash_text)

    # THEN
    assert swim_ideaunit._road_delimiter == slash_text


def test_IdeaUnit_set_idea_id_RaisesErrorIfParameterContains_road_delimiter_And_party_mirror_True():
    # GIVEN
    slash_text = "/"
    bob_text = f"Bob{slash_text}Texas"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        ideaunit_shop(bob_text, _party_mirror=True, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{bob_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_IdeaUnit_set_idea_id_RaisesErrorIfParameterDoesNotContain_road_delimiter_party_mirror_False():
    # GIVEN
    comma_text = ","
    texas_text = f"Texas{comma_text}Arkansas"

    # WHEN / THEN
    slash_text = "/"
    with pytest_raises(Exception) as excinfo:
        ideaunit_shop(idea_id=texas_text, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{texas_text}' needs to not be a RoadNode. Must contain delimiter: '{slash_text}'"
    )


def test_IdeaUnit_set_idea_id_SetsAttrCorrectly():
    # GIVEN
    swim_text = ",swimmers"
    swim_idea = ideaunit_shop(idea_id=swim_text)
    assert swim_idea.idea_id == swim_text

    # WHEN
    water_text = ",water people"
    swim_idea.set_idea_id(idea_id=water_text)

    # THEN
    assert swim_idea.idea_id == water_text


def test_IdeaUnit_set_partylink_CorrectlySetsAttr():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_party = partylink_shop(party_id=todd_text, credor_weight=13, debtor_weight=7)
    mery_party = partylink_shop(party_id=mery_text, credor_weight=23, debtor_weight=5)

    swimmers_idea = ideaunit_shop(idea_id=",swimmers", _partys={})

    # WHEN
    swimmers_idea.set_partylink(todd_party)
    swimmers_idea.set_partylink(mery_party)

    # THEN
    swimmers_partys = {todd_party.party_id: todd_party, mery_party.party_id: mery_party}
    assert swimmers_idea._partys == swimmers_partys


def test_IdeaUnit_get_partylink_ReturnsCorrectObj():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    swimmers_idea = ideaunit_shop(idea_id=",swimmers", _partys={})
    swimmers_idea.set_partylink(partylink_shop(todd_text, 13, 7))
    swimmers_idea.set_partylink(partylink_shop(mery_text, 23, 5))

    # WHEN / THEN
    assert swimmers_idea.get_partylink(todd_text) != None
    assert swimmers_idea.get_partylink(mery_text) != None
    assert swimmers_idea.get_partylink("todd") is None


def test_IdeaUnit_edit_partylink_CorrectlySetsAttr():
    # GIVEN
    todd_text = "Todd"
    old_todd_credor_weight = 13
    todd_debtor_weight = 7
    swimmers_idea = ideaunit_shop(idea_id=",swimmers")
    swimmers_idea.set_partylink(
        partylink_shop(todd_text, old_todd_credor_weight, todd_debtor_weight)
    )
    todd_partylink = swimmers_idea.get_partylink(todd_text)
    assert todd_partylink.credor_weight == old_todd_credor_weight

    # WHEN
    new_todd_credor_weight = 17
    swimmers_idea.edit_partylink(
        party_id=todd_text, credor_weight=new_todd_credor_weight
    )

    # THEN
    assert todd_partylink.credor_weight == new_todd_credor_weight


def test_partylink_exists_ReturnsCorrectObj():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    swimmers_idea = ideaunit_shop(idea_id=",swimmers", _partys={})
    swimmers_idea.set_partylink(partylink_shop(todd_text, 13, 7))
    swimmers_idea.set_partylink(partylink_shop(mery_text, 23, 5))

    # WHEN / THEN
    assert swimmers_idea.partylink_exists(todd_text)
    assert swimmers_idea.partylink_exists(mery_text)
    assert swimmers_idea.partylink_exists("todd") is False


def test_IdeaUnit_del_partylink_SetsAttrCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_party = partylink_shop(party_id=todd_text)
    mery_party = partylink_shop(party_id=mery_text)
    swimmers_partys = {todd_party.party_id: todd_party, mery_party.party_id: mery_party}
    swimmers_idea = ideaunit_shop(idea_id=",swimmers", _partys={})
    swimmers_idea.set_partylink(todd_party)
    swimmers_idea.set_partylink(mery_party)
    assert len(swimmers_idea._partys) == 2
    assert swimmers_idea._partys == swimmers_partys

    # WHEN
    swimmers_idea.del_partylink(party_id=todd_text)

    # THEN
    assert len(swimmers_idea._partys) == 1
    assert swimmers_idea._partys.get(todd_text) is None


def test_IdeaUnit_clear_partylinks_SetsAttrCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_party = partylink_shop(party_id=todd_text)
    mery_party = partylink_shop(party_id=mery_text)
    swimmers_partys = {todd_party.party_id: todd_party, mery_party.party_id: mery_party}
    swimmers_idea = ideaunit_shop(idea_id=",swimmers", _partys={})
    swimmers_idea.set_partylink(todd_party)
    swimmers_idea.set_partylink(mery_party)
    assert len(swimmers_idea._partys) == 2
    assert swimmers_idea._partys == swimmers_partys

    # WHEN
    swimmers_idea.clear_partylinks()

    # THEN
    assert len(swimmers_idea._partys) == 0
    assert swimmers_idea._partys.get(todd_text) is None


def test_IdeaUnit_reset_agenda_importance_SetsAttrCorrectly():
    # GIVEN
    maria_idea_id = "maria"
    maria_ideaunit = ideaunit_shop(idea_id=maria_idea_id, _party_mirror=True)
    maria_ideaunit._agenda_cred = 0.33
    maria_ideaunit._agenda_debt = 0.44
    maria_ideaunit._agenda_intent_cred = 0.13
    maria_ideaunit._agenda_intent_debt = 0.23
    print(f"{maria_ideaunit}")
    assert maria_ideaunit._agenda_cred == 0.33
    assert maria_ideaunit._agenda_debt == 0.44
    assert maria_ideaunit._agenda_intent_cred == 0.13
    assert maria_ideaunit._agenda_intent_debt == 0.23

    # WHEN
    maria_ideaunit.reset_agenda_cred_debt()

    # THEN
    assert maria_ideaunit._agenda_cred == 0
    assert maria_ideaunit._agenda_debt == 0
    assert maria_ideaunit._agenda_intent_cred == 0
    assert maria_ideaunit._agenda_intent_debt == 0


def test_IdeaUnit_reset_agenda_importance_reset_partylinks():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_party = partylink_shop(
        party_id=todd_text,
        _agenda_cred=0.13,
        _agenda_debt=0.7,
        _agenda_intent_cred=0.53,
        _agenda_intent_debt=0.77,
    )
    mery_party = partylink_shop(
        party_id=mery_text,
        _agenda_cred=0.23,
        _agenda_debt=0.5,
        _agenda_intent_cred=0.54,
        _agenda_intent_debt=0.57,
    )
    bikers_partys = {todd_party.party_id: todd_party, mery_party.party_id: mery_party}
    bikers_idea_id = ",bikers"
    bikers_ideaunit = ideaunit_shop(idea_id=bikers_idea_id)
    bikers_ideaunit._agenda_cred = (0.33,)
    bikers_ideaunit._agenda_debt = (0.44,)
    bikers_ideaunit._agenda_intent_cred = (0.1,)
    bikers_ideaunit._agenda_intent_debt = (0.2,)
    bikers_ideaunit.set_partylink(partylink=todd_party)
    bikers_ideaunit.set_partylink(partylink=mery_party)
    print(f"{bikers_ideaunit}")
    biker_partylink_todd = bikers_ideaunit._partys.get(todd_text)
    assert biker_partylink_todd._agenda_cred == 0.13
    assert biker_partylink_todd._agenda_debt == 0.7
    assert biker_partylink_todd._agenda_intent_cred == 0.53
    assert biker_partylink_todd._agenda_intent_debt == 0.77

    biker_partylink_mery = bikers_ideaunit._partys.get(mery_text)
    assert biker_partylink_mery._agenda_cred == 0.23
    assert biker_partylink_mery._agenda_debt == 0.5
    assert biker_partylink_mery._agenda_intent_cred == 0.54
    assert biker_partylink_mery._agenda_intent_debt == 0.57

    # WHEN
    bikers_ideaunit.reset_agenda_cred_debt()

    # THEN
    assert biker_partylink_todd._agenda_cred == 0
    assert biker_partylink_todd._agenda_debt == 0
    assert biker_partylink_todd._agenda_intent_cred == 0
    assert biker_partylink_todd._agenda_intent_debt == 0
    assert biker_partylink_mery._agenda_cred == 0
    assert biker_partylink_mery._agenda_debt == 0
    assert biker_partylink_mery._agenda_intent_cred == 0
    assert biker_partylink_mery._agenda_intent_debt == 0


def test_partylink_meld_ReturnsCorrectObj_BaseScenario():
    # GIVEN
    todd_party = partylink_shop(party_id="Todd")
    merry_party = partylink_shop(party_id="Merry")
    bikers_idea_id = ",bikers"
    bikers_idea = ideaunit_shop(idea_id=bikers_idea_id, _partys={})
    bikers_idea.set_partylink(partylink=todd_party)
    bikers_idea.set_partylink(partylink=merry_party)

    x2_idea = ideaunit_shop(idea_id=bikers_idea_id, _partys={})

    # WHEN
    bikers_idea.meld(other_idea=x2_idea)
    print(f"{bikers_idea.idea_id=} {x2_idea.idea_id=}")

    # THEN
    assert len(bikers_idea._partys) == 2


def test_partylink_meld_ReturnsCorrectObj_GainScenario():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_party = partylink_shop(party_id=todd_text, credor_weight=13, debtor_weight=7)
    mery_party = partylink_shop(party_id=mery_text, credor_weight=23, debtor_weight=5)
    bikers_idea_id = ",bikers"
    bikers_idea = ideaunit_shop(idea_id=bikers_idea_id, _partys={})

    x2_idea = ideaunit_shop(idea_id=bikers_idea_id, _partys={})
    x2_idea.set_partylink(partylink=todd_party)
    x2_idea.set_partylink(partylink=mery_party)

    # WHEN
    bikers_idea.meld(other_idea=x2_idea)

    # THEN
    assert len(bikers_idea._partys) == 2
    assert bikers_idea._partys.get(todd_text) != None


def test_IdeaUnit_meld_RaiseSameparty_idException():
    # GIVEN
    todd_text = "Todd"
    todd_idea = ideaunit_shop(idea_id=todd_text, _party_mirror=True)
    mery_text = "Merry"
    mery_idea = ideaunit_shop(idea_id=mery_text, _party_mirror=True)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        todd_idea.meld(mery_idea)
    assert (
        str(excinfo.value)
        == f"Meld fail IdeaUnit {todd_idea.idea_id} .idea_id='{todd_idea.idea_id}' not the same as .idea_id='{mery_idea.idea_id}"
    )


def test_IdeaUnit_get_dict_ReturnsDictWithAttrsCorrectlySet():
    # GIVEN
    todd_text = "Todd"
    todd_idea = ideaunit_shop(idea_id=todd_text, _party_mirror=True)
    sue_text = "Sue"
    todd_idea.set_partylink(partylink_shop(party_id=sue_text))

    assert todd_idea.idea_id == todd_text
    assert todd_idea._party_mirror
    assert len(todd_idea._partys) == 1

    # WHEN
    todd_dict = todd_idea.get_dict()

    # THEN
    assert todd_dict["idea_id"] == todd_text
    assert todd_dict["_party_mirror"]
    assert len(todd_dict["_partys"]) == 1


def test_IdeaUnit_get_dict_ReturnsDictWithAttrsCorrectlyEmpty():
    # GIVEN
    swim_text = ",Swimmers"
    swim_idea = ideaunit_shop(idea_id=swim_text)
    assert swim_idea._party_mirror is False
    assert swim_idea._partys == {}

    # WHEN
    swim_dict = swim_idea.get_dict()

    # THEN
    assert swim_dict.get("_party_mirror") is None
    assert swim_dict.get("_partys") is None


def test_IdeaUnit_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    swim_text = ",swimmers"

    # WHEN
    swimmers_idea = ideaunit_shop(idea_id=swim_text)
    print(f"{swim_text}")

    # THEN
    ee_dict = swimmers_idea.get_dict()
    assert ee_dict != None
    # assert ee_dict == {"idea_id": swimmers}
    assert ee_dict == {"idea_id": swim_text}

    # GIVEN
    sue_text = "Marie"
    marie_partylink = partylink_shop(
        party_id=sue_text, credor_weight=29, debtor_weight=3
    )
    partylinks_dict = {marie_partylink.party_id: marie_partylink}
    marie_json_dict = {
        sue_text: {
            "party_id": sue_text,
            "credor_weight": 29,
            "debtor_weight": 3,
        }
    }

    teacher_text = ",teachers"
    swim_road = "swim"
    teachers_idea = ideaunit_shop(
        idea_id=teacher_text,
        _partys=partylinks_dict,
    )

    # WHEN
    teachers_dict = teachers_idea.get_dict()

    # THEN
    print(f"{marie_json_dict=}")
    assert teachers_dict == {
        "idea_id": teacher_text,
        "_partys": marie_json_dict,
    }


def test_ideaunit_get_from_dict_CorrectlyReturnsIdeaUnitWith_road_delimiter():
    # GIVEN
    slash_text = "/"
    teacher_text = f"{slash_text}teachers"
    before_teacher_ideaunit = ideaunit_shop(teacher_text, _road_delimiter=slash_text)
    teacher_dict = before_teacher_ideaunit.get_dict()

    # WHEN
    print(f"{teacher_dict=}")
    after_teacher_ideaunit = get_ideaunit_from_dict(teacher_dict, slash_text)

    # THEN
    assert after_teacher_ideaunit == before_teacher_ideaunit


def test_IdeaUnit_get_from_JSON_ReturnsCorrectObj_SimpleExample():
    # GIVEN
    sue_text = "Sue"
    marie_partylink = partylink_shop(
        party_id=sue_text, credor_weight=29, debtor_weight=3
    )
    partylinks_dict = {marie_partylink.party_id: marie_partylink}

    teacher_text = ",teachers"
    swim_road = "swim"
    teacher_idea = ideaunit_shop(idea_id=teacher_text, _partys=partylinks_dict)
    teacher_dict = teacher_idea.get_dict()
    ideas_dict = {teacher_text: teacher_dict}

    teachers_json = get_json_from_dict(dict_x=ideas_dict)
    assert teachers_json != None
    assert x_is_json(json_x=teachers_json)

    # WHEN
    ideaunits_obj_dict = ideaunits_get_from_json(ideaunits_json=teachers_json)

    # THEN
    assert ideaunits_obj_dict != None
    teachers_obj_check_dict = {teacher_idea.idea_id: teacher_idea}
    print(f"    {ideaunits_obj_dict=}")
    print(f"{teachers_obj_check_dict=}")
    assert ideaunits_obj_dict == teachers_obj_check_dict


def test_IdeaUnit_get_ideaunits_from_dict_ReturnsCorrectObjWith_road_delimiter():
    # GIVEN
    slash_text = "/"
    teacher_text = f"{slash_text}teachers"
    teacher_ideaunit = ideaunit_shop(teacher_text, _road_delimiter=slash_text)
    teacher_dict = teacher_ideaunit.get_dict()

    teacher_dict = teacher_ideaunit.get_dict()
    ideaunits_dict = {teacher_text: teacher_dict}

    # WHEN
    x_ideaunits = get_ideaunits_from_dict(ideaunits_dict, slash_text)

    # THEN
    assert x_ideaunits != None
    teachers_obj_check_dict = {teacher_ideaunit.idea_id: teacher_ideaunit}
    print(f"{teachers_obj_check_dict=}")
    assert x_ideaunits == teachers_obj_check_dict


def test_BalanceLink_exists():
    # GIVEN
    bikers_idea_id = IdeaID("bikers")

    # WHEN
    bikers_balancelink = BalanceLink(idea_id=bikers_idea_id)

    # THEN
    assert bikers_balancelink.idea_id == bikers_idea_id
    assert bikers_balancelink.credor_weight == 1.0
    assert bikers_balancelink.debtor_weight == 1.0


def test_balancelink_shop_ReturnsCorrectObj():
    # GIVEN
    bikers_idea_id = IdeaID("bikers")
    bikers_credor_weight = 3.0
    bikers_debtor_weight = 5.0

    # WHEN
    bikers_balancelink = balancelink_shop(
        idea_id=bikers_idea_id,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debtor_weight,
    )

    # THEN
    assert bikers_balancelink.credor_weight == bikers_credor_weight
    assert bikers_balancelink.debtor_weight == bikers_debtor_weight


def test_BalanceHeir_set_agenda_importance_CorrectlySetsAttr():
    # GIVEN
    bikers_idea_id = IdeaID("bikers")
    bikers_credor_weight = 3.0
    bikers_debt_weight = 6.0
    balancelinks_sum_credor_weight = 60
    balancelinks_sum_debtor_weight = 60
    fact_agenda_importance = 1
    idea_heir_x = balanceheir_shop(
        idea_id=bikers_idea_id,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debt_weight,
    )

    # WHEN
    idea_heir_x.set_agenda_cred_debt(
        fact_agenda_importance=fact_agenda_importance,
        balanceheirs_credor_weight_sum=balancelinks_sum_credor_weight,
        balanceheirs_debtor_weight_sum=balancelinks_sum_debtor_weight,
    )

    # THEN
    assert idea_heir_x._agenda_cred == 0.05
    assert idea_heir_x._agenda_debt == 0.1


def test_BalanceLink_get_dict_ReturnsDictWithNecessaryDataForJSON():
    # GIVEN
    bikers_idea_id = IdeaID("bikers")
    bikers_credor_weight = 3.0
    bikers_debtor_weight = 5.0
    bikers_link = balancelink_shop(
        idea_id=bikers_idea_id,
        credor_weight=bikers_credor_weight,
        debtor_weight=bikers_debtor_weight,
    )

    print(f"{bikers_link}")

    # WHEN
    biker_dict = bikers_link.get_dict()

    # THEN
    assert biker_dict != None
    assert biker_dict == {
        "idea_id": bikers_link.idea_id,
        "credor_weight": bikers_link.credor_weight,
        "debtor_weight": bikers_link.debtor_weight,
    }


def test_balancelinks_get_from_JSON_ReturnsCorrectObj_SimpleExample():
    # GIVEN
    teacher_text = "teachers"
    teacher_balancelink = balancelink_shop(
        idea_id=teacher_text, credor_weight=103, debtor_weight=155
    )
    teacher_dict = teacher_balancelink.get_dict()
    balancelinks_dict = {teacher_balancelink.idea_id: teacher_dict}

    teachers_json = get_json_from_dict(dict_x=balancelinks_dict)
    assert teachers_json != None
    assert x_is_json(json_x=teachers_json)

    # WHEN
    balancelinks_obj_dict = balancelinks_get_from_json(balancelinks_json=teachers_json)

    # THEN
    assert balancelinks_obj_dict != None
    teachers_obj_check_dict = {teacher_balancelink.idea_id: teacher_balancelink}
    print(f"    {balancelinks_obj_dict=}")
    print(f"{teachers_obj_check_dict=}")
    assert balancelinks_obj_dict == teachers_obj_check_dict


def test_BalanceLine_exists():
    # GIVEN
    bikers_idea_id = IdeaID("bikers")
    bikers_agenda_cred = 0.33
    bikers_agenda_debt = 0.55

    # WHEN
    bikers_balanceline = BalanceLine(
        idea_id=bikers_idea_id,
        _agenda_cred=bikers_agenda_cred,
        _agenda_debt=bikers_agenda_debt,
    )

    # THEN
    assert bikers_balanceline.idea_id == bikers_idea_id
    assert bikers_balanceline._agenda_cred == bikers_agenda_cred
    assert bikers_balanceline._agenda_debt == bikers_agenda_debt


def test_balanceline_shop_ReturnsCorrectObj_exists():
    # GIVEN
    bikers_idea_id = IdeaID("bikers")
    bikers_idea_id = bikers_idea_id
    bikers_agenda_cred = 0.33
    bikers_agenda_debt = 0.55

    # WHEN
    biker_balanceline = balanceline_shop(
        idea_id=bikers_idea_id,
        _agenda_cred=bikers_agenda_cred,
        _agenda_debt=bikers_agenda_debt,
    )

    assert biker_balanceline != None
    assert biker_balanceline.idea_id == bikers_idea_id
    assert biker_balanceline._agenda_cred == bikers_agenda_cred
    assert biker_balanceline._agenda_debt == bikers_agenda_debt


def test_BalanceLine_add_agenda_cred_debt_CorrectlyModifiesAttr():
    # GIVEN
    bikers_idea_id = IdeaID("bikers")
    bikers_balanceline = balanceline_shop(
        idea_id=bikers_idea_id, _agenda_cred=0.33, _agenda_debt=0.55
    )
    assert bikers_balanceline.idea_id == bikers_idea_id
    assert bikers_balanceline._agenda_cred == 0.33
    assert bikers_balanceline._agenda_debt == 0.55

    # WHEN
    bikers_balanceline.add_agenda_cred_debt(agenda_cred=0.11, agenda_debt=0.2)

    # THEN
    assert bikers_balanceline._agenda_cred == 0.44
    assert bikers_balanceline._agenda_debt == 0.75
