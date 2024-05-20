from src._road.road import default_road_delimiter_if_none
from src.agenda.idea import ideaunit_shop
from src.agenda.healer import healerhold_shop
from src.agenda.reason_idea import beliefunit_shop
from src.agenda.examples.example_agendas import (
    agenda_v001 as example_agendas_agenda_v001,
    get_agenda_x1_3levels_1reason_1beliefs as example_agendas_get_agenda_x1_3levels_1reason_1beliefs,
    get_agenda_base_time_example as example_agendas_get_agenda_base_time_example,
)
from src.agenda.agenda import (
    agendaunit_shop,
    get_from_json as agenda_get_from_json,
    get_dict_of_agenda_from_dict,
)
from src.agenda.examples.agenda_env import (
    get_agenda_temp_env_dir,
    env_dir_setup_cleanup,
)
from src.agenda.group import groupunit_shop, balancelink_shop
from src.agenda.party import partylink_shop
from src.agenda.reason_assign import assignedunit_shop
from src.instrument.python import x_is_json, get_dict_from_json
from src.instrument.file import save_file, open_file
from pytest import raises as pytest_raises


def test_AgendaUnit_get_dict_ReturnsDictObject():
    # GIVEN
    x_agenda = example_agendas_agenda_v001()
    day_hour_text = "day_hour"
    day_hour_road = x_agenda.make_l1_road(day_hour_text)
    day_hour_idea = x_agenda.get_idea_obj(day_hour_road)
    day_hour_idea._originunit.set_originlink(party_id="Bob", weight=2)
    x_agenda.set_belief(
        base=day_hour_road,
        pick=day_hour_road,
        open=0,
        nigh=23,
    )
    time_minute = x_agenda.make_l1_road("day_minute")
    x_agenda.set_belief(base=time_minute, pick=time_minute, open=0, nigh=1440)
    yao_text = "Yao"
    x_agenda._originunit.set_originlink(yao_text, 1)
    agenda_weight = 23
    x_agenda._weight = agenda_weight
    x_party_creditor_pool = 22
    x_party_debtor_pool = 22
    x_agenda.set_party_creditor_pool(x_party_creditor_pool)
    x_agenda.set_party_debtor_pool(x_party_debtor_pool)
    override_text = "override"
    x_agenda.set_meld_strategy(override_text)
    x_last_gift_id = 77
    x_agenda.set_last_gift_id(x_last_gift_id)

    # WHEN
    agenda_dict = x_agenda.get_dict()

    # THEN
    assert agenda_dict != None
    assert str(type(agenda_dict)) == "<class 'dict'>"
    assert agenda_dict["_owner_id"] == x_agenda._owner_id
    assert agenda_dict["_world_id"] == x_agenda._world_id
    assert agenda_dict["_weight"] == x_agenda._weight
    assert agenda_dict["_weight"] == agenda_weight
    assert agenda_dict["_max_tree_traverse"] == x_agenda._max_tree_traverse
    assert agenda_dict["_road_delimiter"] == x_agenda._road_delimiter
    assert agenda_dict["_party_creditor_pool"] == x_agenda._party_creditor_pool
    assert agenda_dict["_party_debtor_pool"] == x_agenda._party_debtor_pool
    assert agenda_dict["_party_debtor_pool"] == x_agenda._party_debtor_pool
    assert agenda_dict["_meld_strategy"] == x_agenda._meld_strategy
    assert agenda_dict["_last_gift_id"] == x_agenda._last_gift_id
    assert len(agenda_dict["_partys"]) == len(x_agenda._partys)
    assert len(agenda_dict["_partys"]) != 12
    assert len(agenda_dict["_groups"]) == 12
    assert len(agenda_dict["_groups"]) != len(x_agenda._groups)

    x_idearoot = x_agenda._idearoot
    idearoot_dict = agenda_dict["_idearoot"]
    _kids = "_kids"
    _range_source_road = "_range_source_road"
    _numeric_road = "_numeric_road"
    assert x_idearoot._label == x_agenda._world_id
    assert idearoot_dict["_label"] == x_idearoot._label
    assert idearoot_dict["_weight"] != agenda_weight
    assert idearoot_dict["_weight"] == x_idearoot._weight
    assert len(idearoot_dict[_kids]) == len(x_idearoot._kids)

    # checking an ideakid._range_source_road attribute
    month_week_text = "month_week"
    month_week_road = x_agenda.make_l1_road(month_week_text)
    month_week_idea_x = x_agenda.get_idea_obj(month_week_road)
    print("checking world_id,month_week...range_source_road equal to...")
    month_week_special_dict = idearoot_dict[_kids][month_week_text][_range_source_road]
    assert month_week_special_dict != None
    assert month_week_special_dict == x_agenda.make_l1_road("ced_week")
    assert month_week_special_dict == month_week_idea_x._range_source_road

    # checking an ideakid._numeric_road attribute
    num1_text = "numeric_road_test"
    num1_road = x_agenda.make_l1_road(num1_text)
    num1_idea_x = x_agenda.get_idea_obj(num1_road)
    print(f"checking {num1_road}...numeric_road equal to...")
    num1_dict_numeric_road = idearoot_dict[_kids][num1_text][_numeric_road]
    assert num1_dict_numeric_road != None
    assert num1_dict_numeric_road == month_week_road
    assert num1_dict_numeric_road == num1_idea_x._numeric_road

    originunit_text = "_originunit"
    day_hour_originunit_dict = idearoot_dict[_kids][day_hour_text][originunit_text]
    assert day_hour_originunit_dict == day_hour_idea._originunit.get_dict()
    _links = "_links"
    x_agenda_originlink = agenda_dict[originunit_text][_links][yao_text]
    print(f"{x_agenda_originlink=}")
    assert x_agenda_originlink
    assert x_agenda_originlink["party_id"] == yao_text
    assert x_agenda_originlink["weight"] == 1


