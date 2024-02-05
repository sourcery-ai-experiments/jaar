from src.agenda.agenda import agendaunit_shop
from src.x_econ.econ import econunit_shop
from src.x_econ.examples.econ_env_kit import (
    get_test_econs_dir,
    econs_dir_setup_cleanup,
)
from src.x_econ.person import personunit_shop


def test_EconUnit_get_econ_agenda_ReturnsCorrectObjWhenThereAreNoSourceAgendas(
    econs_dir_setup_cleanup,
):
    # GIVEN
    texas_econ = econunit_shop(mark="texas", econs_dir=get_test_econs_dir())
    luca_text = "Luca"
    texas_econ._set_person_in_memory(personunit_shop(person_id=luca_text))

    # WHEN
    luca_agenda = texas_econ.get_econ_agenda(luca_text)

    # THEN
    assert luca_agenda == agendaunit_shop(luca_text)


def test_EconUnit_get_econ_agenda_ReturnsCorrectObjWhenThereIsOneSourceAgenda(
    econs_dir_setup_cleanup,
):
    # GIVEN
    texas_econ = econunit_shop(mark="texas", econs_dir=get_test_econs_dir())
    luca_text = "Luca"
    water_text = "Clean water"
    dallas_text = "Dallas"
    texas_econ.create_person_market(luca_text, water_text, luca_text, dallas_text)

    # WHEN
    gen_luca_agenda = texas_econ.get_econ_agenda(luca_text)

    # THEN
    static_luca_agenda = agendaunit_shop(luca_text)
    assert gen_luca_agenda._market_id == static_luca_agenda._market_id
    assert gen_luca_agenda.get_intent_dict() == static_luca_agenda.get_intent_dict()


def test_EconUnit_get_econ_agenda_ReturnsCorrectObjWhenThereIsTwoSourceAgenda(
    econs_dir_setup_cleanup,
):
    # GIVEN
    texas_econ = econunit_shop(mark="texas", econs_dir=get_test_econs_dir())
    luca_text = "Luca"
    water_text = "dirty water"
    dallas_text = "Dallas"
    texas_econ.create_person_market(luca_text, water_text, luca_text, dallas_text)
    air_text = "dirty air"
    gilo_text = "Gilo"
    south_text = "The South"
    texas_econ.create_person_market(luca_text, air_text, gilo_text, south_text)

    # WHEN
    # luca_personunit = texas_econ.get_personunit_from_memory(luca_text)
    # for x_problemunit in luca_personunit._problems.values():
    #     for x_healerlink in x_problemunit._healerlinks.values():
    #         print(
    #             f"{x_problemunit.problem_id=} {x_healerlink.person_id=} {x_healerlink._marketlinks.keys()=}"
    #         )
    # print(f"{texas_econ._personunits.keys()=}")
    gen_luca_agenda = texas_econ.get_econ_agenda(luca_text)

    # THEN
    static_luca_agenda = agendaunit_shop(luca_text)
    assert gen_luca_agenda._market_id == static_luca_agenda._market_id
    assert gen_luca_agenda.get_party(gilo_text) != None
