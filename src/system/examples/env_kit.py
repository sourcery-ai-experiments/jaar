# from lw.calendar import CalendarUnit
from src.system.system import SystemUnit
from os import listdir as os_listdir, rename as os_rename, path as os_path
from pytest import fixture as pytest_fixture
from src.calendar.examples.example_calendars import (
    calendar_v001 as example_calendars_calendar_v001,
    calendar_v002 as example_calendars_calendar_v002,
    get_calendar_1Task_1CE0MinutesRequired_1AcptFact as example_calendars_get_calendar_1Task_1CE0MinutesRequired_1AcptFact,
    get_calendar_with7amCleanTableRequired as example_calendars_get_calendar_with7amCleanTableRequired,
    get_calendar_base_time_example as example_calendars_get_calendar_base_time_example,
    get_calendar_x1_3levels_1required_1acptfacts as example_calendars_get_calendar_x1_3levels_1required_1acptfacts,
)
from src.system.examples.example_persons import (
    get_1node_calendar as example_persons_get_1node_calendar,
    get_7nodeJRootWithH_calendar as example_persons_get_7nodeJRootWithH_calendar,
    get_calendar_2CleanNodesRandomWeights as example_persons_get_calendar_2CleanNodesRandomWeights,
    get_calendar_3CleanNodesRandomWeights as example_persons_get_calendar_3CleanNodesRandomWeights,
)
from src.calendar.calendar import CalendarUnit
from src.system.person import personunit_shop
from src.calendar.x_func import (
    single_dir_create_if_null,
    delete_dir as x_func_delete_dir,
    copy_dir,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
    dir_files as x_func_dir_files,
)


def get_temp_env_name():
    return "ex_env04"


def get_temp_env_dir():
    return f"{get_test_systems_dir()}/{get_temp_env_name()}"


def get_test_systems_dir():
    return "src/system/examples/systems"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_temp_env_dir()
    x_func_delete_dir(dir=env_dir)
    yield env_dir
    x_func_delete_dir(dir=env_dir)


def create_calendar_file_for_systems(system_dir: str, calendar_owner: str):
    calendar_x = CalendarUnit(_owner=calendar_owner)
    calendar_dir = f"{system_dir}/calendars"
    # file_path = f"{calendar_dir}/{calendar_x._owner}.json"
    # if not path.exists(file_path):
    # print(f"{file_path=} {calendar_x._owner=}")

    x_func_save_file(
        dest_dir=calendar_dir,
        file_name=f"{calendar_x._owner}.json",
        file_text=calendar_x.get_json(),
    )


def create_person_file_for_systems(system_dir: str, person_name: str):
    person_x = personunit_shop(name=person_name, env_dir=system_dir)
    person_dir = f"{system_dir}/persons/{person_x._admin._person_name}"
    # file_path = f"{person_dir}/{person_x.name}.json"
    # single_dir_create_if_null(person_dir)
    # with open(f"{file_path}", "w") as f:
    #     f.write(person_x.get_json())

    x_func_save_file(
        dest_dir=person_dir,
        file_name=f"{person_x._admin._person_name}.json",
        file_text=person_x.get_json(),
    )


def get_test_systems_dir():
    return "src/system/examples/systems"


def create_example_systems_list():
    return x_func_dir_files(
        dir_path=get_test_systems_dir(), include_dirs=True, include_files=False
    )


def setup_test_example_environment():
    _delete_and_set_ex3()
    _delete_and_set_ex4()
    _delete_and_set_ex5()
    _delete_and_set_ex6()


def _delete_and_set_ex3():
    system_name = "ex3"
    ex = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    x_func_delete_dir(ex.get_object_root_dir())
    ex.create_dirs_if_null(in_memory_bank=True)

    ex.save_calendarunit_obj_to_calendars_dir(
        calendar_x=example_persons_get_1node_calendar()
    )
    ex.save_calendarunit_obj_to_calendars_dir(
        calendar_x=example_calendars_get_calendar_1Task_1CE0MinutesRequired_1AcptFact()
    )
    ex.save_calendarunit_obj_to_calendars_dir(
        calendar_x=example_calendars_calendar_v001()
    )
    ex.save_calendarunit_obj_to_calendars_dir(
        calendar_x=example_calendars_calendar_v002()
    )

    # ex.set_person(person_x=personunit_shop(name="w1", env_dir=ex.get_object_root_dir()))
    # ex.set_person(person_x=personunit_shop(name="w2", env_dir=ex.get_object_root_dir()))
    w1_text = "w1"
    ex.create_new_personunit(person_name=w1_text)
    ex.create_depotlink_to_saved_calendar(
        person_name=w1_text, calendar_owner="Mycalendar", weight=3
    )
    # w1_obj = ex.get_person_obj_from_system(name=w1_text)

    bob_text = "bob wurld"
    create_calendar_file_for_systems(
        system_dir=ex.get_object_root_dir(), calendar_owner=bob_text
    )
    # print(f"create calendar_list {w1_text=}")
    ex.create_depotlink_to_generated_calendar(
        person_name=w1_text, calendar_owner=bob_text, depotlink_type="ignore"
    )
    land_text = "tim wurld"
    create_calendar_file_for_systems(
        system_dir=ex.get_object_root_dir(), calendar_owner=land_text
    )
    ex.create_depotlink_to_generated_calendar(
        person_name=w1_text, calendar_owner=land_text
    )
    # ex.create_depotlink_to_generated_calendar(person_name=w1_text, calendar_owner="test9")
    # ex.create_depotlink_to_generated_calendar(person_name=w1_text, calendar_owner="Bobs calendar")
    ex.save_person_file(person_name=w1_text)
    # print(f"WHAT WHAT {ex.get_object_root_dir()}")
    # print(f"WHAT WHAT {ex.get_object_root_dir()}/persons/w1/w1.json")
    # file_text = x_func_open_file(
    #     dest_dir=f"{ex.get_object_root_dir}/persons/w1", file_name="w1.json"
    # )
    # print(f"{file_text=}")
    # print(f"{len(ex._personunits.get(w1_text)._depotlinks)=}")
    # print(f"{ex._personunits.get(w1_text)._depotlinks.get(bob_text)=}")
    # print(f"{ex._personunits.get(w1_text).get_json=}")

    w2_text = "w2"
    ex.create_new_personunit(person_name=w2_text)  # , env_dir=ex.get_object_root_dir())
    ex.save_person_file(person_name=w2_text)


