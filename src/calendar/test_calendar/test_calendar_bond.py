from src.calendar.calendar import (
    CalendarUnit,
    get_from_json as calendar_get_from_json,
    get_meld_of_calendar_files,
)
from src.calendar.examples.get_calendar_examples_dir import get_calendar_examples_dir
from src.calendar.idea import IdeaCore, IdeaKid
from src.calendar.road import Road
from src.calendar.required_idea import RequiredUnit
from src.calendar.member import memberlink_shop
from src.calendar.group import groupunit_shop, grouplink_shop
from src.calendar.road import get_global_root_label as root_label
from src.calendar.examples.example_calendars import (
    get_calendar_with_4_levels as example_calendars_get_calendar_with_4_levels,
    get_calendar_with_4_levels_and_2requireds as example_calendars_get_calendar_with_4_levels_and_2requireds,
    get_calendar_with7amCleanTableRequired as example_calendars_get_calendar_with7amCleanTableRequired,
    get_calendar_with_4_levels_and_2requireds_2acptfacts as example_calendars_get_calendar_with_4_levels_and_2requireds_2acptfacts,
    calendar_v001 as example_calendars_calendar_v001,
)
from src.calendar.x_func import (
    dir_files as x_func_dir_files,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
)
from src.system.examples.env_kit import (
    env_dir_setup_cleanup,
    get_temp_env_dir,
)
from pytest import raises as pytest_raises


