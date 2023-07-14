from lib.polity.person import personunit_shop
import lib.polity.examples.example_persons as example_persons
from lib.polity.test_person.env_tools import (
    env_dir_setup_cleanup,
    get_temp_person_dir,
    create_agent_file_for_person,
)
from lib.polity.examples.env_tools import get_temp_env_name
from lib.polity.polity import PolityUnit
from os import path as os_path, scandir as os_scandir
from pytest import raises as pytest_raises
from lib.agent.x_func import (
    count_files as x_func_count_files,
    dir_files as x_func_dir_files,
)


def test_personunit__set_src_agentlinks_RaisesErrorWhenAgentDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    person1_text = "person1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=person1_text, env_dir=env_dir)
    swim_text = "swim"
    assert px._src_agentlinks == {}

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        px._set_src_agentlinks(agent_desc=swim_text)
    assert str(excinfo.value) == f"Person {person1_text} cannot find agent {swim_text}"


def test_personunit__set_src_agentlinks_CorrectlyUsed(env_dir_setup_cleanup):
    # GIVEN
    person1_text = "person1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=person1_text, env_dir=env_dir)
    swim_text = "swim"
    create_agent_file_for_person(
        person_agent_dir=px._person_agents_dir, agent_desc=swim_text
    )
    assert px._src_agentlinks == {}

    # WHEN
    px._set_src_agentlinks(agent_desc=swim_text)

    # THEN
    assert list(px._src_agentlinks.keys()) == [swim_text]


def test_personunit_delete_agentlink_CorrectlyDeletesObj(env_dir_setup_cleanup):
    # GIVEN
    person1_text = "person1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=person1_text, env_dir=env_dir)
    swim_text = "swim"
    create_agent_file_for_person(
        person_agent_dir=px._person_agents_dir, agent_desc=swim_text
    )
    px._set_src_agentlinks(agent_desc=swim_text)
    assert list(px._src_agentlinks.keys()) == [swim_text]

    # WHEN
    px.delete_agentlink(agent_desc=swim_text)

    # THEN
    assert px._src_agentlinks == {}


def test_personunit_delete_agentlink_CorrectlyDeletesBlindTrustFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    person1_text = "person1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=person1_text, env_dir=env_dir)
    swim_text = "swim"
    create_agent_file_for_person(
        person_agent_dir=px._person_agents_dir, agent_desc=swim_text
    )
    px._set_src_agentlinks(agent_desc=swim_text, link_type="blind_trust")
    assert x_func_count_files(dir_path=px._person_agents_dir) == 1
    assert x_func_count_files(dir_path=px._digest_agents_dir) == 1

    # WHEN
    px.delete_agentlink(agent_desc=swim_text)

    # THEN
    assert x_func_count_files(dir_path=px._person_agents_dir) == 0
    assert x_func_count_files(dir_path=px._digest_agents_dir) == 0


def test_personunit_receive_src_agentunit_obj_SavesFileCorrectly(env_dir_setup_cleanup):
    # GIVEN
    person_name = "person1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=person_name, env_dir=env_dir)
    assert x_func_count_files(px._person_agents_dir) is None

    # WHEN
    px.receive_src_agentunit_obj(agent_x=example_persons.get_1node_agent())

    # THEN
    print(f"Saving to {px._person_agents_dir=}")
    for path_x in os_scandir(px._person_agents_dir):
        print(f"{path_x=}")
    assert x_func_count_files(px._person_agents_dir) == 1


def test_personunit_receive_src_agentunit_file_SavesFileCorrectly(
    env_dir_setup_cleanup,
):
    # GIVEN
    person_name = "person1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=person_name, env_dir=env_dir)
    s1 = example_persons.get_2node_agent()
    sx_json = s1.get_json()
    assert x_func_count_files(px._person_agents_dir) is None  # dir does not exist

    # WHEN
    px.receive_src_agentunit_file(agent_json=sx_json)

    # THEN
    print(f"Saving to {px._person_agents_dir=}")
    for path_x in os_scandir(px._person_agents_dir):
        print(f"{path_x=}")
    assert x_func_count_files(px._person_agents_dir) == 1


