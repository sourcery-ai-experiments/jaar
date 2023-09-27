import contextlib
from src.contract.contract import ContractUnit
from src.contract.idea import IdeaKid
from src.contract.required_idea import acptfactunit_shop
from src.contract.examples.example_contracts import (
    contract_v001 as example_contracts_contract_v001,
    get_contract_x1_3levels_1required_1acptfacts as example_contracts_get_contract_x1_3levels_1required_1acptfacts,
    get_contract_base_time_example as example_contracts_get_contract_base_time_example,
)
from src.contract.contract import (
    get_from_json as contract_get_from_json,
    get_dict_of_contract_from_dict,
)
from src.contract.examples.contract_env import (
    get_contract_temp_env_dir,
    env_dir_setup_cleanup,
)
from src.contract.group import groupunit_shop, grouplink_shop
from src.contract.member import memberlink_shop
from src.contract.required_assign import assigned_unit_shop
from src.contract.road import get_economy_root_label as root_label
from src.contract.x_func import (
    x_is_json,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
)
from json import loads as json_loads
from pytest import raises as pytest_raises


def test_contract_get_dict_ReturnsDictObject():
    # GIVEN
    x_contract = example_contracts_contract_v001()
    day_hour_text = "day_hour"
    day_hour_road = f"{root_label()},{day_hour_text}"
    day_hour_idea = x_contract.get_idea_kid(road=day_hour_road)
    day_hour_idea._originunit.set_originlink(name="bob", weight=2)
    x_contract.set_acptfact(
        base=day_hour_road,
        pick=day_hour_road,
        open=0,
        nigh=23,
    )
    time_minute = f"{root_label()},day_minute"
    x_contract.set_acptfact(base=time_minute, pick=time_minute, open=0, nigh=1440)
    yao_text = "Yao"
    x_contract._originunit.set_originlink(yao_text, 1)

    # WHEN
    x_dict = x_contract.get_dict()

    # THEN
    assert x_dict != None
    assert str(type(x_dict)) == "<class 'dict'>"
    assert x_dict["_owner"] == x_contract._owner
    assert x_dict["_weight"] == x_contract._weight
    assert x_dict["_max_tree_traverse"] == x_contract._max_tree_traverse
    assert x_dict["_auto_output_to_public"] == x_contract._auto_output_to_public
    assert len(x_dict["_members"]) == len(x_contract._members)
    assert len(x_dict["_groups"]) == len(x_contract._groups)

    x_idearoot = x_contract._idearoot
    _kids = "_kids"
    _range_source_road = "_range_source_road"
    _numeric_road = "_numeric_road"
    assert x_idearoot._label == root_label()
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
    month_week_road = f"{root_label()},{month_week_text}"
    month_week_idea_x = x_contract.get_idea_kid(road=month_week_road)
    print("checking TlME,month_week...range_source_road equal to...")
    month_week_special_dict = x_dict[_kids][month_week_text][_range_source_road]
    assert month_week_special_dict != None
    assert month_week_special_dict == f"{root_label()},ced_week"
    assert month_week_special_dict == month_week_idea_x._range_source_road

    # checking an ideakid._numeric_road attribute
    num1_text = "numeric_road_test"
    num1_road = f"{root_label()},{num1_text}"
    num1_idea_x = x_contract.get_idea_kid(road=num1_road)
    print(f"checking {num1_road}...numeric_road equal to...")
    num1_dict_numeric_road = x_dict[_kids][num1_text][_numeric_road]
    assert num1_dict_numeric_road != None
    assert num1_dict_numeric_road == month_week_road
    assert num1_dict_numeric_road == num1_idea_x._numeric_road

    originunit_text = "_originunit"
    day_hour_originunit_dict = x_dict[_kids][day_hour_text][originunit_text]
    assert day_hour_originunit_dict == day_hour_idea._originunit.get_dict()
    _links = "_links"
    contract_x_originlink = x_dict[originunit_text][_links][yao_text]
    print(f"{contract_x_originlink=}")
    assert contract_x_originlink
    assert contract_x_originlink["name"] == yao_text
    assert contract_x_originlink["weight"] == 1


def test_contract_get_dict_ReturnsDictWith_idearoot_AssignedUnit():
    # GIVEN
    run_text = "runners"
    owner_text = "Tom"
    x_contract = ContractUnit(_owner=owner_text)
    assigned_unit_x = assigned_unit_shop()
    assigned_unit_x.set_suffgroup(name=run_text)
    x_contract.edit_idea_attr(assignedunit=assigned_unit_x, road=root_label())

    # WHEN
    x_dict = x_contract.get_dict()

    # THEN
    assert x_dict["_assignedunit"] == assigned_unit_x.get_dict()
    assert x_dict["_assignedunit"] == {"_suffgroups": {run_text: run_text}}


