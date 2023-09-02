import contextlib
from src.calendar.calendar import CalendarUnit
from src.calendar.idea import IdeaKid
from src.calendar.required_idea import acptfactunit_shop
from src.calendar.examples.example_calendars import (
    calendar_v001 as example_calendars_calendar_v001,
    get_calendar_x1_3levels_1required_1acptfacts as example_calendars_get_calendar_x1_3levels_1required_1acptfacts,
    get_calendar_base_time_example as example_calendars_get_calendar_base_time_example,
)
from src.calendar.calendar import (
    get_from_json as calendar_get_from_json,
    get_dict_of_calendar_from_dict,
)
from src.calendar.examples.get_calendar_examples_dir import (
    get_calendar_temp_env_dir,
    env_dir_setup_cleanup,
)
from src.calendar.group import groupunit_shop, grouplink_shop
from src.calendar.member import memberlink_shop
from src.calendar.required_assign import assigned_unit_shop
from src.calendar.x_func import (
    x_is_json,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
)
from json import loads as json_loads
from pytest import raises as pytest_raises


def test_calendar_get_dict_ReturnsDictObject():
    # GIVEN
    x_calendar = example_calendars_calendar_v001()
    x_calendar.set_acptfact(base="TlME,day_hour", pick="TlME,day_hour", open=0, nigh=23)
    time_minute = "TlME,day_minute"
    x_calendar.set_acptfact(base=time_minute, pick=time_minute, open=0, nigh=1440)

    # WHEN
    x_dict = x_calendar.get_dict()

    # THEN
    assert x_dict != None
    assert str(type(x_dict)) == "<class 'dict'>"
    assert x_dict["_desc"] == x_calendar._desc
    assert x_dict["_weight"] == x_calendar._weight
    assert x_dict["_max_tree_traverse"] == x_calendar._max_tree_traverse
    assert len(x_dict["_members"]) == len(x_calendar._members)
    assert len(x_dict["_groups"]) == len(x_calendar._groups)

    x_idearoot = x_calendar._idearoot
    _kids = "_kids"
    _special_road = "_special_road"
    _numeric_road = "_numeric_road"
    assert x_dict["_desc"] == x_idearoot._desc
    assert x_dict["_weight"] == x_idearoot._weight
    assert x_dict["_addin"] == x_idearoot._addin
    assert x_dict["_numor"] == x_idearoot._numor
    assert x_dict["_denom"] == x_idearoot._denom
    assert x_dict["_reest"] == x_idearoot._reest
    assert x_dict["_problem_bool"] == x_idearoot._problem_bool
    assert x_dict["_on_meld_weight_action"] == x_idearoot._on_meld_weight_action
    assert len(x_dict[_kids]) == len(x_idearoot._kids)

    # checking an ideakid._special_road attribute
    month_week_text = "month_week"
    month_week_road = f"{x_calendar._desc},{month_week_text}"
    month_week_idea_x = x_calendar.get_idea_kid(road=month_week_road)
    print("checking TlME,month_week...special_road equal to...")
    month_week_special_dict = x_dict[_kids][month_week_text][_special_road]
    assert month_week_special_dict != None
    assert month_week_special_dict == "TlME,ced_week"
    assert month_week_special_dict == month_week_idea_x._special_road

    # checking an ideakid._numeric_road attribute
    num1_text = "numeric_road_test"
    num1_road = f"TlME,{num1_text}"
    num1_idea_x = x_calendar.get_idea_kid(road=num1_road)
    print(f"checking {num1_road}...numeric_road equal to...")
    num1_dict_numeric_road = x_dict[_kids][num1_text][_numeric_road]
    assert num1_dict_numeric_road != None
    assert num1_dict_numeric_road == month_week_road
    assert num1_dict_numeric_road == num1_idea_x._numeric_road


def test_calendar_get_dict_ReturnsDictWith_idearoot_AssignedUnit():
    # GIVEN
    src_text = "src"
    run_text = "runners"
    x_calendar = CalendarUnit(_desc=src_text)
    assigned_unit_x = assigned_unit_shop()
    assigned_unit_x.set_suffgroup(name=run_text)
    x_calendar.edit_idea_attr(assignedunit=assigned_unit_x, road=src_text)

    # WHEN
    x_dict = x_calendar.get_dict()

    # THEN
    assert x_dict["_assignedunit"] == assigned_unit_x.get_dict()
    assert x_dict["_assignedunit"] == {"_suffgroups": {run_text: run_text}}


