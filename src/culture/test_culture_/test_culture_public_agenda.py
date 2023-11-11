from src.agenda.agenda import agendaunit_shop
from src.agenda.examples.example_agendas import (
    get_agenda_1Task_1CE0MinutesRequired_1AcptFact as example_agendas_get_agenda_1Task_1CE0MinutesRequired_1AcptFact,
)
from src.culture.culture import cultureunit_shop
from src.culture.examples.example_councils import (
    get_1node_agenda as example_healers_get_1node_agenda,
    get_1node_agenda as example_healers_get_7nodeJRootWithH_agenda,
)
from src.culture.examples.culture_env_kit import (
    get_temp_env_title,
    get_test_cultures_dir,
    env_dir_setup_cleanup,
)
from os import path as os_path
from pytest import raises as pytest_raises


def test_culture_set_agenda_CreatesAgendaFile(env_dir_setup_cleanup):
    # GIVEN
    x_title = get_temp_env_title()
    x_culture = cultureunit_shop(title=x_title, cultures_dir=get_test_cultures_dir())
    x_culture.create_dirs_if_null()
    y_agenda = example_healers_get_1node_agenda()
    y_path = f"{x_culture.get_public_dir()}/{y_agenda._healer}.json"
    assert os_path.exists(y_path) == False

    # WHEN
    x_culture.save_public_agenda(x_agenda=y_agenda)

    # THEN
    print(f"{y_path=}")
    assert os_path.exists(y_path)


def test_culture_get_agenda_currentlyGetsAgenda(env_dir_setup_cleanup):
    # GIVEN
    x_title = get_temp_env_title()
    x_culture = cultureunit_shop(title=x_title, cultures_dir=get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)
    y_agenda = example_healers_get_7nodeJRootWithH_agenda()
    x_culture.save_public_agenda(x_agenda=y_agenda)

    # WHEN / THEN
    assert x_culture.get_public_agenda(healer=y_agenda._healer) == y_agenda


def test_culture_change_public_agenda_healer_ChangesAgendaHandle(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_title = get_temp_env_title()
    x_culture = cultureunit_shop(x_title, get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)
    old_agenda_healer = "old1"
    y_agenda = agendaunit_shop(_healer=old_agenda_healer)
    old_y_agenda_path = f"{x_culture.get_public_dir()}/{old_agenda_healer}.json"
    x_culture.save_public_agenda(x_agenda=y_agenda)
    print(f"{old_y_agenda_path=}")

    # WHEN
    new_agenda_healer = "new1"
    new_y_agenda_path = f"{x_culture.get_public_dir()}/{new_agenda_healer}.json"
    assert os_path.exists(new_y_agenda_path) == False
    assert os_path.exists(old_y_agenda_path)
    x_culture.change_public_agenda_healer(
        old_healer=old_agenda_healer, new_healer=new_agenda_healer
    )

    # THEN
    assert os_path.exists(old_y_agenda_path) == False
    assert os_path.exists(new_y_agenda_path)


def test_culture_SetsIdeaRootLabel(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_title = get_temp_env_title()
    x_culture = cultureunit_shop(title=x_title, cultures_dir=get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)
    old_x_agenda = example_agendas_get_agenda_1Task_1CE0MinutesRequired_1AcptFact()
    assert old_x_agenda._idearoot._label == "A"

    # WHEN
    x_culture.save_public_agenda(old_x_agenda)

    # THEN
    new_x_agenda = x_culture.get_public_agenda(old_x_agenda._healer)
    assert new_x_agenda._idearoot._label == x_title
