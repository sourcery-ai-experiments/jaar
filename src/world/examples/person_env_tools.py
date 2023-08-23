# from os import listdir as os_listdir
from pytest import fixture as pytest_fixture
from src.agent.agent import AgentUnit
from src.agent.x_func import delete_dir, save_file as x_func_save_file


def get_temp_person_dir():
    return "src/world/examples/ex_env"


@pytest_fixture()
def person_dir_setup_cleanup():
    person_dir = get_temp_person_dir()
    delete_dir(dir=person_dir)
    yield person_dir
    delete_dir(dir=person_dir)


def create_agent_file_for_person(person_agent_dir: str, agent_desc: str):
    agent_x = AgentUnit(_desc=agent_desc)
    # file_path = f"{person_agent_dir}/{agent_x._desc}.json"
    # # if not path.exists(file_path):
    # print(f"{file_path=} {agent_x._desc=}")
    # with open(f"{file_path}", "w") as f:
    #     print(f" saving {agent_x._desc=} to {file_path=}")
    #     f.write(agent_x.get_json())
    x_func_save_file(
        dest_dir=person_agent_dir,
        file_name=f"{agent_x._desc}.json",
        file_text=agent_x.get_json(),
    )
    # print(f"print all {agent_dir=} {os_listdir(path=agent_dir)}")
    # for file_path_y in os_listdir(path=agent_dir):
    #     print(f"{file_path_y}")
