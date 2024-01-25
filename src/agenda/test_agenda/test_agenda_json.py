from src._prime.road import default_road_delimiter_if_none
from src.agenda.agenda import agendaunit_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.reason_idea import beliefunit_shop
from src.agenda.examples.example_agendas import (
    agenda_v001 as example_agendas_agenda_v001,
    get_agenda_x1_3levels_1reason_1beliefs as example_agendas_get_agenda_x1_3levels_1reason_1beliefs,
    get_agenda_base_time_example as example_agendas_get_agenda_base_time_example,
)
from src.agenda.agenda import (
    get_from_json as agenda_get_from_json,
    get_dict_of_agenda_from_dict,
)
from src.agenda.examples.agenda_env import (
    get_agenda_temp_env_dir,
    env_dir_setup_cleanup,
)
from src.agenda.group import groupunit_shop, balancelink_shop
from src.agenda.party import partylink_shop
from src.agenda.reason_assign import assigned_unit_shop
from src.tools.python import x_is_json
from src.tools.file import save_file, open_file
from json import loads as json_loads
from pytest import raises as pytest_raises


def test_agenda_get_dict_ReturnsDictObject():
    # GIVEN
    x_agenda = example_agendas_agenda_v001()
    day_hour_text = "day_hour"
    day_hour_road = x_agenda.make_l1_road(day_hour_text)
    day_hour_idea = x_agenda.get_idea_obj(day_hour_road)
    day_hour_idea._originunit.set_originlink(person_id="Bob", weight=2)
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

    # WHEN
    agenda_dict = x_agenda.get_dict()

    # THEN
    assert agenda_dict != None
    assert str(type(agenda_dict)) == "<class 'dict'>"
    assert agenda_dict["_agent_id"] == x_agenda._agent_id
    assert agenda_dict["_economy_id"] == x_agenda._economy_id
    assert agenda_dict["_weight"] == x_agenda._weight
    assert agenda_dict["_weight"] == agenda_weight
    assert agenda_dict["_max_tree_traverse"] == x_agenda._max_tree_traverse
    assert agenda_dict["_auto_output_to_forum"] == x_agenda._auto_output_to_forum
    assert agenda_dict["_road_delimiter"] == x_agenda._road_delimiter
    assert agenda_dict["_party_creditor_pool"] == x_agenda._party_creditor_pool
    assert agenda_dict["_party_debtor_pool"] == x_agenda._party_debtor_pool
    assert agenda_dict["_party_debtor_pool"] == x_agenda._party_debtor_pool
    assert agenda_dict["_meld_strategy"] == x_agenda._meld_strategy
    assert len(agenda_dict["_partys"]) == len(x_agenda._partys)
    assert len(agenda_dict["_groups"]) == len(x_agenda._groups)

    x_idearoot = x_agenda._idearoot
    idearoot_dict = agenda_dict["_idearoot"]
    _kids = "_kids"
    _range_source_road = "_range_source_road"
    _numeric_road = "_numeric_road"
    assert x_idearoot._label == x_agenda._economy_id
    assert idearoot_dict["_label"] == x_idearoot._label
    assert idearoot_dict["_weight"] != agenda_weight
    assert idearoot_dict["_weight"] == x_idearoot._weight
    assert len(idearoot_dict[_kids]) == len(x_idearoot._kids)

    # checking an ideakid._range_source_road attribute
    month_week_text = "month_week"
    month_week_road = x_agenda.make_l1_road(month_week_text)
    month_week_idea_x = x_agenda.get_idea_obj(month_week_road)
    print("checking economy_id,month_week...range_source_road equal to...")
    month_week_special_dict = idearoot_dict[_kids][month_week_text][_range_source_road]
    assert month_week_special_dict != None
    assert month_week_special_dict == x_agenda.make_road(
        x_agenda._economy_id, "ced_week"
    )
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
    assert x_agenda_originlink["person_id"] == yao_text
    assert x_agenda_originlink["weight"] == 1


def test_agenda_get_dict_ReturnsDictWith_idearoot_AssignedUnit():
    # GIVEN
    run_text = "runners"
    tom_agenda = agendaunit_shop("Tom")
    assigned_unit_x = assigned_unit_shop()
    assigned_unit_x.set_suffgroup(brand=run_text)
    tom_agenda.edit_idea_attr(assignedunit=assigned_unit_x, road=tom_agenda._economy_id)

    # WHEN
    agenda_dict = tom_agenda.get_dict()
    idearoot_dict = agenda_dict.get("_idearoot")

    # THEN
    assert idearoot_dict["_assignedunit"] == assigned_unit_x.get_dict()
    assert idearoot_dict["_assignedunit"] == {"_suffgroups": {run_text: run_text}}


