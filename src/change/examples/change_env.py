from src._instrument.file import delete_dir
from src._road.road import create_road_from_nodes, get_default_real_id_roadnode
from src.change.agendanox import AgendaNox, agendanox_shop, pipeline_role_job_text
from pytest import fixture as pytest_fixture


def get_codespace_change_dir() -> str:
    return "src/change"


def get_change_examples_dir():
    return f"{get_codespace_change_dir()}/examples"


def get_change_temp_env_dir():
    return f"{get_change_examples_dir()}/temp"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_change_temp_env_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)


def get_texas_agendanox() -> AgendaNox:
    real_id = get_default_real_id_roadnode()
    nation_text = "nation-state"
    usa_text = "USA"
    texas_text = "Texas"
    texas_road = create_road_from_nodes([real_id, nation_text, usa_text, texas_text])
    return agendanox_shop(
        get_change_temp_env_dir(),
        real_id,
        person_id="Sue",
        econ_road=texas_road,
        nox_type=pipeline_role_job_text(),
    )
