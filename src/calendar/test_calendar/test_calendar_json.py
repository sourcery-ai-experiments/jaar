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
from src.calendar.examples.get_calendar_examples_dir import get_calendar_examples_dir
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
    assert x_dict["_desc"] == x_calendar._idearoot._desc
    assert x_dict["_weight"] == x_calendar._weight
    assert x_dict["_weight"] == x_calendar._idearoot._weight
    assert x_dict["_max_tree_traverse"] == x_calendar._max_tree_traverse
    assert x_dict["_addin"] == x_calendar._idearoot._addin
    assert x_dict["_numor"] == x_calendar._idearoot._numor
    assert x_dict["_denom"] == x_calendar._idearoot._denom
    assert x_dict["_reest"] == x_calendar._idearoot._reest
    assert x_dict["_problem_bool"] == x_calendar._idearoot._problem_bool
    assert (
        x_dict["_on_meld_weight_action"] == x_calendar._idearoot._on_meld_weight_action
    )
    assert len(x_dict["_members"]) == len(x_calendar._members)
    assert len(x_dict["_groups"]) == len(x_calendar._groups)
    assert len(x_dict["_kids"]) == len(x_calendar._idearoot._kids)
    with pytest_raises(KeyError) as excinfo:
        x_dict["_level"]
    assert str(excinfo.value) == "'_level'"

    # for kid in x_calendar._idearoot._kids.values():
    #     # print(len(x_dict["_kids"][kid._desc]["_kids"]))
    #     # print(x_dict["_kids"][kid._desc])
    #     # print(len(kid._kids))
    #     print(f"{kid._desc=}")
    #     # print(kid._kids)
    #     # for gkid in kid._kids.keys():
    #     #     print(gkid)
    #     with contextlib.suppress(KeyError):
    #         dict_grandkids = x_dict["_kids"][kid._desc]["_kids"]
    #         # if dict_grandkids not in (None, {}):
    #         # print(f"{dict_grandkids=}")
    #         # print(f"{len(kid._kids)}")
    #         assert len(dict_grandkids) == len(kid._kids)

    # ap_text = "Asset management"
    # ap_road = f"{x_calendar._desc},{ap_text}"
    # ap_idea = x_calendar.get_idea_kid(road=ap_road)
    # print(f"checking {ap_text}...")
    # print(x_dict["_kids"][ap_idea._desc]["_requiredunits"])
    # assert len(x_dict["_kids"][ap_idea._desc]["_requiredunits"]) == 1

    month_week_text = "month_week"
    _kids = "_kids"
    _special_road = "_special_road"
    month_week_road = f"{x_calendar._desc},{month_week_text}"
    month_week_idea = x_calendar.get_idea_kid(road=month_week_road)
    print("checking TlME,month_week...special_road equal to...")
    print(x_dict[_kids][month_week_text][_special_road])
    print(x_dict[_kids][month_week_text])
    assert x_dict[_kids][month_week_text][_special_road] != None
    assert x_dict[_kids][month_week_text][_special_road] == "TlME,ced_week"

    numeric_text = "numeric_road_test"
    numeric_road = f"TlME,{numeric_text}"
    _numeric_road = "_numeric_road"
    print(f"checking {numeric_road}...numeric_road equal to...")
    print(x_dict[_kids][numeric_text][_numeric_road])
    print(x_dict[_kids][numeric_text])
    assert x_dict[_kids][numeric_text][_numeric_road] != None
    assert x_dict[_kids][numeric_text][_numeric_road] == "TlME,month_week"

    # with contextlib.suppress(KeyError):
    #     if x_dict["_kids"][kid._desc]["_requiredunits"] not in (None, {}):
    #         print(x_dict["_kids"][kid._desc]["_requiredunits"])
    #         print(f"{kid._requiredunits=}")
    #         assert len(x_dict["_kids"][kid._desc]["_requiredunits"]) == len(
    #             kid._requiredunits
    #         )


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
    assert x_dict["_assignedunit"] == {"_suffgroups": {"runners": "runners"}}


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
    assert x_dict[_kids][morn_text][_assignedunit] == assigned_unit_x.get_dict()
    assert x_dict[_kids][morn_text][_assignedunit] == {"_suffgroups": {"run": "run"}}


