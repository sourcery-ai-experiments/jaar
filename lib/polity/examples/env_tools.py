# from lw.agent import AgentUnit
from lib.polity.polity import PolityUnit
from os import listdir as os_listdir, rename as os_rename, path as os_path
from pytest import fixture as pytest_fixture
from lib.agent.examples.example_agents import (
    agent_v001 as example_agents_agent_v001,
    agent_v002 as example_agents_agent_v002,
    get_agent_1Task_1CE0MinutesRequired_1AcptFact as example_agents_get_agent_1Task_1CE0MinutesRequired_1AcptFact,
    get_agent_with7amCleanTableRequired as example_agents_get_agent_with7amCleanTableRequired,
    get_agent_base_time_example as example_agents_get_agent_base_time_example,
    get_agent_x1_3levels_1required_1acptfacts as example_agents_get_agent_x1_3levels_1required_1acptfacts,
)
from lib.polity.examples.example_persons import (
    get_1node_agent as example_persons_get_1node_agent,
    get_7nodeJRootWithH_agent as example_persons_get_7nodeJRootWithH_agent,
    get_agent_2CleanNodesRandomWeights as example_persons_get_agent_2CleanNodesRandomWeights,
    get_agent_3CleanNodesRandomWeights as example_persons_get_agent_3CleanNodesRandomWeights,
)
from lib.agent.agent import AgentUnit
from lib.polity.person import personunit_shop
from lib.agent.x_func import (
    single_dir_create_if_null,
    delete_dir,
    copy_dir,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
    dir_files as x_func_dir_files,
)


def get_temp_env_name():
    return "ex_env04"


def get_temp_env_dir():
    return f"{get_test_politys_dir()}/{get_temp_env_name()}"


def get_test_politys_dir():
    return "lib/polity/examples/politys"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_temp_env_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)


def create_agent_file_for_politys(polity_dir: str, agent_desc: str):
    agent_x = AgentUnit(_desc=agent_desc)
    agent_dir = f"{polity_dir}/agents"
    # file_path = f"{agent_dir}/{agent_x._desc}.json"
    # if not path.exists(file_path):
    # print(f"{file_path=} {agent_x._desc=}")

    x_func_save_file(
        dest_dir=agent_dir,
        file_name=f"{agent_x._desc}.json",
        file_text=agent_x.get_json(),
    )


def create_person_file_for_politys(polity_dir: str, person_name: str):
    person_x = personunit_shop(name=person_name, env_dir=polity_dir)
    person_dir = f"{polity_dir}/persons/{person_x.name}"
    # file_path = f"{person_dir}/{person_x.name}.json"
    # single_dir_create_if_null(person_dir)
    # with open(f"{file_path}", "w") as f:
    #     f.write(person_x.get_json())

    x_func_save_file(
        dest_dir=person_dir,
        file_name=f"{person_x.name}.json",
        file_text=person_x.get_json(),
    )


def get_test_politys_dir():
    return "lib/polity/examples/politys"


def create_test_politys_list():
    return x_func_dir_files(
        dir_path=get_test_politys_dir(), include_dirs=True, include_files=False
    )


def setup_test_example_environment():
    _delete_and_set_ex3()
    _delete_and_set_ex4()
    _delete_and_set_ex5()
    _delete_and_set_ex6()


def _delete_and_set_ex3():
    polity_name = "ex3"
    ex = PolityUnit(name=polity_name, politys_dir=get_test_politys_dir())
    delete_dir(ex.get_object_root_dir())
    ex.create_dirs_if_null(in_memory_bank=True)

    ex.save_agentunit_obj_to_agents_dir(agent_x=example_persons_get_1node_agent())
    ex.save_agentunit_obj_to_agents_dir(
        agent_x=example_agents_get_agent_1Task_1CE0MinutesRequired_1AcptFact()
    )
    ex.save_agentunit_obj_to_agents_dir(agent_x=example_agents_agent_v001())
    ex.save_agentunit_obj_to_agents_dir(agent_x=example_agents_agent_v002())

    # ex.set_person(person_x=personunit_shop(name="w1", env_dir=ex.get_object_root_dir()))
    # ex.set_person(person_x=personunit_shop(name="w2", env_dir=ex.get_object_root_dir()))
    w1_text = "w1"
    ex.create_new_personunit(person_name=w1_text)
    ex.create_agentlink_to_saved_agent(
        person_name=w1_text, agent_desc="Myagent", weight=3
    )
    # w1_obj = ex.get_person_obj_from_polity(name=w1_text)

    bob_text = "bob wurld"
    create_agent_file_for_politys(
        polity_dir=ex.get_object_root_dir(), agent_desc=bob_text
    )
    # print(f"create agent_list {w1_text=}")
    ex.create_agentlink_to_generated_agent(
        person_name=w1_text, agent_desc=bob_text, link_type="ignore"
    )
    land_text = "tim wurld"
    create_agent_file_for_politys(
        polity_dir=ex.get_object_root_dir(), agent_desc=land_text
    )
    ex.create_agentlink_to_generated_agent(person_name=w1_text, agent_desc=land_text)
    # ex.create_agentlink_to_generated_agent(person_name=w1_text, agent_desc="test9")
    # ex.create_agentlink_to_generated_agent(person_name=w1_text, agent_desc="Bobs agent")
    ex.save_person_file(person_name=w1_text)
    # print(f"WHAT WHAT {ex.get_object_root_dir()}")
    # print(f"WHAT WHAT {ex.get_object_root_dir()}/persons/w1/w1.json")
    # file_text = x_func_open_file(
    #     dest_dir=f"{ex.get_object_root_dir}/persons/w1", file_name="w1.json"
    # )
    # print(f"{file_text=}")
    # print(f"{len(ex._personunits.get(w1_text)._src_agentlinks)=}")
    # print(f"{ex._personunits.get(w1_text)._src_agentlinks.get(bob_text)=}")
    # print(f"{ex._personunits.get(w1_text).get_json=}")

    w2_text = "w2"
    ex.create_new_personunit(person_name=w2_text)  # , env_dir=ex.get_object_root_dir())
    ex.save_person_file(person_name=w2_text)


