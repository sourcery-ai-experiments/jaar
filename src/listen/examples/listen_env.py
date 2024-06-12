from src._instrument.file import delete_dir
from src._road.road import (
    create_road_from_nodes,
    get_default_real_id_roadnode,
    RoadUnit,
)
from src.listen.userhub import UserHub, userhub_shop, pipeline_role_job_text
from pytest import fixture as pytest_fixture


def get_codespace_listen_dir() -> str:
    return "src/listen"


def get_listen_examples_dir():
    return f"{get_codespace_listen_dir()}/examples"


def get_listen_temp_env_dir():
    return f"{get_listen_examples_dir()}/temp"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_listen_temp_env_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)


def get_texas_road() -> RoadUnit:
    real_id = get_default_real_id_roadnode()
    nation_text = "nation-state"
    usa_text = "USA"
    texas_text = "Texas"
    return create_road_from_nodes([real_id, nation_text, usa_text, texas_text])


def get_texas_userhub() -> UserHub:
    real_id = get_default_real_id_roadnode()
    return userhub_shop(
        get_listen_temp_env_dir(),
        real_id,
        person_id="Sue",
        econ_road=get_texas_road(),
        nox_type=pipeline_role_job_text(),
    )


def get_dakota_road() -> RoadUnit:
    real_id = get_default_real_id_roadnode()
    nation_text = "nation-state"
    usa_text = "USA"
    dakota_text = "Dakota"
    return create_road_from_nodes([real_id, nation_text, usa_text, dakota_text])


def get_dakota_userhub() -> UserHub:
    real_id = get_default_real_id_roadnode()
    return userhub_shop(
        get_listen_temp_env_dir(),
        real_id,
        person_id="Sue",
        econ_road=get_dakota_road(),
        nox_type=pipeline_role_job_text(),
    )
