import contextlib
from src.pact.pact import PactUnit
from src.pact.idea import IdeaKid
from src.pact.required_idea import acptfactunit_shop
from src.pact.examples.example_pacts import (
    pact_v001 as example_pacts_pact_v001,
    get_pact_x1_3levels_1required_1acptfacts as example_pacts_get_pact_x1_3levels_1required_1acptfacts,
    get_pact_base_time_example as example_pacts_get_pact_base_time_example,
)
from src.pact.pact import (
    get_from_json as pact_get_from_json,
    get_dict_of_pact_from_dict,
)
from src.pact.examples.pact_env import (
    get_pact_temp_env_dir,
    env_dir_setup_cleanup,
)
from src.pact.group import groupunit_shop, balancelink_shop
from src.pact.party import partylink_shop
from src.pact.required_assign import assigned_unit_shop
from src.pact.x_func import (
    x_is_json,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
)
from json import loads as json_loads
from pytest import raises as pytest_raises


def test_pact_get_dict_ReturnsDictObject():
    # GIVEN
    x_pact = example_pacts_pact_v001()
    day_hour_text = "day_hour"
    day_hour_road = f"{x_pact._cure_handle},{day_hour_text}"
    day_hour_idea = x_pact.get_idea_kid(road=day_hour_road)
    day_hour_idea._originunit.set_originlink(title="bob", weight=2)
    x_pact.set_acptfact(
        base=day_hour_road,
        pick=day_hour_road,
        open=0,
        nigh=23,
    )
    time_minute = f"{x_pact._cure_handle},day_minute"
    x_pact.set_acptfact(base=time_minute, pick=time_minute, open=0, nigh=1440)
    yao_text = "Yao"
    x_pact._originunit.set_originlink(yao_text, 1)

    # WHEN
    x_dict = x_pact.get_dict()

    # THEN
    assert x_dict != None
    assert str(type(x_dict)) == "<class 'dict'>"
    assert x_dict["_healer"] == x_pact._healer
    assert x_dict["_cure_handle"] == x_pact._cure_handle
    assert x_dict["_weight"] == x_pact._weight
    assert x_dict["_max_tree_traverse"] == x_pact._max_tree_traverse
    assert x_dict["_auto_output_to_public"] == x_pact._auto_output_to_public
    assert len(x_dict["_partys"]) == len(x_pact._partys)
    assert len(x_dict["_groups"]) == len(x_pact._groups)

    x_idearoot = x_pact._idearoot
    _kids = "_kids"
    _range_source_road = "_range_source_road"
    _numeric_road = "_numeric_road"
    assert x_idearoot._label == x_pact._cure_handle
    assert x_dict["_weight"] == x_idearoot._weight
    assert x_dict["_addin"] == x_idearoot._addin
    assert x_dict["_numor"] == x_idearoot._numor
    assert x_dict["_denom"] == x_idearoot._denom
    assert x_dict["_reest"] == x_idearoot._reest
    assert x_dict["_problem_bool"] == x_idearoot._problem_bool
    assert x_dict["_on_meld_weight_action"] == x_idearoot._on_meld_weight_action
    assert len(x_dict[_kids]) == len(x_idearoot._kids)

    # checking an ideakid._range_source_road attribute
    month_week_text = "month_week"
    month_week_road = f"{x_pact._cure_handle},{month_week_text}"
    month_week_idea_x = x_pact.get_idea_kid(road=month_week_road)
    print("checking TlME,month_week...range_source_road equal to...")
    month_week_special_dict = x_dict[_kids][month_week_text][_range_source_road]
    assert month_week_special_dict != None
    assert month_week_special_dict == f"{x_pact._cure_handle},ced_week"
    assert month_week_special_dict == month_week_idea_x._range_source_road

    # checking an ideakid._numeric_road attribute
    num1_text = "numeric_road_test"
    num1_road = f"{x_pact._cure_handle},{num1_text}"
    num1_idea_x = x_pact.get_idea_kid(road=num1_road)
    print(f"checking {num1_road}...numeric_road equal to...")
    num1_dict_numeric_road = x_dict[_kids][num1_text][_numeric_road]
    assert num1_dict_numeric_road != None
    assert num1_dict_numeric_road == month_week_road
    assert num1_dict_numeric_road == num1_idea_x._numeric_road

    originunit_text = "_originunit"
    day_hour_originunit_dict = x_dict[_kids][day_hour_text][originunit_text]
    assert day_hour_originunit_dict == day_hour_idea._originunit.get_dict()
    _links = "_links"
    x_pact_originlink = x_dict[originunit_text][_links][yao_text]
    print(f"{x_pact_originlink=}")
    assert x_pact_originlink
    assert x_pact_originlink["title"] == yao_text
    assert x_pact_originlink["weight"] == 1