def test_agenda_get_dict_ReturnsDictWith_ideakid_AssignedUnit():
    # GIVEN
    tom_agenda = agendaunit_shop("Tom")
    run_text = ",run"
    tom_agenda.set_groupunit(y_groupunit=groupunit_shop(run_text))

    morn_text = "morning"
    morn_road = tom_agenda.make_l1_road(morn_text)
    tom_agenda.add_l1_idea(ideaunit_shop(morn_text))
    assigned_unit_x = assigned_unit_shop()
    assigned_unit_x.set_suffgroup(brand=run_text)
    tom_agenda.edit_idea_attr(assignedunit=assigned_unit_x, road=morn_road)

    # WHEN
    agenda_dict = tom_agenda.get_dict()
    idearoot_dict = agenda_dict.get("_idearoot")

    # THEN
    _kids = "_kids"
    _assignedunit = "_assignedunit"

    assigned_dict_x = idearoot_dict[_kids][morn_text][_assignedunit]
    assert assigned_dict_x == assigned_unit_x.get_dict()
    assert assigned_dict_x == {"_suffgroups": {run_text: run_text}}


def test_export_to_JSON_simple_example_works():
    # GIVEN
    x_agenda = example_agendas_get_agenda_x1_3levels_1reason_1beliefs()
    tiger_economy_id = "tiger_econ"
    x_agenda.set_economy_id(tiger_economy_id)
    override_text = "override"
    x_agenda.set_meld_strategy(override_text)

    # WHEN
    x_json = x_agenda.get_json()

    # THEN
    _kids = "_kids"

    assert x_json != None
    assert True == x_is_json(x_json)
    agenda_dict = json_loads(x_json)

    assert agenda_dict["_agent_id"] == x_agenda._agent_id
    assert agenda_dict["_economy_id"] == x_agenda._economy_id
    assert agenda_dict["_weight"] == x_agenda._weight
    assert agenda_dict["_meld_strategy"] == x_agenda._meld_strategy
    with pytest_raises(Exception) as excinfo:
        agenda_dict["_party_creditor_pool"]
    assert str(excinfo.value) == "'_party_creditor_pool'"
    with pytest_raises(Exception) as excinfo:
        agenda_dict["_party_debtor_pool"]
    assert str(excinfo.value) == "'_party_debtor_pool'"

    x_idearoot = x_agenda._idearoot
    idearoot_dict = agenda_dict.get("_idearoot")

    assert len(idearoot_dict[_kids]) == len(x_idearoot._kids)

    shave_text = "shave"
    shave_dict = idearoot_dict[_kids][shave_text]
    shave_beliefunits = shave_dict["_beliefunits"]
    print(f"{shave_beliefunits=}")
    assert len(shave_beliefunits) == 1
    assert len(shave_beliefunits) == len(x_idearoot._kids[shave_text]._beliefunits)