def test_calendar_get_dict_ReturnsDictWith_ideakid_AssignedUnit():
    # GIVEN
    src_text = "src"
    run_text = "run"
    morn_text = "morning"
    morn_road = f"{src_text},{morn_text}"
    x_calendar = CalendarUnit(_desc=src_text)
    x_calendar.add_idea(idea_kid=IdeaKid(_desc=morn_text), walk=src_text)
    assigned_unit_x = assigned_unit_shop()
    assigned_unit_x.set_suffgroup(name=run_text)
    x_calendar.edit_idea_attr(assignedunit=assigned_unit_x, road=morn_road)

    # WHEN
    x_dict = x_calendar.get_dict()

    # THEN
    _kids = "_kids"
    _assignedunit = "_assignedunit"

    assigned_dict_x = x_dict[_kids][morn_text][_assignedunit]
    assert assigned_dict_x == assigned_unit_x.get_dict()
    assert assigned_dict_x == {"_suffgroups": {run_text: run_text}}


def test_export_to_JSON_simple_example_works():
    # GIVEN
    x_calendar = example_calendars_get_calendar_x1_3levels_1required_1acptfacts()

    # WHEN
    x_json = x_calendar.get_json()

    # THEN
    _kids = "_kids"

    assert x_json != None
    assert True == x_is_json(x_json)
    x_dict = json_loads(x_json)

    assert x_dict["_desc"] == x_calendar._desc
    assert x_dict["_weight"] == x_calendar._weight

    x_idearoot = x_calendar._idearoot
    assert x_dict["_addin"] == x_idearoot._addin
    assert x_dict["_numor"] == x_idearoot._numor
    assert x_dict["_denom"] == x_idearoot._denom
    assert x_dict["_reest"] == x_idearoot._reest
    assert x_dict["_problem_bool"] == x_idearoot._problem_bool
    assert len(x_dict[_kids]) == len(x_idearoot._kids)

    shave_text = "shave"
    shave_dict = x_dict[_kids][shave_text]
    shave_acptfactunits = shave_dict["_acptfactunits"]
    print(f"{shave_acptfactunits=}")
    assert len(shave_acptfactunits) == 1
    assert len(shave_acptfactunits) == len(x_idearoot._kids[shave_text]._acptfactunits)


def test_export_to_JSON_BigExampleCorrectlyReturnsValues():
    # GIVEN
    x_calendar = example_calendars_calendar_v001()
    src_text = x_calendar._desc
    day_hour_text = "day_hour"
    day_hour_road = f"{src_text},{day_hour_text}"
    x_calendar.set_acptfact(base=day_hour_road, pick=day_hour_road, open=0, nigh=23)
    day_min_text = "day_minute"
    day_min_road = f"{src_text},{day_min_text}"
    x_calendar.set_acptfact(base=day_min_road, pick=day_min_road, open=0, nigh=59)
    acptfactunit_x = acptfactunit_shop(day_min_road, day_min_road, 5, 59)
    x_calendar.edit_idea_attr(road=acptfactunit_x.base, acptfactunit=acptfactunit_x)
    x_calendar.set_max_tree_traverse(int_x=2)
    x_lw_json = x_calendar.get_json()

    # WHEN
    x_dict = json_loads(x_lw_json)

    # THEN
    _kids = "_kids"
    assert x_dict["_desc"] == x_calendar._desc
    assert x_dict["_weight"] == x_calendar._weight
    assert x_dict["_desc"] == x_calendar._desc
    assert x_dict["_max_tree_traverse"] == 2
    assert x_dict["_max_tree_traverse"] == x_calendar._max_tree_traverse

    x_idearoot = x_calendar._idearoot
    assert x_dict["_addin"] == x_idearoot._addin
    assert x_dict["_numor"] == x_idearoot._numor
    assert x_dict["_denom"] == x_idearoot._denom
    assert x_dict["_reest"] == x_idearoot._reest
    assert x_dict["_problem_bool"] == x_idearoot._problem_bool
    assert len(x_dict[_kids]) == len(x_idearoot._kids)

    kids = x_dict[_kids]
    day_min_dict = kids[day_min_text]
    day_min_acptfactunits_dict = day_min_dict["_acptfactunits"]
    day_min_idea_x = x_calendar.get_idea_kid(road=day_min_road)
    print(f"{day_min_acptfactunits_dict=}")
    assert len(day_min_acptfactunits_dict) == 1
    assert len(day_min_acptfactunits_dict) == len(day_min_idea_x._acptfactunits)

    _requiredunits = "_requiredunits"
    cont_text = "Contractor"
    ulti_text = "Ultimate Frisbee"
    cont_road = f"{src_text},{cont_text}"
    ulti_road = f"{src_text},{ulti_text}"
    cont_idea = x_calendar.get_idea_kid(road=cont_road)
    ulti_idea = x_calendar.get_idea_kid(road=ulti_road)
    cont_requiredunits_dict = x_dict[_kids][cont_text][_requiredunits]
    ulti_requiredunits_dict = x_dict[_kids][ulti_text][_requiredunits]
    assert len(cont_requiredunits_dict) == len(cont_idea._requiredunits)
    assert len(ulti_requiredunits_dict) == len(ulti_idea._requiredunits)


