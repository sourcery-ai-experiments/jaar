from src._prime.road import create_road, default_road_delimiter_if_none
from src.market.market import (
    get_temp_env_problem_id,
    get_temp_env_market_id,
    get_temp_env_healer_id,
    get_temp_env_person_id,
)
from src.world.person import PersonUnit, personunit_shop
from pytest import raises as pytest_raises
from src.world.examples.world_env_kit import (
    get_temp_world_dir,
    worlds_dir_setup_cleanup,
)



def test_PersonUnit_exists():
    # GIVEN / WHEN
    x_person = PersonUnit()

    # THEN
    assert x_person.person_id is None
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
    assert x_person.person_dir is None
    assert x_person._gut_file_name is None
    assert x_person._gut_path is None

    # GIVEN
    yao_text = "Yao"
    x_person.set_person_id(yao_text)

    # THEN
    assert x_person.person_id == yao_text
    assert x_person.person_dir == f"/persons/{yao_text}"
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
    sue_personroad = create_road(sue_text, "problem1")
    sue_personroad = create_road(sue_personroad, "healer1")
    sue_personroad = create_road(sue_personroad, "market1")

    # WHEN
    x_person = personunit_shop(person_id=sue_text)

    # THEN
    assert x_person.person_id == sue_text
    assert x_person.person_dir == f"/persons/{sue_text}"
    assert x_person._gut_file_name == "gut.json"
    assert x_person._gut_path == f"{x_person.person_dir}/{x_person._gut_file_name}"
    assert x_person._markets == {}
    assert x_person._problems == {}
    assert x_person._road_delimiter == default_road_delimiter_if_none()