def test_export_to_JSON_BigExampleCorrectlyReturnsValues():
    # GIVEN
    x_agenda = example_agendas_agenda_v001()
    day_hour_text = "day_hour"
    day_hour_road = x_agenda.make_l1_road(day_hour_text)
    x_agenda.set_belief(base=day_hour_road, pick=day_hour_road, open=0, nigh=23)
    day_min_text = "day_minute"
    day_min_road = x_agenda.make_l1_road(day_min_text)
    x_agenda.set_belief(base=day_min_road, pick=day_min_road, open=0, nigh=59)
    beliefunit_x = beliefunit_shop(day_min_road, day_min_road, 5, 59)
    x_agenda.edit_idea_attr(road=beliefunit_x.base, beliefunit=beliefunit_x)
    x_agenda.set_max_tree_traverse(int_x=2)
    yao_text = "Yao"
    x_agenda._originunit.set_originlink(yao_text, 1)

    # WHEN
    agenda_dict = json_loads(x_agenda.get_json())

    # THEN
    _kids = "_kids"
    assert agenda_dict["_agent_id"] == x_agenda._agent_id
    assert agenda_dict["_economy_id"] == x_agenda._economy_id
    assert agenda_dict["_weight"] == x_agenda._weight
    assert agenda_dict["_max_tree_traverse"] == 2
    assert agenda_dict["_max_tree_traverse"] == x_agenda._max_tree_traverse
    assert agenda_dict["_road_delimiter"] == x_agenda._road_delimiter

    x_idearoot = x_agenda._idearoot
    idearoot_dict = agenda_dict.get("_idearoot")
    assert len(idearoot_dict[_kids]) == len(x_idearoot._kids)

    kids = idearoot_dict[_kids]
    day_min_dict = kids[day_min_text]
    day_min_beliefunits_dict = day_min_dict["_beliefunits"]
    day_min_idea_x = x_agenda.get_idea_obj(day_min_road)
    print(f"{day_min_beliefunits_dict=}")
    assert len(day_min_beliefunits_dict) == 1
    assert len(day_min_beliefunits_dict) == len(day_min_idea_x._beliefunits)

    _reasonunits = "_reasonunits"
    cont_text = "Freelancing"
    ulti_text = "Ultimate Frisbee"
    cont_road = x_agenda.make_l1_road(cont_text)
    ulti_road = x_agenda.make_l1_road(ulti_text)
    cont_idea = x_agenda.get_idea_obj(cont_road)
    ulti_idea = x_agenda.get_idea_obj(ulti_road)
    cont_reasonunits_dict = idearoot_dict[_kids][cont_text][_reasonunits]
    ulti_reasonunits_dict = idearoot_dict[_kids][ulti_text][_reasonunits]
    assert len(cont_reasonunits_dict) == len(cont_idea._reasonunits)
    assert len(ulti_reasonunits_dict) == len(ulti_idea._reasonunits)
    originunit_text = "_originunit"
    _links = "_links"
    assert len(agenda_dict[originunit_text][_links])


def test_save_file_CorrectlySavesAgendaJSON(env_dir_setup_cleanup):
    # GIVEN
    x_agenda = example_agendas_agenda_v001()
    x_x_agenda_json = x_agenda.get_json()
    file_name_x = "example_agenda1.json"

    # WHEN
    save_file(
        dest_dir=get_agenda_temp_env_dir(),
        file_name=file_name_x,
        file_text=x_x_agenda_json,
    )

    # THEN
    assert open_file(dest_dir=get_agenda_temp_env_dir(), file_name=file_name_x)


