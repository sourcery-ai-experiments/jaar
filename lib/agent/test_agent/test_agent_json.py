import contextlib
from lib.agent.required import acptfactunit_shop
from lib.agent.examples.example_agents import (
    agent_v001 as example_agents_agent_v001,
    get_agent_x1_3levels_1required_1acptfacts as example_agents_get_agent_x1_3levels_1required_1acptfacts,
    get_agent_base_time_example as example_agents_get_agent_base_time_example,
)
from lib.agent.agent import (
    get_from_json as agent_get_from_json,
    get_dict_of_agent_from_dict,
)
from lib.agent.examples.get_agent_examples_dir import get_agent_examples_dir
from lib.agent.brand import BrandLink, BrandName
from lib.agent.x_func import (
    x_is_json,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
)
from json import loads as json_loads
from pytest import raises as pytest_raises


def test_agent_get_dict_ReturnsDictObject():
    x_dict = None
    x_agent = example_agents_agent_v001()
    x_agent.set_acptfact(base="TlME,day_hour", pick="TlME,day_hour", open=0, nigh=23)
    time_minute = "TlME,day_minute"
    x_agent.set_acptfact(base=time_minute, pick=time_minute, open=0, nigh=1440)
    assert x_dict is None
    x_dict = x_agent.get_dict()
    assert x_dict != None
    assert str(type(x_dict)) == "<class 'dict'>"
    assert x_dict["_desc"] == x_agent._desc
    assert x_dict["_desc"] == x_agent._idearoot._desc
    assert x_dict["_weight"] == x_agent._weight
    assert x_dict["_weight"] == x_agent._idearoot._weight
    assert x_dict["_max_tree_traverse"] == x_agent._max_tree_traverse
    assert x_dict["_addin"] == x_agent._idearoot._addin
    assert x_dict["_numor"] == x_agent._idearoot._numor
    assert x_dict["_denom"] == x_agent._idearoot._denom
    assert x_dict["_reest"] == x_agent._idearoot._reest
    assert x_dict["_problem_bool"] == x_agent._idearoot._problem_bool
    assert x_dict["_on_meld_weight_action"] == x_agent._idearoot._on_meld_weight_action
    assert len(x_dict["_allys"]) == len(x_agent._allys)
    assert len(x_dict["_brands"]) == len(x_agent._brands)
    assert len(x_dict["_kids"]) == len(x_agent._idearoot._kids)
    with pytest_raises(KeyError) as excinfo:
        x_dict["_level"]
    assert str(excinfo.value) == "'_level'"

    # for kid in x_agent._idearoot._kids.values():
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
    # ap_road = f"{x_agent._desc},{ap_text}"
    # ap_idea = x_agent.get_idea_kid(road=ap_road)
    # print(f"checking {ap_text}...")
    # print(x_dict["_kids"][ap_idea._desc]["_requiredunits"])
    # assert len(x_dict["_kids"][ap_idea._desc]["_requiredunits"]) == 1

    month_week_text = "month_week"
    month_week_road = f"{x_agent._desc},{month_week_text}"
    month_week_idea = x_agent.get_idea_kid(road=month_week_road)
    print("checking TlME,month_week...special_road equal to...")
    print(x_dict["_kids"][month_week_text]["_special_road"])
    print(x_dict["_kids"][month_week_text])
    assert x_dict["_kids"][month_week_text]["_special_road"] != None
    assert x_dict["_kids"][month_week_text]["_special_road"] == "TlME,ced_week"

    numeric_text = "numeric_road_test"
    numeric_road = f"TlME,{numeric_text}"
    print(f"checking {numeric_road}...numeric_road equal to...")
    print(x_dict["_kids"][numeric_text]["_numeric_road"])
    print(x_dict["_kids"][numeric_text])
    assert x_dict["_kids"][numeric_text]["_numeric_road"] != None
    assert x_dict["_kids"][numeric_text]["_numeric_road"] == "TlME,month_week"

    # with contextlib.suppress(KeyError):
    #     if x_dict["_kids"][kid._desc]["_requiredunits"] not in (None, {}):
    #         print(x_dict["_kids"][kid._desc]["_requiredunits"])
    #         print(f"{kid._requiredunits=}")
    #         assert len(x_dict["_kids"][kid._desc]["_requiredunits"]) == len(
    #             kid._requiredunits
    #         )