def test_save_file_CorrectlySavesCalendarJSON(env_dir_setup_cleanup):
    # GIVEN
    x_calendar = example_calendars_calendar_v001()
    x_lw_json = x_calendar.get_json()
    file_name_x = "example_calendar1.json"

    # WHEN
    x_func_save_file(
        dest_dir=get_calendar_temp_env_dir(),
        file_name=file_name_x,
        file_text=x_lw_json,
    )

    # THEN
    assert x_func_open_file(dest_dir=get_calendar_temp_env_dir(), file_name=file_name_x)


def test_calendar_get_json_CorrectlyWorksForSimpleExample():
    # GIVEN
    calendar_y = example_calendars_get_calendar_x1_3levels_1required_1acptfacts()
    calendar_y.set_max_tree_traverse(23)
    src_text = calendar_y._desc

    shave_text = "shave"
    shave_road = f"{calendar_y._desc},{shave_text}"
    shave_idea_x = calendar_y.get_idea_kid(road=shave_road)

    sue_text = "sue"
    calendar_y.add_memberunit(name=sue_text)
    tim_text = "tim"
    calendar_y.add_memberunit(name=tim_text)
    run_text = "runners"
    run_group = groupunit_shop(name=run_text)
    run_group.set_memberlink(memberlink=memberlink_shop(name=sue_text))
    run_group.set_memberlink(memberlink=memberlink_shop(name=tim_text))
    calendar_y.set_groupunit(groupunit=run_group)

    run_assigned_unit = assigned_unit_shop()
    run_assigned_unit.set_suffgroup(name=run_text)
    calendar_y.edit_idea_attr(road=src_text, assignedunit=run_assigned_unit)
    tim_assigned_unit = assigned_unit_shop()
    tim_assigned_unit.set_suffgroup(name=tim_text)
    calendar_y.edit_idea_attr(road=shave_road, assignedunit=tim_assigned_unit)
    calendar_y.edit_idea_attr(road=shave_road, grouplink=grouplink_shop(name=tim_text))
    calendar_y.edit_idea_attr(road=shave_road, grouplink=grouplink_shop(name=sue_text))

    calendar_y.edit_idea_attr(road=src_text, grouplink=grouplink_shop(name=sue_text))

    # WHEN
    x_json = calendar_y.get_json()
    assert x_is_json(x_json) == True
    calendar_x = calendar_get_from_json(lw_json=x_json)

    # THEN
    assert str(type(calendar_x)).find(".calendar.CalendarUnit'>") > 0
    assert calendar_x._desc != None
    assert calendar_x._desc == calendar_y._desc
    assert calendar_x._max_tree_traverse == 23
    assert calendar_x._max_tree_traverse == calendar_y._max_tree_traverse

    idearoot_x = calendar_x._idearoot
    assert idearoot_x._walk == ""
    assert idearoot_x._walk == calendar_y._idearoot._walk
    assert idearoot_x._requiredunits == {}
    assert idearoot_x._assignedunit == calendar_y._idearoot._assignedunit
    assert idearoot_x._assignedunit == run_assigned_unit
    assert len(idearoot_x._acptfactunits) == 1
    assert len(idearoot_x._grouplinks) == 1

    assert len(calendar_x._idearoot._kids) == 2

    weekday_text = "weekdays"
    weekday_road = f"{calendar_x._desc},{weekday_text}"
    weekday_idea_x = calendar_x.get_idea_kid(road=weekday_road)
    assert len(weekday_idea_x._kids) == 2

    sunday_text = "Sunday"
    sunday_road = f"{weekday_road},{sunday_text}"
    sunday_idea_x = calendar_x.get_idea_kid(road=sunday_road)
    assert sunday_idea_x._weight == 20

    shave_idea_x = calendar_x.get_idea_kid(road=shave_road)
    shave_idea_y = calendar_y.get_idea_kid(road=shave_road)
    assert len(shave_idea_x._requiredunits) == 1
    assert shave_idea_x._assignedunit == shave_idea_y._assignedunit
    assert shave_idea_x._assignedunit == tim_assigned_unit
    assert len(shave_idea_x._grouplinks) == 2
    assert len(shave_idea_x._acptfactunits) == 1


