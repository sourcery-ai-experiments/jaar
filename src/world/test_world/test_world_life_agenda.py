from src.agenda.healer import healerhold_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.world.world import worldunit_shop
from src.world.examples.world_env_kit import (
    get_test_worlds_dir,
    worlds_dir_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_WorldUnit_generate_life_agenda_Sets_life_A.gendaFile(worlds_dir_setup_cleanup):
    # GIVEN
    music_text = "Music"
    music_world = worldunit_shop(music_text, get_test_worlds_dir(), True)
    luca_text = "Luca"
    x_luca_life_path = f"{music_world._persons_dir}/{luca_text}/life.json"
    assert os_path_exists(x_luca_life_path) == False
    luca_person = music_world.add_personunit(luca_text)
    assert luca_person._life_path == x_luca_life_path
    assert os_path_exists(x_luca_life_path)

    # WHEN
    luca_life = music_world.generate_life_agenda(luca_text)

    # THEN
    example_agenda = agendaunit_shop(luca_text, music_text)
    example_agenda.set_agenda_metrics()
    assert luca_life._world_id == example_agenda._world_id
    assert luca_life == example_agenda


def test_WorldUnit_generate_life_agenda_ReturnsRegeneratedObj(worlds_dir_setup_cleanup):
    # GIVEN
    music_world = worldunit_shop("music", get_test_worlds_dir(), True)
    luca_text = "Luca"
    luca_person = music_world.add_personunit(luca_text)
    before_luca_agenda = luca_person.get_life_file_agenda()
    bob_text = "Bob"
    before_luca_agenda.add_partyunit(bob_text)
    luca_person._save_life_file(before_luca_agenda)
    assert luca_person.get_life_file_agenda().get_party(bob_text) != None

    # WHEN
    after_luca_agenda = music_world.generate_life_agenda(luca_text)

    # THEN method should wipe over life agenda
    assert after_luca_agenda.get_party(bob_text) is None


def test_WorldUnit_generate_life_agenda_SetsCorrectFile(worlds_dir_setup_cleanup):
    # GIVEN
    music_world = worldunit_shop("music", get_test_worlds_dir(), True)

    bob_text = "Bob"
    bob_person = music_world.add_personunit(bob_text)
    after_bob_life_agenda = music_world.generate_life_agenda(bob_text)
    assert after_bob_life_agenda.get_party(bob_text) is None

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
    after_bob_life_agenda = music_world.generate_life_agenda(bob_text)

    # THEN
    assert after_bob_life_agenda.get_party(bob_text) != None


def test_WorldUnit_generate_all_life_agendas_SetsCorrectFiles(worlds_dir_setup_cleanup):
    # GIVEN
    music_world = worldunit_shop("music", get_test_worlds_dir(), True)

    bob_text = "Bob"
    sue_text = "Sue"
    bob_person = music_world.add_personunit(bob_text)
    sue_person = music_world.add_personunit(sue_text)
    bob_gut_agenda = music_world.generate_life_agenda(bob_text)
    sue_gut_agenda = music_world.generate_life_agenda(sue_text)

    texas_text = "Texas"
    texas_road = bob_gut_agenda.make_l1_road(texas_text)
    elpaso_text = "el paso"
    elpaso_road = bob_gut_agenda.make_road(texas_road, elpaso_text)
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({bob_text}))

    bob_gut_agenda = bob_person.get_gut_file_agenda()
    bob_gut_agenda.add_partyunit(bob_text)
    bob_gut_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    bob_gut_agenda.add_idea(elpaso_idea, texas_road)
    bob_person._save_gut_file(bob_gut_agenda)

    sue_gut_agenda = sue_person.get_gut_file_agenda()
    sue_gut_agenda.add_partyunit(sue_text)
    sue_gut_agenda.add_partyunit(bob_text)
    sue_gut_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    sue_gut_agenda.add_idea(elpaso_idea, texas_road)
    sue_person._save_gut_file(sue_gut_agenda)

    before_bob_life_agenda = music_world.get_life_file_agenda(bob_text)
    before_sue_life_agenda = music_world.get_life_file_agenda(sue_text)
    assert before_bob_life_agenda.get_party(bob_text) is None
    assert before_sue_life_agenda.get_party(sue_text) is None

    # WHEN
    music_world.generate_all_life_agendas()

    # THEN
    after_bob_life_agenda = music_world.get_life_file_agenda(bob_text)
    after_sue_life_agenda = music_world.get_life_file_agenda(sue_text)
    assert after_bob_life_agenda.get_party(bob_text) != None
    assert after_sue_life_agenda.get_party(sue_text) != None
