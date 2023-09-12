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
    delete_dir as x_func_delete_dir,
)


def test_personunit_exists(person_dir_setup_cleanup):
    # GIVEN
    person_text = "test1"
    env_dir = get_temp_person_dir()

    # WHEN
    px = personunit_shop(name=person_text, env_dir=env_dir)

    # GIVEN
    assert px._admin._person_name != None
    assert px._isol is None


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
    px.set_depot_calendar(CalendarUnit(_owner=tim_text), "blind_trust")

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
    px.set_depot_calendar(CalendarUnit(_owner=tim_text), depotlink_type="blind_trust")

    # THEN
    assert os_path.exists(public_file_path) is False


def test_personunit_get_isol_calendar_createsEmptyCalendarWhenFileDoesNotExist(
    person_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_px = personunit_shop(tim_text, get_temp_person_dir())
    tim_px.create_core_dir_and_files()
    assert os_path.exists(tim_px._admin._isol_file_path)
    x_func_delete_dir(dir=tim_px._admin._isol_file_path)
    assert os_path.exists(tim_px._admin._isol_file_path) is False
    assert tim_px._isol is None

    # WHEN
    cx_isol = tim_px.get_isol_calendar()

    # THEN
    assert os_path.exists(tim_px._admin._isol_file_path)
    assert tim_px._isol != None


def test_personunit_get_isol_calendar_getsMemoryCalendarIfExists(
    person_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_px = personunit_shop(tim_text, get_temp_person_dir())
    tim_px.create_core_dir_and_files()
    isol_file_path = f"{tim_px._admin._person_dir}/{tim_px._admin._isol_file_name}"
    cx_isol1 = tim_px.get_isol_calendar()
    assert os_path.exists(isol_file_path)
    assert tim_px._isol != None

    # WHEN
    ray_text = "Ray"
    tim_px._isol = CalendarUnit(_owner=ray_text)
    cx_isol2 = tim_px.get_isol_calendar()

    # THEN
    assert cx_isol2._owner == ray_text
    assert cx_isol2 != cx_isol1

    # WHEN
    tim_px._isol = None
    cx_isol3 = tim_px.get_isol_calendar()

    # THEN
    assert cx_isol3._owner != ray_text
    assert cx_isol3 == cx_isol1


def test_personunit_set_isol_calendar_savesIsolCalendarSet_isol_None(
    person_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_px = personunit_shop(tim_text, get_temp_person_dir())
    tim_px.create_core_dir_and_files()
    isol_file_path = f"{tim_px._admin._person_dir}/{tim_px._admin._isol_file_name}"
    cx_isol1 = tim_px.get_isol_calendar()
    assert os_path.exists(isol_file_path)
    assert tim_px._isol != None

    # WHEN
    uid_text = "Not a real uid"
    tim_px._isol._idearoot._uid = uid_text
    tim_px.set_isol_calendar()

    # THEN
    assert os_path.exists(isol_file_path)
    assert tim_px._isol is None
    cx_isol2 = tim_px.get_isol_calendar()
    assert cx_isol2._idearoot._uid == uid_text


def test_personunit_set_isol_calendar_savesGivenCalendarSet_isol_None(
    person_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    px = personunit_shop(tim_text, get_temp_person_dir())
    px.create_core_dir_and_files()
    isol_file_path = f"{px._admin._person_dir}/{px._admin._isol_file_name}"
    cx_isol1 = px.get_isol_calendar()
    assert os_path.exists(isol_file_path)
    assert px._isol != None

    # WHEN
    isol_uid_text = "this is ._isol uid"
    px._isol._idearoot._uid = isol_uid_text

    new_cx = CalendarUnit(_owner=tim_text)
    new_cx_uid_text = "this is pulled CalendarUnit uid"
    new_cx._idearoot._uid = new_cx_uid_text

    px.set_isol_calendar(new_cx)

    # THEN
    assert os_path.exists(isol_file_path)
    assert px._isol is None
    assert px.get_isol_calendar()._idearoot._uid != isol_uid_text
    assert px.get_isol_calendar()._idearoot._uid == new_cx_uid_text

    # GIVEN
    px.set_isol_calendar(new_cx)
    assert os_path.exists(isol_file_path)
    assert px._isol is None

    # WHEN
    px.set_isol_calendar_if_empty()

    # THEN
    assert px._isol != None
    assert os_path.exists(isol_file_path)

    # WHEN
    isol_uid_text = "this is ._isol uid"
    px._isol._idearoot._uid = isol_uid_text


def test_personunit_set_isol_calendar_if_emtpy_DoesNotReplace_isol(
    person_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    px = personunit_shop(tim_text, get_temp_person_dir())
    px.create_core_dir_and_files()
    saved_cx = CalendarUnit(_owner=tim_text)
    saved_cx_uid_text = "this is pulled CalendarUnit uid"
    saved_cx._idearoot._uid = saved_cx_uid_text
    px.set_isol_calendar(saved_cx)
    px.get_isol_calendar()
    assert px._isol != None

    # WHEN
    isol_uid_text = "this is ._isol uid"
    px._isol._idearoot._uid = isol_uid_text
    px.set_isol_calendar_if_empty()

    # THEN
    assert px._isol != None
    assert px._isol._idearoot._uid == isol_uid_text
    assert px._isol._idearoot._uid != saved_cx_uid_text