# def test_calendar_get_json_CorrectlyWorksForNotSimpleExample():
#     # GIVEN
#     cx1 = example_calendars_calendar_v001()
#     cx1.set_calendar_metrics()
#     cx1_json = cx1.get_json()
#     assert x_is_json(json_x=cx1_json)

#     file_name = "example_calendar1.json"
#     file_dir = get_calendar_examples_dir()
#     print("File may fail since example_calendar1.json is created by a later test")
#     cx3_json = x_func_open_file(dest_dir=file_dir, file_name=file_name)
#     # print(cx3_json[299000:299155])

#     # WHEN
#     cx3 = calendar_get_from_json(lw_json=cx3_json)

#     # THEN
#     assert str(type(cx3)).find(".calendar.CalendarUnit'>") > 0
#     assert cx3._desc != None
#     assert cx3._desc == cx1._desc
#     assert cx3._max_tree_traverse == 2
#     assert cx3._max_tree_traverse == cx1._max_tree_traverse
#     assert cx3._idearoot._desc != None
#     assert cx3._idearoot._desc == cx1._idearoot._desc
#     assert cx3._idearoot._walk == ""
#     assert cx3._idearoot._walk == cx1._idearoot._walk
#     assert len(cx3._idearoot._kids) == len(cx1._idearoot._kids)
#     assert len(cx3._groups) == 34
#     assert len(cx3._members) == 22


def test_get_dict_of_calendar_from_dict_ReturnsDictOfCalendarUnits():
    # GIVEN
    cx1 = example_calendars_calendar_v001()
    cx2 = example_calendars_get_calendar_x1_3levels_1required_1acptfacts()
    cx3 = example_calendars_get_calendar_base_time_example()

    cn_dict_of_dicts = {
        cx1._desc: cx1.get_dict(),
        cx2._desc: cx2.get_dict(),
        cx3._desc: cx3.get_dict(),
    }

    # WHEN
    ccn_dict_of_obj = get_dict_of_calendar_from_dict(cn_dict_of_dicts)

    # THEN
    assert ccn_dict_of_obj.get(cx1._desc) != None
    assert ccn_dict_of_obj.get(cx2._desc) != None
    assert ccn_dict_of_obj.get(cx3._desc) != None
    assert ccn_dict_of_obj.get(cx1._desc) == cx1
    assert ccn_dict_of_obj.get(cx2._desc) == cx2
    assert ccn_dict_of_obj.get(cx3._desc) == cx3


def test_calendar_jsonExportCorrectyExportsWeights():
    # GIVEN
    cx1 = example_calendars_calendar_v001()
    cx1._weight = 15
    assert 15 == cx1._weight
    assert cx1._idearoot._weight != cx1._weight
    assert cx1._idearoot._weight == 1

    # WHEN
    cx2 = calendar_get_from_json(cx1.get_json())

    # THEN
    assert cx1._weight == 15
    assert cx1._weight == cx2._weight
    assert cx1._idearoot._weight == 1
    assert cx1._idearoot._weight == cx2._idearoot._weight
    assert cx1._idearoot._kids == cx2._idearoot._kids
