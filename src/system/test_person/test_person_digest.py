from src.system.person import personunit_shop
from src.calendar.calendar import (
    CalendarUnit,
    get_from_json as calendarunit_get_from_json,
)
from src.calendar.examples.example_calendars import (
    get_calendar_with_4_levels as example_calendars_get_calendar_with_4_levels,
)
import src.system.examples.example_persons as example_persons
from src.system.examples.person_env_kit import (
    person_dir_setup_cleanup,
    get_temp_person_dir,
)
from src.calendar.road import get_global_root_label as root_label
from src.calendar.origin import originunit_shop
from os import path as os_path, scandir as os_scandir
from src.calendar.x_func import (
    open_file as x_func_open_file,
    count_files as x_func_count_files,
)
from pytest import raises as pytest_raises


# def test_person_save_isol_calendar_CreateStartingCalendarFile(
#     person_dir_setup_cleanup,
# ):
#     # GIVEN
#     lai_name = "Lai"
#     env_dir = get_temp_person_dir()
#     lai_calendar = personunit_shop(name=lai_name, env_dir=env_dir)
#     lai_isol_file_name = lai_calendar._admin._isol_file_name
#     with pytest_raises(Exception) as excinfo:
#         x_func_open_file(lai_calendar._admin._person_dir, lai_isol_file_name)
#     assert (
#         str(excinfo.value)
#         == f"Could not load file {lai_calendar._admin._isol_file_path} (2, 'No such file or directory')"
#     )

#     # WHEN
#     lai_calendar._admin.save_isol_calendar(
#         calendar_x=example_calendars_get_calendar_with_4_levels()
#     )

#     # THEN
#     assert x_func_open_file(lai_calendar._admin._person_dir, lai_isol_file_name) != None


def test_personopen_isol_calendar_WhenStartingCalendarFileDoesNotExists(
    person_dir_setup_cleanup,
):
    # GIVEN
    p_name = "Game1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=p_name, env_dir=env_dir)

    # WHEN
    assert px._admin.open_isol_calendar() != None
    isol_calendar = px._admin.open_isol_calendar()

    # THEN
    x_calendar = CalendarUnit(_owner=p_name)
    x_calendar.set_calendar_metrics()
    # x_idearoot = IdeaRoot(_label=p_name, _walk="")
    # x_idearoot.set_grouplines_empty_if_null()
    # x_idearoot.set_kids_empty_if_null()
    # x_idearoot.set_grouplink_empty_if_null()
    # x_idearoot.set_groupheir_empty_if_null()
    # x_idearoot.set_requiredunits_empty_if_null()
    # x_idearoot.set_requiredheirs_empty_if_null()
    # x_idearoot._calendar_importance = 1
    # x_idearoot._level = 0
    # x_idearoot._ancestor_promise_count = 0
    # x_idearoot._descendant_promise_count = 0
    # x_idearoot._all_member_credit = True
    # x_idearoot._all_member_debt = True

    assert isol_calendar._idearoot == x_calendar._idearoot
    assert isol_calendar._idearoot._acptfactunits == {}
    assert isol_calendar._members == {}
    assert isol_calendar._groups == {}


def test_person_save_isol_calendar_IsolCalendarOwnerMustBePerson(
    person_dir_setup_cleanup,
):
    # GIVEN
    p_name = "Game1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=p_name, env_dir=env_dir)
    cx1 = example_calendars_get_calendar_with_4_levels()
    assert cx1._owner != p_name

    # WHEN
    px._admin.save_isol_calendar(calendar_x=cx1)

    # THEN
    assert px._admin.open_isol_calendar()._owner == px._admin._person_name


def test_person_open_isol_calendar_WhenStartingCalendarFileExists(
    person_dir_setup_cleanup,
):
    # GIVEN
    p_name = "Game1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=p_name, env_dir=env_dir)
    px._admin.save_isol_calendar(
        calendar_x=example_calendars_get_calendar_with_4_levels()
    )

    # WHEN
    assert px._admin.open_isol_calendar() != None
    isol_calendar = px._admin.open_isol_calendar()

    # THEN
    x_calendar = example_calendars_get_calendar_with_4_levels()
    x_calendar.set_owner(new_owner=p_name)
    x_calendar.set_calendar_metrics()

    assert isol_calendar._idearoot._kids == x_calendar._idearoot._kids
    assert isol_calendar._idearoot == x_calendar._idearoot
    assert isol_calendar._idearoot._acptfactunits == {}
    assert isol_calendar._members == {}
    assert isol_calendar._groups == {}
    assert isol_calendar._owner == px._admin._person_name


