from src._prime.road import create_road, default_road_delimiter_if_none

# from src.market.market import (
#     get_temp_env_problem_id,
#     get_temp_env_market_id,
#     get_temp_env_healer_id,
#     get_temp_env_person_id,
# )
from src.world.person import PersonUnit, personunit_shop
from pytest import raises as pytest_raises
from src.world.examples.world_env_kit import (
    get_temp_world_dir,
    worlds_dir_setup_cleanup,
)
from os.path import exists as os_path_exists, isdir as os_path_isdir
from src.instrument.file import delete_dir, dir_files


def test_PersonUnit_exists():
    # GIVEN / WHEN
    x_person = PersonUnit()

    # THEN
    assert x_person.person_id is None
    assert x_person.world_dir is None
    assert x_person.persons_dir is None
    assert x_person.person_dir is None
    assert x_person._gut_obj is None
    assert x_person._gut_file_name is None
    assert x_person._gut_path is None
    assert x_person._markets is None
    assert x_person._market_metrics is None
    assert x_person._problems is None
    assert x_person._road_delimiter is None


def test_PersonUnit_set_person_id_CorrectlySetsAttr():
    # GIVEN / WHEN
    x_person = PersonUnit()
    assert x_person.person_id is None
    assert x_person.world_dir is None
    assert x_person.persons_dir is None
    assert x_person.person_dir is None
    assert x_person._gut_file_name is None
    assert x_person._gut_path is None

    # GIVEN
    yao_text = "Yao"
    x_person.set_person_id(yao_text)

    # THEN
    assert x_person.person_id == yao_text
    assert x_person.world_dir == get_temp_world_dir()
    assert x_person.persons_dir == f"{x_person.world_dir}/persons"
    assert x_person.person_dir == f"{x_person.persons_dir}/{yao_text}"
    assert x_person._gut_file_name == "gut.json"
    assert x_person._gut_path == f"{x_person.person_dir}/{x_person._gut_file_name}"


def test_PersonUnit_set_person_id_RaisesErrorIf_person_id_Contains_road_delimiter():
    # GIVEN
    slash_text = "/"
    bob_text = f"Bob{slash_text}Sue"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        personunit_shop(person_id=bob_text, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{bob_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_personunit_shop_ReturnsNonePersonUnitWithCorrectAttrs_v1():
    # GIVEN
    sue_text = "Sue"
    x_world_dir = "/worlds1"

    # WHEN
    x_person = personunit_shop(person_id=sue_text, world_dir=x_world_dir)

    # THEN
    assert x_person.person_id == sue_text
    assert x_person.world_dir == x_world_dir
    assert x_person.persons_dir == f"{x_world_dir}/persons"
    assert x_person.person_dir == f"{x_person.persons_dir}/{sue_text}"
    assert x_person._gut_file_name == "gut.json"
    assert x_person._gut_path == f"{x_person.person_dir}/{x_person._gut_file_name}"
    assert x_person._markets == {}
    assert x_person._problems == {}
    assert x_person._road_delimiter == default_road_delimiter_if_none()


# def test_personunit_shop_CreatesPersonAgenda_gut_IfItDoesNotExist(
#     worlds_dir_setup_cleanup,
# ):
#     # GIVEN
#     sue_text = "Sue"
#     x_person_dir = f"/persons/{sue_text}"
#     x_gut_file_name = "gut.json"
#     x_gut_path = f"{x_person_dir}/{x_gut_file_name}"
#     assert os_path_exists(x_gut_path) == False

#     # WHEN
#     x_person = personunit_shop(person_id=sue_text)

#     # THEN
#     assert os_path_exists(x_gut_path)
