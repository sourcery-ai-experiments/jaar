from src.agenda.healer import healerhold_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.real.nook import (
    nookunit_shop,
    _save_work_file as person_save_work_file,
    save_duty_file,
    get_duty_file_agenda,
    get_work_file_agenda,
)
from src.real.gift import init_gift_id
from src.real.real import realunit_shop
from src.real.examples.real_env_kit import get_test_reals_dir, reals_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_RealUnit_generate_work_agenda_Sets_work_AgendaFile(reals_dir_setup_cleanup):
    # GIVEN
    music_text = "Music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), True)
    sue_text = "Sue"
    x_sue_work_path = f"{music_real._persons_dir}/{sue_text}/work.json"
    assert os_path_exists(x_sue_work_path) == False
    sue_person = music_real.add_personunit(sue_text)
    assert sue_person._work_path == x_sue_work_path
    assert os_path_exists(x_sue_work_path)

    # WHEN
    sue_work = music_real.generate_work_agenda(sue_text)

    # THEN
    example_agenda = agendaunit_shop(sue_text, music_text)
    example_agenda._last_gift_id = init_gift_id()
    example_agenda.calc_agenda_metrics()
    assert sue_work._real_id == example_agenda._real_id
    assert sue_work._last_gift_id == example_agenda._last_gift_id
    assert sue_work == example_agenda


def test_RealUnit_generate_work_agenda_ReturnsRegeneratedObj(reals_dir_setup_cleanup):
    # GIVEN
    music_real = realunit_shop("music", get_test_reals_dir(), True)
    sue_text = "Sue"
    sue_person = music_real.add_personunit(sue_text)
    sue_nookunit = nookunit_shop(music_real.reals_dir, music_real.real_id, sue_text)
    before_sue_agenda = get_work_file_agenda(sue_nookunit)
    bob_text = "Bob"
    before_sue_agenda.add_partyunit(bob_text)
    person_save_work_file(sue_nookunit, before_sue_agenda)
    assert get_work_file_agenda(sue_nookunit).get_party(bob_text) != None

    # WHEN
    after_sue_agenda = music_real.generate_work_agenda(sue_text)

    # THEN method should wipe over work agenda
    assert after_sue_agenda.get_party(bob_text) is None


def test_RealUnit_generate_work_agenda_SetsCorrectFileWithout_healerhold(
    reals_dir_setup_cleanup,
):
    # GIVEN
    music_real = realunit_shop("music", get_test_reals_dir(), True)
    bob_text = "Bob"
    bob_person = music_real.add_personunit(bob_text)
    bob_nookunit = nookunit_shop(music_real.reals_dir, music_real.real_id, bob_text)
    before_bob_work_agenda = music_real.generate_work_agenda(bob_text)
    sue_text = "Sue"
    assert before_bob_work_agenda.get_party(sue_text) is None

    # WHEN
    bob_duty_agenda = get_duty_file_agenda(bob_nookunit)
    bob_duty_agenda.add_partyunit(sue_text)
    save_duty_file(bob_nookunit, bob_duty_agenda)

    # WHEN
    after_bob_work_agenda = music_real.generate_work_agenda(bob_text)

    # THEN
    assert after_bob_work_agenda.get_party(sue_text) != None


def test_RealUnit_generate_work_agenda_SetsCorrectFileWith_healerhold(
    reals_dir_setup_cleanup,
):
    # GIVEN
    music_real = realunit_shop("music", get_test_reals_dir(), True)

    bob_text = "Bob"
    bob_person = music_real.add_personunit(bob_text)
    bob_nookunit = nookunit_shop(music_real.reals_dir, music_real.real_id, bob_text)
    after_bob_work_agenda = music_real.generate_work_agenda(bob_text)
    assert after_bob_work_agenda.get_party(bob_text) is None

    # WHEN
    bob_duty_agenda = get_duty_file_agenda(bob_nookunit)
    bob_duty_agenda.add_partyunit(bob_text)
    texas_text = "Texas"
    texas_road = bob_duty_agenda.make_l1_road(texas_text)
    elpaso_text = "el paso"
    elpaso_road = bob_duty_agenda.make_road(texas_road, elpaso_text)
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({bob_text}))
    bob_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    bob_duty_agenda.add_idea(elpaso_idea, texas_road)
    save_duty_file(bob_nookunit, bob_duty_agenda)
    after_bob_work_agenda = music_real.generate_work_agenda(bob_text)

    # THEN
    assert after_bob_work_agenda.get_party(bob_text) != None


def test_RealUnit_generate_all_work_agendas_SetsCorrectFiles(
    reals_dir_setup_cleanup,
):
    # GIVEN
    music_real = realunit_shop("music", get_test_reals_dir(), True)

    bob_text = "Bob"
    sue_text = "Sue"
    bob_person = music_real.add_personunit(bob_text)
    bob_nookunit = nookunit_shop(music_real.reals_dir, music_real.real_id, bob_text)
    sue_person = music_real.add_personunit(sue_text)
    sue_nookunit = nookunit_shop(music_real.reals_dir, music_real.real_id, sue_text)
    bob_duty_agenda = music_real.generate_work_agenda(bob_text)
    sue_duty_agenda = music_real.generate_work_agenda(sue_text)

    texas_text = "Texas"
    texas_road = bob_duty_agenda.make_l1_road(texas_text)
    elpaso_text = "el paso"
    elpaso_road = bob_duty_agenda.make_road(texas_road, elpaso_text)
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({bob_text}))

    bob_duty_agenda = get_duty_file_agenda(bob_nookunit)
    bob_duty_agenda.add_partyunit(bob_text)
    bob_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    bob_duty_agenda.add_idea(elpaso_idea, texas_road)
    save_duty_file(bob_nookunit, bob_duty_agenda)

    sue_duty_agenda = get_duty_file_agenda(sue_nookunit)
    sue_duty_agenda.add_partyunit(sue_text)
    sue_duty_agenda.add_partyunit(bob_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    sue_duty_agenda.add_idea(elpaso_idea, texas_road)
    save_duty_file(sue_nookunit, sue_duty_agenda)

    before_bob_work_agenda = music_real.get_work_file_agenda(bob_text)
    before_sue_work_agenda = music_real.get_work_file_agenda(sue_text)
    assert before_bob_work_agenda.get_party(bob_text) is None
    assert before_sue_work_agenda.get_party(sue_text) is None

    # WHEN
    music_real.generate_all_work_agendas()

    # THEN
    after_bob_work_agenda = music_real.get_work_file_agenda(bob_text)
    after_sue_work_agenda = music_real.get_work_file_agenda(sue_text)
    assert after_bob_work_agenda.get_party(bob_text) != None
    assert after_sue_work_agenda.get_party(sue_text) != None