def test_person_erase_isol_calendar_file_DeletesFileCorrectly(
    person_dir_setup_cleanup,
):
    # GIVEN
    p_name = "Game1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=p_name, env_dir=env_dir)
    px._admin.save_isol_calendar(example_calendars_get_calendar_with_4_levels())
    file_name = px._admin._isol_file_name
    assert x_func_open_file(px._admin._person_dir, file_name) != None

    # WHEN
    px._admin.erase_isol_calendar_file()

    # THEN
    with pytest_raises(Exception) as excinfo:
        x_func_open_file(px._admin._person_dir, file_name)
    assert (
        str(excinfo.value)
        == f"Could not load file {px._admin._person_dir}/isol_calendar.json (2, 'No such file or directory')"
    )


def test_personunit_save_calendar_to_digest_SavesFileCorrectly(
    person_dir_setup_cleanup,
):
    # GIVEN
    person_name = "person1"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=person_name, env_dir=env_dir)
    px.create_core_dir_and_files()
    cx = example_persons.get_2node_calendar()
    src_calendar_owner = cx._owner
    assert x_func_count_files(px._admin._calendars_digest_dir) == 0

    # WHEN
    px._admin.save_calendar_to_digest(cx, src_calendar_owner=src_calendar_owner)

    # THEN
    cx_file_name = f"{cx._owner}.json"
    digest_file_path = f"{px._admin._calendars_digest_dir}/{cx_file_name}"
    print(f"Saving to {digest_file_path=}")
    assert os_path.exists(digest_file_path)
    # for path_x in os_scandir(px._admin._calendars_digest_dir):
    #     print(f"{path_x=}")
    assert x_func_count_files(px._admin._calendars_digest_dir) == 1
    digest_cx_json = x_func_open_file(
        dest_dir=px._admin._calendars_digest_dir,
        file_name=f"{src_calendar_owner}.json",
    )
    assert digest_cx_json == cx.get_json()


