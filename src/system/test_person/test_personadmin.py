from src.system.person import PersonAdmin, personadmin_shop
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
    assert pdx._calendar_output_file_name is None
    assert pdx._calendar_output_file_path is None
    assert pdx._calendars_public_dir is None
    assert pdx._calendars_depot_dir is None
    assert pdx._calendars_ignore_dir is None
    assert pdx._calendars_bond_dir is None
    assert pdx._calendars_digest_dir is None
    assert pdx._isol_calendar_file_name is None


def test_PersonAdmin_set_dir_CorrectSetsPersonAdminAttribute():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_person_dir()
    pdx = PersonAdmin(_person_name=bob_text, _env_dir=env_dir)
    assert pdx._person_dir is None
    assert pdx._calendar_output_file_name is None
    assert pdx._calendar_output_file_path is None
    assert pdx._calendars_public_dir is None
    assert pdx._calendars_depot_dir is None
    assert pdx._calendars_ignore_dir is None
    assert pdx._calendars_digest_dir is None
    assert pdx._calendars_bond_dir is None
    assert pdx._person_file_name is None
    assert pdx._person_file_path is None
    assert pdx._isol_calendar_file_name is None
    # WHEN
    pdx.set_dirs()

    # THEN
    assert pdx._person_dir != None
    assert pdx._calendar_output_file_name != None
    assert pdx._calendar_output_file_path != None
    assert pdx._calendars_public_dir != None
    assert pdx._calendars_depot_dir != None
    assert pdx._calendars_ignore_dir != None
    assert pdx._calendars_digest_dir != None
    assert pdx._calendars_bond_dir != None
    assert pdx._person_file_name != None
    assert pdx._person_file_path != None
    assert pdx._isol_calendar_file_name != None

    persons_drectory_name = "persons"
    x_persons_dir = f"{env_dir}/{persons_drectory_name}"
    x_person_dir = f"{x_persons_dir}/{bob_text}"
    x_person_file_name = f"{bob_text}.json"
    x_person_file_path = f"{x_person_dir}/{x_person_file_name}"
    x_calendar_output_file_name = "output.json"
    x_calendar_output_file_path = f"{x_person_dir}/{x_calendar_output_file_name}"
    calendars_str = "calendars"
    x_calendars_depot_dir = f"{x_person_dir}/{calendars_str}"
    x_calendars_ignore_dir = f"{x_person_dir}/ignores"
    x_calendars_bond_dir = f"{x_person_dir}/bonds"
    x_calendars_digest_dir = f"{x_person_dir}/digests"
    x_calendars_public_dir = f"{env_dir}/{calendars_str}"
    x_isol_calendar_file_name = "isol_calendar.json"
    assert pdx._persons_dir == x_persons_dir
    assert pdx._person_dir == x_person_dir
    assert pdx._person_file_name == x_person_file_name
    assert pdx._person_file_path == x_person_file_path
    assert pdx._calendar_output_file_name == x_calendar_output_file_name
    assert pdx._calendar_output_file_path == x_calendar_output_file_path
    assert pdx._calendars_depot_dir == x_calendars_depot_dir
    assert pdx._calendars_ignore_dir == x_calendars_ignore_dir
    assert pdx._calendars_bond_dir == x_calendars_bond_dir
    assert pdx._calendars_digest_dir == x_calendars_digest_dir
    assert pdx._calendars_public_dir == x_calendars_public_dir
    assert pdx._isol_calendar_file_name == x_isol_calendar_file_name


def test_PersonAdmin_create_core_dir_and_files_CreatesDirsAndFiles(
    person_dir_setup_cleanup,
):
    # GIVEN create person
    jul_text = "julian"
    env_dir = get_temp_person_dir()
    pdx = PersonAdmin(_person_name=jul_text, _env_dir=env_dir)
    pdx.set_dirs()
    assert os_path.exists(pdx._persons_dir) is False
    assert os_path.exists(pdx._person_dir) is False
    assert os_path.exists(pdx._person_file_path) is False
    assert os_path.isdir(pdx._person_dir) is False
    assert os_path.exists(pdx._calendars_depot_dir) is False
    assert os_path.exists(pdx._calendars_digest_dir) is False
    assert os_path.exists(pdx._calendars_ignore_dir) is False
    assert os_path.exists(pdx._calendars_bond_dir) is False

    # WHEN
    calendar_x = example_persons.get_7nodeJRootWithH_calendar()
    pdx.create_core_dir_and_files(calendar_x.get_json())

    # THEN confirm calendars src directory created
    print(f"Checking {pdx._persons_dir=}")
    print(f"Checking {pdx._person_dir=}")
    assert os_path.exists(pdx._persons_dir)
    assert os_path.exists(pdx._person_dir)
    assert os_path.exists(pdx._person_file_path)
    assert os_path.isdir(pdx._person_dir)
    assert os_path.exists(pdx._calendars_depot_dir)
    assert os_path.exists(pdx._calendars_digest_dir)
    assert os_path.exists(pdx._calendars_ignore_dir)
    assert os_path.exists(pdx._calendars_bond_dir)


def test_PersonAdmin_set_person_name_WorksCorrectly(person_dir_setup_cleanup):
    # GIVEN create person
    env_dir = get_temp_person_dir()

    old_person_text = "bob"
    pdx = PersonAdmin(_person_name=old_person_text, _env_dir=env_dir)
    calendar_x = example_persons.get_7nodeJRootWithH_calendar()
    pdx.set_dirs()
    pdx.create_core_dir_and_files(calendar_x.get_json())
    old_person_dir = pdx._person_dir
    # old_person_dir = f"{env_dir}/persons/{old_person_text}"
    print(f"{pdx._person_dir}")
    print(f"{env_dir}/persons/{old_person_text}")
    old_person_file_name = f"{old_person_text}.json"
    old_person_file_path = f"{old_person_dir}/{old_person_file_name}"

    assert os_path.exists(old_person_dir)
    assert os_path.isdir(old_person_dir)
    assert os_path.exists(old_person_file_path)

    new_person_text = "tim"
    new_person_dir = f"{env_dir}/persons/{new_person_text}"
    new_person_file_name = f"{new_person_text}.json"
    new_person_file_path = f"{new_person_dir}/{new_person_file_name}"
    assert os_path.exists(new_person_dir) == False
    assert os_path.isdir(new_person_dir) == False
    assert os_path.exists(new_person_file_path) == False

    # WHEN
    pdx.set_person_name(new_name=new_person_text)

    # THEN
    assert os_path.exists(old_person_dir) == False
    assert os_path.isdir(old_person_dir) == False
    assert os_path.exists(old_person_file_path) == False
    assert os_path.exists(new_person_dir)
    assert os_path.isdir(new_person_dir)
    assert os_path.exists(new_person_file_path)


def test_personunit_auto_output_to_public_SavesCalendarToPublicDir(
    person_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "bob"
    pdx = personadmin_shop(bob_text, get_temp_person_dir())
    calendar_x = example_persons.get_6node_calendar()
    calendar_x.set_owner(new_owner=bob_text)
    pdx.create_core_dir_and_files(calendar_x.get_json())

    public_file_path = f"{pdx._calendars_public_dir}/{pdx._person_file_name}"
    print(f"{public_file_path=}")
    assert os_path.exists(public_file_path) is False

    # WHEN
    pdx.save_calendar_to_public(calendar_x=calendar_x)

    # THEN
    assert os_path.exists(public_file_path)
