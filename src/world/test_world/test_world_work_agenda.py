from src.agenda.agenda import agendaunit_shop
from src.world.world import worldunit_shop
from src.world.examples.world_env_kit import (
    get_test_worlds_dir,
    worlds_dir_setup_cleanup,
)
from src.world.person import personunit_shop
from src.instrument.file import open_file
from os.path import exists as os_path_exists


def test_WorldUnit_get_work_agenda_ReturnsCorrectObjWhenThereAreNoSourceAgendas(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    texas_text = "Texas"
    texas_world = worldunit_shop(world_id=texas_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"
    x_luca_work_path = f"{texas_world._persons_dir}/{luca_text}/work.json"
    assert os_path_exists(x_luca_work_path) == False
    luca_person = texas_world.add_personunit(luca_text)
    assert luca_person._work_path == x_luca_work_path
    assert os_path_exists(x_luca_work_path)

    # WHEN
    luca_agenda = texas_world.get_work_agenda(luca_text)

    # THEN
    example_agenda = agendaunit_shop(luca_text, texas_text)
    example_agenda.set_agenda_metrics()
    assert luca_agenda._world_id == example_agenda._world_id
    assert luca_agenda == example_agenda


def test_WorldUnit_get_work_agenda_ReturnsCorrectObjWhenThereIsOneSourceAgenda(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    texas_world = worldunit_shop(world_id="texas", worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"
    luca_person = texas_world.add_personunit(luca_text)
    before_luca_agenda = luca_person.get_work_file_agenda()
    bob_text = "Bob"
    before_luca_agenda.add_partyunit(bob_text)
    luca_person._save_work_file(before_luca_agenda)
    assert luca_person.get_work_file_agenda().get_party(bob_text) != None

    # WHEN
    after_luca_agenda = texas_world.get_work_agenda(luca_text)

    # THEN method should wipe over work agenda
    assert after_luca_agenda.get_party(bob_text) is None


# TODO reopen this after econ creation from Agenda exists.
# def test_WorldUnit_get_work_agenda_ReturnsCorrectObjWhenThereIsTwoSourceAgenda(
#     worlds_dir_setup_cleanup,
# ):
#     # GIVEN
#     texas_world = worldunit_shop(world_id="texas", worlds_dir=get_test_worlds_dir())
#     luca_text = "Luca"
#     water_text = "dirty water"
#     dallas_text = "Dallas"
#     air_text = "dirty air"
#     gilo_text = "Gilo"
#     south_text = "The South"

#     # WHEN
#     # luca_personunit = texas_world.get_personunit_from_memory(luca_text)
#     # for x_problemunit in luca_personunit._problems.values():
#     # print(f"{texas_world._personunits.keys()=}")
#     gen_luca_agenda = texas_world.get_work_agenda(luca_text)

#     # THEN
#     static_luca_agenda = agendaunit_shop(luca_text)
#     assert gen_luca_agenda._world_id == static_luca_agenda._world_id
#     assert gen_luca_agenda.get_party(gilo_text) != None
