from src.system.person import PersonAdmin
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


def test_admin_exists():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_person_dir()

    # WHEN
    pdx = PersonAdmin(_person_name=bob_text, _env_dir=env_dir)

    # THEN
    assert pdx._person_name != None
    assert pdx._env_dir != None
    assert pdx._person_dir is None
    assert pdx._person_file_name is None
    assert pdx._person_file_path is None
    assert pdx._calendars_public_dir is None
    assert pdx._calendars_depot_dir is None
    assert pdx._calendars_ignore_dir is None
    assert pdx._calendars_bond_dir is None
    assert pdx._calendars_digest_dir is None
    assert pdx._isol_calendar_file_name is None


def test_admin__set_calendars_depot_dir_CorrectSetsPersonAdminAttribute():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_person_dir()
    pdx = PersonAdmin(_person_name=bob_text, _env_dir=env_dir)
    pdx._person_dir = "c:\\cmmm"
    assert pdx._calendars_public_dir is None

    # WHEN
    pdx.set_dirs()

    # THEN
    assert pdx._person_dir != None
    assert pdx._calendars_public_dir != None
    assert pdx._calendars_depot_dir != None
    assert pdx._calendars_ignore_dir != None
    assert pdx._calendars_digest_dir != None
    assert pdx._calendars_bond_dir != None
    assert pdx._person_file_name != None
    assert pdx._person_file_path != None
    assert pdx._isol_calendar_file_name != None

    persons_drectory_name = "persons"
    assert pdx._persons_dir == f"{env_dir}/{persons_drectory_name}"
    assert pdx._person_dir == f"{pdx._persons_dir}/{bob_text}"
    assert pdx._person_file_name == f"{bob_text}.json"
    assert pdx._person_file_path == f"{pdx._person_dir}/{pdx._person_file_name}"
    calendars_str = "calendars"
    assert pdx._calendars_depot_dir == f"{pdx._person_dir}/{calendars_str}"
    assert pdx._calendars_ignore_dir == f"{pdx._person_dir}/ignores"
    assert pdx._calendars_bond_dir == f"{pdx._person_dir}/bonds"
    assert pdx._calendars_digest_dir == f"{pdx._person_dir}/digests"
    assert pdx._calendars_public_dir == f"{env_dir}/{calendars_str}"
    assert pdx._isol_calendar_file_name == "isol_calendar.json"
