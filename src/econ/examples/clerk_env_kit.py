# from os import listdir as os_listdir
from src._road.road import AgentID
from src.agenda.agenda import agendaunit_shop
from src.instrument.file import delete_dir, save_file
from pytest import fixture as pytest_fixture


def get_temp_clerkunit_dir() -> str:
    return f"src/econ/examples/{get_temp_econ_id()}"


def get_temp_econ_id() -> str:
    return "ex_env"


@pytest_fixture()
def clerk_dir_setup_cleanup():
    agent_id_dir = get_temp_clerkunit_dir()
    delete_dir(dir=agent_id_dir)
    yield agent_id_dir
    delete_dir(dir=agent_id_dir)


def create_agenda_file(agenda_clerkunit_dir: str, agent_id: AgentID):
    x_agenda = agendaunit_shop(_agent_id=agent_id)
    # file_path = f"{agenda_clerkunit_dir}/{x_agenda._agent_id}.json"
    # # if not path.exists(file_path):
    # print(f"{file_path=} {x_agenda._agent_id=}")
    # with open(f"{file_path}", "w") as f:
    #     print(f" saving {x_agenda._agent_id=} to {file_path=}")
    #     f.write(x_agenda.get_json())
    save_file(
        dest_dir=agenda_clerkunit_dir,
        file_name=f"{x_agenda._agent_id}.json",
        file_text=x_agenda.get_json(),
    )
    # print(f"print all {agenda_dir=} {os_listdir(path=agenda_dir)}")
    # for file_path_y in os_listdir(path=agenda_dir):
    #     print(f"{file_path_y}")