def test_export_to_JSON_simple_example_works():
    x_json = None
    x_agent = example_agents_get_agent_x1_3levels_1required_1acptfacts()

    assert x_json is None
    x_json = x_agent.get_json()
    assert x_json != None
    assert True == x_is_json(x_json)
    x_dict = json_loads(x_json)
    # print(x_dict)
    assert x_dict["_desc"] == x_agent._desc
    assert x_dict["_weight"] == x_agent._weight
    assert x_dict["_addin"] == x_agent._idearoot._addin
    assert x_dict["_numor"] == x_agent._idearoot._numor
    assert x_dict["_denom"] == x_agent._idearoot._denom
    assert x_dict["_reest"] == x_agent._idearoot._reest
    assert x_dict["_problem_bool"] == x_agent._idearoot._problem_bool
    assert len(x_dict["_kids"]) == len(x_agent._idearoot._kids)
    kids = x_dict["_kids"]
    shave_dict = kids["shave"]
    shave_acptfactunits = shave_dict["_acptfactunits"]
    print(f"{shave_acptfactunits=}")
    assert len(shave_acptfactunits) == 1
    assert len(shave_acptfactunits) == len(
        x_agent._idearoot._kids["shave"]._acptfactunits
    )

    # for _ in x_agent._idearoot._kids.values():
    #     # check requireds exist have correct values
    #     pass


def test_export_to_JSON_BigExampleCorrectlyReturnsValues():
    x_lw_json = None
    x_agent = example_agents_agent_v001()
    print("step 1")
    time_dayhour = "TlME,day_hour"
    x_agent.set_acptfact(base=time_dayhour, pick=time_dayhour, open=0, nigh=23)
    hour_min_road = "TlME,day_minute"
    x_agent.set_acptfact(base=hour_min_road, pick=hour_min_road, open=0, nigh=59)
    acptfactunit_x = acptfactunit_shop(
        base=hour_min_road, pick=hour_min_road, open=5, nigh=59
    )
    print("step 2")
    x_agent.edit_idea_attr(road=acptfactunit_x.base, acptfactunit=acptfactunit_x)
    print("step 3")

    x_agent.set_max_tree_traverse(int_x=2)

    assert x_lw_json is None
    x_lw_json = x_agent.get_json()
    assert x_lw_json != None
    assert True == x_is_json(x_lw_json)
    x_dict = json_loads(x_lw_json)
    # print(x_dict)
    assert x_dict["_desc"] == x_agent._desc
    assert x_dict["_weight"] == x_agent._weight
    assert x_dict["_desc"] == x_agent._desc
    assert x_dict["_max_tree_traverse"] == 2
    assert x_dict["_max_tree_traverse"] == x_agent._max_tree_traverse
    assert x_dict["_addin"] == x_agent._idearoot._addin
    assert x_dict["_numor"] == x_agent._idearoot._numor
    assert x_dict["_denom"] == x_agent._idearoot._denom
    assert x_dict["_reest"] == x_agent._idearoot._reest
    assert x_dict["_problem_bool"] == x_agent._idearoot._problem_bool
    assert len(x_dict["_kids"]) == len(x_agent._idearoot._kids)
    kids = x_dict["_kids"]
    shave_dict = kids["day_minute"]
    shave_acptfactunits = shave_dict["_acptfactunits"]
    print(f"{shave_acptfactunits=}")
    assert len(shave_acptfactunits) == 1
    assert len(shave_acptfactunits) == len(
        x_agent._idearoot._kids["day_minute"]._acptfactunits
    )

    # assert x_dict["_level"] == x_agent._level

    # sourcery skip: no-loop-in-tests
    for kid in x_agent._idearoot._kids.values():
        print(kid._desc)
        with contextlib.suppress(KeyError):
            requireds = x_dict["_kids"][kid._desc]["_requiredunits"]
            assert len(requireds) == len(kid._requiredunits)

    # Test if save works
    x_func_save_file(
        dest_dir=get_agent_examples_dir(),
        file_name="example_agent1.json",
        file_text=x_lw_json,
    )