def test_AgendaUnit_get_dict_ReturnsDictWith_idearoot_assignedunit():
    # GIVEN
    run_text = "runners"
    tom_agenda = agendaunit_shop("Tom")
    x_assignedunit = assignedunit_shop()
    x_assignedunit.set_suffgroup(group_id=run_text)
    tom_agenda.edit_idea_attr(assignedunit=x_assignedunit, road=tom_agenda._world_id)

    # WHEN
    agenda_dict = tom_agenda.get_dict()
    idearoot_dict = agenda_dict.get("_idearoot")

    # THEN
    assert idearoot_dict["_assignedunit"] == x_assignedunit.get_dict()
    assert idearoot_dict["_assignedunit"] == {"_suffgroups": {run_text: run_text}}


def test_AgendaUnit_get_dict_ReturnsDictWith_idearoot_healerhold():
    # GIVEN
    tom_agenda = agendaunit_shop("Tom")
    yao_text = "Yao"
    tom_agenda.add_partyunit(yao_text)
    run_text = ",runners"
    run_groupunit = groupunit_shop(run_text)
    run_groupunit.set_partylink(partylink_shop(yao_text))
    tom_agenda.set_groupunit(run_groupunit)
    run_healerhold = healerhold_shop()
    run_healerhold.set_group_id(x_group_id=run_text)
    tom_agenda.edit_idea_attr(road=tom_agenda._world_id, healerhold=run_healerhold)

    # WHEN
    agenda_dict = tom_agenda.get_dict()
    idearoot_dict = agenda_dict.get("_idearoot")

    # THEN
    assert idearoot_dict["_healerhold"] == run_healerhold.get_dict()


