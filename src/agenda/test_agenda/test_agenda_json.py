from src.agenda.road import get_node_delimiter
from src.agenda.agenda import agendaunit_shop
from src.agenda.idea import ideacore_shop
from src.agenda.required_idea import acptfactunit_shop
from src.agenda.examples.example_agendas import (
    agenda_v001 as example_agendas_agenda_v001,
    get_agenda_x1_3levels_1required_1acptfacts as example_agendas_get_agenda_x1_3levels_1required_1acptfacts,
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
from src.agenda.required_assign import assigned_unit_shop
from src.agenda.x_func import (
    x_is_json,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
)
from json import loads as json_loads
from pytest import raises as pytest_raises


def test_agenda_get_dict_ReturnsDictObject():
    # GIVEN
    x_agenda = example_agendas_agenda_v001()
    day_hour_text = "day_hour"
    day_hour_road = x_agenda.make_road(x_agenda._culture_qid, day_hour_text)
    day_hour_idea = x_agenda.get_idea_kid(day_hour_road)
    day_hour_idea._originunit.set_originlink(pid="bob", weight=2)
    x_agenda.set_acptfact(
        base=day_hour_road,
        pick=day_hour_road,
        open=0,
        nigh=23,
    )
    time_minute = x_agenda.make_road(x_agenda._culture_qid, "day_minute")
    x_agenda.set_acptfact(base=time_minute, pick=time_minute, open=0, nigh=1440)
    yao_text = "Yao"
    x_agenda._originunit.set_originlink(yao_text, 1)
    agenda_weight = 23
    x_agenda._weight = agenda_weight

    # WHEN
    agenda_dict = x_agenda.get_dict()

    # THEN
    assert agenda_dict != None
    assert str(type(agenda_dict)) == "<class 'dict'>"
    assert agenda_dict["_healer"] == x_agenda._healer
    assert agenda_dict["_culture_qid"] == x_agenda._culture_qid
    assert agenda_dict["_weight"] == x_agenda._weight
    assert agenda_dict["_weight"] == agenda_weight
    assert agenda_dict["_max_tree_traverse"] == x_agenda._max_tree_traverse
    assert agenda_dict["_auto_output_to_public"] == x_agenda._auto_output_to_public
    assert agenda_dict["_road_node_delimiter"] == x_agenda._road_node_delimiter
    assert len(agenda_dict["_partys"]) == len(x_agenda._partys)
    assert len(agenda_dict["_groups"]) == len(x_agenda._groups)

    x_idearoot = x_agenda._idearoot
    idearoot_dict = agenda_dict["_idearoot"]
    _kids = "_kids"
    _range_source_road = "_range_source_road"
    _numeric_road = "_numeric_road"
    assert x_idearoot._label == x_agenda._culture_qid
    assert idearoot_dict["_label"] == x_idearoot._label
    assert idearoot_dict["_weight"] != agenda_weight
    assert idearoot_dict["_weight"] == x_idearoot._weight
    assert len(idearoot_dict[_kids]) == len(x_idearoot._kids)

    # checking an ideakid._range_source_road attribute
    month_week_text = "month_week"
    month_week_road = x_agenda.make_road(x_agenda._culture_qid, month_week_text)
    month_week_idea_x = x_agenda.get_idea_kid(month_week_road)
    print("checking TlME,month_week...range_source_road equal to...")
    month_week_special_dict = idearoot_dict[_kids][month_week_text][_range_source_road]
    assert month_week_special_dict != None
    assert month_week_special_dict == x_agenda.make_road(
        x_agenda._culture_qid, "ced_week"
    )
    assert month_week_special_dict == month_week_idea_x._range_source_road

    # checking an ideakid._numeric_road attribute
    num1_text = "numeric_road_test"
    num1_road = x_agenda.make_road(x_agenda._culture_qid, num1_text)
    num1_idea_x = x_agenda.get_idea_kid(num1_road)
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
    assert x_agenda_originlink["pid"] == yao_text
    assert x_agenda_originlink["weight"] == 1


def test_agenda_get_dict_ReturnsDictWith_idearoot_AssignedUnit():
    # GIVEN
    run_text = "runners"
    healer_text = "Tom"
    x_agenda = agendaunit_shop(_healer=healer_text)
    assigned_unit_x = assigned_unit_shop()
    assigned_unit_x.set_suffgroup(brand=run_text)
    x_agenda.edit_idea_attr(assignedunit=assigned_unit_x, road=x_agenda._culture_qid)

    # WHEN
    agenda_dict = x_agenda.get_dict()
    idearoot_dict = agenda_dict.get("_idearoot")

    # THEN
    assert idearoot_dict["_assignedunit"] == assigned_unit_x.get_dict()
    assert idearoot_dict["_assignedunit"] == {"_suffgroups": {run_text: run_text}}


def test_agenda_get_dict_ReturnsDictWith_ideakid_AssignedUnit():
    # GIVEN
    healer_text = "Tom"
    x_agenda = agendaunit_shop(_healer=healer_text)
    run_text = "run"
    x_agenda.set_groupunit(groupunit=groupunit_shop(run_text))

    morn_text = "morning"
    morn_road = x_agenda.make_road(x_agenda._culture_qid, morn_text)
    x_agenda.add_idea(idea_kid=ideacore_shop(morn_text), pad=x_agenda._culture_qid)
    assigned_unit_x = assigned_unit_shop()
    assigned_unit_x.set_suffgroup(brand=run_text)
    x_agenda.edit_idea_attr(assignedunit=assigned_unit_x, road=morn_road)

    # WHEN
    agenda_dict = x_agenda.get_dict()
    idearoot_dict = agenda_dict.get("_idearoot")

    # THEN
    _kids = "_kids"
    _assignedunit = "_assignedunit"

    assigned_dict_x = idearoot_dict[_kids][morn_text][_assignedunit]
    assert assigned_dict_x == assigned_unit_x.get_dict()
    assert assigned_dict_x == {"_suffgroups": {run_text: run_text}}


def test_export_to_JSON_simple_example_works():
    # GIVEN
    x_agenda = example_agendas_get_agenda_x1_3levels_1required_1acptfacts()
    tiger_culture_qid = "tiger_econ"
    x_agenda.set_culture_qid(tiger_culture_qid)

    # WHEN
    x_json = x_agenda.get_json()

    # THEN
    _kids = "_kids"

    assert x_json != None
    assert True == x_is_json(x_json)
    agenda_dict = json_loads(x_json)

    assert agenda_dict["_healer"] == x_agenda._healer
    assert agenda_dict["_culture_qid"] == x_agenda._culture_qid
    assert agenda_dict["_weight"] == x_agenda._weight

    x_idearoot = x_agenda._idearoot
    idearoot_dict = agenda_dict.get("_idearoot")

    assert len(idearoot_dict[_kids]) == len(x_idearoot._kids)

    shave_text = "shave"
    shave_dict = idearoot_dict[_kids][shave_text]
    shave_acptfactunits = shave_dict["_acptfactunits"]
    print(f"{shave_acptfactunits=}")
    assert len(shave_acptfactunits) == 1
    assert len(shave_acptfactunits) == len(x_idearoot._kids[shave_text]._acptfactunits)


def test_export_to_JSON_BigExampleCorrectlyReturnsValues():
    # GIVEN
    x_agenda = example_agendas_agenda_v001()
    day_hour_text = "day_hour"
    day_hour_road = x_agenda.make_road(x_agenda._culture_qid, day_hour_text)
    x_agenda.set_acptfact(base=day_hour_road, pick=day_hour_road, open=0, nigh=23)
    day_min_text = "day_minute"
    day_min_road = x_agenda.make_road(x_agenda._culture_qid, day_min_text)
    x_agenda.set_acptfact(base=day_min_road, pick=day_min_road, open=0, nigh=59)
    acptfactunit_x = acptfactunit_shop(day_min_road, day_min_road, 5, 59)
    x_agenda.edit_idea_attr(road=acptfactunit_x.base, acptfactunit=acptfactunit_x)
    x_agenda.set_max_tree_traverse(int_x=2)
    yao_text = "Yao"
    x_agenda._originunit.set_originlink(yao_text, 1)

    # WHEN
    agenda_dict = json_loads(x_agenda.get_json())

    # THEN
    _kids = "_kids"
    assert agenda_dict["_healer"] == x_agenda._healer
    assert agenda_dict["_culture_qid"] == x_agenda._culture_qid
    assert agenda_dict["_weight"] == x_agenda._weight
    assert agenda_dict["_max_tree_traverse"] == 2
    assert agenda_dict["_max_tree_traverse"] == x_agenda._max_tree_traverse
    assert agenda_dict["_road_node_delimiter"] == x_agenda._road_node_delimiter

    x_idearoot = x_agenda._idearoot
    idearoot_dict = agenda_dict.get("_idearoot")
    assert len(idearoot_dict[_kids]) == len(x_idearoot._kids)

    kids = idearoot_dict[_kids]
    day_min_dict = kids[day_min_text]
    day_min_acptfactunits_dict = day_min_dict["_acptfactunits"]
    day_min_idea_x = x_agenda.get_idea_kid(day_min_road)
    print(f"{day_min_acptfactunits_dict=}")
    assert len(day_min_acptfactunits_dict) == 1
    assert len(day_min_acptfactunits_dict) == len(day_min_idea_x._acptfactunits)

    _requiredunits = "_requiredunits"
    cont_text = "Freelancing"
    ulti_text = "Ultimate Frisbee"
    cont_road = x_agenda.make_road(x_agenda._culture_qid, cont_text)
    ulti_road = x_agenda.make_road(x_agenda._culture_qid, ulti_text)
    cont_idea = x_agenda.get_idea_kid(cont_road)
    ulti_idea = x_agenda.get_idea_kid(ulti_road)
    cont_requiredunits_dict = idearoot_dict[_kids][cont_text][_requiredunits]
    ulti_requiredunits_dict = idearoot_dict[_kids][ulti_text][_requiredunits]
    assert len(cont_requiredunits_dict) == len(cont_idea._requiredunits)
    assert len(ulti_requiredunits_dict) == len(ulti_idea._requiredunits)
    originunit_text = "_originunit"
    _links = "_links"
    assert len(agenda_dict[originunit_text][_links])


def test_save_file_CorrectlySavesAgendaJSON(env_dir_setup_cleanup):
    # GIVEN
    x_agenda = example_agendas_agenda_v001()
    x_x_agenda_json = x_agenda.get_json()
    file_name_x = "example_agenda1.json"

    # WHEN
    x_func_save_file(
        dest_dir=get_agenda_temp_env_dir(),
        file_name=file_name_x,
        file_text=x_x_agenda_json,
    )

    # THEN
    assert x_func_open_file(dest_dir=get_agenda_temp_env_dir(), file_name=file_name_x)


def test_agenda_get_json_CorrectlyWorksForSimpleExample():
    # GIVEN
    y_agenda = example_agendas_get_agenda_x1_3levels_1required_1acptfacts()
    y_agenda.set_max_tree_traverse(23)
    tiger_culture_qid = "tiger_econ"
    y_agenda.set_culture_qid(tiger_culture_qid)

    shave_text = "shave"
    shave_road = y_agenda.make_road(y_agenda._culture_qid, shave_text)
    shave_idea_y1 = y_agenda.get_idea_kid(shave_road)
    shave_idea_y1._originunit.set_originlink(pid="Sue", weight=4.3)
    # print(f"{shave_road=}")
    # print(f"{shave_idea_x._label=} {shave_idea_x._pad=}")

    sue_text = "sue"
    y_agenda.add_partyunit(pid=sue_text)
    tim_text = "tim"
    y_agenda.add_partyunit(pid=tim_text)
    run_text = "runners"
    run_group = groupunit_shop(brand=run_text)
    run_group.set_partylink(partylink=partylink_shop(pid=sue_text))
    run_group.set_partylink(partylink=partylink_shop(pid=tim_text))
    y_agenda.set_groupunit(groupunit=run_group)

    run_assigned_unit = assigned_unit_shop()
    run_assigned_unit.set_suffgroup(brand=run_text)
    y_agenda.edit_idea_attr(road=y_agenda._culture_qid, assignedunit=run_assigned_unit)
    tim_assigned_unit = assigned_unit_shop()
    tim_assigned_unit.set_suffgroup(brand=tim_text)
    y_agenda.edit_idea_attr(shave_road, assignedunit=tim_assigned_unit)
    y_agenda.edit_idea_attr(shave_road, balancelink=balancelink_shop(tim_text))
    y_agenda.edit_idea_attr(shave_road, balancelink=balancelink_shop(sue_text))
    y_agenda.edit_idea_attr(
        y_agenda._culture_qid, balancelink=balancelink_shop(sue_text)
    )

    yao_text = "Yao"
    y_agenda._originunit.set_originlink(yao_text, 1)
    y_agenda._auto_output_to_public = True

    # WHEN
    x_json = y_agenda.get_json()
    assert x_is_json(x_json) == True
    x_agenda = agenda_get_from_json(x_agenda_json=x_json)

    # THEN
    assert str(type(x_agenda)).find(".agenda.AgendaUnit'>") > 0
    assert x_agenda._healer != None
    assert x_agenda._healer == y_agenda._healer
    assert x_agenda._culture_qid == y_agenda._culture_qid
    assert x_agenda._max_tree_traverse == 23
    assert x_agenda._max_tree_traverse == y_agenda._max_tree_traverse
    assert x_agenda._auto_output_to_public == y_agenda._auto_output_to_public
    assert x_agenda._road_node_delimiter == y_agenda._road_node_delimiter
    # assert x_agenda._road_node_delimiter == slash_road_node_delimiter

    idearoot_x = x_agenda._idearoot
    assert idearoot_x._pad == ""
    assert idearoot_x._pad == y_agenda._idearoot._pad
    assert idearoot_x._requiredunits == {}
    assert idearoot_x._assignedunit == y_agenda._idearoot._assignedunit
    assert idearoot_x._assignedunit == run_assigned_unit
    assert len(idearoot_x._acptfactunits) == 1
    assert len(idearoot_x._balancelinks) == 1

    assert len(x_agenda._idearoot._kids) == 2

    weekday_text = "weekdays"
    weekday_road = x_agenda.make_road(y_agenda._culture_qid, weekday_text)
    weekday_idea_x = x_agenda.get_idea_kid(weekday_road)
    assert len(weekday_idea_x._kids) == 2

    sunday_text = "Sunday"
    sunday_road = x_agenda.make_road(weekday_road, sunday_text)
    sunday_idea_x = x_agenda.get_idea_kid(sunday_road)
    assert sunday_idea_x._weight == 20

    shave_idea_x = x_agenda.get_idea_kid(shave_road)
    shave_idea_y2 = y_agenda.get_idea_kid(shave_road)
    assert len(shave_idea_x._requiredunits) == 1
    assert shave_idea_x._assignedunit == shave_idea_y2._assignedunit
    assert shave_idea_x._assignedunit == tim_assigned_unit
    assert shave_idea_x._originunit == shave_idea_y2._originunit
    assert len(shave_idea_x._balancelinks) == 2
    assert len(shave_idea_x._acptfactunits) == 1

    assert len(x_agenda._originunit._links) == 1
    assert x_agenda._originunit == y_agenda._originunit


def test_agenda_get_json_CorrectlyWorksFor_delimiter_Data():
    # GIVEN
    slash_delimiter = "/"
    a_bob_agenda = agendaunit_shop("bob", _road_node_delimiter=slash_delimiter)
    assert a_bob_agenda._road_node_delimiter != get_node_delimiter()

    # WHEN
    bob_json = a_bob_agenda.get_json()
    b_bob_agenda = agenda_get_from_json(bob_json)

    # THEN
    assert b_bob_agenda._road_node_delimiter != get_node_delimiter()
    assert b_bob_agenda._road_node_delimiter == slash_delimiter
    assert b_bob_agenda._road_node_delimiter == a_bob_agenda._road_node_delimiter


# def test_agenda_get_json_CorrectlyWorksForNotSimpleExample():
#     # GIVEN
#     x_agenda1 = example_agendas_agenda_v001()
#     x_agenda1.set_agenda_metrics()
#     x_agenda1_json = x_agenda1.get_json()
#     assert x_is_json(json_x=x_agenda1_json)

#     file_name = "example_agenda1.json"
#     file_dir = agenda_env()
#     print("File may fail since example_agenda1.json is created by a later test")
#     x_agenda3_json = x_func_open_file(dest_dir=file_dir, file_name=file_name)
#     # print(x_agenda3_json[299000:299155])

#     # WHEN
#     x_agenda3 = agenda_get_from_json(x_agenda_json=x_agenda3_json)

#     # THEN
#     assert str(type(x_agenda3)).find(".agenda.AgendaUnit'>") > 0
#     assert x_agenda3._healer != None
#     assert x_agenda3._healer == x_agenda1._healer
#     assert x_agenda3._max_tree_traverse == 2
#     assert x_agenda3._max_tree_traverse == x_agenda1._max_tree_traverse
#     assert x_agenda3._idearoot._healer != None
#     assert x_agenda3._idearoot._healer == x_agenda1._idearoot._healer
#     assert x_agenda3._idearoot._pad == ""
#     assert x_agenda3._idearoot._pad == x_agenda1._idearoot._pad
#     assert len(x_agenda3._idearoot._kids) == len(x_agenda1._idearoot._kids)
#     assert len(x_agenda3._groups) == 34
#     assert len(x_agenda3._partys) == 22


def test_get_dict_of_agenda_from_dict_ReturnsDictOfAgendaUnits():
    # GIVEN
    x_agenda1 = example_agendas_agenda_v001()
    x_agenda2 = example_agendas_get_agenda_x1_3levels_1required_1acptfacts()
    x_agenda3 = example_agendas_get_agenda_base_time_example()

    cn_dict_of_dicts = {
        x_agenda1._healer: x_agenda1.get_dict(),
        x_agenda2._healer: x_agenda2.get_dict(),
        x_agenda3._healer: x_agenda3.get_dict(),
    }

    # WHEN
    ccn_dict_of_obj = get_dict_of_agenda_from_dict(cn_dict_of_dicts)

    # THEN
    assert ccn_dict_of_obj.get(x_agenda1._healer) != None
    assert ccn_dict_of_obj.get(x_agenda2._healer) != None
    assert ccn_dict_of_obj.get(x_agenda3._healer) != None
    cc1_idea_root = ccn_dict_of_obj.get(x_agenda1._healer)._idearoot
    assert cc1_idea_root._originunit == x_agenda1._idearoot._originunit
    assert ccn_dict_of_obj.get(x_agenda1._healer)._idea_dict == x_agenda1._idea_dict
    assert ccn_dict_of_obj.get(x_agenda1._healer) == x_agenda1
    assert ccn_dict_of_obj.get(x_agenda2._healer) == x_agenda2
    assert ccn_dict_of_obj.get(x_agenda3._healer) == x_agenda3


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