def test_agent_get_json_CorrectlyWorksForSimpleExample():
    x_json = None
    agent_y = example_agents_get_agent_x1_3levels_1required_1acptfacts()
    agent_y.set_max_tree_traverse(23)

    bikers_link = BrandLink(name=BrandName("bikers"))
    brandlinks_dict = {bikers_link.name: bikers_link}
    agent_y._idearoot._brandlinks = brandlinks_dict

    flyers_name = BrandName("flyers")
    flyers_link = BrandLink(name=flyers_name)
    brandlinks_dict_f = {flyers_link.name: flyers_link, bikers_link.name: bikers_link}
    agent_y._idearoot._kids["shave"]._brandlinks = brandlinks_dict_f

    x_json = agent_y.get_json()
    assert x_is_json(x_json) == True
    agent_x = agent_get_from_json(lw_json=x_json)
    assert str(type(agent_x)).find(".agent.AgentUnit'>") > 0
    assert agent_x._desc != None
    assert agent_x._desc == agent_y._desc
    assert agent_x._max_tree_traverse == 23
    assert agent_x._max_tree_traverse == agent_y._max_tree_traverse
    assert agent_x._idearoot._walk == ""
    assert agent_x._idearoot._walk == agent_y._idearoot._walk
    assert agent_x._idearoot._requiredunits == {}
    assert len(agent_x._idearoot._kids) == 2
    assert len(agent_x._idearoot._kids["weekdays"]._kids) == 2
    assert agent_x._idearoot._kids["weekdays"]._kids["Sunday"]._weight == 20
    # print(agent_y.get_dict())
    assert len(agent_x._idearoot._kids["shave"]._requiredunits) == 1
    assert len(agent_x._idearoot._acptfactunits) == 1
    assert len(agent_x._idearoot._brandlinks) == 1
    assert len(agent_x._idearoot._kids["shave"]._brandlinks) == 2
    print(agent_x._idearoot._kids["shave"]._acptfactunits)
    assert len(agent_x._idearoot._kids["shave"]._acptfactunits) == 1


def test_agent_get_json_CorrectlyWorksForNotSimpleExample():
    lw1 = example_agents_agent_v001()
    lw1.set_agent_metrics()  # clean up idea _road defintions
    lw1_json = lw1.get_json()
    assert x_is_json(json_x=lw1_json)

    file_name = "example_agent1.json"
    file_dir = get_agent_examples_dir()
    print("File may fail since example_agent1.json is created by a later test")
    lw3_json = x_func_open_file(dest_dir=file_dir, file_name=file_name)
    # print(lw3_json[299000:299155])
    lw3 = agent_get_from_json(lw_json=lw3_json)

    assert str(type(lw3)).find(".agent.AgentUnit'>") > 0
    assert lw3._desc != None
    assert lw3._desc == lw1._desc
    assert lw3._max_tree_traverse == 2
    assert lw3._max_tree_traverse == lw1._max_tree_traverse
    assert lw3._idearoot._desc != None
    assert lw3._idearoot._desc == lw1._idearoot._desc
    assert lw3._idearoot._walk == ""
    assert lw3._idearoot._walk == lw1._idearoot._walk
    assert len(lw3._idearoot._kids) == len(lw1._idearoot._kids)
    assert len(lw3._brands) == 34
    assert len(lw3._allys) == 22
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


def test_get_dict_of_agent_from_dict_ReturnsDictOfAgentUnits():
    # GIVEN
    cx1 = example_agents_agent_v001()
    cx2 = example_agents_get_agent_x1_3levels_1required_1acptfacts()
    cx3 = example_agents_get_agent_base_time_example()

    cn_dict_of_dicts = {
        cx1._desc: cx1.get_dict(),
        cx2._desc: cx2.get_dict(),
        cx3._desc: cx3.get_dict(),
    }

    # WHEN
    ccn_dict_of_obj = get_dict_of_agent_from_dict(cn_dict_of_dicts)

    # THEN
    assert ccn_dict_of_obj.get(cx1._desc) != None
    assert ccn_dict_of_obj.get(cx2._desc) != None
    assert ccn_dict_of_obj.get(cx3._desc) != None
    assert ccn_dict_of_obj.get(cx1._desc) == cx1
    assert ccn_dict_of_obj.get(cx2._desc) == cx2
    assert ccn_dict_of_obj.get(cx3._desc) == cx3


def test_agent_jsonExportCorrectyExportsWeights():
    # GIVEN
    cx1 = example_agents_agent_v001()
    cx1._weight = 15
    assert 15 == cx1._weight
    assert cx1._idearoot._weight != cx1._weight
    assert cx1._idearoot._weight == 1

    # WHEN
    cx2 = agent_get_from_json(cx1.get_json())

    # THEN
    assert cx1._weight == 15
    assert cx1._weight == cx2._weight
    assert cx1._idearoot._weight == 1
    assert cx1._idearoot._weight == cx2._idearoot._weight
    assert cx1._idearoot._kids == cx2._idearoot._kids
