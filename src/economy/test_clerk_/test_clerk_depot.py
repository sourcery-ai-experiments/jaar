from src.economy.examples.example_clerks import (
    get_healer_2agenda as healer_examples_get_healer_2agenda,
)
from src.economy.examples.clerk_env_kit import (
    clerk_dir_setup_cleanup,
    get_temp_clerkunit_dir,
    get_temp_economy_id,
)
from src.agenda.agenda import agendaunit_shop


def test_clerkunit_set_depot_agenda_SetsCorrectInfo(clerk_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_clerkunit_dir()
    x_clerk = healer_examples_get_healer_2agenda(env_dir, get_temp_economy_id())
    assert x_clerk._contract.get_partys_depotlink_count() == 2
    print(f"{x_clerk._contract._partys.keys()=}")

    # WHEN
    assignment_text = "assignment"
    zia_text = "Zia"
    x_clerk.set_depot_agenda(agendaunit_shop(_healer=zia_text), assignment_text)
    zoa_text = "Zoa"
    x_clerk.set_depot_agenda(agendaunit_shop(_healer=zoa_text), assignment_text)

    # THEN
    print(f"{x_clerk._contract._partys.keys()=}")
    assert x_clerk._contract.get_partys_depotlink_count() == 4