def test_contract_get_dict_ReturnsDictWith_ideakid_AssignedUnit():
    # GIVEN
    run_text = "run"
    morn_text = "morning"
    morn_road = f"{root_label()},{morn_text}"
    owner_text = "Tom"
    x_contract = ContractUnit(_owner=owner_text)
    x_contract.set_groupunit(groupunit=groupunit_shop(run_text))
    x_contract.add_idea(idea_kid=IdeaKid(_label=morn_text), walk=root_label())
    assigned_unit_x = assigned_unit_shop()
    assigned_unit_x.set_suffgroup(name=run_text)
    x_contract.edit_idea_attr(assignedunit=assigned_unit_x, road=morn_road)

    # WHEN
    x_dict = x_contract.get_dict()

    # THEN
    _kids = "_kids"
    _assignedunit = "_assignedunit"

    assigned_dict_x = x_dict[_kids][morn_text][_assignedunit]
    assert assigned_dict_x == assigned_unit_x.get_dict()
    assert assigned_dict_x == {"_suffgroups": {run_text: run_text}}


def test_export_to_JSON_simple_example_works():
    # GIVEN
    x_contract = example_contracts_get_contract_x1_3levels_1required_1acptfacts()

    # WHEN
    x_json = x_contract.get_json()

    # THEN
    _kids = "_kids"

    assert x_json != None
    assert True == x_is_json(x_json)
    x_dict = json_loads(x_json)

    assert x_dict["_owner"] == x_contract._owner
    assert x_dict["_weight"] == x_contract._weight

    x_idearoot = x_contract._idearoot
    assert x_dict["_addin"] == x_idearoot._addin
    assert x_dict["_numor"] == x_idearoot._numor
    assert x_dict["_denom"] == x_idearoot._denom
    assert x_dict["_reest"] == x_idearoot._reest
    assert x_dict["_problem_bool"] == x_idearoot._problem_bool
    assert x_dict["_auto_output_to_public"] == x_contract._auto_output_to_public
    assert len(x_dict[_kids]) == len(x_idearoot._kids)

    shave_text = "shave"
    shave_dict = x_dict[_kids][shave_text]
    shave_acptfactunits = shave_dict["_acptfactunits"]
    print(f"{shave_acptfactunits=}")
    assert len(shave_acptfactunits) == 1
    assert len(shave_acptfactunits) == len(x_idearoot._kids[shave_text]._acptfactunits)


def test_export_to_JSON_BigExampleCorrectlyReturnsValues():
    # GIVEN
    x_contract = example_contracts_contract_v001()
    day_hour_text = "day_hour"
    day_hour_road = f"{root_label()},{day_hour_text}"
    x_contract.set_acptfact(base=day_hour_road, pick=day_hour_road, open=0, nigh=23)
    day_min_text = "day_minute"
    day_min_road = f"{root_label()},{day_min_text}"
    x_contract.set_acptfact(base=day_min_road, pick=day_min_road, open=0, nigh=59)
    acptfactunit_x = acptfactunit_shop(day_min_road, day_min_road, 5, 59)
    x_contract.edit_idea_attr(road=acptfactunit_x.base, acptfactunit=acptfactunit_x)
    x_contract.set_max_tree_traverse(int_x=2)
    yao_text = "Yao"
    x_contract._originunit.set_originlink(yao_text, 1)

    # WHEN
    x_dict = json_loads(x_contract.get_json())

    # THEN
    _kids = "_kids"
    assert x_dict["_owner"] == x_contract._owner
    assert x_dict["_weight"] == x_contract._weight
    assert x_dict["_max_tree_traverse"] == 2
    assert x_dict["_max_tree_traverse"] == x_contract._max_tree_traverse

    x_idearoot = x_contract._idearoot
    assert x_dict["_addin"] == x_idearoot._addin
    assert x_dict["_numor"] == x_idearoot._numor
    assert x_dict["_denom"] == x_idearoot._denom
    assert x_dict["_reest"] == x_idearoot._reest
    assert x_dict["_problem_bool"] == x_idearoot._problem_bool
    assert len(x_dict[_kids]) == len(x_idearoot._kids)

    kids = x_dict[_kids]
    day_min_dict = kids[day_min_text]
    day_min_acptfactunits_dict = day_min_dict["_acptfactunits"]
    day_min_idea_x = x_contract.get_idea_kid(road=day_min_road)
    print(f"{day_min_acptfactunits_dict=}")
    assert len(day_min_acptfactunits_dict) == 1
    assert len(day_min_acptfactunits_dict) == len(day_min_idea_x._acptfactunits)

    _requiredunits = "_requiredunits"
    cont_text = "Freelancing"
    ulti_text = "Ultimate Frisbee"
    cont_road = f"{root_label()},{cont_text}"
    ulti_road = f"{root_label()},{ulti_text}"
    cont_idea = x_contract.get_idea_kid(road=cont_road)
    ulti_idea = x_contract.get_idea_kid(road=ulti_road)
    cont_requiredunits_dict = x_dict[_kids][cont_text][_requiredunits]
    ulti_requiredunits_dict = x_dict[_kids][ulti_text][_requiredunits]
    assert len(cont_requiredunits_dict) == len(cont_idea._requiredunits)
    assert len(ulti_requiredunits_dict) == len(ulti_idea._requiredunits)
    originunit_text = "_originunit"
    _links = "_links"
    assert len(x_dict[originunit_text][_links])


