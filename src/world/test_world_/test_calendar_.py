from src.world.world import WorldUnit, worldunit_shop
from src.world.examples.world_env_kit import (
    get_temp_world_dir,
    get_temp_economy_id,
    get_test_worlds_dir,
    worlds_dir_setup_cleanup,
)

from src.world.person import personunit_shop, painunit_shop
from pytest import raises as pytest_raises


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
