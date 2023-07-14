from lib.polity.person import personunit_shop
from lib.agent.agent import AgentUnit, get_from_json as agentunit_get_from_json
from lib.agent.examples.example_agents import (
    get_agent_with_4_levels as example_agents_get_agent_with_4_levels,
)
import lib.polity.examples.example_persons as example_persons
from lib.polity.examples.person_env_tools import (
    person_dir_setup_cleanup,
    get_temp_person_dir,
)
from os import path as os_path, scandir as os_scandir
from lib.agent.x_func import (
    open_file as x_func_open_file,
    count_files as x_func_count_files,
)
from pytest import raises as pytest_raises


def test_person_set_starting_digest_agent_CreateStartingAgentFile(
    person_dir_setup_cleanup,
):
    # GIVEN
    p_name = "Game1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=p_name, env_dir=env_dir)
    file_name = "starting_digest_agent.json"
    with pytest_raises(Exception) as excinfo:
        x_func_open_file(px._person_dir, file_name)
    assert (
        str(excinfo.value)
        == f"Could not load file {px._person_dir}/starting_digest_agent.json (2, 'No such file or directory')"
    )

    # WHEN
    px.set_starting_digest_agent(agentunit=example_agents_get_agent_with_4_levels())

    # THEN
    assert x_func_open_file(px._person_dir, file_name) != None


def test_personget_starting_digest_agent_WhenStartingAgentFileDoesNotExists(
    person_dir_setup_cleanup,
):
    # GIVEN
    p_name = "Game1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=p_name, env_dir=env_dir)

    # WHEN
    assert px.get_starting_digest_agent() != None
    starting_dest_agent = px.get_starting_digest_agent()

    # THEN
    x_agent = AgentUnit(_desc=p_name)
    x_agent.set_agent_metrics()
    # x_idearoot = IdeaRoot(_desc=p_name, _walk="")
    # x_idearoot.set_brandlines_empty_if_null()
    # x_idearoot.set_kids_empty_if_null()
    # x_idearoot.set_brandlink_empty_if_null()
    # x_idearoot.set_brandheir_empty_if_null()
    # x_idearoot.set_requiredunits_empty_if_null()
    # x_idearoot.set_requiredheirs_empty_if_null()
    # x_idearoot._agent_importance = 1
    # x_idearoot._level = 0
    # x_idearoot._ancestor_promise_count = 0
    # x_idearoot._descendant_promise_count = 0
    # x_idearoot._all_ally_credit = True
    # x_idearoot._all_ally_debt = True

    assert starting_dest_agent._idearoot == x_agent._idearoot
    assert starting_dest_agent._idearoot._acptfactunits == {}
    assert starting_dest_agent._allys == {}
    assert starting_dest_agent._brands == {}


def test_person_get_starting_digest_agent_WhenStartingAgentFileExists(
    person_dir_setup_cleanup,
):
    # GIVEN
    p_name = "Game1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=p_name, env_dir=env_dir)
    px.set_starting_digest_agent(agentunit=example_agents_get_agent_with_4_levels())

    # WHEN
    assert px.get_starting_digest_agent() != None
    starting_dest_agent = px.get_starting_digest_agent()

    # THEN
    x_agent = example_agents_get_agent_with_4_levels()
    x_agent.agent_and_idearoot_desc_edit(new_desc=p_name)
    x_agent.set_agent_metrics()

    assert starting_dest_agent._idearoot._kids == x_agent._idearoot._kids
    assert starting_dest_agent._idearoot == x_agent._idearoot
    assert starting_dest_agent._idearoot._acptfactunits == {}
    assert starting_dest_agent._allys == {}
    assert starting_dest_agent._brands == {}
    assert starting_dest_agent._desc == px.name


def test_person_del_starting_digest_agent_file_DeletesFileCorrectly(
    person_dir_setup_cleanup,
):
    # GIVEN
    p_name = "Game1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=p_name, env_dir=env_dir)
    px.set_starting_digest_agent(agentunit=example_agents_get_agent_with_4_levels())
    file_name = "starting_digest_agent.json"
    assert x_func_open_file(px._person_dir, file_name) != None

    # WHEN
    px.del_starting_digest_agent_file()

    # THEN
    with pytest_raises(Exception) as excinfo:
        x_func_open_file(px._person_dir, file_name)
    assert (
        str(excinfo.value)
        == f"Could not load file {px._person_dir}/starting_digest_agent.json (2, 'No such file or directory')"
    )