def test_save_file_CorrectlySavesContractJSON(env_dir_setup_cleanup):
    # GIVEN
    x_contract = example_contracts_contract_v001()
    x_cx_json = x_contract.get_json()
    file_name_x = "example_contract1.json"

    # WHEN
    x_func_save_file(
        dest_dir=get_contract_temp_env_dir(),
        file_name=file_name_x,
        file_text=x_cx_json,
    )

    # THEN
    assert x_func_open_file(dest_dir=get_contract_temp_env_dir(), file_name=file_name_x)


def test_contract_get_json_CorrectlyWorksForSimpleExample():
    # GIVEN
    contract_y = example_contracts_get_contract_x1_3levels_1required_1acptfacts()
    contract_y.set_max_tree_traverse(23)

    shave_text = "shave"
    shave_road = f"{root_label()},{shave_text}"
    shave_idea_y1 = contract_y.get_idea_kid(road=shave_road)
    shave_idea_y1._originunit.set_originlink(name="Sue", weight=4.3)
    # print(f"{shave_road=}")
    # print(f"{shave_idea_x._label=} {shave_idea_x._walk=}")

    sue_text = "sue"
    contract_y.add_memberunit(name=sue_text)
    tim_text = "tim"
    contract_y.add_memberunit(name=tim_text)
    run_text = "runners"
    run_group = groupunit_shop(name=run_text)
    run_group.set_memberlink(memberlink=memberlink_shop(name=sue_text))
    run_group.set_memberlink(memberlink=memberlink_shop(name=tim_text))
    contract_y.set_groupunit(groupunit=run_group)

    run_assigned_unit = assigned_unit_shop()
    run_assigned_unit.set_suffgroup(name=run_text)
    contract_y.edit_idea_attr(road=root_label(), assignedunit=run_assigned_unit)
    tim_assigned_unit = assigned_unit_shop()
    tim_assigned_unit.set_suffgroup(name=tim_text)
    contract_y.edit_idea_attr(road=shave_road, assignedunit=tim_assigned_unit)
    contract_y.edit_idea_attr(road=shave_road, grouplink=grouplink_shop(name=tim_text))
    contract_y.edit_idea_attr(road=shave_road, grouplink=grouplink_shop(name=sue_text))

    contract_y.edit_idea_attr(
        road=root_label(), grouplink=grouplink_shop(name=sue_text)
    )

    yao_text = "Yao"
    contract_y._originunit.set_originlink(yao_text, 1)
    contract_y._auto_output_to_public = True

    # WHEN
    x_json = contract_y.get_json()
    assert x_is_json(x_json) == True
    contract_x = contract_get_from_json(cx_json=x_json)

    # THEN
    assert str(type(contract_x)).find(".contract.ContractUnit'>") > 0
    assert contract_x._owner != None
    assert contract_x._owner == contract_y._owner
    assert contract_x._max_tree_traverse == 23
    assert contract_x._max_tree_traverse == contract_y._max_tree_traverse
    assert contract_x._auto_output_to_public == contract_y._auto_output_to_public

    idearoot_x = contract_x._idearoot
    assert idearoot_x._walk == ""
    assert idearoot_x._walk == contract_y._idearoot._walk
    assert idearoot_x._requiredunits == {}
    assert idearoot_x._assignedunit == contract_y._idearoot._assignedunit
    assert idearoot_x._assignedunit == run_assigned_unit
    assert len(idearoot_x._acptfactunits) == 1
    assert len(idearoot_x._grouplinks) == 1

    assert len(contract_x._idearoot._kids) == 2

    weekday_text = "weekdays"
    weekday_road = f"{root_label()},{weekday_text}"
    weekday_idea_x = contract_x.get_idea_kid(road=weekday_road)
    assert len(weekday_idea_x._kids) == 2

    sunday_text = "Sunday"
    sunday_road = f"{weekday_road},{sunday_text}"
    sunday_idea_x = contract_x.get_idea_kid(road=sunday_road)
    assert sunday_idea_x._weight == 20

    shave_idea_x = contract_x.get_idea_kid(road=shave_road)
    shave_idea_y2 = contract_y.get_idea_kid(road=shave_road)
    assert len(shave_idea_x._requiredunits) == 1
    assert shave_idea_x._assignedunit == shave_idea_y2._assignedunit
    assert shave_idea_x._assignedunit == tim_assigned_unit
    assert shave_idea_x._originunit == shave_idea_y2._originunit
    assert len(shave_idea_x._grouplinks) == 2
    assert len(shave_idea_x._acptfactunits) == 1

    assert len(contract_x._originunit._links) == 1
    assert contract_x._originunit == contract_y._originunit


