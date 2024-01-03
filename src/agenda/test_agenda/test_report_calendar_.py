from datetime import datetime
from src.agenda.agenda import agendaunit_shop, get_from_json
from src.agenda.examples.agenda_env import agenda_env
from src.agenda.idea import IdeaUnit, ideaunit_shop
from src.agenda.required_idea import requiredunit_shop, SuffFactStatusFinder
from src.agenda.group import groupunit_shop, balancelink_shop
from src.agenda.party import partylink_shop
from src.agenda.required_assign import assigned_unit_shop
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels as example_agendas_get_agenda_with_4_levels,
    get_agenda_with_4_levels_and_2requireds as example_agendas_get_agenda_with_4_levels_and_2requireds,
    get_agenda_with7amCleanTableRequired as example_agendas_get_agenda_with7amCleanTableRequired,
    get_agenda_with_4_levels_and_2requireds_2acptfacts as example_agendas_get_agenda_with_4_levels_and_2requireds_2acptfacts,
    agenda_v001 as example_agendas_agenda_v001,
    agenda_v001_with_large_intent as example_agendas_agenda_v001_with_large_intent,
    agenda_v002 as example_agendas_agenda_v002,
)
from src.tools.file import open_file
from src.world.person import personunit_shop, painunit_shop
from pytest import raises as pytest_raises

# from src.agenda.reporting import CalendarRangeUnit

# def test_CalendarRangeUnit_exists():
#     # WHEN
#     x_calendarrangeunit = CalendarRangeUnit()

#     # THEN
#     assert x_calendarrangeunit.
#     assert x_calendarrangeunit.
#     assert x_calendarrangeunit.


# def test_worldunit_shop_ReturnsWorldUnit(worlds_dir_setup_cleanup):
#     # GIVEN
#     dallas_text = "dallas"

#     # WHEN
#     x_world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())

#     # THEN
#     assert x_world.mark == dallas_text
#     assert x_world.worlds_dir == get_test_worlds_dir()
#     assert x_world._personunits == {}
