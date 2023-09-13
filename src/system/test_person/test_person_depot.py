import src.system.examples.example_persons as person_examples
from src.system.examples.person_env_kit import (
    person_dir_setup_cleanup,
    get_temp_person_dir,
)
from src.calendar.calendar import CalendarUnit


def test_person_set_depot_calendar_SetsCorrectInfo(person_dir_setup_cleanup):
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