def test_AgendaUnit_get_dict_ReturnsDictWith_ideakid_AssignedUnit():
    # GIVEN
    tom_agenda = agendaunit_shop("Tom")
    run_text = ",run"
    tom_agenda.set_groupunit(y_groupunit=groupunit_shop(run_text))

    morn_text = "morning"
    morn_road = tom_agenda.make_l1_road(morn_text)
    tom_agenda.add_l1_idea(ideaunit_shop(morn_text))
    x_assignedunit = assignedunit_shop()
    x_assignedunit.set_suffgroup(group_id=run_text)
    tom_agenda.edit_idea_attr(assignedunit=x_assignedunit, road=morn_road)

    # WHEN
    agenda_dict = tom_agenda.get_dict()
    idearoot_dict = agenda_dict.get("_idearoot")

    # THEN
    _kids = "_kids"
    _assignedunit = "_assignedunit"

    assigned_dict_x = idearoot_dict[_kids][morn_text][_assignedunit]
    assert assigned_dict_x == x_assignedunit.get_dict()
    assert assigned_dict_x == {"_suffgroups": {run_text: run_text}}


def test_AgendaUnit_get_json_ReturnsCorrectJSON_SimpleExample():
    # GIVEN
    zia_agenda = example_agendas_get_agenda_x1_3levels_1reason_1beliefs()
    tiger_world_id = "tiger"
    zia_agenda.set_world_id(tiger_world_id)
    seven_int = 7
    zia_agenda._planck = seven_int
    override_text = "override"
    zia_agenda.set_meld_strategy(override_text)
    yao_text = "Yao"
    zia_agenda.add_partyunit(yao_text)
    run_text = ",runners"
    run_groupunit = groupunit_shop(run_text)
    run_groupunit.set_partylink(partylink_shop(yao_text))
    zia_agenda.set_groupunit(run_groupunit)
    run_healerhold = healerhold_shop({run_text})
    zia_agenda.edit_idea_attr(road=zia_agenda._world_id, healerhold=run_healerhold)
    zia_agenda.edit_idea_attr(road=zia_agenda._world_id, problem_bool=True)

    # WHEN
    x_json = zia_agenda.get_json()

    # THEN
    _kids = "_kids"

    assert x_json != None
    assert True == x_is_json(x_json)
    agenda_dict = get_dict_from_json(x_json)

    assert agenda_dict["_owner_id"] == zia_agenda._owner_id
    assert agenda_dict["_world_id"] == zia_agenda._world_id
    assert agenda_dict["_weight"] == zia_agenda._weight
    assert agenda_dict["_meld_strategy"] == zia_agenda._meld_strategy
    assert agenda_dict["_planck"] == zia_agenda._planck
    with pytest_raises(Exception) as excinfo:
        agenda_dict["_party_creditor_pool"]
    assert str(excinfo.value) == "'_party_creditor_pool'"
    with pytest_raises(Exception) as excinfo:
        agenda_dict["_party_debtor_pool"]
    assert str(excinfo.value) == "'_party_debtor_pool'"
    with pytest_raises(Exception) as excinfo:
        agenda_dict["_last_gift_id"]

    x_idearoot = zia_agenda._idearoot
    idearoot_dict = agenda_dict.get("_idearoot")

    assert len(idearoot_dict[_kids]) == len(x_idearoot._kids)

    shave_text = "shave"
    shave_dict = idearoot_dict[_kids][shave_text]
    shave_beliefunits = shave_dict["_beliefunits"]
    print(f"{shave_beliefunits=}")
    assert len(shave_beliefunits) == 1
    assert len(shave_beliefunits) == len(x_idearoot._kids[shave_text]._beliefunits)
    idearoot_healerhold = idearoot_dict["_healerhold"]
    print(f"{idearoot_healerhold=}")
    assert len(idearoot_healerhold) == 1
    assert x_idearoot._healerhold.any_group_id_exists()
    assert x_idearoot._problem_bool