def _delete_and_set_ex4():
    polity_name = "ex4"
    ex = PolityUnit(name=polity_name, politys_dir=get_test_politys_dir())
    delete_dir(ex.get_object_root_dir())
    ex.create_dirs_if_null(in_memory_bank=True)
    ex.save_agentunit_obj_to_agents_dir(example_persons_get_7nodeJRootWithH_agent())
    ex.save_agentunit_obj_to_agents_dir(
        example_agents_get_agent_with7amCleanTableRequired()
    )
    ex.save_agentunit_obj_to_agents_dir(example_agents_get_agent_base_time_example())
    ex.save_agentunit_obj_to_agents_dir(
        example_agents_get_agent_x1_3levels_1required_1acptfacts()
    )


def _delete_and_set_ex5():
    polity_name = "ex5"
    ex = PolityUnit(name=polity_name, politys_dir=get_test_politys_dir())
    delete_dir(ex.get_object_root_dir())
    ex.create_dirs_if_null(in_memory_bank=True)

    # ethical code ernie
    # ethical code steve
    # ethical code Jessica
    # ethical code Francine
    # ethical code Clay
    agent_1 = example_persons_get_agent_2CleanNodesRandomWeights(_desc="ernie")
    agent_2 = example_persons_get_agent_2CleanNodesRandomWeights(_desc="steve")
    agent_3 = example_persons_get_agent_2CleanNodesRandomWeights(_desc="jessica")
    agent_4 = example_persons_get_agent_2CleanNodesRandomWeights(_desc="francine")
    agent_5 = example_persons_get_agent_2CleanNodesRandomWeights(_desc="clay")

    ex.save_agentunit_obj_to_agents_dir(agent_x=agent_1)
    ex.save_agentunit_obj_to_agents_dir(agent_x=agent_2)
    ex.save_agentunit_obj_to_agents_dir(agent_x=agent_3)
    ex.save_agentunit_obj_to_agents_dir(agent_x=agent_4)
    ex.save_agentunit_obj_to_agents_dir(agent_x=agent_5)

    ex.create_new_personunit(person_name=agent_1._desc)
    ex.create_new_personunit(person_name=agent_2._desc)
    ex.create_new_personunit(person_name=agent_3._desc)
    ex.create_new_personunit(person_name=agent_4._desc)
    ex.create_new_personunit(person_name=agent_5._desc)

    ex.create_agentlink_to_saved_agent(agent_1._desc, agent_2._desc, "blind_trust", 3)
    ex.create_agentlink_to_saved_agent(agent_1._desc, agent_3._desc, "blind_trust", 7)
    ex.create_agentlink_to_saved_agent(agent_1._desc, agent_4._desc, "blind_trust", 4)
    ex.create_agentlink_to_saved_agent(agent_1._desc, agent_5._desc, "blind_trust", 5)

    ex.create_agentlink_to_saved_agent(agent_2._desc, agent_1._desc, "blind_trust", 3)
    ex.create_agentlink_to_saved_agent(agent_2._desc, agent_3._desc, "blind_trust", 7)
    ex.create_agentlink_to_saved_agent(agent_2._desc, agent_4._desc, "blind_trust", 4)
    icx = example_persons_get_agent_3CleanNodesRandomWeights()
    ex.create_agentlink_to_saved_agent(agent_2._desc, agent_5._desc, "ignore", 5, icx)

    ex.create_agentlink_to_saved_agent(agent_3._desc, agent_1._desc, "blind_trust", 3)
    ex.create_agentlink_to_saved_agent(agent_3._desc, agent_2._desc, "blind_trust", 7)
    ex.create_agentlink_to_saved_agent(agent_3._desc, agent_4._desc, "blind_trust", 4)
    ex.create_agentlink_to_saved_agent(agent_3._desc, agent_5._desc, "blind_trust", 5)

    ex.create_agentlink_to_saved_agent(agent_4._desc, agent_1._desc, "blind_trust", 3)
    ex.create_agentlink_to_saved_agent(agent_4._desc, agent_2._desc, "blind_trust", 7)
    ex.create_agentlink_to_saved_agent(agent_4._desc, agent_3._desc, "blind_trust", 4)
    ex.create_agentlink_to_saved_agent(agent_4._desc, agent_5._desc, "blind_trust", 5)

    ex.create_agentlink_to_saved_agent(agent_5._desc, agent_1._desc, "blind_trust", 3)
    ex.create_agentlink_to_saved_agent(agent_5._desc, agent_2._desc, "blind_trust", 7)
    ex.create_agentlink_to_saved_agent(agent_5._desc, agent_3._desc, "blind_trust", 4)
    ex.create_agentlink_to_saved_agent(agent_5._desc, agent_4._desc, "blind_trust", 5)

    ex.save_person_file(person_name=agent_1._desc)
    ex.save_person_file(person_name=agent_2._desc)
    ex.save_person_file(person_name=agent_3._desc)
    ex.save_person_file(person_name=agent_4._desc)
    ex.save_person_file(person_name=agent_5._desc)