def test_presonunit__set_depotlink_CorrectlySets_blind_trust_DigestCalendar(
    person_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    env_dir = get_temp_person_dir()
    sue_cx = personunit_shop(name=sue_text, env_dir=env_dir)
    sue_cx.create_core_dir_and_files()
    cx = example_persons.get_2node_calendar()
    src_calendar_owner = cx._owner
    assert x_func_count_files(sue_cx._admin._calendars_digest_dir) == 0

    # WHEN
    sue_cx.set_depot_calendar(calendar_x=cx, depotlink_type="blind_trust")

    # THEN
    cx_file_name = f"{cx._owner}.json"
    digest_file_path = f"{sue_cx._admin._calendars_digest_dir}/{cx_file_name}"
    print(f"Saving to {digest_file_path=}")
    assert os_path.exists(digest_file_path)
    # for path_x in os_scandir(sue_cx._admin._calendars_digest_dir):
    #     print(f"{path_x=}")
    assert x_func_count_files(sue_cx._admin._calendars_digest_dir) == 1
    digest_cx_json = x_func_open_file(
        dest_dir=sue_cx._admin._calendars_digest_dir,
        file_name=f"{src_calendar_owner}.json",
    )
    assert digest_cx_json == cx.get_json()


def test_person_get_refreshed_output_calendar_withEmptyDigestDict(
    person_dir_setup_cleanup,
):
    # GIVEN
    person_name_x = "boots3"
    px = personunit_shop(name=person_name_x, env_dir=get_temp_person_dir())
    px.create_core_dir_and_files()
    sx_output_before = px.get_refreshed_output_calendar()
    assert str(type(sx_output_before)).find(".calendar.CalendarUnit'>")
    assert sx_output_before._owner == person_name_x
    assert sx_output_before._idearoot._label == root_label()
    # px.set_digested_calendar(calendar_x=CalendarUnit(_owner="digested1"))

    # WHEN
    sx_output_after = px.get_refreshed_output_calendar()

    # THEN
    person_calendar_x = CalendarUnit(_owner=person_name_x, _weight=0.0)
    person_calendar_x._idearoot._walk = ""
    person_calendar_x.set_calendar_metrics()

    assert str(type(sx_output_after)).find(".calendar.CalendarUnit'>")
    assert sx_output_after._weight == person_calendar_x._weight
    assert sx_output_after._idearoot._walk == person_calendar_x._idearoot._walk
    assert (
        sx_output_after._idearoot._acptfactunits
        == person_calendar_x._idearoot._acptfactunits
    )
    assert sx_output_after._idearoot == person_calendar_x._idearoot


def test_person_get_refreshed_output_calendar_with1DigestedCalendar(
    person_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    env_dir = get_temp_person_dir()
    px = personunit_shop(name=yao_text, env_dir=env_dir)
    px.create_core_dir_and_files()
    sx_output_old = px.get_refreshed_output_calendar()
    assert str(type(sx_output_old)).find(".calendar.CalendarUnit'>")
    assert sx_output_old._owner == yao_text
    assert sx_output_old._idearoot._label == root_label()
    input_calendar = example_persons.get_2node_calendar()
    input_calendar.meld(input_calendar)
    px.set_depot_calendar(calendar_x=input_calendar, depotlink_type="blind_trust")

    # WHEN
    sx_output_new = px.get_refreshed_output_calendar()

    # THEN
    assert str(type(sx_output_new)).find(".calendar.CalendarUnit'>")

    assert sx_output_new._weight == 0
    assert sx_output_new._weight != input_calendar._weight
    sx_idearoot = sx_output_new._idearoot
    input_idearoot = input_calendar._idearoot
    assert sx_idearoot._walk == input_idearoot._walk
    assert sx_idearoot._acptfactunits == input_idearoot._acptfactunits
    input_b_idea = input_idearoot._kids.get("B")
    sx_output_new_b_idea = sx_idearoot._kids.get("B")
    assert sx_output_new_b_idea._walk == input_b_idea._walk
    assert sx_output_new._idearoot._kids == input_calendar._idearoot._kids
    assert sx_idearoot._kids_total_weight == input_idearoot._kids_total_weight
    assert sx_idearoot == input_idearoot
    assert sx_output_new._owner != input_calendar._owner
    assert sx_output_new != input_calendar


# def test_person_set_digested_calendar_with2Groups(person_dir_setup_cleanup):
#     # GIVEN
#     env_dir = get_temp_person_dir()
#     px = personunit_shop(name="test8", env_dir=env_dir)
#     sx_output_old = px.get_refreshed_output_calendar()
#     assert str(type(sx_output_old)).find(".calendar.CalendarUnit'>")
#     assert sx_output_old._groups == {}
#     assert sx_output_old._members == {}
#     assert sx_output_old._acptfacts == {}

#     src1 = "test1"
#     src1_road = Road(f"{src1}")
#     s1 = CalendarUnit(_owner=src1)

#     ceci_text = "Ceci"
#     s1.set_memberunit(memberunit=MemberUnit(name=ceci_text))
#     swim_text = "swimmers"
#     swim_group = BraUnit(name=swim_text)
#     swim_group.set_memberlink(memberlink=memberlink_shop(name=ceci_text))
#     s1.set_groupunit(groupunit=swim_group)

#     yaya_text = "yaya"
#     yaya_road = Road(f"{src1},{yaya_text}")
#     s1.add_idea(idea_kid=IdeaKid(_label=yaya_text), walk=src1_road)
#     s1.set_acptfact(base=yaya_road, acptfact=yaya_road)

#     assert s1._groups.get(swim_text).name == swim_text
#     assert s1._members.get(ceci_text).name == ceci_text
#     assert s1._idearoot._label == src1
#     assert s1._acptfacts.get(yaya_road).base == yaya_road

#     # WHEN
#     px.set_single_digested_calendar(_calendar_owner="test1", digest_calendar_x=s1)
#     sx_output_new = px.get_refreshed_output_calendar()

#     # THEN
#     assert str(type(sx_output_new)).find(".calendar.CalendarUnit'>")
#     assert sx_output_new._acptfacts == s1._acptfacts
#     assert sx_output_new._members == s1._members
#     assert sx_output_new._groups == s1._groups
#     assert sx_output_new._weight == s1._weight
#     assert sx_output_new._weight == s1._weight
#     assert sx_output_new._idearoot._walk == s1._idearoot._walk
#     assert sx_output_new._idearoot._acptfactunits == s1._idearoot._acptfactunits
#     assert sx_output_new._idearoot._kids == s1._idearoot._kids
#     assert sx_output_new._idearoot._kids_total_weight == s1._idearoot._kids_total_weight
#     assert sx_output_new._idearoot == s1._idearoot
#     assert sx_output_new._label != s1._label
#     assert sx_output_new != s1


def test_person_isol_calendar_CorrectlysHasOriginLinksWithOwnerAsSource(
    person_dir_setup_cleanup,
):
    # GIVEN
    # personunit with isol_calendar and no other depot calendars
    yao_text = "Yao"
    isol_origin_weight = 1
    yao_originunit = originunit_shop()
    yao_originunit.set_originlink(name=yao_text, weight=isol_origin_weight)
    isol_calendar_x = example_persons.get_7nodeJRoot_calendar()
    isol_calendar_x.set_owner(yao_text)

    assert isol_calendar_x._idearoot._originunit == originunit_shop()
    assert isol_calendar_x._idearoot._originunit != yao_originunit

    px = personunit_shop(name=yao_text, env_dir=get_temp_person_dir())
    px.create_core_dir_and_files()
    px._admin.save_isol_calendar(calendar_x=isol_calendar_x)

    # WHEN
    output_calendar_x = px.get_refreshed_output_calendar()

    # THEN
    assert output_calendar_x._idearoot._originunit == originunit_shop()
    d_road = "J,A,C,D"
    d_idea = output_calendar_x.get_idea_kid(road=d_road)
    assert d_idea._originunit == yao_originunit

    print(f"{output_calendar_x._originunit=}")
    assert output_calendar_x._originunit == yao_originunit

    output_originlink = output_calendar_x._originunit._links.get(yao_text)
    assert output_originlink.name == yao_text
    assert output_originlink.weight == isol_origin_weight
