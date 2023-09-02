import src.system.examples.example_persons as person_examples
from src.system.person import (
    get_from_json as get_person_from_json,
    calendarlink_shop,
)
from src.calendar.x_func import x_is_json, x_get_dict
from json import loads as json_loads
from src.system.examples.person_env_kit import (
    person_dir_setup_cleanup,
    get_temp_person_dir,
)
from src.calendar.calendar import CalendarUnit


def test_person_receive_src_calendarunit_obj_SetsCorrectInfo():
    # GIVEN
    env_dir = get_temp_person_dir()
    person_x = person_examples.get_person_2calendar(env_dir=env_dir)
    assert len(person_x.get_calendar_from_calendars_dirlinks_dict()) == 2

    # WHEN
    swim_text = "swim1"
    person_x.receive_src_calendarunit_obj(calendar_x=CalendarUnit(_owner=swim_text))
    run_text = "run1"
    person_x.receive_src_calendarunit_obj(calendar_x=CalendarUnit(_owner=run_text))

    # THEN
    assert len(person_x.get_calendar_from_calendars_dirlinks_dict()) == 4


def test_person_get_calendar_from_calendars_dirlinks_dict_ReturnsCorrectInfo():
    # GIVEN
    env_dir = get_temp_person_dir()
    person_x = person_examples.get_person_2calendar(env_dir=env_dir)
    assert len(person_x.get_calendar_from_calendars_dirlinks_dict()) == 2
    swim_text = "swim1"
    person_x.receive_src_calendarunit_obj(calendar_x=CalendarUnit(_owner=swim_text))
    run_text = "run1"
    person_x.receive_src_calendarunit_obj(calendar_x=CalendarUnit(_owner=run_text))

    # WHEN
    src_calendarlinks_dict = person_x.get_calendar_from_calendars_dirlinks_dict()

    # THEN
    assert len(src_calendarlinks_dict) == 4
    swim_dict = src_calendarlinks_dict.get(swim_text)
    assert str(type(swim_dict)) == "<class 'dict'>"
    assert len(swim_dict) > 1
    assert swim_dict.get("calendar_desc") == swim_text
    assert swim_dict.get("link_type") == "blind_trust"


def test_person_get_dict_ReturnsDictObject(person_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_person_dir()
    person_x = person_examples.get_person_2calendar(env_dir=env_dir)
    person_x.receive_src_calendarunit_obj(calendar_x=CalendarUnit(_owner="swim8"))

    # WHEN
    x_dict = person_x.get_dict()

    # THEN
    assert x_dict != None
    assert str(type(x_dict)) == "<class 'dict'>"
    assert x_dict["name"] == person_x.name
    assert (
        x_dict["_auto_dest_calendar_to_public_calendar"]
        == person_x._auto_dest_calendar_to_public_calendar
    )
    assert x_dict["_env_dir"] == person_x._env_dir
    assert x_dict["_public_calendars_dir"] == person_x._public_calendars_dir
    assert x_dict["_digest_calendars_dir"] == person_x._digest_calendars_dir
    print("check internal obj attributes")
    # for src_calendar_desc, src_calendar_obj in x_dict["_src_calendarlinks"].items():
    #     print(f"{src_calendar_desc=}")

    assert x_dict["_src_calendarlinks"]["A"] != None
    assert x_dict["_src_calendarlinks"]["J"] != None
    assert len(x_dict["_src_calendarlinks"]) == 3
    assert (
        x_dict["_src_calendarlinks"]
        == person_x.get_calendar_from_calendars_dirlinks_dict()
    )
    assert len(person_x.get_calendar_from_calendars_dirlinks_dict()) == 3

    assert x_dict["_dest_calendar"] == person_x._dest_calendar.get_dict()


def test_person_export_to_JSON_simple_example_works(person_dir_setup_cleanup):
    x_json = None
    env_dir = get_temp_person_dir()
    x_person = person_examples.get_person_2calendar(env_dir=env_dir)

    assert x_json is None
    x_json = x_person.get_json()
    assert x_json != None
    assert True == x_is_json(x_json)
    x_dict = json_loads(x_json)
    # print(x_dict)
    assert x_dict["name"] == x_person.name
    assert x_dict["_env_dir"] == x_person._env_dir
    assert x_dict["_public_calendars_dir"] == x_person._public_calendars_dir
    assert x_dict["_digest_calendars_dir"] == x_person._digest_calendars_dir
    assert x_dict["_src_calendarlinks"]["A"] != None
    assert x_dict["_src_calendarlinks"]["J"] != None
    assert len(x_dict["_src_calendarlinks"]) == 2
    assert (
        x_dict["_src_calendarlinks"]
        == x_person.get_calendar_from_calendars_dirlinks_dict()
    )
    assert x_dict["_dest_calendar"] == x_person._dest_calendar.get_dict()


def test_person_get_json_CorrectlyWorksForSimpleExample(
    person_dir_setup_cleanup,
):
    # GIVEN
    x_json = None
    person_algo = person_examples.get_person_2calendar(env_dir=get_temp_person_dir())

    # WHEN
    x_json = person_algo.get_json()

    # THEN
    assert x_is_json(x_json) == True

    # WHEN
    x_dict = x_get_dict(json_x=x_json)

    # THEN check x_dict

    # WHEN
    person_json = get_person_from_json(person_json=x_json)

    # THEN check json
    assert str(type(person_json)).find(".person.PersonUnit'>") > 0
    assert person_json.name != None
    assert person_json.name == person_algo.name
    assert (
        person_json._auto_dest_calendar_to_public_calendar
        == person_algo._auto_dest_calendar_to_public_calendar
    )
    assert person_json._env_dir == person_algo._env_dir
    assert person_json._public_calendars_dir == person_algo._public_calendars_dir
    assert person_json._digest_calendars_dir == person_algo._digest_calendars_dir
    assert person_json._person_dir != None
    assert len(person_json._src_calendarlinks) == 2
    assert (
        person_json._src_calendarlinks.keys() == person_algo._src_calendarlinks.keys()
    )

    # for algo_calendarlink_x in person_algo._src_calendarlinks.values():
    #     assert algo_calendarlink_x == person_json._src_calendarlinks.get(
    #         algo_calendarlink_x.calendar_desc
    #     )

    assert len(person_json._src_calendarlinks) == len(person_algo._src_calendarlinks)
    assert person_json._dest_calendar == person_json._dest_calendar
