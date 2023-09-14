from src.system.person import personunit_shop
from src.system.examples.example_persons import (
    get_2node_calendar,
    get_calendar_2CleanNodesRandomWeights as get_cal2nodes,
    get_calendar_3CleanNodesRandomWeights as get_cal3nodes,
    get_calendar_assignment_laundry_example1 as get_america_assign_ex,
)
from src.system.examples.person_env_kit import (
    person_dir_setup_cleanup,
    get_temp_person_dir,
    create_calendar_file,
)
from src.system.examples.system_env_kit import get_temp_env_name
from src.system.system import SystemUnit
from os import path as os_path
from pytest import raises as pytest_raises
from src.calendar.calendar import CalendarUnit, get_from_json as calendar_get_from_json
from src.calendar.x_func import (
    count_files as x_func_count_files,
    open_file as x_func_open_file,
)


def test_personunit_set_depotlink_RaisesErrorWhenCalendarDoesNotExist(
    person_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    env_dir = get_temp_person_dir()
    sue_cx = personunit_shop(name=sue_text, env_dir=env_dir)
    sue_cx.set_isol_if_empty()
    tim_text = "Tim"
    assert list(sue_cx._isol._members.keys()) == [sue_text]

    # WHEN / THEN
    file_path_x = f"{sue_cx._admin._calendars_depot_dir}/{tim_text}.json"
    print(f"{file_path_x=}")
    with pytest_raises(Exception) as excinfo:
        sue_cx._set_depotlink(outer_owner=tim_text)
    assert (
        str(excinfo.value)
        == f"Person {sue_text} cannot find calendar {tim_text} in {file_path_x}"
    )


def test_personunit_set_depotlink_CorrectlySetsIsolMembers(person_dir_setup_cleanup):
    # GIVEN
    yao_text = "yao"
    env_dir = get_temp_person_dir()
    yao_px = personunit_shop(name=yao_text, env_dir=env_dir)
    yao_px.set_isol_if_empty()
    sue_text = "sue"
    create_calendar_file(yao_px._admin._calendars_depot_dir, sue_text)
    assert list(yao_px._isol._members.keys()) == [yao_text]

    # WHEN
    yao_px._set_depotlink(outer_owner=sue_text)

    # THEN
    assert list(yao_px._isol._members.keys()) == [yao_text, sue_text]
    assert yao_px._isol.get_member(sue_text).depotlink_type is None


def test_personunit_set_depotlink_CorrectlySetsAssignment(person_dir_setup_cleanup):
    # GIVEN
    america_cx = get_america_assign_ex()
    print(f"{len(america_cx._idea_dict)=}")
    joachim_text = "Joachim"
    joachim_px = personunit_shop(joachim_text, get_temp_person_dir())
    joachim_px.create_core_dir_and_files()
    joachim_px.set_isol_if_empty()
    joachim_px._admin.save_calendar_to_depot(america_cx)
    assert joachim_px.get_isol().get_member(america_cx._owner) is None
    america_digest_path = (
        f"{joachim_px._admin._calendars_digest_dir}/{america_cx._owner}.json"
    )
    assert os_path.exists(america_digest_path) is False

    # WHEN
    assignment_text = "assignment"
    joachim_px._set_depotlink(america_cx._owner, link_type=assignment_text)

    # THEN
    assert (
        joachim_px.get_isol().get_member(america_cx._owner).depotlink_type
        == assignment_text
    )
    assert os_path.exists(america_digest_path)
    digest_cx = calendar_get_from_json(
        x_func_open_file(
            dest_dir=joachim_px._admin._calendars_digest_dir,
            file_name=f"{america_cx._owner}.json",
        )
    )
    print(f"{digest_cx._owner=}")
    print(f"{len(digest_cx._idea_dict)=}")
    digest_cx.set_calendar_metrics()
    assert len(digest_cx._idea_dict) == 9
    assert digest_cx._owner == joachim_text


def test_personunit_del_depot_calendar_CorrectlyDeletesObj(person_dir_setup_cleanup):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_person_dir()
    bob_cx = personunit_shop(name=bob_text, env_dir=env_dir)
    yao_text = "Yao"
    create_calendar_file(bob_cx._admin._calendars_depot_dir, yao_text)
    assignment_text = "assignment"
    bob_cx._set_depotlinks_empty_if_null()
    bob_cx._set_depotlink(yao_text, link_type=assignment_text)
    assert list(bob_cx._isol._members.keys()) == [bob_text, yao_text]
    assert bob_cx._isol.get_member(yao_text).depotlink_type == assignment_text

    # WHEN
    bob_cx.del_depot_calendar(calendar_owner=yao_text)

    # THEN
    assert list(bob_cx._isol._members.keys()) == [bob_text, yao_text]
    assert bob_cx._isol.get_member(yao_text).depotlink_type is None


def test_personunit_del_depot_calendar_CorrectlyDeletesBlindTrustFile(
    person_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_person_dir()
    bob_cx = personunit_shop(name=bob_text, env_dir=env_dir)
    lai_text = "Lai"
    create_calendar_file(bob_cx._admin._calendars_depot_dir, lai_text)
    bob_cx.set_isol_if_empty()
    bob_cx._set_depotlink(lai_text, link_type="blind_trust")
    assert x_func_count_files(dir_path=bob_cx._admin._calendars_depot_dir) == 1
    assert x_func_count_files(dir_path=bob_cx._admin._calendars_digest_dir) == 1

    # WHEN
    bob_cx.del_depot_calendar(calendar_owner=lai_text)

    # THEN
    assert x_func_count_files(dir_path=bob_cx._admin._calendars_depot_dir) == 0
    assert x_func_count_files(dir_path=bob_cx._admin._calendars_digest_dir) == 0


def test_personunit_set_depot_calendar_SavesFileCorrectly(
    person_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_person_dir()
    bob_cx = personunit_shop(name=bob_text, env_dir=env_dir)
    cal1 = get_2node_calendar()
    assert (
        x_func_count_files(bob_cx._admin._calendars_depot_dir) is None
    )  # dir does not exist

    # WHEN
    bob_cx.set_isol_if_empty()
    bob_cx.set_depot_calendar(calendar_x=cal1, depotlink_type="blind_trust")

    # THEN
    print(f"Saving to {bob_cx._admin._calendars_depot_dir=}")
    # for path_x in os_scandir(px._admin._calendars_depot_dir):
    #     print(f"{path_x=}")
    assert x_func_count_files(bob_cx._admin._calendars_depot_dir) == 1


def test_personunit_delete_ignore_depotlink_CorrectlyDeletesObj(
    person_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_person_dir()
    bob_cx = personunit_shop(name=bob_text, env_dir=env_dir)
    yao_text = "Yao"
    create_calendar_file(bob_cx._admin._calendars_depot_dir, yao_text)
    assignment_text = "assignment"
    bob_cx.set_isol_if_empty()
    bob_cx._set_depotlink(yao_text, link_type=assignment_text)
    assert list(bob_cx._isol._members.keys()) == [bob_text, yao_text]
    assert bob_cx._isol.get_member(yao_text).depotlink_type == assignment_text

    # WHEN
    bob_cx.del_depot_calendar(calendar_owner=yao_text)

    # THEN
    assert list(bob_cx._isol._members.keys()) == [bob_text, yao_text]
    assert bob_cx._isol.get_member(yao_text).depotlink_type is None


def test_personunit_del_depot_calendar_CorrectlyDoesNotDeletesIgnoreFile(
    person_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "bob"
    env_dir = get_temp_person_dir()
    bob_cx = personunit_shop(name=bob_text, env_dir=env_dir)
    zia_text = "Zia"
    create_calendar_file(bob_cx._admin._calendars_depot_dir, zia_text)
    bob_cx.set_isol_if_empty()
    bob_cx._set_depotlink(zia_text, link_type="ignore")
    assert x_func_count_files(dir_path=bob_cx._admin._calendars_depot_dir) == 1
    assert x_func_count_files(dir_path=bob_cx._admin._calendars_digest_dir) == 1
    assert x_func_count_files(dir_path=bob_cx._admin._calendars_ignore_dir) == 1

    # WHEN
    bob_cx.del_depot_calendar(calendar_owner=zia_text)

    # THEN
    assert x_func_count_files(dir_path=bob_cx._admin._calendars_depot_dir) == 0
    assert x_func_count_files(dir_path=bob_cx._admin._calendars_digest_dir) == 0
    assert x_func_count_files(dir_path=bob_cx._admin._calendars_ignore_dir) == 1


def test_personunit_set_ignore_calendar_file_CorrectlyUpdatesIgnoreFile(
    person_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_person_dir()
    bob_px = personunit_shop(name=bob_text, env_dir=env_dir)
    zia_text = "Zia"
    create_calendar_file(bob_px._admin._calendars_depot_dir, zia_text)
    bob_px.set_isol_if_empty()
    bob_px._set_depotlink(zia_text, link_type="ignore")
    assert x_func_count_files(dir_path=bob_px._admin._calendars_ignore_dir) == 1
    cx1 = bob_px._admin.open_ignore_calendar(owner=zia_text)
    assert len(cx1._members) == 0
    cx1.add_memberunit(name="tim")
    assert len(cx1._members) == 1

    # WHEN
    zia_calendar = CalendarUnit(_owner=zia_text)
    bob_px.set_ignore_calendar_file(zia_calendar, src_calendar_owner=None)

    # THEN
    cx2 = bob_px._admin.open_ignore_calendar(owner=zia_text)
    assert len(cx2._members) == 0
    assert x_func_count_files(dir_path=bob_px._admin._calendars_ignore_dir) == 1


def test_personunit_refresh_depotlinks_CorrectlyPullsAllPublicCalendars(
    person_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_person_dir()
    system_name = get_temp_env_name()
    sx = SystemUnit(name=system_name, systems_dir=env_dir)
    sx.create_dirs_if_null()
    yao_text = "Yao"
    sx.create_new_personunit(person_name=yao_text)
    yao_calendar = sx.get_person_obj(name=yao_text)
    assert len(yao_calendar._admin.get_remelded_output_calendar().get_idea_list()) == 1

    ernie_text = "ernie"
    ernie_calendar = get_cal2nodes(_owner=ernie_text)
    steve_text = "steve"
    old_steve_calendar = get_cal2nodes(_owner=steve_text)
    sx.save_public_calendar(calendar_x=ernie_calendar)
    sx.save_public_calendar(calendar_x=old_steve_calendar)
    yao_calendar.set_depot_calendar(
        calendar_x=ernie_calendar, depotlink_type="blind_trust"
    )
    yao_calendar.set_depot_calendar(
        calendar_x=old_steve_calendar, depotlink_type="blind_trust"
    )

    assert len(yao_calendar._admin.get_remelded_output_calendar().get_idea_list()) == 4
    new_steve_calendar = get_cal3nodes(_owner=steve_text)
    sx.save_public_calendar(calendar_x=new_steve_calendar)
    print(f"{env_dir=} {yao_calendar._admin._calendars_public_dir=}")
    # for file_name in x_func_dir_files(dir_path=env_dir):
    #     print(f"{bob_cx._admin._calendars_public_dir=} {file_name=}")

    # for file_name in x_func_dir_files(dir_path=bob_cx._admin._calendars_public_dir):
    #     print(f"{bob_cx._admin._calendars_public_dir=} {file_name=}")

    # WHEN
    yao_calendar.refresh_depot_calendars()

    # THEN
    assert len(yao_calendar._admin.get_remelded_output_calendar().get_idea_list()) == 5
