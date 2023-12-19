from src.economy.examples.example_councils import (
    get_healer_2agenda as healer_examples_get_healer_2agenda,
)
from src.economy.examples.council_env_kit import (
    council_dir_setup_cleanup,
    get_temp_councilunit_dir,
    get_temp_economy_id,
)
from src.agenda.agenda import agendaunit_shop


def test_councilunit_set_depot_agenda_SetsCorrectInfo(council_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_councilunit_dir()
    x_council = healer_examples_get_healer_2agenda(env_dir, get_temp_economy_id())
    assert x_council._seed.get_partys_depotlink_count() == 2
    print(f"{x_council._seed._partys.keys()=}")

    # WHEN
    assignment_text = "assignment"
    zia_text = "Zia"
    x_council.set_depot_agenda(agendaunit_shop(_healer=zia_text), assignment_text)
    zoa_text = "Zoa"
    x_council.set_depot_agenda(agendaunit_shop(_healer=zoa_text), assignment_text)

    # THEN
    print(f"{x_council._seed._partys.keys()=}")
    assert x_council._seed.get_partys_depotlink_count() == 4
