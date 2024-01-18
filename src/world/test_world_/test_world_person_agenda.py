from src.agenda.agenda import agendaunit_shop
from src.world.world import worldunit_shop
from src.world.examples.world_env_kit import (
    get_test_worlds_dir,
    worlds_dir_setup_cleanup,
)
from src.world.person import personunit_shop


def test_worldunit_get_priority_agenda_ReturnsCorrectObjWhenThereAreNoSourceAgendas(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    texas_world = worldunit_shop(mark="texas", worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"
    texas_world._set_person_in_memory(personunit_shop(pid=luca_text))

    # WHEN
    luca_agenda = texas_world.get_priority_agenda(luca_text)

    # THEN
    assert luca_agenda == agendaunit_shop(luca_text)


def test_worldunit_get_priority_agenda_ReturnsCorrectObjWhenThereIsOneSourceAgenda(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    texas_world = worldunit_shop(mark="texas", worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"
    water_text = "Clean water"
    dallas_text = "Dallas"
    texas_world.create_person_economy(luca_text, water_text, luca_text, dallas_text)

    # WHEN
    gen_luca_agenda = texas_world.get_priority_agenda(luca_text)

    # THEN
    static_luca_agenda = agendaunit_shop(luca_text)
    assert gen_luca_agenda._economy_id == static_luca_agenda._economy_id
    assert gen_luca_agenda.get_intent_dict() == static_luca_agenda.get_intent_dict()


def test_worldunit_get_priority_agenda_ReturnsCorrectObjWhenThereIsTwoSourceAgenda(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    texas_world = worldunit_shop(mark="texas", worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"
    water_text = "dirty water"
    dallas_text = "Dallas"
    texas_world.create_person_economy(luca_text, water_text, luca_text, dallas_text)
    air_text = "dirty air"
    gilo_text = "Gilo"
    south_text = "The South"
    texas_world.create_person_economy(luca_text, air_text, gilo_text, south_text)

    # WHEN
    # luca_personunit = texas_world.get_personunit_from_memory(luca_text)
    # for x_problemunit in luca_personunit._problems.values():
    #     for x_healerlink in x_problemunit._healerlinks.values():
    #         print(
    #             f"{x_problemunit.problem_id=} {x_healerlink.person_id=} {x_healerlink._economylinks.keys()=}"
    #         )
    # print(f"{texas_world._personunits.keys()=}")
    gen_luca_agenda = texas_world.get_priority_agenda(luca_text)

    # THEN
    static_luca_agenda = agendaunit_shop(luca_text)
    assert gen_luca_agenda._economy_id == static_luca_agenda._economy_id
    assert gen_luca_agenda.get_party(gilo_text) != None
