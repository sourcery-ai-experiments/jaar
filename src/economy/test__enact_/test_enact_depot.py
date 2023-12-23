from src.economy.examples.example_enacts import (
    get_healer_2agenda as healer_examples_get_healer_2agenda,
)
from src.economy.examples.enact_env_kit import (
    enact_dir_setup_cleanup,
    get_temp_enactunit_dir,
    get_temp_economy_id,
)
from src.agenda.agenda import agendaunit_shop


def test_enactunit_set_depot_agenda_SetsCorrectInfo(enact_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_enactunit_dir()
    x_enact = healer_examples_get_healer_2agenda(env_dir, get_temp_economy_id())
    assert x_enact._contract.get_partys_depotlink_count() == 2
    print(f"{x_enact._contract._partys.keys()=}")

    # WHEN
    assignment_text = "assignment"
    zia_text = "Zia"
    x_enact.set_depot_agenda(agendaunit_shop(_healer=zia_text), assignment_text)
    zoa_text = "Zoa"
    x_enact.set_depot_agenda(agendaunit_shop(_healer=zoa_text), assignment_text)

    # THEN
    print(f"{x_enact._contract._partys.keys()=}")
    assert x_enact._contract.get_partys_depotlink_count() == 4