def test_personunit_delete_ignore_agentlink_CorrectlyDeletesObj(env_dir_setup_cleanup):
    # GIVEN
    person1_text = "person1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=person1_text, env_dir=env_dir)
    swim_text = "swim"
    create_agent_file_for_person(
        person_agent_dir=px._person_agents_dir, agent_desc=swim_text
    )
    px._set_src_agentlinks(agent_desc=swim_text)
    assert list(px._src_agentlinks.keys()) == [swim_text]

    # WHEN
    px.delete_agentlink(agent_desc=swim_text)

    # THEN
    assert px._src_agentlinks == {}


def test_personunit_delete_agentlink_CorrectlyDoesNotDeletesIgnoreFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    person1_text = "person1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=person1_text, env_dir=env_dir)
    swim_text = "swim"
    create_agent_file_for_person(px._person_agents_dir, swim_text)
    px._set_src_agentlinks(agent_desc=swim_text, link_type="ignore")
    assert x_func_count_files(dir_path=px._person_agents_dir) == 1
    assert x_func_count_files(dir_path=px._digest_agents_dir) == 1
    assert x_func_count_files(dir_path=px._ignore_agents_dir) == 1

    # WHEN
    px.delete_agentlink(agent_desc=swim_text)

    # THEN
    assert x_func_count_files(dir_path=px._person_agents_dir) == 0
    assert x_func_count_files(dir_path=px._digest_agents_dir) == 0
    assert x_func_count_files(dir_path=px._ignore_agents_dir) == 1


# def test_personunit_set_ignore_agent_file_CorrectlyUpdatesIgnoreFile(
#     env_dir_setup_cleanup,
# ):
#     # GIVEN
#     person1_text = "person1"
#     env_dir = get_temp_person_dir()
#     px = personunit_shop(name=person1_text, env_dir=env_dir)
#     swim_text = "swim"
#     create_agent_file_for_person(px._person_agents_dir, swim_text)
#     px._set_src_agentlinks(agent_desc=swim_text, link_type="ignore")
#     assert x_func_count_files(dir_path=px._ignore_agents_dir) == 1
#     cx1 = px.get_ignore_agent_from_ignore_agent_files(_desc=swim_text)
#     assert len(cx1._allys) == 0
#     cx1.add_allyunit(name="tim")
#     assert len(cx1._allys) == 1

#     # WHEN
#     px.set_ignore_agent_file()

#     # THEN
#     cx2 = px.get_ignore_agent_from_ignore_agent_files(_desc=swim_text)
#     assert len(cx2._allys) == 0

#     assert x_func_count_files(dir_path=px._ignore_agents_dir) == 1


def test_personunit_refresh_agentlinks_CorrectlyPullsAllPublicAgents(
    env_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_person_dir()
    polity_name = get_temp_env_name()
    e1 = PolityUnit(name=polity_name, politys_dir=env_dir)
    e1.create_dirs_if_null()
    person1_text = "person1"
    # px = personunit_shop(name=person1_text, env_dir=env_dir)
    e1.create_new_personunit(person_name=person1_text)
    px = e1.get_person_obj_from_polity(name=person1_text)

    ernie_agent = example_persons.get_agent_2CleanNodesRandomWeights(_desc="ernie")
    old_steve_agent = example_persons.get_agent_2CleanNodesRandomWeights(_desc="steve")
    e1.save_agentunit_obj_to_agents_dir(agent_x=ernie_agent)
    e1.save_agentunit_obj_to_agents_dir(agent_x=old_steve_agent)
    px.receive_src_agentunit_obj(agent_x=ernie_agent)
    px.receive_src_agentunit_obj(agent_x=old_steve_agent)
    assert len(px.get_dest_agent_from_digest_agent_files().get_idea_list()) == 4
    new_steve_agent = example_persons.get_agent_3CleanNodesRandomWeights(_desc="steve")
    e1.save_agentunit_obj_to_agents_dir(agent_x=new_steve_agent)
    print(f"{env_dir=} {px._public_agents_dir=}")
    for file_name in x_func_dir_files(dir_path=env_dir):
        print(f"{px._public_agents_dir=} {file_name=}")

    for file_name in x_func_dir_files(dir_path=px._public_agents_dir):
        print(f"{px._public_agents_dir=} {file_name=}")

    # WHEN
    px.receive_all_src_agentunit_files()

    # THEN
    assert len(px.get_dest_agent_from_digest_agent_files().get_idea_list()) == 5
