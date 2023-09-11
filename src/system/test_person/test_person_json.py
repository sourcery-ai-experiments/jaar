import src.system.examples.example_persons as person_examples
from src.system.person import get_from_json as person_get_from_json
from src.calendar.x_func import x_is_json, x_get_dict
from json import loads as json_loads
from src.system.examples.person_env_kit import (
    person_dir_setup_cleanup,
    get_temp_person_dir,
)
from src.calendar.calendar import CalendarUnit


def test_person_set_depot_calendar_SetsCorrectInfo():
    # GIVEN
    env_dir = get_temp_person_dir()
    person_x = person_examples.get_person_2calendar(env_dir=env_dir)
    assert person_x._isol.get_members_depotlink_count() == 2
    print(f"{person_x._isol._members.keys()=}")

    # WHEN
    assignment_text = "assignment"
    zia_text = "Zia"
    person_x.set_depot_calendar(CalendarUnit(_owner=zia_text), assignment_text)
    zoa_text = "Zoa"
    person_x.set_depot_calendar(CalendarUnit(_owner=zoa_text), assignment_text)

    # THEN
    print(f"{person_x._isol._members.keys()=}")
    assert person_x._isol.get_members_depotlink_count() == 4


def test_person_get_dict_ReturnsDictObject(person_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_person_dir()
    person_x = person_examples.get_person_2calendar(env_dir=env_dir)
    person_x.set_depot_calendar(
        calendar_x=CalendarUnit(_owner="swim8"), depotlink_type="blind_trust"
    )

    # WHEN
    x_dict = person_x.get_dict()

    # THEN
    assert x_dict != None
    assert str(type(x_dict)) == "<class 'dict'>"
    assert x_dict["name"] == person_x._admin._person_name
    assert x_dict["_auto_output_to_public"] == person_x._admin._auto_output_to_public
    print("check internal obj attributes")
    # for src_calendar_owner, src_calendar_obj in x_dict["_depotlinks"].items():
    #     print(f"{src_calendar_owner=}")


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
    assert x_dict["name"] == x_person._admin._person_name


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
    person_json = person_get_from_json(
        person_json=x_json, env_dir=get_temp_person_dir()
    )

    # THEN check json
    assert str(type(person_json)).find(".person.PersonUnit'>") > 0
    assert person_json._admin._person_name != None
    assert person_json._admin._person_name == person_algo._admin._person_name
    assert (
        person_json._admin._auto_output_to_public
        == person_algo._admin._auto_output_to_public
    )
    assert person_json._admin._env_dir == person_algo._admin._env_dir
    assert (
        person_json._admin._calendars_public_dir
        == person_algo._admin._calendars_public_dir
    )
    assert (
        person_json._admin._calendars_digest_dir
        == person_algo._admin._calendars_digest_dir
    )
    assert person_json._admin._person_dir != None