def test_pact_get_dict_ReturnsDictWith_idearoot_AssignedUnit():
    # GIVEN
    run_text = "runners"
    healer_text = "Tom"
    x_pact = PactUnit(_healer=healer_text)
    assigned_unit_x = assigned_unit_shop()
    assigned_unit_x.set_suffgroup(title=run_text)
    x_pact.edit_idea_attr(assignedunit=assigned_unit_x, road=x_pact._cure_handle)

    # WHEN
    x_dict = x_pact.get_dict()

    # THEN
    assert x_dict["_assignedunit"] == assigned_unit_x.get_dict()
    assert x_dict["_assignedunit"] == {"_suffgroups": {run_text: run_text}}


def test_pact_get_dict_ReturnsDictWith_ideakid_AssignedUnit():
    # GIVEN
    healer_text = "Tom"
    x_pact = PactUnit(_healer=healer_text)
    run_text = "run"
    x_pact.set_groupunit(groupunit=groupunit_shop(run_text))

    morn_text = "morning"
    morn_road = f"{x_pact._cure_handle},{morn_text}"
    x_pact.add_idea(idea_kid=IdeaKid(_label=morn_text), pad=x_pact._cure_handle)
    assigned_unit_x = assigned_unit_shop()
    assigned_unit_x.set_suffgroup(title=run_text)
    x_pact.edit_idea_attr(assignedunit=assigned_unit_x, road=morn_road)

    # WHEN
    x_dict = x_pact.get_dict()

    # THEN
    _kids = "_kids"
    _assignedunit = "_assignedunit"

    assigned_dict_x = x_dict[_kids][morn_text][_assignedunit]
    assert assigned_dict_x == assigned_unit_x.get_dict()
    assert assigned_dict_x == {"_suffgroups": {run_text: run_text}}


def test_export_to_JSON_simple_example_works():
    # GIVEN
    x_pact = example_pacts_get_pact_x1_3levels_1required_1acptfacts()
    cure_handle_text = "tiger_econ"
    x_pact.set_cure_handle(cure_handle_text)

    # WHEN
    x_json = x_pact.get_json()

    # THEN
    _kids = "_kids"

    assert x_json != None
    assert True == x_is_json(x_json)
    x_dict = json_loads(x_json)

    assert x_dict["_healer"] == x_pact._healer
    assert x_dict["_cure_handle"] == x_pact._cure_handle
    assert x_dict["_weight"] == x_pact._weight

    x_idearoot = x_pact._idearoot
    assert x_dict["_addin"] == x_idearoot._addin
    assert x_dict["_numor"] == x_idearoot._numor
    assert x_dict["_denom"] == x_idearoot._denom
    assert x_dict["_reest"] == x_idearoot._reest
    assert x_dict["_problem_bool"] == x_idearoot._problem_bool
    assert x_dict["_auto_output_to_public"] == x_pact._auto_output_to_public
    assert len(x_dict[_kids]) == len(x_idearoot._kids)

    shave_text = "shave"
    shave_dict = x_dict[_kids][shave_text]
    shave_acptfactunits = shave_dict["_acptfactunits"]
    print(f"{shave_acptfactunits=}")
    assert len(shave_acptfactunits) == 1
    assert len(shave_acptfactunits) == len(x_idearoot._kids[shave_text]._acptfactunits)