def test_agenda_get_json_CorrectlyWorksForSimpleExample():
    # GIVEN
    yue_agenda = example_agendas_get_agenda_x1_3levels_1reason_1beliefs()
    yue_agenda.set_max_tree_traverse(23)
    tiger_economy_id = "tiger_econ"
    yue_agenda.set_economy_id(tiger_economy_id)
    yue_party_creditor_pool = 2
    yue_party_debtor_pool = 2
    yue_agenda.set_party_creditor_pool(yue_party_creditor_pool)
    yue_agenda.set_party_debtor_pool(yue_party_debtor_pool)

    shave_text = "shave"
    shave_road = yue_agenda.make_l1_road(shave_text)
    shave_idea_y1 = yue_agenda.get_idea_obj(shave_road)
    shave_idea_y1._originunit.set_originlink(person_id="Sue", weight=4.3)
    # print(f"{shave_road=}")
    # print(f"{shave_idea_x._label=} {shave_idea_x._parent_road=}")

    sue_text = "sue"
    yue_agenda.add_partyunit(party_id=sue_text)
    tim_text = "tim"
    yue_agenda.add_partyunit(party_id=tim_text)
    run_text = ",runners"
    run_group = groupunit_shop(brand=run_text)
    run_group.set_partylink(partylink=partylink_shop(party_id=sue_text))
    run_group.set_partylink(partylink=partylink_shop(party_id=tim_text))
    yue_agenda.set_groupunit(y_groupunit=run_group)

    run_assigned_unit = assigned_unit_shop()
    run_assigned_unit.set_suffgroup(brand=run_text)
    yue_agenda.edit_idea_attr(yue_agenda._economy_id, assignedunit=run_assigned_unit)
    tim_assigned_unit = assigned_unit_shop()
    tim_assigned_unit.set_suffgroup(brand=tim_text)
    yue_agenda.edit_idea_attr(shave_road, assignedunit=tim_assigned_unit)
    yue_agenda.edit_idea_attr(shave_road, balancelink=balancelink_shop(tim_text))
    yue_agenda.edit_idea_attr(shave_road, balancelink=balancelink_shop(sue_text))
    yue_agenda.edit_idea_attr(
        yue_agenda._economy_id, balancelink=balancelink_shop(sue_text)
    )

    yao_text = "Yao"
    yue_agenda._originunit.set_originlink(yao_text, 1)
    yue_agenda._auto_output_to_forum = True
    override_text = "override"
    yue_agenda.set_meld_strategy(override_text)

    # WHEN
    x_json = yue_agenda.get_json()
    assert x_is_json(x_json) == True
    json_agenda = agenda_get_from_json(x_agenda_json=x_json)

    # THEN
    assert str(type(json_agenda)).find(".agenda.AgendaUnit'>") > 0
    assert json_agenda._agent_id != None
    assert json_agenda._agent_id == yue_agenda._agent_id
    assert json_agenda._economy_id == yue_agenda._economy_id
    assert json_agenda._max_tree_traverse == 23
    assert json_agenda._max_tree_traverse == yue_agenda._max_tree_traverse
    assert json_agenda._auto_output_to_forum == yue_agenda._auto_output_to_forum
    assert json_agenda._road_delimiter == yue_agenda._road_delimiter
    assert json_agenda._party_creditor_pool == yue_agenda._party_creditor_pool
    assert json_agenda._party_debtor_pool == yue_agenda._party_debtor_pool
    assert json_agenda._party_creditor_pool == yue_party_creditor_pool
    assert json_agenda._party_debtor_pool == yue_party_debtor_pool
    assert json_agenda._meld_strategy == yue_agenda._meld_strategy
    assert json_agenda._meld_strategy == override_text

    json_idearoot = json_agenda._idearoot
    assert json_idearoot._parent_road == ""
    assert json_idearoot._parent_road == yue_agenda._idearoot._parent_road
    assert json_idearoot._reasonunits == {}
    assert json_idearoot._assignedunit == yue_agenda._idearoot._assignedunit
    assert json_idearoot._assignedunit == run_assigned_unit
    assert len(json_idearoot._beliefunits) == 1
    assert len(json_idearoot._balancelinks) == 1

    assert len(json_agenda._idearoot._kids) == 2

    weekday_text = "weekdays"
    weekday_road = json_agenda.make_l1_road(weekday_text)
    weekday_idea_x = json_agenda.get_idea_obj(weekday_road)
    assert len(weekday_idea_x._kids) == 2

    sunday_text = "Sunday"
    sunday_road = json_agenda.make_road(weekday_road, sunday_text)
    sunday_idea_x = json_agenda.get_idea_obj(sunday_road)
    assert sunday_idea_x._weight == 20

    shave_idea_x = json_agenda.get_idea_obj(shave_road)
    shave_idea_y2 = yue_agenda.get_idea_obj(shave_road)
    assert len(shave_idea_x._reasonunits) == 1
    assert shave_idea_x._assignedunit == shave_idea_y2._assignedunit
    assert shave_idea_x._assignedunit == tim_assigned_unit
    assert shave_idea_x._originunit == shave_idea_y2._originunit
    assert len(shave_idea_x._balancelinks) == 2
    assert len(shave_idea_x._beliefunits) == 1

    assert len(json_agenda._originunit._links) == 1
    assert json_agenda._originunit == yue_agenda._originunit


def test_agenda_get_json_CorrectlyWorksFor_delimiter_Data():
    # GIVEN
    slash_delimiter = "/"
    a_bob_agenda = agendaunit_shop("Bob", _road_delimiter=slash_delimiter)
    assert a_bob_agenda._road_delimiter != default_road_delimiter_if_none()

    # WHEN
    bob_json = a_bob_agenda.get_json()
    b_bob_agenda = agenda_get_from_json(bob_json)

    # THEN
    assert b_bob_agenda._road_delimiter != default_road_delimiter_if_none()
    assert b_bob_agenda._road_delimiter == slash_delimiter
    assert b_bob_agenda._road_delimiter == a_bob_agenda._road_delimiter


# def test_agenda_get_json_CorrectlyWorksForNotSimpleExample():
#     # GIVEN
#     x_agenda1 = example_agendas_agenda_v001()
#     x_agenda1.set_agenda_metrics()
#     x_agenda1_json = x_agenda1.get_json()
#     assert x_is_json(json_x=x_agenda1_json)

#     file_name = "example_agenda1.json"
#     file_dir = agenda_env()
#     print("File may fail since example_agenda1.json is created by a later test")
#     x_agenda3_json = open_file(dest_dir=file_dir, file_name=file_name)
#     # print(x_agenda3_json[299000:299155])

