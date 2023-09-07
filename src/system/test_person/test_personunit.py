from src.system.person import personunit_shop
from src.calendar.calendar import CalendarUnit
from src.calendar.idea import IdeaRoot
import src.system.examples.example_persons as example_persons
from src.system.examples.person_env_kit import (
    person_dir_setup_cleanup,
    get_temp_person_dir,
    create_calendar_file_for_person,
)
from os import path as os_path, scandir as os_scandir
from pytest import raises as pytest_raises
from src.calendar.x_func import (
    count_files as x_func_count_files,
    open_file as x_func_open_file,
)


def test_personunit_exists(person_dir_setup_cleanup):
    # GIVEN
    person_text = "test1"
    env_dir = get_temp_person_dir()

    # WHEN
    px = personunit_shop(name=person_text, env_dir=env_dir)

    # GIVEN
    assert px._depotlinks == {}


def test_personunit_auto_output_to_public_SavesCalendarToPublicDirWhenTrue(
    person_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_person_dir()
    tim_text = "Tim"
    public_file_name = f"{tim_text}.json"
    public_file_path = f"{get_temp_person_dir()}/calendars/{public_file_name}"
    print(f"{public_file_path=}")
    # public_file_path = f"src/system/examples/ex_env/calendars/{public_file_name}"
    px = personunit_shop(tim_text, env_dir, _auto_output_to_public=True)
    px.create_core_dir_and_files()
    assert os_path.exists(public_file_path) is False

    # WHEN
    px.set_src_calendar(calendar_x=CalendarUnit(_owner=tim_text))

    # THEN
    assert os_path.exists(public_file_path)


def test_personunit_auto_output_to_public_DoesNotSaveCalendarToPublicDirWhenFalse(
    person_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_person_dir()
    tim_text = "Tim"
    public_file_name = f"{tim_text}.json"
    public_file_path = f"{get_temp_person_dir()}/calendars/{public_file_name}"
    print(f"{public_file_path=}")
    # public_file_path = f"src/system/examples/ex_env/calendars/{public_file_name}"
    px = personunit_shop(tim_text, env_dir, _auto_output_to_public=False)
    px.create_core_dir_and_files()
    assert os_path.exists(public_file_path) is False

    # WHEN
    px.set_src_calendar(calendar_x=CalendarUnit(_owner=tim_text))

    # THEN
    assert os_path.exists(public_file_path) is False