def _delete_and_set_ex4():
    system_name = "ex4"
    ex = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    x_func_delete_dir(ex.get_object_root_dir())
    ex.create_dirs_if_null(in_memory_bank=True)
    ex.save_calendarunit_obj_to_calendars_dir(
        example_persons_get_7nodeJRootWithH_calendar()
    )
    ex.save_calendarunit_obj_to_calendars_dir(
        example_calendars_get_calendar_with7amCleanTableRequired()
    )
    ex.save_calendarunit_obj_to_calendars_dir(
        example_calendars_get_calendar_base_time_example()
    )
    ex.save_calendarunit_obj_to_calendars_dir(
        example_calendars_get_calendar_x1_3levels_1required_1acptfacts()
    )


def _delete_and_set_ex5():
    system_name = "ex5"
    ex = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    x_func_delete_dir(ex.get_object_root_dir())
    ex.create_dirs_if_null(in_memory_bank=True)

    # ethical code ernie
    # ethical code steve
    # ethical code Jessica
    # ethical code Francine
    # ethical code Clay
    calendar_1 = example_persons_get_calendar_2CleanNodesRandomWeights(_owner="ernie")
    calendar_2 = example_persons_get_calendar_2CleanNodesRandomWeights(_owner="steve")
    calendar_3 = example_persons_get_calendar_2CleanNodesRandomWeights(_owner="jessica")
    calendar_4 = example_persons_get_calendar_2CleanNodesRandomWeights(
        _owner="francine"
    )
    calendar_5 = example_persons_get_calendar_2CleanNodesRandomWeights(_owner="clay")

    ex.save_calendarunit_obj_to_calendars_dir(calendar_x=calendar_1)
    ex.save_calendarunit_obj_to_calendars_dir(calendar_x=calendar_2)
    ex.save_calendarunit_obj_to_calendars_dir(calendar_x=calendar_3)
    ex.save_calendarunit_obj_to_calendars_dir(calendar_x=calendar_4)
    ex.save_calendarunit_obj_to_calendars_dir(calendar_x=calendar_5)

    ex.create_new_personunit(person_name=calendar_1._owner)
    ex.create_new_personunit(person_name=calendar_2._owner)
    ex.create_new_personunit(person_name=calendar_3._owner)
    ex.create_new_personunit(person_name=calendar_4._owner)
    ex.create_new_personunit(person_name=calendar_5._owner)

    ex.create_depotlink_to_saved_calendar(
        calendar_1._owner, calendar_2._owner, "blind_trust", 3
    )
    ex.create_depotlink_to_saved_calendar(
        calendar_1._owner, calendar_3._owner, "blind_trust", 7
    )
    ex.create_depotlink_to_saved_calendar(
        calendar_1._owner, calendar_4._owner, "blind_trust", 4
    )
    ex.create_depotlink_to_saved_calendar(
        calendar_1._owner, calendar_5._owner, "blind_trust", 5
    )

    ex.create_depotlink_to_saved_calendar(
        calendar_2._owner, calendar_1._owner, "blind_trust", 3
    )
    ex.create_depotlink_to_saved_calendar(
        calendar_2._owner, calendar_3._owner, "blind_trust", 7
    )
    ex.create_depotlink_to_saved_calendar(
        calendar_2._owner, calendar_4._owner, "blind_trust", 4
    )
    icx = example_persons_get_calendar_3CleanNodesRandomWeights()
    ex.create_depotlink_to_saved_calendar(
        calendar_2._owner, calendar_5._owner, "ignore", 5, icx
    )

    ex.create_depotlink_to_saved_calendar(
        calendar_3._owner, calendar_1._owner, "blind_trust", 3
    )
    ex.create_depotlink_to_saved_calendar(
        calendar_3._owner, calendar_2._owner, "blind_trust", 7
    )
    ex.create_depotlink_to_saved_calendar(
        calendar_3._owner, calendar_4._owner, "blind_trust", 4
    )
    ex.create_depotlink_to_saved_calendar(
        calendar_3._owner, calendar_5._owner, "blind_trust", 5
    )

    ex.create_depotlink_to_saved_calendar(
        calendar_4._owner, calendar_1._owner, "blind_trust", 3
    )
    ex.create_depotlink_to_saved_calendar(
        calendar_4._owner, calendar_2._owner, "blind_trust", 7
    )
    ex.create_depotlink_to_saved_calendar(
        calendar_4._owner, calendar_3._owner, "blind_trust", 4
    )
    ex.create_depotlink_to_saved_calendar(
        calendar_4._owner, calendar_5._owner, "blind_trust", 5
    )

    ex.create_depotlink_to_saved_calendar(
        calendar_5._owner, calendar_1._owner, "blind_trust", 3
    )
    ex.create_depotlink_to_saved_calendar(
        calendar_5._owner, calendar_2._owner, "blind_trust", 7
    )
    ex.create_depotlink_to_saved_calendar(
        calendar_5._owner, calendar_3._owner, "blind_trust", 4
    )
    ex.create_depotlink_to_saved_calendar(
        calendar_5._owner, calendar_4._owner, "blind_trust", 5
    )

    ex.save_person_file(person_name=calendar_1._owner)
    ex.save_person_file(person_name=calendar_2._owner)
    ex.save_person_file(person_name=calendar_3._owner)
    ex.save_person_file(person_name=calendar_4._owner)
    ex.save_person_file(person_name=calendar_5._owner)


