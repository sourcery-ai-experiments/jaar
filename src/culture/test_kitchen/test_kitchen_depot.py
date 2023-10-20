from src.culture.examples.example_kitchens import (
    get_healer_2agenda as healer_examples_get_healer_2agenda,
)
from src.culture.examples.kitchen_env_kit import (
    kitchen_dir_setup_cleanup,
    get_temp_kitchenunit_dir,
    get_temp_culture_handle,
)
from src.agenda.agenda import agendaunit_shop


def test_kitchenunit_set_depot_agenda_SetsCorrectInfo(kitchen_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_kitchenunit_dir()
    x_kitchen = healer_examples_get_healer_2agenda(env_dir, get_temp_culture_handle())
    assert x_kitchen._seed.get_partys_depotlink_count() == 2
    print(f"{x_kitchen._seed._partys.keys()=}")

    # WHEN
    assignment_text = "assignment"
    zia_text = "Zia"
    x_kitchen.set_depot_agenda(agendaunit_shop(_healer=zia_text), assignment_text)
    zoa_text = "Zoa"
    x_kitchen.set_depot_agenda(agendaunit_shop(_healer=zoa_text), assignment_text)

    # THEN
    print(f"{x_kitchen._seed._partys.keys()=}")
    assert x_kitchen._seed.get_partys_depotlink_count() == 4
