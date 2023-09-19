import src.system.examples.example_authors as author_examples
from src.system.examples.author_env_kit import (
    author_dir_setup_cleanup,
    get_temp_author_dir,
)
from src.calendar.calendar import CalendarUnit


def test_author_set_depot_calendar_SetsCorrectInfo(author_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_author_dir()
    author_x = author_examples.get_author_2calendar(env_dir=env_dir)
    assert author_x._isol.get_members_depotlink_count() == 2
    print(f"{author_x._isol._members.keys()=}")

    # WHEN
    assignment_text = "assignment"
    zia_text = "Zia"
    author_x.set_depot_calendar(CalendarUnit(_owner=zia_text), assignment_text)
    zoa_text = "Zoa"
    author_x.set_depot_calendar(CalendarUnit(_owner=zoa_text), assignment_text)

    # THEN
    print(f"{author_x._isol._members.keys()=}")
    assert author_x._isol.get_members_depotlink_count() == 4