def test_calendarunit_get_bond_status_ReturnsCorrectBool():
    # GIVEN
    jessi_text = "jessi"
    cx = CalendarUnit(_owner=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{jessi_text},{casa_text}")

    # WHEN\THEN no action idea exists
    cx.add_idea(idea_kid=IdeaKid(_label=casa_text), walk=jessi_text)
    assert cx.get_bond_status() == False

    # WHEN\THEN 1 action idea exists
    clean_cookery_text = "clean cookery"
    cx.add_idea(
        idea_kid=IdeaKid(_label=clean_cookery_text, promise=True), walk=casa_road
    )
    assert cx.get_bond_status()

    # WHEN\THEN 2 action idea exists
    clean_hallway_text = "clean hallway"
    cx.add_idea(
        idea_kid=IdeaKid(_label=clean_hallway_text, promise=True), walk=casa_road
    )
    assert cx.get_bond_status() == False

    # WHEN\THEN 1 action idea deleted (1 total)
    clean_hallway_road = Road(f"{jessi_text},{casa_text},{clean_hallway_text}")
    cx.del_idea_kid(road=clean_hallway_road)
    assert cx.get_bond_status()

    # WHEN\THEN 1 action idea deleted (0 total)
    clean_cookery_road = Road(f"{jessi_text},{casa_text},{clean_cookery_text}")
    cx.del_idea_kid(road=clean_cookery_road)
    assert cx.get_bond_status() == False

    # for idea_kid in cx._idearoot._kids.values():
    #     print(f"after {idea_kid._label=} {idea_kid.promise=}")


def test_calendarunit_get_bond_status_ReturnsCorrectBoolWhenOnlyActionIdeaGroupheirsMatchCalendarGroups():
    # GIVEN
    jessi_text = "jessi"
    cx = CalendarUnit(_owner=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{jessi_text},{casa_text}")
    cx.add_idea(idea_kid=IdeaKid(_label=casa_text), walk=jessi_text)
    clean_cookery_text = "clean cookery"
    clean_cookery_road = Road(f"{jessi_text},{casa_text},{clean_cookery_text}")
    cx.add_idea(
        idea_kid=IdeaKid(_label=clean_cookery_text, promise=True), walk=casa_road
    )
    tom_text = "tom"
    cx.add_memberunit(name=tom_text)
    assert cx.get_bond_status() == False

    # WHEN
    cx.edit_idea_attr(road=clean_cookery_road, grouplink=grouplink_shop(name=tom_text))
    # THEN
    assert cx.get_bond_status()

    # WHEN
    bob_text = "bob"
    cx.add_memberunit(name=bob_text)
    # THEN
    assert cx.get_bond_status() == False


def test_calendarunit_get_bond_status_ChecksActionIdeaGroupsheirsEqualCalendarGroupunits():
    # GIVEN
    jessi_text = "jessi"
    cx = CalendarUnit(_owner=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{jessi_text},{casa_text}")
    cx.add_idea(idea_kid=IdeaKid(_label=casa_text), walk=jessi_text)
    clean_cookery_text = "clean cookery"
    clean_cookery_road = Road(f"{jessi_text},{casa_text},{clean_cookery_text}")
    cx.add_idea(
        idea_kid=IdeaKid(_label=clean_cookery_text, promise=True), walk=casa_road
    )
    tom_text = "tom"
    cx.add_memberunit(name=tom_text)
    assert cx.get_bond_status() == False

    # WHEN
    cx.edit_idea_attr(road=clean_cookery_road, grouplink=grouplink_shop(name=tom_text))
    clean_cookery_idea = cx.get_idea_kid(road=clean_cookery_road)
    assert len(clean_cookery_idea._groupheirs) == 1
    # THEN
    assert cx.get_bond_status()

    # WHEN
    bob_text = "bob"
    cx.add_memberunit(name=bob_text)
    # THEN
    assert cx.get_bond_status() == False


def test_calendarunit_get_bond_status_ChecksActionIdeaGroupsheirsEqualCalendarGroupunits2():
    # GIVEN
    jessi_text = "jessi"
    cx = CalendarUnit(_owner=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{jessi_text},{casa_text}")
    cx.add_idea(idea_kid=IdeaKid(_label=casa_text), walk=jessi_text)
    clean_cookery_text = "clean cookery"
    clean_cookery_road = Road(f"{jessi_text},{casa_text},{clean_cookery_text}")
    cx.add_idea(
        idea_kid=IdeaKid(_label=clean_cookery_text, promise=True), walk=casa_road
    )
    assert cx.get_bond_status()

    tom_text = "tom"
    cx.add_memberunit(name=tom_text)
    bob_text = "bob"
    cx.add_memberunit(name=bob_text)
    home_occupants_text = "home occupants"
    home_occupants_groupunit = groupunit_shop(name=home_occupants_text)
    home_occupants_groupunit.set_memberlink(memberlink=memberlink_shop(name=tom_text))
    home_occupants_groupunit.set_memberlink(memberlink=memberlink_shop(name=bob_text))
    cx.set_groupunit(groupunit=home_occupants_groupunit)
    assert cx.get_bond_status() == False

    # WHEN
    cx.edit_idea_attr(
        road=clean_cookery_road, grouplink=grouplink_shop(name=home_occupants_text)
    )
    # THEN
    assert cx.get_bond_status()

    # WHEN
    yuri_text = "yuri"
    cx.add_memberunit(name=yuri_text)

    # THEN
    assert cx.get_bond_status() == False


def test_calendarunit_get_bond_status_ChecksOnlyNecessaryIdeasExist_MultipleScenario():
    # GIVEN
    jessi_text = "jessi"
    cx = CalendarUnit(_owner=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{root_label()},{casa_text}")
    cx.add_idea(idea_kid=IdeaKid(_label=casa_text), walk=jessi_text)
    clean_cookery_text = "clean cookery"
    clean_cookery_road = Road(f"{root_label()},{casa_text},{clean_cookery_text}")

    # WHEN/THEN
    cx.add_idea(
        idea_kid=IdeaKid(_label=clean_cookery_text, promise=True), walk=casa_road
    )
    assert cx.get_bond_status()

    # WHEN/THEN
    water_text = "water"
    water_road = Road(f"{root_label()},{water_text}")
    cx.add_idea(idea_kid=IdeaKid(_label=water_text), walk=jessi_text)
    assert cx.get_bond_status() == False

    rain_text = "rain"
    rain_road = Road(f"{root_label()},{water_text},{rain_text}")
    cx.add_idea(idea_kid=IdeaKid(_label=rain_text), walk=water_road)

    # WHEN/THEN
    cx.edit_idea_attr(
        road=clean_cookery_road, required_base=water_road, required_sufffact=rain_road
    )
    assert cx.get_bond_status()


def test_calendarunit_get_calendar_sprung_from_single_idea_ReturnsCorrectCalendarScenario1():
    # GIVEN
    jessi_text = "jessi"
    cx = CalendarUnit(_owner=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{root_label()},{casa_text}")
    cx.add_idea(
        idea_kid=IdeaKid(_label=casa_text, _begin=-1, _close=19), walk=root_label()
    )
    clean_cookery_text = "clean cookery"
    clean_cookery_road = Road(f"{root_label()},{casa_text},{clean_cookery_text}")
    cx.add_idea(
        idea_kid=IdeaKid(_label=clean_cookery_text, promise=True, _begin=2, _close=4),
        walk=casa_road,
    )
    water_text = "water"
    water_road = Road(f"{root_label()},{water_text}")
    cx.add_idea(idea_kid=IdeaKid(_label=water_text), walk=root_label())
    assert cx.get_bond_status() == False

    # WHEN
    bond_calendar = cx.get_calendar_sprung_from_single_idea(road=clean_cookery_road)

    # THEN
    # assert bond_calendar._label == clean_cookery_text
    print(f"{len(bond_calendar._idea_dict)=}")
    assert len(bond_calendar._idea_dict) == 3
    b_src_idea = bond_calendar.get_idea_kid(road=root_label())
    source_x_idea = cx.get_idea_kid(road=root_label())
    assert b_src_idea._uid == source_x_idea._uid
    assert b_src_idea._begin == source_x_idea._begin
    assert b_src_idea._close == source_x_idea._close
    assert b_src_idea != source_x_idea

    b_casa_idea = bond_calendar.get_idea_kid(road=casa_road)
    src_casa_idea = cx.get_idea_kid(road=casa_road)
    assert b_casa_idea._uid == src_casa_idea._uid
    assert b_casa_idea._begin == src_casa_idea._begin
    assert b_casa_idea._close == src_casa_idea._close
    assert b_casa_idea != src_casa_idea

    b_clean_cookery_idea = bond_calendar.get_idea_kid(road=clean_cookery_road)
    src_clean_cookery_idea = cx.get_idea_kid(road=clean_cookery_road)
    assert b_clean_cookery_idea._uid == src_clean_cookery_idea._uid
    assert b_clean_cookery_idea._begin == src_clean_cookery_idea._begin
    assert b_clean_cookery_idea._close == src_clean_cookery_idea._close
    assert b_clean_cookery_idea != src_clean_cookery_idea

    assert bond_calendar._idearoot._kids.get(water_text) is None

    # for byx in bond_calendar._idea_dict.values():
    #     cyx = cx.get_idea_kid(road=byx.get_road())
    #     assert byx._uid == cyx._uid
    #     print(f"{byx.get_road()=} {byx._begin=} {byx._close=}")
    #     print(f"{cyx.get_road()=} {cyx._begin=} {cyx._close=}")
    #     assert byx._begin == cyx._begin
    #     assert byx._close == cyx._close
    #     for yx4 in byx._kids.values():
    #         assert yx4._label == cyx._kids.get(yx4._label)._label
    #     for cx3 in cyx._kids.values():
    #         if cx3._label == water_text:
    #             print(f"checking src calendar idea kid_label='{cx3._label}'")
    #             assert byx._kids.get(cx3._label) is None
    #         else:
    #             assert cx3._label == byx._kids.get(cx3._label)._label
    #     # assert len(byx._kids) != len(cyx._kids)
    #     # assert byx._kids_total_weight != cyx._kids_total_weight
    #     # assert byx._kids != cyx._kids
    #     assert byx != cyx

    assert len(bond_calendar._idea_dict) == 3
    assert bond_calendar._idearoot._kids.get(water_text) is None


def test_calendarunit_export_all_bonds_ExportsFileOfBonds_2files(env_dir_setup_cleanup):
    # GIVEN
    cx = example_calendars_get_calendar_with_4_levels_and_2requireds_2acptfacts()
    cx_idea_list = cx.get_idea_list()
    action_count = sum(bool(yx.promise) for yx in cx_idea_list)
    assert action_count == 2
    with pytest_raises(Exception) as excinfo:
        x_func_dir_files(dir_path=get_temp_env_dir())

    sys_word_part1 = "sys"  # the built word might be find and replaced in the future.
    sys_word_part2 = "tem"  # the built word might be find and replaced in the future.
    assert (
        str(excinfo.value)
        == f"[WinError 3] The {sys_word_part1}{sys_word_part2} cannot find the path specified: '{get_temp_env_dir()}'"
    )

    # WHEN
    cx.export_all_bonds(dir=get_temp_env_dir())

    # THEN
    # for bond_file_x in x_func_dir_files(dir_path=get_temp_env_dir()).keys():
    #     print(f"files exported {bond_file_x=}")

    assert len(x_func_dir_files(dir_path=get_temp_env_dir())) == 2


# deactivated since it takes too long
# def test_calendarunit_export_all_bonds_ExportsFileOfBonds_69files(env_dir_setup_cleanup):
#     # GIVEN
#     cx = example_calendars_calendar_v001()
#     cx_idea_list = cx.get_idea_list()
#     action_count = 0
#     for yx in cx_idea_list:
#         if yx.promise:
#             action_count += 1
#     assert action_count == 69
#     # WHEN/THEN
#     with pytest_raises(Exception) as excinfo:
#         assert x_func_dir_files(dir_path=get_temp_env_dir())
#     assert (
#         str(excinfo.value)
#         == f"[WinError 3] Cannot find the path specified: '{get_temp_env_dir()}'"
#     )

#     # WHEN
#     cx.export_all_bonds(dir=get_temp_env_dir())

#     # THEN
#     for bond_file_x in x_func_dir_files(dir_path=get_temp_env_dir()).keys():
#         print(f"files exported {bond_file_x=}")

#     assert len(x_func_dir_files(dir_path=get_temp_env_dir())) == action_count


# def test_calendarunit_export_all_bonds_ReturnsDictOfBonds(env_dir_setup_cleanup):
#     # GIVEN
#     cx = example_calendars_get_calendar_with_4_levels_and_2requireds_2acptfacts()
#     cx_idea_list = cx.get_idea_list()
#     action_count = sum(bool(yx.promise) for yx in cx_idea_list)
#     assert action_count == 2

#     # WHEN
#     cx.export_all_bonds(dir=get_temp_env_dir())

#     # THEN
#     dir_files = x_func_dir_files(dir_path=get_temp_env_dir())
#     file_17_name = "17.json"
#     assert dir_files[file_17_name]
#     json_17 = x_func_open_file(dest_dir=get_temp_env_dir(), file_name=file_17_name)
#     bond_17 = calendar_get_from_json(lw_json=json_17)
#     assert bond_17.get_bond_status()

#     file_2_name = "2.json"
#     assert dir_files[file_2_name]
#     json_2 = x_func_open_file(dest_dir=get_temp_env_dir(), file_name=file_2_name)
#     bond_2 = calendar_get_from_json(lw_json=json_2)
#     assert bond_2.get_bond_status()


def test_calendarunit_get_meld_of_calendar_files_MeldsIntoSourceCalendar_Scenario1(
    env_dir_setup_cleanup,
):
    # GIVEN
    owner_text = "Nia"
    src_cx = CalendarUnit(_owner=owner_text, _weight=10)

    work = "work"
    idea_kid_work = IdeaKid(_weight=30, _label=work, promise=True)
    src_cx.add_idea(idea_kid=idea_kid_work, walk=f"{root_label()}")

    cat = "feed cat"
    idea_kid_feedcat = IdeaKid(_weight=20, _label=cat, promise=True)
    src_cx.add_idea(idea_kid=idea_kid_feedcat, walk=f"{root_label()}")

    src_cx.export_all_bonds(dir=get_temp_env_dir())

    # WHEN
    new_cx = get_meld_of_calendar_files(
        calendarunit=CalendarUnit(_owner=src_cx._owner, _weight=10),
        dir=get_temp_env_dir(),
    )

    # THEN
    assert src_cx._weight == new_cx._weight
    assert src_cx._idearoot._weight == new_cx._idearoot._weight
    cat_t = "feed cat"
    assert (
        src_cx._idearoot._kids.get(cat_t)._calendar_coin_onset
        == new_cx._idearoot._kids.get(cat_t)._calendar_coin_onset
    )
    assert src_cx._idearoot._kids.get(cat_t) == new_cx._idearoot._kids.get(cat_t)
    assert src_cx._idearoot._kids == new_cx._idearoot._kids
    assert src_cx._idearoot == new_cx._idearoot
    assert src_cx == new_cx


# def test_calendarunit_get_meld_of_calendar_files_MeldsIntoSourceCalendar_Scenario2(
#     env_dir_setup_cleanup,
# ):
#     # GIVEN
#     sourrcecx = CalendarUnit(_owner=owner_text, _weight=10)

#     work_text = "work"
#     work_road = f"{root_label()},{work_text}"

#     cat_text = "feed cat"
#     cat_idea = IdeaKid(_weight=20, _label=cat_text, promise=True)
#     sourrce_cx.add_idea(idea_kid=cat_idea, walk=work_road)

#     plant_text = "water plant"
#     plant_idea = IdeaKid(_weight=30, _label=plant_text, promise=True)
#     sourrce_cx.add_idea(idea_kid=plant_idea, walk=work_road)
#     sourrce_cx.export_all_bonds(dir=get_temp_env_dir())

#     # WHEN
#     new_cx = get_meld_of_calendar_files(
#         calendarunit=CalendarUnit(_owner=sourrce_cx._owner, _weight=0), dir=get_temp_env_dir()
#     )

#     # THEN
#     assert sourrce_cx._weight == new_cx._weight
#     assert sourrce_cx._idearoot._weight == new_cx._idearoot._weight
#     assert len(sourrce_cx._idearoot._kids) == 1
#     assert len(sourrce_cx._idearoot._kids) == len(new_cx._idearoot._kids)
#     sourrce_work_idea = sourrce_cx._idearoot._kids.get(work_text)
#     new_work_idea = new_cx._idearoot._kids.get(work_text)
#     sourrce_cat_idea = sourrce_work_idea._kids.get(cat_text)
#     new_cat_idea = new_work_idea._kids.get(cat_text)
#     print(f"{sourrce_cat_idea._calendar_importance=} {new_cat_idea._calendar_importance=}")
#     assert sourrce_cat_idea._weight == new_cat_idea._weight
#     assert sourrce_work_idea._kids.get(cat_text) == new_work_idea._kids.get(cat_text)

#     assert sourrce_cx._idearoot._kids.get(cat_text) == new_cx._idearoot._kids.get(cat_text)
#     assert sourrce_cx._idearoot._kids == new_cx._idearoot._kids
#     assert sourrce_cx._idearoot == new_cx._idearoot
#     assert sourrce_cx == new_cx


# - [ ] create test_calendarunit_get_bond_status_ReturnsFalseWhenNotOnlyActionIdeaAcptFactsExist
