from src.system.person import personunit_shop
import src.system.examples.example_persons as example_persons
from src.system.examples.person_env_kit import (
    person_dir_setup_cleanup,
    get_temp_person_dir,
    create_calendar_file_for_person,
)
from src.system.examples.env_kit import get_temp_env_name
from src.system.system import SystemUnit
from os import path as os_path, scandir as os_scandir
from pytest import raises as pytest_raises
from src.calendar.x_func import (
    count_files as x_func_count_files,
    dir_files as x_func_dir_files,
)


def test_personunitset_depotlink_RaisesErrorWhenCalendarDoesNotExist(
    person_dir_setup_cleanup,
):
    # GIVEN
    person1_text = "person1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=person1_text, env_dir=env_dir)
    swim_text = "swim"
    assert px._depotlinks == {}

    # WHEN / THEN
    file_path_x = f"{px._admin._calendars_depot_dir}/{swim_text}.json"
    print(f"{file_path_x=}")
    with pytest_raises(Exception) as excinfo:
        px.set_depotlink(owner=swim_text)
    assert (
        str(excinfo.value)
        == f"Person {person1_text} cannot find calendar {swim_text} in {file_path_x}"
    )


def test_personunitset_depotlink_CorrectlyUsed(person_dir_setup_cleanup):
    # GIVEN
    person1_text = "person1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=person1_text, env_dir=env_dir)
    swim_text = "swim"
    create_calendar_file_for_person(px._admin._calendars_depot_dir, swim_text)
    assert px._depotlinks == {}

    # WHEN
    px.set_depotlink(owner=swim_text)

    # THEN
    assert list(px._depotlinks.keys()) == [swim_text]


def test_personunit_delete_depotlink_CorrectlyDeletesObj(person_dir_setup_cleanup):
    # GIVEN
    person1_text = "person1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=person1_text, env_dir=env_dir)
    swim_text = "swim"
    create_calendar_file_for_person(
        px._admin._calendars_depot_dir, calendar_owner=swim_text
    )
    px.set_depotlink(owner=swim_text)
    assert list(px._depotlinks.keys()) == [swim_text]

    # WHEN
    px.delete_depotlink(calendar_owner=swim_text)

    # THEN
    assert px._depotlinks == {}


def test_personunit_delete_depotlink_CorrectlyDeletesBlindTrustFile(
    person_dir_setup_cleanup,
):
    # GIVEN
    person1_text = "person1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=person1_text, env_dir=env_dir)
    swim_text = "swim"
    create_calendar_file_for_person(
        calendar_person_dir=px._admin._calendars_depot_dir,
        calendar_owner=swim_text,
    )
    px.set_depotlink(owner=swim_text, depotlink_type="blind_trust")
    assert x_func_count_files(dir_path=px._admin._calendars_depot_dir) == 1
    assert x_func_count_files(dir_path=px._admin._calendars_digest_dir) == 1

    # WHEN
    px.delete_depotlink(calendar_owner=swim_text)

    # THEN
    assert x_func_count_files(dir_path=px._admin._calendars_depot_dir) == 0
    assert x_func_count_files(dir_path=px._admin._calendars_digest_dir) == 0


def test_personunit_post_calendar_to_depot_SavesFileCorrectly(
    person_dir_setup_cleanup,
):
    # GIVEN
    person_name = "person1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=person_name, env_dir=env_dir)
    assert x_func_count_files(px._admin._calendars_depot_dir) is None

    # WHEN
    px.post_calendar_to_depot(calendar_x=example_persons.get_1node_calendar())

    # THEN
    print(f"Saving to {px._admin._calendars_depot_dir=}")
    # for path_x in os_scandir(px._admin._calendars_depot_dir):
    #     print(f"{path_x=}")
    assert x_func_count_files(px._admin._calendars_depot_dir) == 1


def test_personunit_receive_src_calendarunit_file_SavesFileCorrectly(
    person_dir_setup_cleanup,
):
    # GIVEN
    person_name = "person1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=person_name, env_dir=env_dir)
    s1 = example_persons.get_2node_calendar()
    sx_json = s1.get_json()
    assert (
        x_func_count_files(px._admin._calendars_depot_dir) is None
    )  # dir does not exist

    # WHEN
    px.receive_src_calendarunit_file(calendar_json=sx_json)

    # THEN
    print(f"Saving to {px._admin._calendars_depot_dir=}")
    # for path_x in os_scandir(px._admin._calendars_depot_dir):
    #     print(f"{path_x=}")
    assert x_func_count_files(px._admin._calendars_depot_dir) == 1