def test_AgendaUnit_get_json_ReturnsCorrectJSON_BigExample():
    # GIVEN
    yao_agenda = example_agendas_agenda_v001()
    day_hour_text = "day_hour"
    day_hour_road = yao_agenda.make_l1_road(day_hour_text)
    yao_agenda.set_belief(base=day_hour_road, pick=day_hour_road, open=0, nigh=23)
    day_min_text = "day_minute"
    day_min_road = yao_agenda.make_l1_road(day_min_text)
    yao_agenda.set_belief(base=day_min_road, pick=day_min_road, open=0, nigh=59)
    beliefunit_x = beliefunit_shop(day_min_road, day_min_road, 5, 59)
    yao_agenda.edit_idea_attr(road=beliefunit_x.base, beliefunit=beliefunit_x)
    yao_agenda.set_max_tree_traverse(int_x=2)
    yao_text = "Yao"
    yao_agenda._originunit.set_originlink(yao_text, 1)

    # WHEN
    agenda_dict = get_dict_from_json(json_x=yao_agenda.get_json())

    # THEN
    _kids = "_kids"
    assert agenda_dict["_owner_id"] == yao_agenda._owner_id
    assert agenda_dict["_world_id"] == yao_agenda._world_id
    assert agenda_dict["_weight"] == yao_agenda._weight
    assert agenda_dict["_max_tree_traverse"] == 2
    assert agenda_dict["_max_tree_traverse"] == yao_agenda._max_tree_traverse
    assert agenda_dict["_road_delimiter"] == yao_agenda._road_delimiter

    x_idearoot = yao_agenda._idearoot
    idearoot_dict = agenda_dict.get("_idearoot")
    assert len(idearoot_dict[_kids]) == len(x_idearoot._kids)

    kids = idearoot_dict[_kids]
    day_min_dict = kids[day_min_text]
    day_min_beliefunits_dict = day_min_dict["_beliefunits"]
    day_min_idea_x = yao_agenda.get_idea_obj(day_min_road)
    print(f"{day_min_beliefunits_dict=}")
    assert len(day_min_beliefunits_dict) == 1
    assert len(day_min_beliefunits_dict) == len(day_min_idea_x._beliefunits)

    _reasonunits = "_reasonunits"
    cont_text = "Freelancing"
    ulti_text = "Ultimate Frisbee"
    cont_road = yao_agenda.make_l1_road(cont_text)
    ulti_road = yao_agenda.make_l1_road(ulti_text)
    cont_idea = yao_agenda.get_idea_obj(cont_road)
    ulti_idea = yao_agenda.get_idea_obj(ulti_road)
    cont_reasonunits_dict = idearoot_dict[_kids][cont_text][_reasonunits]
    ulti_reasonunits_dict = idearoot_dict[_kids][ulti_text][_reasonunits]
    assert len(cont_reasonunits_dict) == len(cont_idea._reasonunits)
    assert len(ulti_reasonunits_dict) == len(ulti_idea._reasonunits)
    originunit_text = "_originunit"
    _links = "_links"
    assert len(agenda_dict[originunit_text][_links])


def test_save_file_CorrectlySavesAgendaUnitJSON(env_dir_setup_cleanup):
    # GIVEN
    yao_agenda = example_agendas_agenda_v001()
    x_yao_agenda_json = yao_agenda.get_json()
    file_name_x = "example_agenda1.json"

    # WHEN
    save_file(
        dest_dir=get_agenda_temp_env_dir(),
        file_name=file_name_x,
        file_text=x_yao_agenda_json,
    )

    # THEN
    assert open_file(dest_dir=get_agenda_temp_env_dir(), file_name=file_name_x)


