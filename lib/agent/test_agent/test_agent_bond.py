from lib.agent.agent import (
    AgentUnit,
    get_from_json as agent_get_from_json,
    get_meld_of_agent_files,
)
from lib.agent.examples.get_agent_examples_dir import get_agent_examples_dir
from lib.agent.idea import IdeaCore, IdeaKid
from lib.agent.road import Road
from lib.agent.required import RequiredUnit
from lib.agent.ally import allylink_shop
from lib.agent.brand import brandunit_shop, brandlink_shop
from lib.agent.examples.example_agents import (
    get_agent_with_4_levels as example_agents_get_agent_with_4_levels,
    get_agent_with_4_levels_and_2requireds as example_agents_get_agent_with_4_levels_and_2requireds,
    get_agent_with7amCleanTableRequired as example_agents_get_agent_with7amCleanTableRequired,
    get_agent_with_4_levels_and_2requireds_2acptfacts as example_agents_get_agent_with_4_levels_and_2requireds_2acptfacts,
    agent_v001 as example_agents_agent_v001,
)
from lib.agent.x_func import (
    dir_files as x_func_dir_files,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
)
from lib.polity.examples.env_tools import (
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

    # WHEN\THEN no action idea exists
    cx.add_idea(idea_kid=IdeaKid(_desc=casa_text), walk=jessi_text)
    assert cx.get_bond_status() == False

    # WHEN\THEN 1 action idea exists
    clean_kitchen_text = "clean kitchen"
    cx.add_idea(
        idea_kid=IdeaKid(_desc=clean_kitchen_text, promise=True), walk=casa_road
    )
    assert cx.get_bond_status()

    # WHEN\THEN 2 action idea exists
    clean_hallway_text = "clean hallway"
    cx.add_idea(
        idea_kid=IdeaKid(_desc=clean_hallway_text, promise=True), walk=casa_road
    )
    assert cx.get_bond_status() == False

    # WHEN\THEN 1 action idea deleted (1 total)
    clean_hallway_road = Road(f"{jessi_text},{casa_text},{clean_hallway_text}")
    cx.del_idea_kid(road=clean_hallway_road)
    assert cx.get_bond_status()

    # WHEN\THEN 1 action idea deleted (0 total)
    clean_kitchen_road = Road(f"{jessi_text},{casa_text},{clean_kitchen_text}")
    cx.del_idea_kid(road=clean_kitchen_road)
    assert cx.get_bond_status() == False

    # for idea_kid in cx._idearoot._kids.values():
    #     print(f"after {idea_kid._desc=} {idea_kid.promise=}")


def test_agentunit_get_bond_status_ReturnsCorrectBoolWhenOnlyActionIdeaBrandheirsMatchAgentBrands():
    # GIVEN
    jessi_text = "jessi"
    cx = AgentUnit(_desc=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{jessi_text},{casa_text}")
    cx.add_idea(idea_kid=IdeaKid(_desc=casa_text), walk=jessi_text)
    clean_kitchen_text = "clean kitchen"
    clean_kitchen_road = Road(f"{jessi_text},{casa_text},{clean_kitchen_text}")
    cx.add_idea(
        idea_kid=IdeaKid(_desc=clean_kitchen_text, promise=True), walk=casa_road
    )
    tom_text = "tom"
    cx.add_allyunit(name=tom_text)
    assert cx.get_bond_status() == False

    # WHEN
    cx.edit_idea_attr(road=clean_kitchen_road, brandlink=brandlink_shop(name=tom_text))
    # THEN
    assert cx.get_bond_status()

    # WHEN
    bob_text = "bob"
    cx.add_allyunit(name=bob_text)
    # THEN
    assert cx.get_bond_status() == False


def test_agentunit_get_bond_status_ChecksActionIdeaBrandsheirsEqualAgentBrandunits():
    # GIVEN
    jessi_text = "jessi"
    cx = AgentUnit(_desc=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{jessi_text},{casa_text}")
    cx.add_idea(idea_kid=IdeaKid(_desc=casa_text), walk=jessi_text)
    clean_kitchen_text = "clean kitchen"
    clean_kitchen_road = Road(f"{jessi_text},{casa_text},{clean_kitchen_text}")
    cx.add_idea(
        idea_kid=IdeaKid(_desc=clean_kitchen_text, promise=True), walk=casa_road
    )
    tom_text = "tom"
    cx.add_allyunit(name=tom_text)
    assert cx.get_bond_status() == False

    # WHEN
    cx.edit_idea_attr(road=clean_kitchen_road, brandlink=brandlink_shop(name=tom_text))
    clean_kitchen_idea = cx.get_idea_kid(road=clean_kitchen_road)
    assert len(clean_kitchen_idea._brandheirs) == 1
    # THEN
    assert cx.get_bond_status()

    # WHEN
    bob_text = "bob"
    cx.add_allyunit(name=bob_text)
    # THEN
    assert cx.get_bond_status() == False


def test_agentunit_get_bond_status_ChecksActionIdeaBrandsheirsEqualAgentBrandunits2():
    # GIVEN
    jessi_text = "jessi"
    cx = AgentUnit(_desc=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{jessi_text},{casa_text}")
    cx.add_idea(idea_kid=IdeaKid(_desc=casa_text), walk=jessi_text)
    clean_kitchen_text = "clean kitchen"
    clean_kitchen_road = Road(f"{jessi_text},{casa_text},{clean_kitchen_text}")
    cx.add_idea(
        idea_kid=IdeaKid(_desc=clean_kitchen_text, promise=True), walk=casa_road
    )
    assert cx.get_bond_status()

    tom_text = "tom"
    cx.add_allyunit(name=tom_text)
    bob_text = "bob"
    cx.add_allyunit(name=bob_text)
    home_occupants_text = "home occupants"
    home_occupants_brandunit = brandunit_shop(name=home_occupants_text)
    home_occupants_brandunit.set_allylink(allylink=allylink_shop(name=tom_text))
    home_occupants_brandunit.set_allylink(allylink=allylink_shop(name=bob_text))
    cx.set_brandunit(brandunit=home_occupants_brandunit)
    assert cx.get_bond_status() == False

    # WHEN
    cx.edit_idea_attr(
        road=clean_kitchen_road, brandlink=brandlink_shop(name=home_occupants_text)
    )
    # THEN
    assert cx.get_bond_status()

    # WHEN
    yuri_text = "yuri"
    cx.add_allyunit(name=yuri_text)

    # THEN
    assert cx.get_bond_status() == False


def test_agentunit_get_bond_status_ChecksOnlyNecessaryIdeasExist_MultipleScenario():
    # GIVEN
    jessi_text = "jessi"
    cx = AgentUnit(_desc=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{jessi_text},{casa_text}")
    cx.add_idea(idea_kid=IdeaKid(_desc=casa_text), walk=jessi_text)
    clean_kitchen_text = "clean kitchen"
    clean_kitchen_road = Road(f"{jessi_text},{casa_text},{clean_kitchen_text}")

    # WHEN/THEN
    cx.add_idea(
        idea_kid=IdeaKid(_desc=clean_kitchen_text, promise=True), walk=casa_road
    )
    assert cx.get_bond_status()

    # WHEN/THEN
    water_text = "water"
    water_road = Road(f"{jessi_text},{water_text}")
    cx.add_idea(idea_kid=IdeaKid(_desc=water_text), walk=jessi_text)
    assert cx.get_bond_status() == False

    rain_text = "rain"
    rain_road = Road(f"{jessi_text},{water_text},{rain_text}")
    cx.add_idea(idea_kid=IdeaKid(_desc=rain_text), walk=water_road)

    # WHEN/THEN
    cx.edit_idea_attr(
        road=clean_kitchen_road, required_base=water_road, required_sufffact=rain_road
    )
    assert cx.get_bond_status()


def test_agentunit_get_agent_sprung_from_single_idea_ReturnsCorrectAgentScenario1():
    # GIVEN
    jessi_text = "jessi"
    cx = AgentUnit(_desc=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{jessi_text},{casa_text}")
    cx.add_idea(
        idea_kid=IdeaKid(_desc=casa_text, _begin=-1, _close=19), walk=jessi_text
    )
    clean_kitchen_text = "clean kitchen"
    clean_kitchen_road = Road(f"{jessi_text},{casa_text},{clean_kitchen_text}")
    cx.add_idea(
        idea_kid=IdeaKid(_desc=clean_kitchen_text, promise=True, _begin=2, _close=4),
        walk=casa_road,
    )
    water_text = "water"
    water_road = Road(f"{jessi_text},{water_text}")
    cx.add_idea(idea_kid=IdeaKid(_desc=water_text), walk=jessi_text)
    assert cx.get_bond_status() == False

    # WHEN
    bond_agent = cx.get_agent_sprung_from_single_idea(road=clean_kitchen_road)

    # THEN
    # assert bond_agent._desc == clean_kitchen_text
    print(f"{len(bond_agent._idea_dict)=}")
    assert len(bond_agent._idea_dict) == 3
    b_src_idea = bond_agent.get_idea_kid(road=jessi_text)
    src_src_idea = cx.get_idea_kid(road=jessi_text)
    assert b_src_idea._uid == src_src_idea._uid
    assert b_src_idea._begin == src_src_idea._begin
    assert b_src_idea._close == src_src_idea._close
    assert b_src_idea != src_src_idea

    b_casa_idea = bond_agent.get_idea_kid(road=casa_road)
    src_casa_idea = cx.get_idea_kid(road=casa_road)
    assert b_casa_idea._uid == src_casa_idea._uid
    assert b_casa_idea._begin == src_casa_idea._begin
    assert b_casa_idea._close == src_casa_idea._close
    assert b_casa_idea != src_casa_idea

    b_clean_kitchen_idea = bond_agent.get_idea_kid(road=clean_kitchen_road)
    src_clean_kitchen_idea = cx.get_idea_kid(road=clean_kitchen_road)
    assert b_clean_kitchen_idea._uid == src_clean_kitchen_idea._uid
    assert b_clean_kitchen_idea._begin == src_clean_kitchen_idea._begin
    assert b_clean_kitchen_idea._close == src_clean_kitchen_idea._close
    assert b_clean_kitchen_idea != src_clean_kitchen_idea

    assert bond_agent._idearoot._kids.get(water_text) is None

    # for byx in bond_agent._idea_dict.values():
    #     cyx = cx.get_idea_kid(road=byx.get_road())
    #     assert byx._uid == cyx._uid
    #     print(f"{byx.get_road()=} {byx._begin=} {byx._close=}")
    #     print(f"{cyx.get_road()=} {cyx._begin=} {cyx._close=}")
    #     assert byx._begin == cyx._begin
    #     assert byx._close == cyx._close
    #     for yx4 in byx._kids.values():
    #         assert yx4._desc == cyx._kids.get(yx4._desc)._desc
    #     for cx3 in cyx._kids.values():
    #         if cx3._desc == water_text:
    #             print(f"checking src agent idea kid_desc='{cx3._desc}'")
    #             assert byx._kids.get(cx3._desc) is None
    #         else:
    #             assert cx3._desc == byx._kids.get(cx3._desc)._desc
    #     # assert len(byx._kids) != len(cyx._kids)
    #     # assert byx._kids_total_weight != cyx._kids_total_weight
    #     # assert byx._kids != cyx._kids
    #     assert byx != cyx

    assert len(bond_agent._idea_dict) == 3
    assert bond_agent._idearoot._kids.get(water_text) is None


def test_agentunit_export_all_bonds_ExportsFileOfBonds_2files(env_dir_setup_cleanup):
    # GIVEN
    cx = example_agents_get_agent_with_4_levels_and_2requireds_2acptfacts()
    cx_idea_list = cx.get_idea_list()
    action_count = sum(bool(yx.promise) for yx in cx_idea_list)
    assert action_count == 2
    with pytest_raises(Exception) as excinfo:
        x_func_dir_files(dir_path=get_temp_env_dir())
    assert (
        str(excinfo.value)
        == f"[WinError 3] The system cannot find the path specified: '{get_temp_env_dir()}'"
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
#     cx_idea_list = cx.get_idea_list()
#     action_count = 0
#     for yx in cx_idea_list:
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
    cx_idea_list = cx.get_idea_list()
    action_count = sum(bool(yx.promise) for yx in cx_idea_list)
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
    idea_kid_work = IdeaKid(_weight=30, _desc=work, promise=True)
    src_cx.add_idea(idea_kid=idea_kid_work, walk=f"{src}")

    cat = "feed cat"
    idea_kid_feedcat = IdeaKid(_weight=20, _desc=cat, promise=True)
    src_cx.add_idea(idea_kid=idea_kid_feedcat, walk=f"{src}")

    src_cx.export_all_bonds(dir=get_temp_env_dir())

    # WHEN
    new_cx = get_meld_of_agent_files(
        agentunit=AgentUnit(_desc=src_cx._desc, _weight=10), dir=get_temp_env_dir()
    )

    # THEN
    assert src_cx._weight == new_cx._weight
    assert src_cx._idearoot._weight == new_cx._idearoot._weight
    cat_t = "feed cat"
    assert (
        src_cx._idearoot._kids.get(cat_t)._agent_coin_onset
        == new_cx._idearoot._kids.get(cat_t)._agent_coin_onset
    )
    assert src_cx._idearoot._kids.get(cat_t) == new_cx._idearoot._kids.get(cat_t)
    assert src_cx._idearoot._kids == new_cx._idearoot._kids
    assert src_cx._idearoot == new_cx._idearoot
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
#     cat_idea = IdeaKid(_weight=20, _desc=cat_text, promise=True)
#     src_cx.add_idea(idea_kid=cat_idea, walk=work_road)

#     plant_text = "water plant"
#     plant_idea = IdeaKid(_weight=30, _desc=plant_text, promise=True)
#     src_cx.add_idea(idea_kid=plant_idea, walk=work_road)
#     src_cx.export_all_bonds(dir=get_temp_env_dir())

#     # WHEN
#     new_cx = get_meld_of_agent_files(
#         agentunit=AgentUnit(_desc=src_cx._desc, _weight=0), dir=get_temp_env_dir()
#     )

#     # THEN
#     assert src_cx._weight == new_cx._weight
#     assert src_cx._idearoot._weight == new_cx._idearoot._weight
#     assert len(src_cx._idearoot._kids) == 1
#     assert len(src_cx._idearoot._kids) == len(new_cx._idearoot._kids)
#     src_work_idea = src_cx._idearoot._kids.get(work_text)
#     new_work_idea = new_cx._idearoot._kids.get(work_text)
#     src_cat_idea = src_work_idea._kids.get(cat_text)
#     new_cat_idea = new_work_idea._kids.get(cat_text)
#     print(f"{src_cat_idea._agent_importance=} {new_cat_idea._agent_importance=}")
#     assert src_cat_idea._weight == new_cat_idea._weight
#     assert src_work_idea._kids.get(cat_text) == new_work_idea._kids.get(cat_text)

#     assert src_cx._idearoot._kids.get(cat_text) == new_cx._idearoot._kids.get(cat_text)
#     assert src_cx._idearoot._kids == new_cx._idearoot._kids
#     assert src_cx._idearoot == new_cx._idearoot
#     assert src_cx == new_cx


# - [ ] create test_agentunit_get_bond_status_ReturnsFalseWhenNotOnlyActionIdeaAcptFactsExist