def test_export_to_JSON_BigExampleCorrectlyReturnsValues():
    # GIVEN
    x_pact = example_pacts_pact_v001()
    day_hour_text = "day_hour"
    day_hour_road = f"{x_pact._cure_handle},{day_hour_text}"
    x_pact.set_acptfact(base=day_hour_road, pick=day_hour_road, open=0, nigh=23)
    day_min_text = "day_minute"
    day_min_road = f"{x_pact._cure_handle},{day_min_text}"
    x_pact.set_acptfact(base=day_min_road, pick=day_min_road, open=0, nigh=59)
    acptfactunit_x = acptfactunit_shop(day_min_road, day_min_road, 5, 59)
    x_pact.edit_idea_attr(road=acptfactunit_x.base, acptfactunit=acptfactunit_x)
    x_pact.set_max_tree_traverse(int_x=2)
    yao_text = "Yao"
    x_pact._originunit.set_originlink(yao_text, 1)

    # WHEN
    x_dict = json_loads(x_pact.get_json())

    # THEN
    _kids = "_kids"
    assert x_dict["_healer"] == x_pact._healer
    assert x_dict["_cure_handle"] == x_pact._cure_handle
    assert x_dict["_weight"] == x_pact._weight
    assert x_dict["_max_tree_traverse"] == 2
    assert x_dict["_max_tree_traverse"] == x_pact._max_tree_traverse

    x_idearoot = x_pact._idearoot
    assert x_dict["_addin"] == x_idearoot._addin
    assert x_dict["_numor"] == x_idearoot._numor
    assert x_dict["_denom"] == x_idearoot._denom
    assert x_dict["_reest"] == x_idearoot._reest
    assert x_dict["_problem_bool"] == x_idearoot._problem_bool
    assert len(x_dict[_kids]) == len(x_idearoot._kids)

    kids = x_dict[_kids]
    day_min_dict = kids[day_min_text]
    day_min_acptfactunits_dict = day_min_dict["_acptfactunits"]
    day_min_idea_x = x_pact.get_idea_kid(road=day_min_road)
    print(f"{day_min_acptfactunits_dict=}")
    assert len(day_min_acptfactunits_dict) == 1
    assert len(day_min_acptfactunits_dict) == len(day_min_idea_x._acptfactunits)

    _requiredunits = "_requiredunits"
    cont_text = "Freelancing"
    ulti_text = "Ultimate Frisbee"
    cont_road = f"{x_pact._cure_handle},{cont_text}"
    ulti_road = f"{x_pact._cure_handle},{ulti_text}"
    cont_idea = x_pact.get_idea_kid(road=cont_road)
    ulti_idea = x_pact.get_idea_kid(road=ulti_road)
    cont_requiredunits_dict = x_dict[_kids][cont_text][_requiredunits]
    ulti_requiredunits_dict = x_dict[_kids][ulti_text][_requiredunits]
    assert len(cont_requiredunits_dict) == len(cont_idea._requiredunits)
    assert len(ulti_requiredunits_dict) == len(ulti_idea._requiredunits)
    originunit_text = "_originunit"
    _links = "_links"
    assert len(x_dict[originunit_text][_links])


def test_save_file_CorrectlySavesPactJSON(env_dir_setup_cleanup):
    # GIVEN
    x_pact = example_pacts_pact_v001()
    x_x_pact_json = x_pact.get_json()
    file_title_x = "example_pact1.json"

    # WHEN
    x_func_save_file(
        dest_dir=get_pact_temp_env_dir(),
        file_title=file_title_x,
        file_text=x_x_pact_json,
    )

    # THEN
    assert x_func_open_file(dest_dir=get_pact_temp_env_dir(), file_title=file_title_x)


