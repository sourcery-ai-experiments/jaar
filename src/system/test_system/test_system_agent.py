from src.system.system import SystemUnit
from src.agent.agent import AgentUnit
from src.agent.examples.example_agents import (
    get_agent_1Task_1CE0MinutesRequired_1AcptFact as example_agents_get_agent_1Task_1CE0MinutesRequired_1AcptFact,
    agent_v001 as example_agents_agent_v001,
)
import src.system.examples.example_persons as example_persons
from os import path as os_path
from src.system.examples.env_tools import (
    get_temp_env_name,
    get_test_systems_dir,
    create_person_file_for_systems,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_system_set_agent_CreatesAgentFile(env_dir_setup_cleanup):
    # GIVEN
    system_name = get_temp_env_name()
    e1 = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    e1.create_dirs_if_null()
    sx1_obj = example_persons.get_1node_agent()
    sx1_path = f"{e1.get_agents_dir()}/{sx1_obj._desc}.json"
    assert os_path.exists(sx1_path) == False

    # WHEN
    e1.save_agentunit_obj_to_agents_dir(agent_x=sx1_obj)

    # THEN
    print(f"{sx1_path=}")
    assert os_path.exists(sx1_path)


def test_system_get_agents_dir_list_of_obj_CreatesAgentFilesList(
    env_dir_setup_cleanup,
):
    # GIVEN
    system_name = get_temp_env_name()
    ex = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    ex.create_dirs_if_null(in_memory_bank=True)
    assert ex.get_agents_dir_file_names_list() == []
    assert ex.get_agents_dir_list_of_obj() == []

    # WHEN
    sx1_obj = example_persons.get_1node_agent()
    sx2_obj = example_agents_get_agent_1Task_1CE0MinutesRequired_1AcptFact()
    sx3_obj = example_agents_agent_v001()
    print(f"{sx1_obj._desc=}")
    print(f"{sx2_obj._desc=}")
    print(f"{sx3_obj._desc=}")
    ex.save_agentunit_obj_to_agents_dir(agent_x=sx1_obj)
    ex.save_agentunit_obj_to_agents_dir(agent_x=sx2_obj)
    ex.save_agentunit_obj_to_agents_dir(agent_x=sx3_obj)

    sx1_path = f"{ex.get_agents_dir()}/{sx1_obj._desc}.json"
    sx2_path = f"{ex.get_agents_dir()}/{sx2_obj._desc}.json"
    sx3_path = f"{ex.get_agents_dir()}/{sx3_obj._desc}.json"
    assert os_path.exists(sx1_path)
    assert os_path.exists(sx2_path)
    assert os_path.exists(sx3_path)

    # THEN
    assert len(ex.get_agents_dir_file_names_list()) == 3
    assert ex.get_agents_dir_file_names_list()[0] == f"{sx1_obj._desc}.json"
    assert ex.get_agents_dir_list_of_obj()[0]._desc == sx1_obj._desc
    assert ex.get_agents_dir_list_of_obj()[0] == sx1_obj
    assert ex.get_agents_dir_list_of_obj()[1]._idearoot == sx2_obj._idearoot
    assert ex.get_agents_dir_list_of_obj()[1] == sx2_obj
    assert ex.get_agents_dir_list_of_obj()[2] == sx3_obj


def test_system_get_agent_currentlyGetsAgent(env_dir_setup_cleanup):
    # GIVEN
    system_name = get_temp_env_name()
    e5 = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    sx5_obj = example_persons.get_7nodeJRootWithH_agent()
    e5.save_agentunit_obj_to_agents_dir(agent_x=sx5_obj)

    # WHEN / THEN
    assert e5.get_agent_from_agents_dir(_desc=sx5_obj._desc) == sx5_obj


def test_system_rename_agent_in_agents_dir_ChangesAgentName(env_dir_setup_cleanup):
    # GIVEN
    system_name = get_temp_env_name()
    e5 = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    e5.create_dirs_if_null(in_memory_bank=True)
    old_agent_desc = "old1"
    sx5_obj = AgentUnit(_desc=old_agent_desc)
    old_sx5_path = f"{e5.get_agents_dir()}/{old_agent_desc}.json"
    e5.save_agentunit_obj_to_agents_dir(agent_x=sx5_obj)
    print(f"{old_sx5_path=}")

    # WHEN
    new_agent_desc = "new1"
    new_sx5_path = f"{e5.get_agents_dir()}/{new_agent_desc}.json"
    assert os_path.exists(new_sx5_path) == False
    assert os_path.exists(old_sx5_path)
    e5.rename_agent_in_agents_dir(old_desc=old_agent_desc, new_desc=new_agent_desc)

    # THEN
    assert os_path.exists(old_sx5_path) == False
    assert os_path.exists(new_sx5_path)


def test_personunit_refresh_agentlinks_CorrectlyPullsAllPublicAgents(
    env_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_test_systems_dir()
    system_name = get_temp_env_name()
    e1 = SystemUnit(name=system_name, systems_dir=env_dir)
    e1.create_dirs_if_null(in_memory_bank=True)
    # px = personunit_shop(name=person1_text, env_dir=env_dir)

    ernie_text = "ernie"
    jessi_text = "jessi"
    steve_text = "steve"
    ernie_agent = example_persons.get_agent_2CleanNodesRandomWeights(_desc=ernie_text)
    jessi_agent = example_persons.get_agent_2CleanNodesRandomWeights(_desc=jessi_text)
    old_steve_cx = example_persons.get_agent_2CleanNodesRandomWeights(_desc=steve_text)
    e1.save_agentunit_obj_to_agents_dir(agent_x=ernie_agent)
    e1.save_agentunit_obj_to_agents_dir(agent_x=jessi_agent)
    e1.save_agentunit_obj_to_agents_dir(agent_x=old_steve_cx)
    e1.create_new_personunit(person_name=ernie_text)
    e1.create_new_personunit(person_name=jessi_text)
    # e1.create_new_personunit(person_name=steve_text)
    px_ernie = e1.get_person_obj_from_system(name=ernie_text)
    px_jessi = e1.get_person_obj_from_system(name=jessi_text)
    # px_steve = e1.get_person_obj_from_system(name=steve_text)
    px_ernie.receive_src_agentunit_obj(agent_x=jessi_agent)
    px_ernie.receive_src_agentunit_obj(agent_x=old_steve_cx)
    px_jessi.receive_src_agentunit_obj(agent_x=ernie_agent)
    px_jessi.receive_src_agentunit_obj(agent_x=old_steve_cx)
    # px_steve.receive_src_agentunit_obj(agent_x=ernie_agent)
    # px_steve.receive_src_agentunit_obj(agent_x=jessi_agent)
    assert len(px_ernie.get_dest_agent_from_digest_agent_files().get_idea_list()) == 4
    assert len(px_jessi.get_dest_agent_from_digest_agent_files().get_idea_list()) == 4
    # assert len(px_steve.get_dest_agent_from_digest_agent_files().get_idea_list()) == 4
    new_steve_agent = example_persons.get_agent_3CleanNodesRandomWeights(_desc="steve")
    e1.save_agentunit_obj_to_agents_dir(agent_x=new_steve_agent)
    # print(f"{env_dir=} {px._public_agents_dir=}")
    # for file_name in x_func_dir_files(dir_path=env_dir):
    #     print(f"{px._public_agents_dir=} {file_name=}")

    # for file_name in x_func_dir_files(dir_path=px._public_agents_dir):
    #     print(f"{px._public_agents_dir=} {file_name=}")

    # WHEN
    e1.reload_all_persons_src_agentunits()

    # THEN
    assert len(px_ernie.get_dest_agent_from_digest_agent_files().get_idea_list()) == 5
    assert len(px_jessi.get_dest_agent_from_digest_agent_files().get_idea_list()) == 5
