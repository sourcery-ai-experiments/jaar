from src.agent.agent import (
    AgentUnit,
    get_from_json as agent_get_from_json,
    get_meld_of_agent_files,
)
from src.agent.examples.get_agent_examples_dir import get_agent_examples_dir
from src.agent.tool import ToolCore, ToolKid
from src.agent.road import Road
from src.agent.required import RequiredUnit
from src.agent.member import memberlink_shop
from src.agent.group import groupunit_shop, grouplink_shop
from src.agent.examples.example_agents import (
    get_agent_with_4_levels as example_agents_get_agent_with_4_levels,
    get_agent_with_4_levels_and_2requireds as example_agents_get_agent_with_4_levels_and_2requireds,
    get_agent_with7amCleanTableRequired as example_agents_get_agent_with7amCleanTableRequired,
    get_agent_with_4_levels_and_2requireds_2acptfacts as example_agents_get_agent_with_4_levels_and_2requireds_2acptfacts,
    agent_v001 as example_agents_agent_v001,
)
from src.agent.x_func import (
    dir_files as x_func_dir_files,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
)
from src.system.examples.env_kit import (
    env_dir_setup_cleanup,
    get_temp_env_dir,
)
from pytest import raises as pytest_raises


def test_agentunit_get_bond_status_ReturnsCorrectBool():
    # GIVEN
    jessi_text = "jessi"
    cx = AgentUnit(_desc=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{jessi_text},{casa_text}")

    # WHEN\THEN no action tool exists
    cx.add_tool(tool_kid=ToolKid(_desc=casa_text), walk=jessi_text)
    assert cx.get_bond_status() == False

    # WHEN\THEN 1 action tool exists
    clean_cookery_text = "clean cookery"
    cx.add_tool(
        tool_kid=ToolKid(_desc=clean_cookery_text, promise=True), walk=casa_road
    )
    assert cx.get_bond_status()

    # WHEN\THEN 2 action tool exists
    clean_hallway_text = "clean hallway"
    cx.add_tool(
        tool_kid=ToolKid(_desc=clean_hallway_text, promise=True), walk=casa_road
    )
    assert cx.get_bond_status() == False

    # WHEN\THEN 1 action tool deleted (1 total)
    clean_hallway_road = Road(f"{jessi_text},{casa_text},{clean_hallway_text}")
    cx.del_tool_kid(road=clean_hallway_road)
    assert cx.get_bond_status()

    # WHEN\THEN 1 action tool deleted (0 total)
    clean_cookery_road = Road(f"{jessi_text},{casa_text},{clean_cookery_text}")
    cx.del_tool_kid(road=clean_cookery_road)
    assert cx.get_bond_status() == False

    # for tool_kid in cx._toolroot._kids.values():
    #     print(f"after {tool_kid._desc=} {tool_kid.promise=}")


def test_agentunit_get_bond_status_ReturnsCorrectBoolWhenOnlyActionToolGroupheirsMatchAgentGroups():
    # GIVEN
    jessi_text = "jessi"
    cx = AgentUnit(_desc=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{jessi_text},{casa_text}")
    cx.add_tool(tool_kid=ToolKid(_desc=casa_text), walk=jessi_text)
    clean_cookery_text = "clean cookery"
    clean_cookery_road = Road(f"{jessi_text},{casa_text},{clean_cookery_text}")
    cx.add_tool(
        tool_kid=ToolKid(_desc=clean_cookery_text, promise=True), walk=casa_road
    )
    tom_text = "tom"
    cx.add_memberunit(name=tom_text)
    assert cx.get_bond_status() == False

    # WHEN
    cx.edit_tool_attr(road=clean_cookery_road, grouplink=grouplink_shop(name=tom_text))
    # THEN
    assert cx.get_bond_status()

    # WHEN
    bob_text = "bob"
    cx.add_memberunit(name=bob_text)
    # THEN
    assert cx.get_bond_status() == False


def test_agentunit_get_bond_status_ChecksActionToolGroupsheirsEqualAgentGroupunits():
    # GIVEN
    jessi_text = "jessi"
    cx = AgentUnit(_desc=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{jessi_text},{casa_text}")
    cx.add_tool(tool_kid=ToolKid(_desc=casa_text), walk=jessi_text)
    clean_cookery_text = "clean cookery"
    clean_cookery_road = Road(f"{jessi_text},{casa_text},{clean_cookery_text}")
    cx.add_tool(
        tool_kid=ToolKid(_desc=clean_cookery_text, promise=True), walk=casa_road
    )
    tom_text = "tom"
    cx.add_memberunit(name=tom_text)
    assert cx.get_bond_status() == False

    # WHEN
    cx.edit_tool_attr(road=clean_cookery_road, grouplink=grouplink_shop(name=tom_text))
    clean_cookery_tool = cx.get_tool_kid(road=clean_cookery_road)
    assert len(clean_cookery_tool._groupheirs) == 1
    # THEN
    assert cx.get_bond_status()

    # WHEN
    bob_text = "bob"
    cx.add_memberunit(name=bob_text)
    # THEN
    assert cx.get_bond_status() == False


def test_agentunit_get_bond_status_ChecksActionToolGroupsheirsEqualAgentGroupunits2():
    # GIVEN
    jessi_text = "jessi"
    cx = AgentUnit(_desc=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{jessi_text},{casa_text}")
    cx.add_tool(tool_kid=ToolKid(_desc=casa_text), walk=jessi_text)
    clean_cookery_text = "clean cookery"
    clean_cookery_road = Road(f"{jessi_text},{casa_text},{clean_cookery_text}")
    cx.add_tool(
        tool_kid=ToolKid(_desc=clean_cookery_text, promise=True), walk=casa_road
    )
    assert cx.get_bond_status()

    tom_text = "tom"
    cx.add_memberunit(name=tom_text)
    bob_text = "bob"
    cx.add_memberunit(name=bob_text)
    home_occupants_text = "home occupants"
    home_occupants_groupunit = groupunit_shop(name=home_occupants_text)
    home_occupants_groupunit.set_memberlink(memberlink=memberlink_shop(name=tom_text))
    home_occupants_groupunit.set_memberlink(memberlink=memberlink_shop(name=bob_text))
    cx.set_groupunit(groupunit=home_occupants_groupunit)
    assert cx.get_bond_status() == False

    # WHEN
    cx.edit_tool_attr(
        road=clean_cookery_road, grouplink=grouplink_shop(name=home_occupants_text)
    )
    # THEN
    assert cx.get_bond_status()

    # WHEN
    yuri_text = "yuri"
    cx.add_memberunit(name=yuri_text)

    # THEN
    assert cx.get_bond_status() == False


def test_agentunit_get_bond_status_ChecksOnlyNecessaryToolsExist_MultipleScenario():
    # GIVEN
    jessi_text = "jessi"
    cx = AgentUnit(_desc=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{jessi_text},{casa_text}")
    cx.add_tool(tool_kid=ToolKid(_desc=casa_text), walk=jessi_text)
    clean_cookery_text = "clean cookery"
    clean_cookery_road = Road(f"{jessi_text},{casa_text},{clean_cookery_text}")

    # WHEN/THEN
    cx.add_tool(
        tool_kid=ToolKid(_desc=clean_cookery_text, promise=True), walk=casa_road
    )
    assert cx.get_bond_status()

    # WHEN/THEN
    water_text = "water"
    water_road = Road(f"{jessi_text},{water_text}")
    cx.add_tool(tool_kid=ToolKid(_desc=water_text), walk=jessi_text)
    assert cx.get_bond_status() == False

    rain_text = "rain"
    rain_road = Road(f"{jessi_text},{water_text},{rain_text}")
    cx.add_tool(tool_kid=ToolKid(_desc=rain_text), walk=water_road)

    # WHEN/THEN
    cx.edit_tool_attr(
        road=clean_cookery_road, required_base=water_road, required_sufffact=rain_road
    )
    assert cx.get_bond_status()


def test_agentunit_get_agent_sprung_from_single_tool_ReturnsCorrectAgentScenario1():
    # GIVEN
    jessi_text = "jessi"
    cx = AgentUnit(_desc=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{jessi_text},{casa_text}")
    cx.add_tool(
        tool_kid=ToolKid(_desc=casa_text, _begin=-1, _close=19), walk=jessi_text
    )
    clean_cookery_text = "clean cookery"
    clean_cookery_road = Road(f"{jessi_text},{casa_text},{clean_cookery_text}")
    cx.add_tool(
        tool_kid=ToolKid(_desc=clean_cookery_text, promise=True, _begin=2, _close=4),
        walk=casa_road,
    )
    water_text = "water"
    water_road = Road(f"{jessi_text},{water_text}")
    cx.add_tool(tool_kid=ToolKid(_desc=water_text), walk=jessi_text)
    assert cx.get_bond_status() == False

    # WHEN
    bond_agent = cx.get_agent_sprung_from_single_tool(road=clean_cookery_road)

    # THEN
    # assert bond_agent._desc == clean_cookery_text
    print(f"{len(bond_agent._tool_dict)=}")
    assert len(bond_agent._tool_dict) == 3
    b_src_tool = bond_agent.get_tool_kid(road=jessi_text)
    src_src_tool = cx.get_tool_kid(road=jessi_text)
    assert b_src_tool._uid == src_src_tool._uid
    assert b_src_tool._begin == src_src_tool._begin
    assert b_src_tool._close == src_src_tool._close
    assert b_src_tool != src_src_tool

    b_casa_tool = bond_agent.get_tool_kid(road=casa_road)
    src_casa_tool = cx.get_tool_kid(road=casa_road)
    assert b_casa_tool._uid == src_casa_tool._uid
    assert b_casa_tool._begin == src_casa_tool._begin
    assert b_casa_tool._close == src_casa_tool._close
    assert b_casa_tool != src_casa_tool

    b_clean_cookery_tool = bond_agent.get_tool_kid(road=clean_cookery_road)
    src_clean_cookery_tool = cx.get_tool_kid(road=clean_cookery_road)
    assert b_clean_cookery_tool._uid == src_clean_cookery_tool._uid
    assert b_clean_cookery_tool._begin == src_clean_cookery_tool._begin
    assert b_clean_cookery_tool._close == src_clean_cookery_tool._close
    assert b_clean_cookery_tool != src_clean_cookery_tool

    assert bond_agent._toolroot._kids.get(water_text) is None

    # for byx in bond_agent._tool_dict.values():
    #     cyx = cx.get_tool_kid(road=byx.get_road())
    #     assert byx._uid == cyx._uid
    #     print(f"{byx.get_road()=} {byx._begin=} {byx._close=}")
    #     print(f"{cyx.get_road()=} {cyx._begin=} {cyx._close=}")
    #     assert byx._begin == cyx._begin
    #     assert byx._close == cyx._close
    #     for yx4 in byx._kids.values():
    #         assert yx4._desc == cyx._kids.get(yx4._desc)._desc
    #     for cx3 in cyx._kids.values():
    #         if cx3._desc == water_text:
    #             print(f"checking src agent tool kid_desc='{cx3._desc}'")
    #             assert byx._kids.get(cx3._desc) is None
    #         else:
    #             assert cx3._desc == byx._kids.get(cx3._desc)._desc
    #     # assert len(byx._kids) != len(cyx._kids)
    #     # assert byx._kids_total_weight != cyx._kids_total_weight
    #     # assert byx._kids != cyx._kids
    #     assert byx != cyx

    assert len(bond_agent._tool_dict) == 3
    assert bond_agent._toolroot._kids.get(water_text) is None


def test_agentunit_export_all_bonds_ExportsFileOfBonds_2files(env_dir_setup_cleanup):
    # GIVEN
    cx = example_agents_get_agent_with_4_levels_and_2requireds_2acptfacts()
    cx_tool_list = cx.get_tool_list()
    action_count = sum(bool(yx.promise) for yx in cx_tool_list)
    assert action_count == 2
    with pytest_raises(Exception) as excinfo:
        x_func_dir_files(dir_path=get_temp_env_dir())

    sys_word_part1 = "sys"  # the built word might be find and replaced in the future.
    sys_word_part2 = "tem"  # the built word might be find and replaced in the future.
    assert (
        str(excinfo.value)
        == f"[WinError 3] The {sys_word_part1}{sys_word_part2} cannot find the path specified: '{get_temp_env_dir()}'"
    )

    # WHEN
    cx.export_all_bonds(dir=get_temp_env_dir())

    # THEN
    # for bond_file_x in x_func_dir_files(dir_path=get_temp_env_dir()).keys():
    #     print(f"files exported {bond_file_x=}")

    assert len(x_func_dir_files(dir_path=get_temp_env_dir())) == 2


# deactivated since it takes too long
# def test_agentunit_export_all_bonds_ExportsFileOfBonds_69files(env_dir_setup_cleanup):
#     # GIVEN
#     cx = example_agents_agent_v001()
#     cx_tool_list = cx.get_tool_list()
#     action_count = 0
#     for yx in cx_tool_list:
#         if yx.promise:
#             action_count += 1
#     assert action_count == 69
#     # WHEN/THEN
#     with pytest_raises(Exception) as excinfo:
#         assert x_func_dir_files(dir_path=get_temp_env_dir())
#     assert (
#         str(excinfo.value)
#         == f"[WinError 3] Cannot find the path specified: '{get_temp_env_dir()}'"
#     )

#     # WHEN
#     cx.export_all_bonds(dir=get_temp_env_dir())

#     # THEN
#     for bond_file_x in x_func_dir_files(dir_path=get_temp_env_dir()).keys():
#         print(f"files exported {bond_file_x=}")

#     assert len(x_func_dir_files(dir_path=get_temp_env_dir())) == action_count


def test_agentunit_export_all_bonds_ReturnsDictOfBonds(env_dir_setup_cleanup):
    # GIVEN
    cx = example_agents_get_agent_with_4_levels_and_2requireds_2acptfacts()
    cx_tool_list = cx.get_tool_list()
    action_count = sum(bool(yx.promise) for yx in cx_tool_list)
    assert action_count == 2

    # WHEN
    cx.export_all_bonds(dir=get_temp_env_dir())

    # THEN
    dir_files = x_func_dir_files(dir_path=get_temp_env_dir())
    file_17_name = "17.json"
    assert dir_files[file_17_name]
    json_17 = x_func_open_file(dest_dir=get_temp_env_dir(), file_name=file_17_name)
    bond_17 = agent_get_from_json(lw_json=json_17)
    assert bond_17.get_bond_status()

    file_2_name = "2.json"
    assert dir_files[file_2_name]
    json_2 = x_func_open_file(dest_dir=get_temp_env_dir(), file_name=file_2_name)
    bond_2 = agent_get_from_json(lw_json=json_2)
    assert bond_2.get_bond_status()


def test_agentunit_get_meld_of_agent_files_MeldsIntoSourceAgent_Scenario1(
    env_dir_setup_cleanup,
):
    # GIVEN
    src = "src"
    src_cx = AgentUnit(_weight=10, _desc=src)

    work = "work"
    tool_kid_work = ToolKid(_weight=30, _desc=work, promise=True)
    src_cx.add_tool(tool_kid=tool_kid_work, walk=f"{src}")

    cat = "feed cat"
    tool_kid_feedcat = ToolKid(_weight=20, _desc=cat, promise=True)
    src_cx.add_tool(tool_kid=tool_kid_feedcat, walk=f"{src}")

    src_cx.export_all_bonds(dir=get_temp_env_dir())

    # WHEN
    new_cx = get_meld_of_agent_files(
        agentunit=AgentUnit(_desc=src_cx._desc, _weight=10), dir=get_temp_env_dir()
    )

    # THEN
    assert src_cx._weight == new_cx._weight
    assert src_cx._toolroot._weight == new_cx._toolroot._weight
    cat_t = "feed cat"
    assert (
        src_cx._toolroot._kids.get(cat_t)._agent_coin_onset
        == new_cx._toolroot._kids.get(cat_t)._agent_coin_onset
    )
    assert src_cx._toolroot._kids.get(cat_t) == new_cx._toolroot._kids.get(cat_t)
    assert src_cx._toolroot._kids == new_cx._toolroot._kids
    assert src_cx._toolroot == new_cx._toolroot
    assert src_cx == new_cx


# def test_agentunit_get_meld_of_agent_files_MeldsIntoSourceAgent_Scenario2(
#     env_dir_setup_cleanup,
# ):
#     # GIVEN
#     src = "src"
#     src_cx = AgentUnit(_weight=10, _desc=src)

#     work_text = "work"
#     work_road = f"{src},{work_text}"

#     cat_text = "feed cat"
#     cat_tool = ToolKid(_weight=20, _desc=cat_text, promise=True)
#     src_cx.add_tool(tool_kid=cat_tool, walk=work_road)

#     plant_text = "water plant"
#     plant_tool = ToolKid(_weight=30, _desc=plant_text, promise=True)
#     src_cx.add_tool(tool_kid=plant_tool, walk=work_road)
#     src_cx.export_all_bonds(dir=get_temp_env_dir())

#     # WHEN
#     new_cx = get_meld_of_agent_files(
#         agentunit=AgentUnit(_desc=src_cx._desc, _weight=0), dir=get_temp_env_dir()
#     )

#     # THEN
#     assert src_cx._weight == new_cx._weight
#     assert src_cx._toolroot._weight == new_cx._toolroot._weight
#     assert len(src_cx._toolroot._kids) == 1
#     assert len(src_cx._toolroot._kids) == len(new_cx._toolroot._kids)
#     src_work_tool = src_cx._toolroot._kids.get(work_text)
#     new_work_tool = new_cx._toolroot._kids.get(work_text)
#     src_cat_tool = src_work_tool._kids.get(cat_text)
#     new_cat_tool = new_work_tool._kids.get(cat_text)
#     print(f"{src_cat_tool._agent_importance=} {new_cat_tool._agent_importance=}")
#     assert src_cat_tool._weight == new_cat_tool._weight
#     assert src_work_tool._kids.get(cat_text) == new_work_tool._kids.get(cat_text)

#     assert src_cx._toolroot._kids.get(cat_text) == new_cx._toolroot._kids.get(cat_text)
#     assert src_cx._toolroot._kids == new_cx._toolroot._kids
#     assert src_cx._toolroot == new_cx._toolroot
#     assert src_cx == new_cx


# - [ ] create test_agentunit_get_bond_status_ReturnsFalseWhenNotOnlyActionToolAcptFactsExist