def test_agenda_get_from_json_ReturnsCorrectObjSimpleExample():
    # GIVEN
    zia_agenda = example_agendas_get_agenda_x1_3levels_1reason_1beliefs()
    zia_agenda.set_max_tree_traverse(23)
    tiger_world_id = "tiger"
    zia_agenda.set_world_id(tiger_world_id)
    zia_planck = 0.5
    zia_agenda._planck = zia_planck
    zia_party_creditor_pool = 2
    zia_party_debtor_pool = 2
    zia_agenda.set_party_creditor_pool(zia_party_creditor_pool)
    zia_agenda.set_party_debtor_pool(zia_party_debtor_pool)
    zia_last_gift_id = 73
    zia_agenda.set_last_gift_id(zia_last_gift_id)

    shave_text = "shave"
    shave_road = zia_agenda.make_l1_road(shave_text)
    shave_idea_y1 = zia_agenda.get_idea_obj(shave_road)
    shave_idea_y1._originunit.set_originlink(party_id="Sue", weight=4.3)
    shave_idea_y1._problem_bool = True
    # print(f"{shave_road=}")
    # print(f"{json_shave_idea._label=} {json_shave_idea._parent_road=}")

    sue_text = "Sue"
    zia_agenda.add_partyunit(party_id=sue_text)
    tim_text = "Tim"
    zia_agenda.add_partyunit(party_id=tim_text)
    run_text = ",runners"
    run_group = groupunit_shop(group_id=run_text)
    run_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
    run_group.set_partylink(partylink=partylink_shop(party_id=tim_text))
    zia_agenda.set_groupunit(y_groupunit=run_group)

    run_assignedunit = assignedunit_shop()
    run_assignedunit.set_suffgroup(group_id=run_text)
    zia_agenda.edit_idea_attr(zia_agenda._world_id, assignedunit=run_assignedunit)
    tim_assignedunit = assignedunit_shop()
    tim_assignedunit.set_suffgroup(group_id=tim_text)
    zia_agenda.edit_idea_attr(shave_road, assignedunit=tim_assignedunit)
    zia_agenda.edit_idea_attr(shave_road, balancelink=balancelink_shop(tim_text))
    zia_agenda.edit_idea_attr(shave_road, balancelink=balancelink_shop(sue_text))
    zia_agenda.edit_idea_attr(
        zia_agenda._world_id, balancelink=balancelink_shop(sue_text)
    )
    # add healerhold to shave ideaunit
    run_healerhold = healerhold_shop({run_text})
    zia_agenda.edit_idea_attr(shave_road, healerhold=run_healerhold)

    yao_text = "Yao"
    zia_agenda._originunit.set_originlink(yao_text, 1)
    override_text = "override"
    zia_agenda.set_meld_strategy(override_text)

    # WHEN
    x_json = zia_agenda.get_json()
    assert x_is_json(x_json) == True
    json_agenda = agenda_get_from_json(x_agenda_json=x_json)

    # THEN
    assert str(type(json_agenda)).find(".agenda.AgendaUnit'>") > 0
    assert json_agenda._owner_id != None
    assert json_agenda._owner_id == zia_agenda._owner_id
    assert json_agenda._world_id == zia_agenda._world_id
    assert json_agenda._planck == zia_planck
    assert json_agenda._planck == zia_agenda._planck
    assert json_agenda._max_tree_traverse == 23
    assert json_agenda._max_tree_traverse == zia_agenda._max_tree_traverse
    assert json_agenda._road_delimiter == zia_agenda._road_delimiter
    assert json_agenda._party_creditor_pool == zia_agenda._party_creditor_pool
    assert json_agenda._party_debtor_pool == zia_agenda._party_debtor_pool
    assert json_agenda._party_creditor_pool == zia_party_creditor_pool
    assert json_agenda._party_debtor_pool == zia_party_debtor_pool
    assert json_agenda._meld_strategy == zia_agenda._meld_strategy
    assert json_agenda._meld_strategy == override_text
    assert json_agenda._last_gift_id == zia_agenda._last_gift_id
    assert json_agenda._last_gift_id == zia_last_gift_id
    print(f"{json_agenda._groups.keys()=}")
    print(f"{zia_agenda._groups.keys()=}")
    assert json_agenda._groups == zia_agenda._groups

    json_idearoot = json_agenda._idearoot
    assert json_idearoot._parent_road == ""
    assert json_idearoot._parent_road == zia_agenda._idearoot._parent_road
    assert json_idearoot._reasonunits == {}
    assert json_idearoot._assignedunit == zia_agenda._idearoot._assignedunit
    assert json_idearoot._assignedunit == run_assignedunit
    assert len(json_idearoot._beliefunits) == 1
    assert len(json_idearoot._balancelinks) == 1

    assert len(json_agenda._idearoot._kids) == 2

    weekday_text = "weekdays"
    weekday_road = json_agenda.make_l1_road(weekday_text)
    weekday_idea_x = json_agenda.get_idea_obj(weekday_road)
    assert len(weekday_idea_x._kids) == 2

    sunday_text = "Sunday"
    sunday_road = json_agenda.make_road(weekday_road, sunday_text)
    sunday_idea = json_agenda.get_idea_obj(sunday_road)
    assert sunday_idea._weight == 20

    json_shave_idea = json_agenda.get_idea_obj(shave_road)
    zia_shave_idea = zia_agenda.get_idea_obj(shave_road)
    assert len(json_shave_idea._reasonunits) == 1
    assert json_shave_idea._assignedunit == zia_shave_idea._assignedunit
    assert json_shave_idea._assignedunit == tim_assignedunit
    assert json_shave_idea._originunit == zia_shave_idea._originunit
    print(f"{json_shave_idea._healerhold=}")
    assert json_shave_idea._healerhold == zia_shave_idea._healerhold
    assert len(json_shave_idea._balancelinks) == 2
    assert len(json_shave_idea._beliefunits) == 1
    assert zia_shave_idea._problem_bool
    assert json_shave_idea._problem_bool == zia_shave_idea._problem_bool

    assert len(json_agenda._originunit._links) == 1
    assert json_agenda._originunit == zia_agenda._originunit