# def test_contract_get_json_CorrectlyWorksForNotSimpleExample():
#     # GIVEN
#     cx1 = example_contracts_contract_v001()
#     cx1.set_contract_metrics()
#     cx1_json = cx1.get_json()
#     assert x_is_json(json_x=cx1_json)

#     file_name = "example_contract1.json"
#     file_dir = contract_env()
#     print("File may fail since example_contract1.json is created by a later test")
#     cx3_json = x_func_open_file(dest_dir=file_dir, file_name=file_name)
#     # print(cx3_json[299000:299155])

#     # WHEN
#     cx3 = contract_get_from_json(cx_json=cx3_json)

#     # THEN
#     assert str(type(cx3)).find(".contract.ContractUnit'>") > 0
#     assert cx3._owner != None
#     assert cx3._owner == cx1._owner
#     assert cx3._max_tree_traverse == 2
#     assert cx3._max_tree_traverse == cx1._max_tree_traverse
#     assert cx3._idearoot._owner != None
#     assert cx3._idearoot._owner == cx1._idearoot._owner
#     assert cx3._idearoot._walk == ""
#     assert cx3._idearoot._walk == cx1._idearoot._walk
#     assert len(cx3._idearoot._kids) == len(cx1._idearoot._kids)
#     assert len(cx3._groups) == 34
#     assert len(cx3._members) == 22


def test_get_dict_of_contract_from_dict_ReturnsDictOfContractUnits():
    # GIVEN
    cx1 = example_contracts_contract_v001()
    cx2 = example_contracts_get_contract_x1_3levels_1required_1acptfacts()
    cx3 = example_contracts_get_contract_base_time_example()

    cn_dict_of_dicts = {
        cx1._owner: cx1.get_dict(),
        cx2._owner: cx2.get_dict(),
        cx3._owner: cx3.get_dict(),
    }

    # WHEN
    ccn_dict_of_obj = get_dict_of_contract_from_dict(cn_dict_of_dicts)

    # THEN
    assert ccn_dict_of_obj.get(cx1._owner) != None
    assert ccn_dict_of_obj.get(cx2._owner) != None
    assert ccn_dict_of_obj.get(cx3._owner) != None
    cc1_idea_root = ccn_dict_of_obj.get(cx1._owner)._idearoot
    assert cc1_idea_root._originunit == cx1._idearoot._originunit
    assert ccn_dict_of_obj.get(cx1._owner)._idea_dict == cx1._idea_dict
    assert ccn_dict_of_obj.get(cx1._owner) == cx1
    assert ccn_dict_of_obj.get(cx2._owner) == cx2
    assert ccn_dict_of_obj.get(cx3._owner) == cx3


def test_contract_jsonExportCorrectyExportsWeights():
    # GIVEN
    cx1 = example_contracts_contract_v001()
    cx1._weight = 15
    assert 15 == cx1._weight
    assert cx1._idearoot._weight != cx1._weight
    assert cx1._idearoot._weight == 1

    # WHEN
    cx2 = contract_get_from_json(cx1.get_json())

    # THEN
    assert cx1._weight == 15
    assert cx1._weight == cx2._weight
    assert cx1._idearoot._weight == 1
    assert cx1._idearoot._weight == cx2._idearoot._weight
    assert cx1._idearoot._kids == cx2._idearoot._kids
