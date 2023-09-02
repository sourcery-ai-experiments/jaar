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
    person_text = "test1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(
        name=person_text, env_dir=env_dir, _auto_dest_calendar_to_public_calendar=True
    )
    assert px.name == person_text
    assert px._src_calendarlinks == {}
    assert px._auto_dest_calendar_to_public_calendar
    # assert px._re_idearoot != None
    # assert str(type(px._re_idearoot)).find(".idea.IdeaRoot'>") > 0
    # assert px._re_idearoot._desc == person_text
    # assert px._re_idearoot._weight == 1

    # assert px._re_idearoot._uid == -1
    # assert px._re_idearoot._begin is None
    # assert px._re_idearoot._close is None
    # assert px._re_idearoot._addin is None
    # assert px._re_idearoot._denom is None
    # assert px._re_idearoot._numor is None
    # assert px._re_idearoot._reest is None
    # assert px._re_idearoot._special_road is None
    # assert px._re_idearoot._numeric_road is None
    # assert px._re_idearoot.promise == False
    # assert px._re_idearoot._all_member_credit is None
    # assert px._re_idearoot._all_member_debt is None
    # assert px._re_idearoot._is_expanded == True
    assert px._dest_calendar != None
    assert px._person_dir != None
    assert px._person_calendars_dir != None
    assert px._digest_calendars_dir != None


def test_personunit_creates_files(person_dir_setup_cleanup):
    # GIVEN create person
    person1_text = "person1"
    env_dir = get_temp_person_dir()

    persons_dir = f"{env_dir}/persons"
    calendars_dir = f"{env_dir}/calendars"
    person1_dir = f"{persons_dir}/{person1_text}"
    person_file_name = f"{person1_text}.json"
    person_calendars_dir = f"{persons_dir}/{person1_text}/calendars/"
    digest_calendars_dir = f"{persons_dir}/{person1_text}/digests/"
    ignore_calendars_dir = f"{persons_dir}/{person1_text}/ignores/"
    bond_calendars_dir = f"{persons_dir}/{person1_text}/bonds/"
    person_file_path = f"{person1_dir}/{person_file_name}"
    px = personunit_shop(name=person1_text, env_dir=env_dir)
    px._set_env_dir(env_dir=env_dir)
    px._set_src_calendarlinks_empty_if_null()
    px._set_emtpy_dest_calendar()
    assert os_path.exists(persons_dir) is False
    assert os_path.exists(calendars_dir) is False
    assert os_path.exists(person1_dir) is False
    assert os_path.isdir(person1_dir) is False
    assert os_path.exists(person_calendars_dir) is False
    assert os_path.exists(digest_calendars_dir) is False
    assert os_path.exists(ignore_calendars_dir) is False
    assert os_path.exists(bond_calendars_dir) is False

    # WHEN
    px.create_core_dir_and_files()

    # THEN confirm calendars src directory created
    assert os_path.exists(persons_dir)
    assert os_path.exists(calendars_dir)
    assert os_path.exists(person1_dir)
    assert os_path.isdir(person1_dir)
    assert os_path.exists(person_calendars_dir)
    print(f"{person_file_path=}")
    assert os_path.exists(person_file_path)
    assert os_path.exists(digest_calendars_dir)
    assert os_path.exists(ignore_calendars_dir)
    assert os_path.exists(bond_calendars_dir)


def test_personunit_set_person_name_WorksCorrectly(person_dir_setup_cleanup):
    # GIVEN create person
    env_dir = get_temp_person_dir()

    old_person_text = "person1"
    old_person_dir = f"{env_dir}/persons/{old_person_text}"
    old_person_file_name = f"{old_person_text}.json"
    old_person_file_path = f"{old_person_dir}/{old_person_file_name}"
    px = personunit_shop(name=old_person_text, env_dir=env_dir)
    px.create_core_dir_and_files()
    assert os_path.exists(old_person_dir)
    assert os_path.isdir(old_person_dir)
    assert os_path.exists(old_person_file_path)

    new_person_text = "person2"
    new_person_dir = f"{env_dir}/persons/{new_person_text}"
    new_person_file_name = f"{new_person_text}.json"
    new_person_file_path = f"{new_person_dir}/{new_person_file_name}"
    assert os_path.exists(new_person_dir) == False
    assert os_path.isdir(new_person_dir) == False
    assert os_path.exists(new_person_file_path) == False

    # WHEN
    px.set_person_name(new_name=new_person_text)

    # THEN
    assert os_path.exists(old_person_dir) == False
    assert os_path.isdir(old_person_dir) == False
    assert os_path.exists(old_person_file_path) == False
    assert os_path.exists(new_person_dir)
    assert os_path.isdir(new_person_dir)
    assert os_path.exists(new_person_file_path)


def test_personunit_set_dest_calendar_to_public_calendar_SavesCalendarToPublicDir(
    person_dir_setup_cleanup,
):
    # GIVEN create person
    env_dir = get_temp_person_dir()

    person_text = "person1"
    px = personunit_shop(name=person_text, env_dir=env_dir)
    px.create_core_dir_and_files()
    public_file_name = f"{person_text}.json"
    public_file_path = f"{px._public_calendars_dir}/{public_file_name}"
    assert os_path.exists(public_file_path) is False

    # WHEN
    px.set_dest_calendar_to_public_calendar()

    # THEN
    assert os_path.exists(public_file_path)
    print(f"{public_file_path=}")


def test_personunit_auto_dest_calendar_to_public_calendar_SavesCalendarToPublicDir(
    person_dir_setup_cleanup,
):
    # GIVEN create person
    env_dir = get_temp_person_dir()

    person_text = "person1"
    public_file_name = f"{person_text}.json"
    public_file_path = f"src/system/examples/ex_env/calendars/{public_file_name}"
    px = personunit_shop(
        name=person_text, env_dir=env_dir, _auto_dest_calendar_to_public_calendar=True
    )
    px.create_core_dir_and_files()
    assert os_path.exists(public_file_path) is False

    # WHEN
    px.receive_src_calendarunit_obj(calendar_x=CalendarUnit(_owner="bobs calendarunit"))

    # THEN
    assert os_path.exists(public_file_path)
