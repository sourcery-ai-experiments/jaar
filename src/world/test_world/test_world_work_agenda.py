from src.agenda.healer import healerhold_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.world.world import worldunit_shop
from src.world.examples.world_env_kit import (
    get_test_worlds_dir,
    worlds_dir_setup_cleanup,
)
from src.world.person import personunit_shop
from src.instrument.file import open_file
from os.path import exists as os_path_exists


def test_WorldUnit_generate_work_agenda_ReturnsCorrectObjWhenThereAreNoSourceAgendas(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    music_text = "Music"
    music_world = worldunit_shop(music_text, get_test_worlds_dir(), True)
    luca_text = "Luca"
    x_luca_work_path = f"{music_world._persons_dir}/{luca_text}/work.json"
    assert os_path_exists(x_luca_work_path) == False
    luca_person = music_world.add_personunit(luca_text)
    assert luca_person._work_path == x_luca_work_path
    assert os_path_exists(x_luca_work_path)

    # WHEN
    luca_work = music_world.generate_work_agenda(luca_text)

    # THEN
    example_agenda = agendaunit_shop(luca_text, music_text)
    example_agenda.set_agenda_metrics()
    assert luca_work._world_id == example_agenda._world_id
    assert luca_work == example_agenda


def test_WorldUnit_generate_work_agenda_ReturnsRegeneratedObj(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    music_world = worldunit_shop("music", get_test_worlds_dir(), True)
    luca_text = "Luca"
    luca_person = music_world.add_personunit(luca_text)
    before_luca_agenda = luca_person.get_work_file_agenda()
    bob_text = "Bob"
    before_luca_agenda.add_partyunit(bob_text)
    luca_person._save_work_file(before_luca_agenda)
    assert luca_person.get_work_file_agenda().get_party(bob_text) != None

    # WHEN
    after_luca_agenda = music_world.generate_work_agenda(luca_text)

    # THEN method should wipe over work agenda
    assert after_luca_agenda.get_party(bob_text) is None


def test_WorldUnit_generate_work_agenda_ReturnsCorrectObjWhenThereIsTwoSourceAgenda(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    music_world = worldunit_shop("music", get_test_worlds_dir(), True)

    bob_text = "Bob"
    bob_person = music_world.add_personunit(bob_text)
    assert music_world.generate_work_agenda(bob_text).get_party(bob_text) is None

    # WHEN
    bob_gut_agenda = bob_person.get_gut_file_agenda()
    bob_gut_agenda.add_partyunit(bob_text)
    texas_text = "Texas"
    texas_road = bob_gut_agenda.make_l1_road(texas_text)
    elpaso_text = "el paso"
    elpaso_road = bob_gut_agenda.make_road(texas_road, elpaso_text)
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({bob_text}))
    bob_gut_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    bob_gut_agenda.add_idea(elpaso_idea, texas_road)
    bob_person._save_gut_file(bob_gut_agenda)

    # THEN
    assert music_world.generate_work_agenda(bob_text).get_party(bob_text) != None

    # sue_text = "Sue"
    # sue_person = music_world.add_personunit(sue_text)
    # dallas_text = "dallas"
    # dallas_road = sue_gut_agenda.make_road(texas_road, dallas_text)
    # dallas_idea = ideaunit_shop(dallas_text, _healerhold=healerhold_shop({sue_text}))
    # sue_gut_agenda = sue_person.get_gut_file_agenda()
    # sue_gut_agenda.add_partyunit(sue_text)
    # sue_gut_agenda.add_partyunit(bob_text)
    # sue_gut_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    # sue_gut_agenda.add_idea(dallas_idea, texas_road)
    # sue_gut_agenda.add_idea(elpaso_idea, texas_road)
    # # sue_gut_agenda.set_agenda_metrics()
    # # display_agenda(sue_gut_agenda, mode="Econ").show()
    # sue_person._save_gut_file(sue_gut_agenda)
    # sue_person.create_person_econunits()
    # dallas_econ = sue_person.get_econ(dallas_road)
    # dallas_econ.create_new_clerkunit(sue_text)
    # dallas_sue_clerk = dallas_econ.get_clerkunit(sue_text)
    # assert dallas_sue_clerk.get_plan().get_party(bob_text) is None
    # # assert elpaso_sue_clerk.get_plan().get_party(bob_text) is None

    # # WHEN
    # sue_work_agenda = music_world.generate_work_agenda(sue_text)

    # # THEN
