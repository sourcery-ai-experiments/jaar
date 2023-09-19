import src.system.examples.example_actors as actor_examples
from src.system.examples.actor_env_kit import (
    actor_dir_setup_cleanup,
    get_temp_actor_dir,
)
from src.calendar.calendar import CalendarUnit


def test_actor_set_depot_calendar_SetsCorrectInfo(actor_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_actor_dir()
    actor_x = actor_examples.get_actor_2calendar(env_dir=env_dir)
    assert actor_x._isol.get_members_depotlink_count() == 2
    print(f"{actor_x._isol._members.keys()=}")

    # WHEN
    assignment_text = "assignment"
    zia_text = "Zia"
    actor_x.set_depot_calendar(CalendarUnit(_owner=zia_text), assignment_text)
    zoa_text = "Zoa"
    actor_x.set_depot_calendar(CalendarUnit(_owner=zoa_text), assignment_text)

    # THEN
    print(f"{actor_x._isol._members.keys()=}")
    assert actor_x._isol.get_members_depotlink_count() == 4
