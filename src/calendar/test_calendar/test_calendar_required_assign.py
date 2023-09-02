from pytest import raises as pytest_raises
from src.calendar.examples.example_calendars import (
    get_calendar_with_4_levels as example_calendars_get_calendar_with_4_levels,
    get_calendar_irrational_example as example_calendars_get_calendar_irrational_example,
)
from src.calendar.idea import IdeaKid
from src.calendar.required_idea import sufffactunit_shop, RequiredUnit, RequiredHeir
from src.calendar.calendar import CalendarUnit
from src.calendar.x_func import from_list_get_active_status
