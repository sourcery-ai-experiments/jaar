from src.system.author import authorunit_shop
from src.calendar.calendar import CalendarUnit
from src.calendar.idea import IdeaRoot
import src.system.examples.example_authors as example_authors
from src.system.examples.author_env_kit import (
    author_dir_setup_cleanup,
    get_temp_author_dir,
    create_calendar_file,
)
from os import path as os_path, scandir as os_scandir
from pytest import raises as pytest_raises
from src.calendar.x_func import (
    count_files as x_func_count_files,
    open_file as x_func_open_file,
    delete_dir as x_func_delete_dir,
)


def test_authorunit_exists(author_dir_setup_cleanup):
    # GIVEN
    author_text = "test1"
    env_dir = get_temp_author_dir()

    # WHEN
    ux = authorunit_shop(name=author_text, env_dir=env_dir)

    # GIVEN
    assert ux._admin._author_name != None
    assert ux._isol is None


def test_authorunit_auto_output_to_public_SavesCalendarToPublicDirWhenTrue(
    author_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_author_dir()
    tim_text = "Tim"
    public_file_name = f"{tim_text}.json"
    public_file_path = f"{get_temp_author_dir()}/calendars/{public_file_name}"
    print(f"{public_file_path=}")
    # public_file_path = f"src/system/examples/ex_env/calendars/{public_file_name}"
    ux = authorunit_shop(tim_text, env_dir, _auto_output_to_public=True)
    ux.create_core_dir_and_files()
    assert os_path.exists(public_file_path) is False

    # WHEN
    ux.set_depot_calendar(CalendarUnit(_owner=tim_text), "blind_trust")

    # THEN
    assert os_path.exists(public_file_path)


def test_authorunit_auto_output_to_public_DoesNotSaveCalendarToPublicDirWhenFalse(
    author_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_author_dir()
    tim_text = "Tim"
    public_file_name = f"{tim_text}.json"
    public_file_path = f"{get_temp_author_dir()}/calendars/{public_file_name}"
    print(f"{public_file_path=}")
    # public_file_path = f"src/system/examples/ex_env/calendars/{public_file_name}"
    ux = authorunit_shop(tim_text, env_dir, _auto_output_to_public=False)
    ux.create_core_dir_and_files()
    assert os_path.exists(public_file_path) is False

    # WHEN
    ux.set_depot_calendar(CalendarUnit(_owner=tim_text), depotlink_type="blind_trust")

    # THEN
    assert os_path.exists(public_file_path) is False


def test_authorunit_get_isol_createsEmptyCalendarWhenFileDoesNotExist(
    author_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_ux = authorunit_shop(tim_text, get_temp_author_dir())
    tim_ux.create_core_dir_and_files()
    assert os_path.exists(tim_ux._admin._isol_file_path)
    x_func_delete_dir(dir=tim_ux._admin._isol_file_path)
    assert os_path.exists(tim_ux._admin._isol_file_path) is False
    assert tim_ux._isol is None

    # WHEN
    cx_isol = tim_ux.get_isol()

    # THEN
    assert os_path.exists(tim_ux._admin._isol_file_path)
    assert tim_ux._isol != None


def test_authorunit_get_isol_getsMemoryCalendarIfExists(
    author_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_ux = authorunit_shop(tim_text, get_temp_author_dir())
    tim_ux.create_core_dir_and_files()
    isol_file_path = f"{tim_ux._admin._author_dir}/{tim_ux._admin._isol_file_name}"
    cx_isol1 = tim_ux.get_isol()
    assert os_path.exists(isol_file_path)
    assert tim_ux._isol != None

    # WHEN
    ray_text = "Ray"
    tim_ux._isol = CalendarUnit(_owner=ray_text)
    cx_isol2 = tim_ux.get_isol()

    # THEN
    assert cx_isol2._owner == ray_text
    assert cx_isol2 != cx_isol1

    # WHEN
    tim_ux._isol = None
    cx_isol3 = tim_ux.get_isol()

    # THEN
    assert cx_isol3._owner != ray_text
    assert cx_isol3 == cx_isol1


def test_authorunit_set_isol_savesIsolCalendarSet_isol_None(
    author_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_ux = authorunit_shop(tim_text, get_temp_author_dir())
    tim_ux.create_core_dir_and_files()
    isol_file_path = f"{tim_ux._admin._author_dir}/{tim_ux._admin._isol_file_name}"
    cx_isol1 = tim_ux.get_isol()
    assert os_path.exists(isol_file_path)
    assert tim_ux._isol != None

    # WHEN
    uid_text = "Not a real uid"
    tim_ux._isol._idearoot._uid = uid_text
    tim_ux.set_isol()

    # THEN
    assert os_path.exists(isol_file_path)
    assert tim_ux._isol is None
    cx_isol2 = tim_ux.get_isol()
    assert cx_isol2._idearoot._uid == uid_text


def test_authorunit_set_isol_savesGivenCalendarSet_isol_None(
    author_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    ux = authorunit_shop(tim_text, get_temp_author_dir())
    ux.create_core_dir_and_files()
    isol_file_path = f"{ux._admin._author_dir}/{ux._admin._isol_file_name}"
    cx_isol1 = ux.get_isol()
    assert os_path.exists(isol_file_path)
    assert ux._isol != None

    # WHEN
    isol_uid_text = "this is ._isol uid"
    ux._isol._idearoot._uid = isol_uid_text

    new_cx = CalendarUnit(_owner=tim_text)
    new_cx_uid_text = "this is pulled CalendarUnit uid"
    new_cx._idearoot._uid = new_cx_uid_text

    ux.set_isol(new_cx)

    # THEN
    assert os_path.exists(isol_file_path)
    assert ux._isol is None
    assert ux.get_isol()._idearoot._uid != isol_uid_text
    assert ux.get_isol()._idearoot._uid == new_cx_uid_text

    # GIVEN
    ux.set_isol(new_cx)
    assert os_path.exists(isol_file_path)
    assert ux._isol is None

    # WHEN
    ux.set_isol_if_empty()

    # THEN
    assert ux._isol != None
    assert os_path.exists(isol_file_path)

    # WHEN
    isol_uid_text = "this is ._isol uid"
    ux._isol._idearoot._uid = isol_uid_text


def test_authorunit_set_isol_if_emtpy_DoesNotReplace_isol(
    author_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    ux = authorunit_shop(tim_text, get_temp_author_dir())
    ux.create_core_dir_and_files()
    saved_cx = CalendarUnit(_owner=tim_text)
    saved_cx_uid_text = "this is pulled CalendarUnit uid"
    saved_cx._idearoot._uid = saved_cx_uid_text
    ux.set_isol(saved_cx)
    ux.get_isol()
    assert ux._isol != None

    # WHEN
    isol_uid_text = "this is ._isol uid"
    ux._isol._idearoot._uid = isol_uid_text
    ux.set_isol_if_empty()

    # THEN
    assert ux._isol != None
    assert ux._isol._idearoot._uid == isol_uid_text
    assert ux._isol._idearoot._uid != saved_cx_uid_text