def test_personunit_delete_ignore_depotlink_CorrectlyDeletesObj(
    person_dir_setup_cleanup,
):
    # GIVEN
    person1_text = "person1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=person1_text, env_dir=env_dir)
    swim_text = "swim"
    create_calendar_file_for_person(
        calendar_person_dir=px._admin._calendars_depot_dir,
        calendar_owner=swim_text,
    )
    px.set_depotlink(owner=swim_text)
    assert list(px._depotlinks.keys()) == [swim_text]

    # WHEN
    px.delete_depotlink(calendar_owner=swim_text)

    # THEN
    assert px._depotlinks == {}


def test_personunit_delete_depotlink_CorrectlyDoesNotDeletesIgnoreFile(
    person_dir_setup_cleanup,
):
    # GIVEN
    person1_text = "person1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=person1_text, env_dir=env_dir)
    swim_text = "swim"
    create_calendar_file_for_person(px._admin._calendars_depot_dir, swim_text)
    px.set_depotlink(owner=swim_text, depotlink_type="ignore")
    assert x_func_count_files(dir_path=px._admin._calendars_depot_dir) == 1
    assert x_func_count_files(dir_path=px._admin._calendars_digest_dir) == 1
    assert x_func_count_files(dir_path=px._admin._calendars_ignore_dir) == 1

    # WHEN
    px.delete_depotlink(calendar_owner=swim_text)

    # THEN
    assert x_func_count_files(dir_path=px._admin._calendars_depot_dir) == 0
    assert x_func_count_files(dir_path=px._admin._calendars_digest_dir) == 0
    assert x_func_count_files(dir_path=px._admin._calendars_ignore_dir) == 1


# def test_personunit_set_ignore_calendar_file_CorrectlyUpdatesIgnoreFile(
#     person_dir_setup_cleanup,
# ):
#     # GIVEN
#     person1_text = "person1"
#     env_dir = get_temp_person_dir()
#     px = personunit_shop(name=person1_text, env_dir=env_dir)
#     swim_text = "swim"
#     create_calendar_file_for_person(px._admin._calendars_depot_dir, swim_text)
#     px.set_depotlink(owner=swim_text, depotlink_type="ignore")
#     assert x_func_count_files(dir_path=px._admin._calendars_ignore_dir) == 1
#     cx1 = px.get_ignore_calendar_from_ignore_calendar_files(_owner=swim_text)
#     assert len(cx1._members) == 0
#     cx1.add_memberunit(name="tim")
#     assert len(cx1._members) == 1

#     # WHEN
#     px.set_ignore_calendar_file()

#     # THEN
#     cx2 = px.get_ignore_calendar_from_ignore_calendar_files(_owner=swim_text)
#     assert len(cx2._members) == 0

#     assert x_func_count_files(dir_path=px._admin._calendars_ignore_dir) == 1


def test_personunit_refresh_depotlinks_CorrectlyPullsAllPublicCalendars(
    person_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_person_dir()
    system_name = get_temp_env_name()
    e1 = SystemUnit(name=system_name, systems_dir=env_dir)
    e1.create_dirs_if_null()
    person1_text = "person1"
    # px = personunit_shop(name=person1_text, env_dir=env_dir)
    e1.create_new_personunit(person_name=person1_text)
    px = e1.get_person_obj_from_system(name=person1_text)

    ernie_calendar = example_persons.get_calendar_2CleanNodesRandomWeights(
        _owner="ernie"
    )
    old_steve_calendar = example_persons.get_calendar_2CleanNodesRandomWeights(
        _owner="steve"
    )
    e1.save_calendarunit_obj_to_calendars_dir(calendar_x=ernie_calendar)
    e1.save_calendarunit_obj_to_calendars_dir(calendar_x=old_steve_calendar)
    px.post_calendar_to_depot(calendar_x=ernie_calendar)
    px.post_calendar_to_depot(calendar_x=old_steve_calendar)
    assert len(px.create_output_calendar().get_idea_list()) == 4
    new_steve_calendar = example_persons.get_calendar_3CleanNodesRandomWeights(
        _owner="steve"
    )
    e1.save_calendarunit_obj_to_calendars_dir(calendar_x=new_steve_calendar)
    print(f"{env_dir=} {px._admin._calendars_public_dir=}")
    # for file_name in x_func_dir_files(dir_path=env_dir):
    #     print(f"{px._admin._calendars_public_dir=} {file_name=}")

    # for file_name in x_func_dir_files(dir_path=px._admin._calendars_public_dir):
    #     print(f"{px._admin._calendars_public_dir=} {file_name=}")

    # WHEN
    px.receive_all_src_calendarunit_files()

    # THEN
    assert len(px.create_output_calendar().get_idea_list()) == 5
