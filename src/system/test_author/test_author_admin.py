from src.system.author import AuthorAdmin, authoradmin_shop
import src.system.examples.example_authors as example_authors
from src.system.examples.author_env_kit import (
    get_temp_author_dir,
    author_dir_setup_cleanup,
)
from os import path as os_path
from src.calendar.x_func import (
    open_file as x_func_open_file,
    save_file as x_func_save_file,
)


def test_admin_exists():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_author_dir()

    # WHEN
    pdx = AuthorAdmin(_author_name=bob_text, _env_dir=env_dir)

    # THEN
    assert pdx._author_name != None
    assert pdx._env_dir != None
    assert pdx._author_dir is None
    assert pdx._isol_file_name is None
    assert pdx._isol_file_path is None
    assert pdx._calendar_output_file_name is None
    assert pdx._calendar_output_file_path is None
    assert pdx._public_file_name is None
    assert pdx._calendars_public_dir is None
    assert pdx._calendars_depot_dir is None
    assert pdx._calendars_ignore_dir is None
    assert pdx._calendars_bond_dir is None
    assert pdx._calendars_digest_dir is None


def test_AuthorAdmin_set_dir_CorrectSetsAuthorAdminAttribute():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_author_dir()
    pdx = AuthorAdmin(_author_name=bob_text, _env_dir=env_dir)
    assert pdx._author_dir is None
    assert pdx._calendar_output_file_name is None
    assert pdx._calendar_output_file_path is None
    assert pdx._public_file_name is None
    assert pdx._calendars_public_dir is None
    assert pdx._calendars_depot_dir is None
    assert pdx._calendars_ignore_dir is None
    assert pdx._calendars_digest_dir is None
    assert pdx._calendars_bond_dir is None
    assert pdx._isol_file_name is None
    assert pdx._isol_file_path is None
    # WHEN
    pdx.set_dirs()

    # THEN
    assert pdx._author_dir != None
    assert pdx._calendar_output_file_name != None
    assert pdx._calendar_output_file_path != None
    assert pdx._public_file_name != None
    assert pdx._calendars_public_dir != None
    assert pdx._calendars_depot_dir != None
    assert pdx._calendars_ignore_dir != None
    assert pdx._calendars_digest_dir != None
    assert pdx._calendars_bond_dir != None
    assert pdx._isol_file_name != None
    assert pdx._isol_file_path != None

    authors_drectory_name = "authors"
    x_authors_dir = f"{env_dir}/{authors_drectory_name}"
    x_author_dir = f"{x_authors_dir}/{bob_text}"
    x_public_file_name = f"{bob_text}.json"
    x_isol_file_name = "isol_calendar.json"
    x_isol_file_path = f"{x_author_dir}/{x_isol_file_name}"
    x_calendar_output_file_name = "output_calendar.json"
    x_calendar_output_file_path = f"{x_author_dir}/{x_calendar_output_file_name}"
    calendars_str = "calendars"
    x_calendars_depot_dir = f"{x_author_dir}/{calendars_str}"
    x_calendars_ignore_dir = f"{x_author_dir}/ignores"
    x_calendars_bond_dir = f"{x_author_dir}/bonds"
    x_calendars_digest_dir = f"{x_author_dir}/digests"
    x_calendars_public_dir = f"{env_dir}/{calendars_str}"
    assert pdx._authors_dir == x_authors_dir
    assert pdx._author_dir == x_author_dir
    assert pdx._isol_file_name == x_isol_file_name
    assert pdx._isol_file_path == x_isol_file_path
    assert pdx._calendar_output_file_name == x_calendar_output_file_name
    assert pdx._calendar_output_file_path == x_calendar_output_file_path
    assert pdx._calendars_depot_dir == x_calendars_depot_dir
    assert pdx._calendars_ignore_dir == x_calendars_ignore_dir
    assert pdx._calendars_bond_dir == x_calendars_bond_dir
    assert pdx._calendars_digest_dir == x_calendars_digest_dir
    assert pdx._public_file_name == x_public_file_name
    assert pdx._calendars_public_dir == x_calendars_public_dir