def test_pact_get_json_CorrectlyWorksForSimpleExample():
    # GIVEN
    y_pact = example_pacts_get_pact_x1_3levels_1required_1acptfacts()
    y_pact.set_max_tree_traverse(23)
    cure_handle_text = "tiger_econ"
    y_pact.set_cure_handle(cure_handle_text)

    shave_text = "shave"
    shave_road = f"{y_pact._cure_handle},{shave_text}"
    shave_idea_y1 = y_pact.get_idea_kid(road=shave_road)
    shave_idea_y1._originunit.set_originlink(title="Sue", weight=4.3)
    # print(f"{shave_road=}")
    # print(f"{shave_idea_x._label=} {shave_idea_x._pad=}")

    sue_text = "sue"
    y_pact.add_partyunit(title=sue_text)
    tim_text = "tim"
    y_pact.add_partyunit(title=tim_text)
    run_text = "runners"
    run_group = groupunit_shop(brand=run_text)
    run_group.set_partylink(partylink=partylink_shop(title=sue_text))
    run_group.set_partylink(partylink=partylink_shop(title=tim_text))
    y_pact.set_groupunit(groupunit=run_group)

    run_assigned_unit = assigned_unit_shop()
    run_assigned_unit.set_suffgroup(title=run_text)
    y_pact.edit_idea_attr(road=y_pact._cure_handle, assignedunit=run_assigned_unit)
    tim_assigned_unit = assigned_unit_shop()
    tim_assigned_unit.set_suffgroup(title=tim_text)
    y_pact.edit_idea_attr(road=shave_road, assignedunit=tim_assigned_unit)
    y_pact.edit_idea_attr(road=shave_road, balancelink=balancelink_shop(brand=tim_text))
    y_pact.edit_idea_attr(road=shave_road, balancelink=balancelink_shop(brand=sue_text))

    y_pact.edit_idea_attr(
        road=y_pact._cure_handle, balancelink=balancelink_shop(brand=sue_text)
    )

    yao_text = "Yao"
    y_pact._originunit.set_originlink(yao_text, 1)
    y_pact._auto_output_to_public = True

    # WHEN
    x_json = y_pact.get_json()
    assert x_is_json(x_json) == True
    x_pact = pact_get_from_json(x_pact_json=x_json)

    # THEN
    assert str(type(x_pact)).find(".pact.PactUnit'>") > 0
    assert x_pact._healer != None
    assert x_pact._healer == y_pact._healer
    assert x_pact._cure_handle == y_pact._cure_handle
    assert x_pact._max_tree_traverse == 23
    assert x_pact._max_tree_traverse == y_pact._max_tree_traverse
    assert x_pact._auto_output_to_public == y_pact._auto_output_to_public

    idearoot_x = x_pact._idearoot
    assert idearoot_x._pad == ""
    assert idearoot_x._pad == y_pact._idearoot._pad
    assert idearoot_x._requiredunits == {}
    assert idearoot_x._assignedunit == y_pact._idearoot._assignedunit
    assert idearoot_x._assignedunit == run_assigned_unit
    assert len(idearoot_x._acptfactunits) == 1
    assert len(idearoot_x._balancelinks) == 1

    assert len(x_pact._idearoot._kids) == 2

    weekday_text = "weekdays"
    weekday_road = f"{y_pact._cure_handle},{weekday_text}"
    weekday_idea_x = x_pact.get_idea_kid(road=weekday_road)
    assert len(weekday_idea_x._kids) == 2

    sunday_text = "Sunday"
    sunday_road = f"{weekday_road},{sunday_text}"
    sunday_idea_x = x_pact.get_idea_kid(road=sunday_road)
    assert sunday_idea_x._weight == 20

    shave_idea_x = x_pact.get_idea_kid(road=shave_road)
    shave_idea_y2 = y_pact.get_idea_kid(road=shave_road)
    assert len(shave_idea_x._requiredunits) == 1
    assert shave_idea_x._assignedunit == shave_idea_y2._assignedunit
    assert shave_idea_x._assignedunit == tim_assigned_unit
    assert shave_idea_x._originunit == shave_idea_y2._originunit
    assert len(shave_idea_x._balancelinks) == 2
    assert len(shave_idea_x._acptfactunits) == 1

    assert len(x_pact._originunit._links) == 1
    assert x_pact._originunit == y_pact._originunit


