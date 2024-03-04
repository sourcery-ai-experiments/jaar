from src._road.road import default_road_delimiter_if_none
from src.agenda.healer import healerhold_shop
from src.agenda.idea import ideaunit_shop
from src.world.world import WorldUnit, worldunit_shop
from src.world.examples.world_env_kit import (
    get_test_worlds_dir,
    worlds_dir_setup_cleanup,
)

from src.world.person import personunit_shop
from os import path as os_path
from pytest import raises as pytest_raises


def create_example_world1() -> WorldUnit:
    # GIVEN
    music_world = worldunit_shop("music", get_test_worlds_dir(), in_memory_journal=True)
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_person = music_world.add_personunit(yao_text)
    wei_person = music_world.add_personunit(wei_text)
    zia_person = music_world.add_personunit(zia_text)
    yao_gut_agenda = yao_person.get_gut_file_agenda()
    wei_gut_agenda = wei_person.get_gut_file_agenda()
    zia_gut_agenda = zia_person.get_gut_file_agenda()

    yao_gut_agenda.set_party_creditor_pool(100)
    wei_gut_agenda.set_party_creditor_pool(50)
    zia_gut_agenda.set_party_creditor_pool(50)
    yao_gut_agenda.set_party_debtor_pool(1000)
    wei_gut_agenda.set_party_debtor_pool(500)
    zia_gut_agenda.set_party_debtor_pool(500)

    yao_gut_agenda.add_partyunit(yao_text, 33, 600)
    yao_gut_agenda.add_partyunit(zia_text, 57, 300)
    yao_gut_agenda.add_partyunit(wei_text, 10, 100)
    wei_gut_agenda.add_partyunit(yao_text, 12, 100)
    wei_gut_agenda.add_partyunit(wei_text, 11, 150)
    wei_gut_agenda.add_partyunit(zia_text, 27, 250)
    zia_gut_agenda.add_partyunit(yao_text, 12, 100)
    zia_gut_agenda.add_partyunit(zia_text, 38, 400)
    texas_text = "Texas"
    texas_road = yao_gut_agenda.make_l1_road(texas_text)
    yao_gut_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    zia_gut_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    dallas_road = yao_gut_agenda.make_road(texas_road, dallas_text)
    dallas_healerhold = healerhold_shop({yao_text, zia_text})
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=dallas_healerhold)
    elpaso_text = "el paso"
    elpaso_road = yao_gut_agenda.make_road(texas_road, elpaso_text)
    elpaso_healerhold = healerhold_shop({yao_text})
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=elpaso_healerhold)

    yao_gut_agenda.add_idea(dallas_idea, texas_road)
    yao_gut_agenda.add_idea(elpaso_idea, texas_road)
    zia_gut_agenda.add_idea(dallas_idea, texas_road)
    zia_gut_agenda.add_idea(elpaso_idea, texas_road)
    # display_agenda(yao_gut_agenda.set_agenda_metrics(), mode="Econ").show()
    yao_person._save_gut_file(yao_gut_agenda)
    wei_person._save_gut_file(wei_gut_agenda)
    zia_person._save_gut_file(zia_gut_agenda)
    yao_person.create_person_econunits()
    zia_person.create_person_econunits()
    yao_dallas_econ = yao_person.get_econ(dallas_road)
    zia_dallas_econ = zia_person.get_econ(dallas_road)
    yao_dallas_econ.create_new_clerkunit(yao_text)
    yao_dallas_econ.create_new_clerkunit(zia_text)
    zia_dallas_econ.create_new_clerkunit(yao_text)
    zia_dallas_econ.create_new_clerkunit(zia_text)
    yao_dallas_yao_clerk = yao_dallas_econ.get_clerkunit(yao_text)
    yao_dallas_zia_clerk = yao_dallas_econ.get_clerkunit(zia_text)
    zia_dallas_yao_clerk = zia_dallas_econ.get_clerkunit(yao_text)
    zia_dallas_zia_clerk = zia_dallas_econ.get_clerkunit(zia_text)

    # WHEN
    music_world.set_all_econunits_contract(yao_text)
    music_world.set_all_econunits_contract(zia_text)

    return music_world