def test_agenda_get_from_json_ReturnsCorrectObj_road_delimiter_Example():
    # GIVEN
    slash_delimiter = "/"
    before_bob_agenda = agendaunit_shop("Bob", _road_delimiter=slash_delimiter)
    assert before_bob_agenda._road_delimiter != default_road_delimiter_if_none()

    # WHEN
    bob_json = before_bob_agenda.get_json()
    after_bob_agenda = agenda_get_from_json(bob_json)

    # THEN
    assert after_bob_agenda._road_delimiter != default_road_delimiter_if_none()
    assert after_bob_agenda._road_delimiter == slash_delimiter
    assert after_bob_agenda._road_delimiter == before_bob_agenda._road_delimiter


def test_agenda_get_from_json_ReturnsCorrectObj_road_delimiter_PartyExample():
    # GIVEN
    slash_delimiter = "/"
    before_bob_agenda = agendaunit_shop("Bob", _road_delimiter=slash_delimiter)
    bob_text = ",Bob"
    before_bob_agenda.add_partyunit(bob_text)
    assert before_bob_agenda.get_party(bob_text) != None

    # WHEN
    bob_json = before_bob_agenda.get_json()
    after_bob_agenda = agenda_get_from_json(bob_json)

    # THEN
    after_bob_partyunit = after_bob_agenda.get_party(bob_text)
    assert after_bob_partyunit._road_delimiter == slash_delimiter


def test_agenda_get_from_json_ReturnsCorrectObj_road_delimiter_GroupExample():
    # GIVEN
    slash_delimiter = "/"
    before_bob_agenda = agendaunit_shop("Bob", _road_delimiter=slash_delimiter)
    swimmers_text = f"{slash_delimiter}Swimmers"
    before_bob_agenda.set_groupunit(
        groupunit_shop(swimmers_text, _road_delimiter=slash_delimiter)
    )
    assert before_bob_agenda.get_groupunit(swimmers_text) != None

    # WHEN
    bob_json = before_bob_agenda.get_json()
    after_bob_agenda = agenda_get_from_json(bob_json)

    # THEN
    after_bob_groupunit = after_bob_agenda.get_groupunit(swimmers_text)
    assert after_bob_groupunit._road_delimiter == slash_delimiter