def test_export_to_JSON_simple_example_works():
    x_json = None
    x_calendar = example_calendars_get_calendar_x1_3levels_1required_1acptfacts()

    assert x_json is None
    x_json = x_calendar.get_json()
    assert x_json != None
    assert True == x_is_json(x_json)
    x_dict = json_loads(x_json)
    # print(x_dict)
    assert x_dict["_desc"] == x_calendar._desc
    assert x_dict["_weight"] == x_calendar._weight
    assert x_dict["_addin"] == x_calendar._idearoot._addin
    assert x_dict["_numor"] == x_calendar._idearoot._numor
    assert x_dict["_denom"] == x_calendar._idearoot._denom
    assert x_dict["_reest"] == x_calendar._idearoot._reest
    assert x_dict["_problem_bool"] == x_calendar._idearoot._problem_bool
    assert len(x_dict["_kids"]) == len(x_calendar._idearoot._kids)
    kids = x_dict["_kids"]
    shave_dict = kids["shave"]
    shave_acptfactunits = shave_dict["_acptfactunits"]
    print(f"{shave_acptfactunits=}")
    assert len(shave_acptfactunits) == 1
    assert len(shave_acptfactunits) == len(
        x_calendar._idearoot._kids["shave"]._acptfactunits
    )

    # for _ in x_calendar._idearoot._kids.values():
    #     # check requireds exist have correct values
    #     pass


def test_export_to_JSON_BigExampleCorrectlyReturnsValues():
    x_lw_json = None
    x_calendar = example_calendars_calendar_v001()
    print("step 1")
    time_dayhour = "TlME,day_hour"
    x_calendar.set_acptfact(base=time_dayhour, pick=time_dayhour, open=0, nigh=23)
    hour_min_road = "TlME,day_minute"
    x_calendar.set_acptfact(base=hour_min_road, pick=hour_min_road, open=0, nigh=59)
    acptfactunit_x = acptfactunit_shop(
        base=hour_min_road, pick=hour_min_road, open=5, nigh=59
    )
    print("step 2")
    x_calendar.edit_idea_attr(road=acptfactunit_x.base, acptfactunit=acptfactunit_x)
    print("step 3")

    x_calendar.set_max_tree_traverse(int_x=2)

    assert x_lw_json is None
    x_lw_json = x_calendar.get_json()
    assert x_lw_json != None
    assert True == x_is_json(x_lw_json)
    x_dict = json_loads(x_lw_json)
    # print(x_dict)
    assert x_dict["_desc"] == x_calendar._desc
    assert x_dict["_weight"] == x_calendar._weight
    assert x_dict["_desc"] == x_calendar._desc
    assert x_dict["_max_tree_traverse"] == 2
    assert x_dict["_max_tree_traverse"] == x_calendar._max_tree_traverse
    assert x_dict["_addin"] == x_calendar._idearoot._addin
    assert x_dict["_numor"] == x_calendar._idearoot._numor
    assert x_dict["_denom"] == x_calendar._idearoot._denom
    assert x_dict["_reest"] == x_calendar._idearoot._reest
    assert x_dict["_problem_bool"] == x_calendar._idearoot._problem_bool
    assert len(x_dict["_kids"]) == len(x_calendar._idearoot._kids)
    kids = x_dict["_kids"]
    shave_dict = kids["day_minute"]
    shave_acptfactunits = shave_dict["_acptfactunits"]
    print(f"{shave_acptfactunits=}")
    assert len(shave_acptfactunits) == 1
    assert len(shave_acptfactunits) == len(
        x_calendar._idearoot._kids["day_minute"]._acptfactunits
    )

    # assert x_dict["_level"] == x_calendar._level

    # sourcery skip: no-loop-in-tests
    for kid in x_calendar._idearoot._kids.values():
        print(kid._desc)
        with contextlib.suppress(KeyError):
            requireds = x_dict["_kids"][kid._desc]["_requiredunits"]
            assert len(requireds) == len(kid._requiredunits)

    # Test if save works
    x_func_save_file(
        dest_dir=get_calendar_examples_dir(),
        file_name="example_calendar1.json",
        file_text=x_lw_json,
    )


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

    assert len(calendar_x._idearoot._kids) == 2
    assert len(calendar_x._idearoot._kids["weekdays"]._kids) == 2
    assert calendar_x._idearoot._kids["weekdays"]._kids["Sunday"]._weight == 20
    # print(calendar_y.get_dict())
    shave_idea_x = calendar_x.get_idea_kid(road=shave_road)
    assert len(shave_idea_x._requiredunits) == 1
    assert shave_idea_x._assignedunit == shave_idea_x._assignedunit
    assert shave_idea_x._assignedunit == tim_assigned_unit
    assert len(calendar_x._idearoot._acptfactunits) == 1
    assert len(calendar_x._idearoot._grouplinks) == 1
    assert len(shave_idea_x._grouplinks) == 2
    print(shave_idea_x._acptfactunits)
    assert len(shave_idea_x._acptfactunits) == 1