def test_personunit_save_digest_agent_file_SavesFileCorrectly(
    person_dir_setup_cleanup,
):
    # GIVEN
    person_name = "person1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=person_name, env_dir=env_dir)
    px.create_core_dir_and_files()
    cx = example_persons.get_2node_agent()
    src_agent_desc = cx._desc
    assert x_func_count_files(px._digest_agents_dir) == 0

    # WHEN
    px._save_digest_agent_file(agentunit=cx, src_agent_desc=src_agent_desc)

    # THEN
    cx_file_name = f"{cx._desc}.json"
    digest_file_path = f"{px._digest_agents_dir}/{cx_file_name}"
    print(f"Saving to {digest_file_path=}")
    assert os_path.exists(digest_file_path)
    for path_x in os_scandir(px._digest_agents_dir):
        print(f"{path_x=}")
    assert x_func_count_files(px._digest_agents_dir) == 1
    digest_cx_json = x_func_open_file(
        dest_dir=px._digest_agents_dir, file_name=f"{src_agent_desc}.json"
    )
    assert digest_cx_json == cx.get_json()


def test_presonunit_set_src_agentlinks_CorrectlySets_blind_trust_DigestAgent(
    person_dir_setup_cleanup,
):
    # GIVEN
    person_name = "person1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=person_name, env_dir=env_dir)
    px.create_core_dir_and_files()
    cx = example_persons.get_2node_agent()
    src_agent_desc = cx._desc
    assert x_func_count_files(px._digest_agents_dir) == 0

    # WHEN
    px.receive_src_agentunit_obj(agent_x=cx, link_type="blind_trust")

    # THEN
    cx_file_name = f"{cx._desc}.json"
    digest_file_path = f"{px._digest_agents_dir}/{cx_file_name}"
    print(f"Saving to {digest_file_path=}")
    assert os_path.exists(digest_file_path)
    for path_x in os_scandir(px._digest_agents_dir):
        print(f"{path_x=}")
    assert x_func_count_files(px._digest_agents_dir) == 1
    digest_cx_json = x_func_open_file(
        dest_dir=px._digest_agents_dir, file_name=f"{src_agent_desc}.json"
    )
    assert digest_cx_json == cx.get_json()


def test_person_get_dest_agent_from_digest_agent_files_withEmptyDigestDict(
    person_dir_setup_cleanup,
):
    # GIVEN
    person_name_x = "boots3"
    px = personunit_shop(name=person_name_x, env_dir=get_temp_person_dir())
    px.create_core_dir_and_files()
    sx_output_before = px.get_dest_agent_from_digest_agent_files()
    assert str(type(sx_output_before)).find(".agent.AgentUnit'>")
    assert sx_output_before._desc == person_name_x
    assert sx_output_before._idearoot._desc == person_name_x
    # px.set_digested_agent(agent_x=AgentUnit(_desc="digested1"))

    # WHEN
    sx_output_after = px.get_dest_agent_from_digest_agent_files()

    # THEN
    person_agent_x = AgentUnit(_desc=person_name_x, _weight=0.0)
    person_agent_x._idearoot._walk = ""
    person_agent_x.set_agent_metrics()
    # person_agent_x.set_allys_empty_if_null()
    # person_agent_x.set_brandunits_empty_if_null()
    # person_agent_x._set_acptfacts_empty_if_null()
    # person_agent_x._idearoot.set_brandlink_empty_if_null()
    # person_agent_x._idearoot.set_requiredunits_empty_if_null()
    # person_agent_x._idearoot.set_acptfactunits_empty_if_null()
    # person_agent_x._idearoot.set_kids_empty_if_null()

    assert str(type(sx_output_after)).find(".agent.AgentUnit'>")
    assert sx_output_after._weight == person_agent_x._weight
    assert sx_output_after._idearoot._walk == person_agent_x._idearoot._walk
    assert (
        sx_output_after._idearoot._acptfactunits
        == person_agent_x._idearoot._acptfactunits
    )
    assert sx_output_after._idearoot == person_agent_x._idearoot