def test_AuthorAdmin_create_core_dir_and_files_CreatesDirsAndFiles(
    author_dir_setup_cleanup,
):
    # GIVEN create author
    jul_text = "julian"
    env_dir = get_temp_author_dir()
    pdx = AuthorAdmin(_author_name=jul_text, _env_dir=env_dir)
    pdx.set_dirs()
    assert os_path.exists(pdx._authors_dir) is False
    assert os_path.exists(pdx._author_dir) is False
    assert os_path.exists(pdx._isol_file_path) is False
    assert os_path.isdir(pdx._author_dir) is False
    assert os_path.exists(pdx._calendars_depot_dir) is False
    assert os_path.exists(pdx._calendars_digest_dir) is False
    assert os_path.exists(pdx._calendars_ignore_dir) is False
    assert os_path.exists(pdx._calendars_bond_dir) is False

    # WHEN
    calendar_x = example_authors.get_7nodeJRootWithH_calendar()
    pdx.create_core_dir_and_files(calendar_x)

    # THEN check calendars src directory created
    print(f"Checking {pdx._authors_dir=}")
    print(f"Checking {pdx._author_dir=}")
    assert os_path.exists(pdx._authors_dir)
    assert os_path.exists(pdx._author_dir)
    assert os_path.exists(pdx._isol_file_path)
    assert os_path.isdir(pdx._author_dir)
    assert os_path.exists(pdx._calendars_depot_dir)
    assert os_path.exists(pdx._calendars_digest_dir)
    assert os_path.exists(pdx._calendars_ignore_dir)
    assert os_path.exists(pdx._calendars_bond_dir)


def test_AuthorAdmin_create_core_dir_and_files_DoesNotOverWriteIsolCalendar(
    author_dir_setup_cleanup,
):
    # GIVEN create author
    jul_text = "julian"
    env_dir = get_temp_author_dir()
    jul_pdx = AuthorAdmin(_author_name=jul_text, _env_dir=env_dir)
    jul_pdx.set_dirs()
    calendar_x = example_authors.get_7nodeJRootWithH_calendar()
    jul_pdx.create_core_dir_and_files(calendar_x)
    assert os_path.exists(jul_pdx._isol_file_path)
    # jul_cx = calendar_get_from_json(x_func_open_file(jul_pdx._isol_file_path))
    ex1 = "teesting text"
    x_func_save_file(
        dest_dir=jul_pdx._author_dir,
        file_name=jul_pdx._isol_file_name,
        file_text=ex1,
    )
    assert x_func_open_file(jul_pdx._author_dir, jul_pdx._isol_file_name) == ex1

    # WHEN
    jul_pdx.create_core_dir_and_files(calendar_x)

    # THEN
    assert x_func_open_file(jul_pdx._author_dir, jul_pdx._isol_file_name) == ex1


def test_AuthorAdmin_set_author_name_WorksCorrectly(author_dir_setup_cleanup):
    # GIVEN create author
    env_dir = get_temp_author_dir()

    old_author_text = "bob"
    pdx = AuthorAdmin(_author_name=old_author_text, _env_dir=env_dir)
    calendar_x = example_authors.get_7nodeJRootWithH_calendar()
    pdx.set_dirs()
    pdx.create_core_dir_and_files(calendar_x)
    old_author_dir = pdx._author_dir
    # old_author_dir = f"{env_dir}/authors/{old_author_text}"
    print(f"{pdx._author_dir}")
    print(f"{env_dir}/authors/{old_author_text}")
    isol_file_name = "isol_calendar.json"
    old_isol_file_path = f"{old_author_dir}/{isol_file_name}"

    assert os_path.exists(old_author_dir)
    assert os_path.isdir(old_author_dir)
    assert os_path.exists(old_isol_file_path)

    new_author_text = "tim"
    new_author_dir = f"{env_dir}/authors/{new_author_text}"
    new_isol_file_path = f"{new_author_dir}/{isol_file_name}"
    assert os_path.exists(new_author_dir) == False
    assert os_path.isdir(new_author_dir) == False
    assert os_path.exists(new_isol_file_path) == False

    # WHEN
    pdx.set_author_name(new_name=new_author_text)

    # THEN
    assert os_path.exists(old_author_dir) == False
    assert os_path.isdir(old_author_dir) == False
    assert os_path.exists(old_isol_file_path) == False
    assert os_path.exists(new_author_dir)
    assert os_path.isdir(new_author_dir)
    assert os_path.exists(new_isol_file_path)


def test_authorunit_auto_output_to_public_SavesCalendarToPublicDir(
    author_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "bob"
    pdx = authoradmin_shop(bob_text, get_temp_author_dir())
    calendar_x = example_authors.get_6node_calendar()
    calendar_x.set_owner(new_owner=bob_text)
    pdx.create_core_dir_and_files(calendar_x)

    public_file_path = f"{pdx._calendars_public_dir}/{pdx._public_file_name}"
    print(f"{public_file_path=}")
    assert os_path.exists(public_file_path) is False

    # WHEN
    pdx.save_calendar_to_public(calendar_x=calendar_x)

    # THEN
    assert os_path.exists(public_file_path)