def _delete_and_set_ex6():
    polity_name = "ex6"
    ex = PolityUnit(name=polity_name, politys_dir=get_test_politys_dir())
    delete_dir(ex.get_object_root_dir())
    ex.create_dirs_if_null(in_memory_bank=False)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agent = AgentUnit(_desc=sal_text)
    sal_agent.add_allyunit(name=bob_text, creditor_weight=2)
    sal_agent.add_allyunit(name=tom_text, creditor_weight=7)
    sal_agent.add_allyunit(name=ava_text, creditor_weight=1)
    ex.save_agentunit_obj_to_agents_dir(agent_x=sal_agent)

    bob_agent = AgentUnit(_desc=bob_text)
    bob_agent.add_allyunit(name=sal_text, creditor_weight=3)
    bob_agent.add_allyunit(name=ava_text, creditor_weight=1)
    ex.save_agentunit_obj_to_agents_dir(agent_x=bob_agent)

    tom_agent = AgentUnit(_desc=tom_text)
    tom_agent.add_allyunit(name=sal_text, creditor_weight=2)
    ex.save_agentunit_obj_to_agents_dir(agent_x=tom_agent)

    ava_agent = AgentUnit(_desc=ava_text)
    ava_agent.add_allyunit(name=elu_text, creditor_weight=2)
    ex.save_agentunit_obj_to_agents_dir(agent_x=ava_agent)

    elu_agent = AgentUnit(_desc=elu_text)
    elu_agent.add_allyunit(name=ava_text, creditor_weight=19)
    elu_agent.add_allyunit(name=sal_text, creditor_weight=1)
    ex.save_agentunit_obj_to_agents_dir(agent_x=elu_agent)

    ex.refresh_bank_metrics()
    ex.set_river_sphere_for_agent(agent_name=sal_text, max_flows_count=100)


def create_test_polity(polity_name: str):
    ex = PolityUnit(name=polity_name, politys_dir=get_test_politys_dir())
    ex.create_dirs_if_null(in_memory_bank=True)


def delete_dir_test_polity(polity_obj: PolityUnit):
    delete_dir(polity_obj.get_object_root_dir())


def rename_test_polity(polity_obj: PolityUnit, new_name):
    # base_dir = polity_obj.get_object_root_dir()
    base_dir = "lib/polity/examples/politys"
    src_dir = f"{base_dir}/{polity_obj.name}"
    dst_dir = f"{base_dir}/{new_name}"
    os_rename(src=src_dir, dst=dst_dir)
    polity_obj.set_polityunit_name(name=new_name)


class InvalidPolityCopyException(Exception):
    pass


def copy_test_polity(src_name: str, dest_name: str):
    base_dir = "lib/polity/examples/politys"
    new_dir = f"{base_dir}/{dest_name}"
    if os_path.exists(new_dir):
        raise InvalidPolityCopyException(
            f"Cannot copy polity to '{new_dir}' dir already exists."
        )
    # base_dir = polity_obj.get_object_root_dir()
    src_dir = f"{base_dir}/{src_name}"
    dest_dir = f"{base_dir}/{dest_name}"
    copy_dir(src_dir=src_dir, dest_dir=dest_dir)