def test_person_get_dest_agent_from_digest_agent_files_with1DigestedAgent(
    person_dir_setup_cleanup,
):
    # GIVEN
    person_name_x = "boots3"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=person_name_x, env_dir=env_dir)
    px.create_core_dir_and_files()
    sx_output_old = px.get_dest_agent_from_digest_agent_files()
    assert str(type(sx_output_old)).find(".agent.AgentUnit'>")
    assert sx_output_old._desc == person_name_x
    assert sx_output_old._idearoot._desc == person_name_x
    input_agent = example_persons.get_2node_agent()
    px.receive_src_agentunit_obj(agent_x=input_agent, link_type="blind_trust")

    # WHEN
    sx_output_new = px.get_dest_agent_from_digest_agent_files()

    # THEN
    assert str(type(sx_output_new)).find(".agent.AgentUnit'>")

    input_agent.make_meldable(px.get_starting_digest_agent())
    assert sx_output_new._weight == 0
    assert sx_output_new._weight != input_agent._weight
    assert sx_output_new._idearoot._walk == input_agent._idearoot._walk
    assert (
        sx_output_new._idearoot._acptfactunits == input_agent._idearoot._acptfactunits
    )
    assert sx_output_new._idearoot._kids == input_agent._idearoot._kids
    assert (
        sx_output_new._idearoot._kids_total_weight
        == input_agent._idearoot._kids_total_weight
    )
    assert sx_output_new._idearoot == input_agent._idearoot
    assert sx_output_new._desc != input_agent._desc
    assert sx_output_new != input_agent


# def test_person_set_digested_agent_with2Brands(person_dir_setup_cleanup):
#     # GIVEN
#     env_dir = get_temp_person_dir()
#     px = personunit_shop(name="test8", env_dir=env_dir)
#     sx_output_old = px.get_dest_agent_from_digest_agent_files()
#     assert str(type(sx_output_old)).find(".agent.AgentUnit'>")
#     assert sx_output_old._brands == {}
#     assert sx_output_old._allys == {}
#     assert sx_output_old._acptfacts == {}

#     src1 = "test1"
#     src1_road = Road(f"{src1}")
#     s1 = AgentUnit(_desc=src1)

#     ceci_text = "Ceci"
#     s1.set_allyunit(allyunit=AllyUnit(name=ceci_text))
#     swim_text = "swimmers"
#     swim_brand = BrandUnit(name=swim_text)
#     swim_brand.set_allylink(allylink=allylink_shop(name=ceci_text))
#     s1.set_brandunit(brandunit=swim_brand)

#     yaya_text = "yaya"
#     yaya_road = Road(f"{src1},{yaya_text}")
#     s1.add_idea(idea_kid=IdeaKid(_desc=yaya_text), walk=src1_road)
#     s1.set_acptfact(base=yaya_road, acptfact=yaya_road)

#     assert s1._brands.get(swim_text).name == swim_text
#     assert s1._allys.get(ceci_text).name == ceci_text
#     assert s1._idearoot._desc == src1
#     assert s1._acptfacts.get(yaya_road).base == yaya_road

#     # WHEN
#     px.set_single_digested_agent(_agent_desc="test1", digest_agent_x=s1)
#     sx_output_new = px.get_dest_agent_from_digest_agent_files()

#     # THEN
#     assert str(type(sx_output_new)).find(".agent.AgentUnit'>")
#     assert sx_output_new._acptfacts == s1._acptfacts
#     assert sx_output_new._allys == s1._allys
#     assert sx_output_new._brands == s1._brands
#     assert sx_output_new._weight == s1._weight
#     assert sx_output_new._weight == s1._weight
#     assert sx_output_new._idearoot._walk == s1._idearoot._walk
#     assert sx_output_new._idearoot._acptfactunits == s1._idearoot._acptfactunits
#     assert sx_output_new._idearoot._kids == s1._idearoot._kids
#     assert sx_output_new._idearoot._kids_total_weight == s1._idearoot._kids_total_weight
#     assert sx_output_new._idearoot == s1._idearoot
#     assert sx_output_new._desc != s1._desc
#     assert sx_output_new != s1