def test_agenda_get_from_json_jsonExportCorrectyExportsAgendaUnit_weight():
    # GIVEN
    x1_agenda = example_agendas_agenda_v001()
    x1_agenda._weight = 15
    assert 15 == x1_agenda._weight
    assert x1_agenda._idearoot._weight != x1_agenda._weight
    assert x1_agenda._idearoot._weight == 1

    # WHEN
    x2_agenda = agenda_get_from_json(x1_agenda.get_json())

    # THEN
    assert x1_agenda._weight == 15
    assert x1_agenda._weight == x2_agenda._weight
    assert x1_agenda._idearoot._weight == 1
    assert x1_agenda._idearoot._weight == x2_agenda._idearoot._weight
    assert x1_agenda._idearoot._kids == x2_agenda._idearoot._kids


def test_get_dict_of_agenda_from_dict_ReturnsDictOfAgendaUnits():
    # GIVEN
    x1_agenda = example_agendas_agenda_v001()
    x2_agenda = example_agendas_get_agenda_x1_3levels_1reason_1beliefs()
    x3_agenda = example_agendas_get_agenda_base_time_example()
    print(f"{x1_agenda._owner_id}")
    print(f"{x2_agenda._owner_id}")
    print(f"{x3_agenda._owner_id}")

    cn_dict_of_dicts = {
        x1_agenda._owner_id: x1_agenda.get_dict(),
        x2_agenda._owner_id: x2_agenda.get_dict(),
        x3_agenda._owner_id: x3_agenda.get_dict(),
    }

    # WHEN
    ccn_dict_of_obj = get_dict_of_agenda_from_dict(cn_dict_of_dicts)

    # THEN
    assert ccn_dict_of_obj.get(x1_agenda._owner_id) != None
    assert ccn_dict_of_obj.get(x2_agenda._owner_id) != None
    assert ccn_dict_of_obj.get(x3_agenda._owner_id) != None
    cc1_idea_root = ccn_dict_of_obj.get(x1_agenda._owner_id)._idearoot
    assert cc1_idea_root._originunit == x1_agenda._idearoot._originunit
    assert ccn_dict_of_obj.get(x1_agenda._owner_id)._idea_dict == x1_agenda._idea_dict
    assert ccn_dict_of_obj.get(x1_agenda._owner_id) == x1_agenda
    ccn2_agenda = ccn_dict_of_obj.get(x2_agenda._owner_id)
    assert ccn2_agenda._idearoot._label == x2_agenda._idearoot._label
    assert ccn2_agenda._idearoot._parent_road == x2_agenda._idearoot._parent_road
    shave_road = ccn2_agenda.make_l1_road("shave")
    week_road = ccn2_agenda.make_l1_road("weekdays")
    assert ccn2_agenda.get_idea_obj(shave_road) == x2_agenda.get_idea_obj(shave_road)
    assert ccn2_agenda.get_idea_obj(week_road) == x2_agenda.get_idea_obj(week_road)
    assert ccn2_agenda._idearoot == x2_agenda._idearoot
    print(f"{ccn2_agenda._idea_dict.keys()=}")
    print(f"{x2_agenda._idea_dict.keys()=}")
    assert ccn2_agenda._idea_dict == x2_agenda._idea_dict
    assert ccn2_agenda == x2_agenda
    ccn_agenda3 = ccn_dict_of_obj.get(x3_agenda._owner_id)
    x3_agenda.set_agenda_metrics()
    assert ccn_agenda3 == x3_agenda