def test_calendar_get_json_CorrectlyWorksForNotSimpleExample():
    lw1 = example_calendars_calendar_v001()
    lw1.set_calendar_metrics()  # clean up idea _road defintions
    lw1_json = lw1.get_json()
    assert x_is_json(json_x=lw1_json)

    file_name = "example_calendar1.json"
    file_dir = get_calendar_examples_dir()
    print("File may fail since example_calendar1.json is created by a later test")
    lw3_json = x_func_open_file(dest_dir=file_dir, file_name=file_name)
    # print(lw3_json[299000:299155])
    lw3 = calendar_get_from_json(lw_json=lw3_json)

    assert str(type(lw3)).find(".calendar.CalendarUnit'>") > 0
    assert lw3._desc != None
    assert lw3._desc == lw1._desc
    assert lw3._max_tree_traverse == 2
    assert lw3._max_tree_traverse == lw1._max_tree_traverse
    assert lw3._idearoot._desc != None
    assert lw3._idearoot._desc == lw1._idearoot._desc
    assert lw3._idearoot._walk == ""
    assert lw3._idearoot._walk == lw1._idearoot._walk
    assert len(lw3._idearoot._kids) == len(lw1._idearoot._kids)
    assert len(lw3._groups) == 34
    assert len(lw3._members) == 22
    # for kid in lw3._kids.values():
    #     print(f"{kid._desc=}")

    #     if kid._desc != lw1._kids[kid._desc]._desc:
    #         print(f"{kid._desc=}")
    #         print(f"{lw1._kids[kid._desc]._desc=}")
    #     if kid._kids != None:
    #         print(f"{len(lw1._kids[kid._desc]._kids)=}")

    #     if kid != lw1._kids[kid._desc]:
    #         print(f"{lw1._kids[kid._desc]._desc=}")
    #         # print(f"{kid._walk=}")
    #         # print(f"{lw1._kids[kid._desc]._walk=}")
    #         if kid._requiredunits != lw1._kids[kid._desc]._requiredunits:
    #             if kid._requiredunits != None:
    #                 print(f"{len(kid._requiredunits)=}")
    #                 print(f"{len(lw1._kids[kid._desc]._requiredunits)=}")

    #             print(f"{kid._requiredunits=}")
    #             print(f"{lw1._kids[kid._desc]._requiredunits=}")

    #         print(f"{len(kid._kids)=}")
    #         print(f"{len(lw1._kids[kid._desc]._kids)=}")

    #     assert kid == lw1._kids[kid._desc]

    # assert lw3._kids == lw1._kids


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