def _delete_and_set_ex6():
    system_name = "ex6"
    ex = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    x_func_delete_dir(ex.get_object_root_dir())
    ex.create_dirs_if_null(in_memory_bank=False)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_calendar = CalendarUnit(_owner=sal_text)
    sal_calendar.add_memberunit(name=bob_text, creditor_weight=2)
    sal_calendar.add_memberunit(name=tom_text, creditor_weight=7)
    sal_calendar.add_memberunit(name=ava_text, creditor_weight=1)
    ex.save_calendarunit_obj_to_calendars_dir(calendar_x=sal_calendar)

    bob_calendar = CalendarUnit(_owner=bob_text)
    bob_calendar.add_memberunit(name=sal_text, creditor_weight=3)
    bob_calendar.add_memberunit(name=ava_text, creditor_weight=1)
    ex.save_calendarunit_obj_to_calendars_dir(calendar_x=bob_calendar)

    tom_calendar = CalendarUnit(_owner=tom_text)
    tom_calendar.add_memberunit(name=sal_text, creditor_weight=2)
    ex.save_calendarunit_obj_to_calendars_dir(calendar_x=tom_calendar)

    ava_calendar = CalendarUnit(_owner=ava_text)
    ava_calendar.add_memberunit(name=elu_text, creditor_weight=2)
    ex.save_calendarunit_obj_to_calendars_dir(calendar_x=ava_calendar)

    elu_calendar = CalendarUnit(_owner=elu_text)
    elu_calendar.add_memberunit(name=ava_text, creditor_weight=19)
    elu_calendar.add_memberunit(name=sal_text, creditor_weight=1)
    ex.save_calendarunit_obj_to_calendars_dir(calendar_x=elu_calendar)

    ex.refresh_bank_metrics()
    ex.set_river_sphere_for_calendar(calendar_name=sal_text, max_flows_count=100)


def create_example_system(system_name: str):
    ex = SystemUnit(name=system_name, systems_dir=get_test_systems_dir())
    ex.create_dirs_if_null(in_memory_bank=True)


def delete_dir_example_system(system_obj: SystemUnit):
    x_func_delete_dir(system_obj.get_object_root_dir())


def rename_example_system(system_obj: SystemUnit, new_name):
    # base_dir = system_obj.get_object_root_dir()
    base_dir = "src/system/examples/systems"
    src_dir = f"{base_dir}/{system_obj.name}"
    dst_dir = f"{base_dir}/{new_name}"
    os_rename(src=src_dir, dst=dst_dir)
    system_obj.set_systemunit_name(name=new_name)


class InvalidSystemCopyException(Exception):
    pass


def copy_evaluation_system(src_name: str, dest_name: str):
    base_dir = "src/system/examples/systems"
    new_dir = f"{base_dir}/{dest_name}"
    if os_path.exists(new_dir):
        raise InvalidSystemCopyException(
            f"Cannot copy system to '{new_dir}' directory because '{new_dir}' exists."
        )
    # base_dir = system_obj.get_object_root_dir()
    src_dir = f"{base_dir}/{src_name}"
    dest_dir = f"{base_dir}/{dest_name}"
    copy_dir(src_dir=src_dir, dest_dir=dest_dir)