# def test_pact_get_json_CorrectlyWorksForNotSimpleExample():
#     # GIVEN
#     x_pact1 = example_pacts_pact_v001()
#     x_pact1.set_pact_metrics()
#     x_pact1_json = x_pact1.get_json()
#     assert x_is_json(json_x=x_pact1_json)

#     file_title = "example_pact1.json"
#     file_dir = pact_env()
#     print("File may fail since example_pact1.json is created by a later test")
#     x_pact3_json = x_func_open_file(dest_dir=file_dir, file_title=file_title)
#     # print(x_pact3_json[299000:299155])

#     # WHEN
#     x_pact3 = pact_get_from_json(x_pact_json=x_pact3_json)

#     # THEN
#     assert str(type(x_pact3)).find(".pact.PactUnit'>") > 0
#     assert x_pact3._healer != None
#     assert x_pact3._healer == x_pact1._healer
#     assert x_pact3._max_tree_traverse == 2
#     assert x_pact3._max_tree_traverse == x_pact1._max_tree_traverse
#     assert x_pact3._idearoot._healer != None
#     assert x_pact3._idearoot._healer == x_pact1._idearoot._healer
#     assert x_pact3._idearoot._pad == ""
#     assert x_pact3._idearoot._pad == x_pact1._idearoot._pad
#     assert len(x_pact3._idearoot._kids) == len(x_pact1._idearoot._kids)
#     assert len(x_pact3._groups) == 34
#     assert len(x_pact3._partys) == 22


def test_get_dict_of_pact_from_dict_ReturnsDictOfPactUnits():
    # GIVEN
    x_pact1 = example_pacts_pact_v001()
    x_pact2 = example_pacts_get_pact_x1_3levels_1required_1acptfacts()
    x_pact3 = example_pacts_get_pact_base_time_example()

    cn_dict_of_dicts = {
        x_pact1._healer: x_pact1.get_dict(),
        x_pact2._healer: x_pact2.get_dict(),
        x_pact3._healer: x_pact3.get_dict(),
    }

    # WHEN
    ccn_dict_of_obj = get_dict_of_pact_from_dict(cn_dict_of_dicts)

    # THEN
    assert ccn_dict_of_obj.get(x_pact1._healer) != None
    assert ccn_dict_of_obj.get(x_pact2._healer) != None
    assert ccn_dict_of_obj.get(x_pact3._healer) != None
    cc1_idea_root = ccn_dict_of_obj.get(x_pact1._healer)._idearoot
    assert cc1_idea_root._originunit == x_pact1._idearoot._originunit
    assert ccn_dict_of_obj.get(x_pact1._healer)._idea_dict == x_pact1._idea_dict
    assert ccn_dict_of_obj.get(x_pact1._healer) == x_pact1
    assert ccn_dict_of_obj.get(x_pact2._healer) == x_pact2
    assert ccn_dict_of_obj.get(x_pact3._healer) == x_pact3


def test_pact_jsonExportCorrectyExportsWeights():
    # GIVEN
    x_pact1 = example_pacts_pact_v001()
    x_pact1._weight = 15
    assert 15 == x_pact1._weight
    assert x_pact1._idearoot._weight != x_pact1._weight
    assert x_pact1._idearoot._weight == 1

    # WHEN
    x_pact2 = pact_get_from_json(x_pact1.get_json())

    # THEN
    assert x_pact1._weight == 15
    assert x_pact1._weight == x_pact2._weight
    assert x_pact1._idearoot._weight == 1
    assert x_pact1._idearoot._weight == x_pact2._idearoot._weight
    assert x_pact1._idearoot._kids == x_pact2._idearoot._kids