#     # WHEN
#     x_agenda3 = agenda_get_from_json(x_agenda_json=x_agenda3_json)

#     # THEN
#     assert str(type(x_agenda3)).find(".agenda.AgendaUnit'>") > 0
#     assert x_agenda3._agent_id != None
#     assert x_agenda3._agent_id == x_agenda1._agent_id
#     assert x_agenda3._max_tree_traverse == 2
#     assert x_agenda3._max_tree_traverse == x_agenda1._max_tree_traverse
#     assert x_agenda3._idearoot._agent_id != None
#     assert x_agenda3._idearoot._agent_id == x_agenda1._idearoot._agent_id
#     assert x_agenda3._idearoot._parent_road == ""
#     assert x_agenda3._idearoot._parent_road == x_agenda1._idearoot._parent_road
#     assert len(x_agenda3._idearoot._kids) == len(x_agenda1._idearoot._kids)
#     assert len(x_agenda3._groups) == 34
#     assert len(x_agenda3._partys) == 22


def test_get_dict_of_agenda_from_dict_ReturnsDictOfAgendaUnits():
    # GIVEN
    x_agenda1 = example_agendas_agenda_v001()
    x_agenda2 = example_agendas_get_agenda_x1_3levels_1reason_1beliefs()
    x_agenda3 = example_agendas_get_agenda_base_time_example()

    cn_dict_of_dicts = {
        x_agenda1._agent_id: x_agenda1.get_dict(),
        x_agenda2._agent_id: x_agenda2.get_dict(),
        x_agenda3._agent_id: x_agenda3.get_dict(),
    }

    # WHEN
    ccn_dict_of_obj = get_dict_of_agenda_from_dict(cn_dict_of_dicts)

    # THEN
    assert ccn_dict_of_obj.get(x_agenda1._agent_id) != None
    assert ccn_dict_of_obj.get(x_agenda2._agent_id) != None
    assert ccn_dict_of_obj.get(x_agenda3._agent_id) != None
    cc1_idea_root = ccn_dict_of_obj.get(x_agenda1._agent_id)._idearoot
    assert cc1_idea_root._originunit == x_agenda1._idearoot._originunit
    assert ccn_dict_of_obj.get(x_agenda1._agent_id)._idea_dict == x_agenda1._idea_dict
    assert ccn_dict_of_obj.get(x_agenda1._agent_id) == x_agenda1
    ccn2_agenda = ccn_dict_of_obj.get(x_agenda2._agent_id)
    assert ccn2_agenda._idearoot._label == x_agenda2._idearoot._label
    assert ccn2_agenda._idearoot._parent_road == x_agenda2._idearoot._parent_road
    shave_road = ccn2_agenda.make_road("A", "shave")
    week_road = ccn2_agenda.make_road("A", "weekdays")
    assert ccn2_agenda.get_idea_obj(shave_road) == x_agenda2.get_idea_obj(shave_road)
    assert ccn2_agenda.get_idea_obj(week_road) == x_agenda2.get_idea_obj(week_road)
    assert ccn2_agenda._idearoot == x_agenda2._idearoot
    print(f"{ccn2_agenda._idea_dict.keys()=}")
    print(f"{x_agenda2._idea_dict.keys()=}")
    assert ccn2_agenda._idea_dict == x_agenda2._idea_dict
    assert ccn2_agenda == x_agenda2
    ccn_agenda3 = ccn_dict_of_obj.get(x_agenda3._agent_id)
    x_agenda3.set_agenda_metrics()
    assert ccn_agenda3 == x_agenda3


def test_agenda_jsonExportCorrectyExportsWeights():
    # GIVEN
    x_agenda1 = example_agendas_agenda_v001()
    x_agenda1._weight = 15
    assert 15 == x_agenda1._weight
    assert x_agenda1._idearoot._weight != x_agenda1._weight
    assert x_agenda1._idearoot._weight == 1

    # WHEN
    x_agenda2 = agenda_get_from_json(x_agenda1.get_json())

    # THEN
    assert x_agenda1._weight == 15
    assert x_agenda1._weight == x_agenda2._weight
    assert x_agenda1._idearoot._weight == 1
    assert x_agenda1._idearoot._weight == x_agenda2._idearoot._weight
    assert x_agenda1._idearoot._kids == x_agenda2._idearoot._kids
