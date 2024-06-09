from src.agenda.healer import healerhold_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.change.filehub import filehub_shop
from src.real.real import realunit_shop
from src.real.examples.real_env_kit import get_test_reals_dir, reals_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_RealUnit_generate_work_agenda_Sets_work_AgendaFile(reals_dir_setup_cleanup):
    # GIVEN
    music_text = "Music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), True)
    sue_text = "Sue"
    sue_filehub = filehub_shop(None, music_text, sue_text, None)
    x_sue_work_path = f"{music_real._persons_dir}/{sue_text}/work/{sue_text}.json"
    assert os_path_exists(x_sue_work_path) == False
    music_real.init_person_econs(sue_text)
    assert sue_filehub.work_path() == x_sue_work_path
    assert os_path_exists(x_sue_work_path)

    # WHEN
    sue_work = music_real.generate_work_agenda(sue_text)

    # THEN
    example_agenda = agendaunit_shop(sue_text, music_text)
    assert sue_work._real_id == example_agenda._real_id
    assert sue_work._owner_id == example_agenda._owner_id


def test_RealUnit_generate_work_agenda_ReturnsRegeneratedObj(reals_dir_setup_cleanup):
    # GIVEN
    music_real = realunit_shop("music", get_test_reals_dir(), True)
    sue_text = "Sue"
    music_real.init_person_econs(sue_text)
    sue_filehub = filehub_shop(music_real.reals_dir, music_real.real_id, sue_text, None)
    before_sue_agenda = sue_filehub.get_work_agenda()
    bob_text = "Bob"
    before_sue_agenda.add_partyunit(bob_text)
    sue_filehub.save_work_agenda(before_sue_agenda)
    assert sue_filehub.get_work_agenda().party_exists(bob_text)

    # WHEN
    after_sue_agenda = music_real.generate_work_agenda(sue_text)

    # THEN method should wipe over work agenda
    assert after_sue_agenda.party_exists(bob_text) == False


def test_RealUnit_generate_work_agenda_SetsCorrectFileWithout_healerhold(
    reals_dir_setup_cleanup,
):
    # GIVEN
    music_real = realunit_shop("music", get_test_reals_dir(), True)
    bob_text = "Bob"
    music_real.init_person_econs(bob_text)
    bob_filehub = filehub_shop(music_real.reals_dir, music_real.real_id, bob_text, None)
    before_bob_work_agenda = music_real.generate_work_agenda(bob_text)
    sue_text = "Sue"
    assert before_bob_work_agenda.party_exists(sue_text) == False

    # WHEN
    bob_duty_agenda = bob_filehub.get_duty_agenda()
    bob_duty_agenda.add_partyunit(sue_text)
    bob_filehub.save_duty_agenda(bob_duty_agenda)

    # WHEN
    after_bob_work_agenda = music_real.generate_work_agenda(bob_text)

    # THEN
    assert after_bob_work_agenda.party_exists(sue_text)


def test_RealUnit_generate_work_agenda_SetsFileWith_healerhold(reals_dir_setup_cleanup):
    # GIVEN
    music_real = realunit_shop("music", get_test_reals_dir(), True)

    bob_text = "Bob"
    music_real.init_person_econs(bob_text)
    bob_filehub = filehub_shop(music_real.reals_dir, music_real.real_id, bob_text, None)
    after_bob_work_agenda = music_real.generate_work_agenda(bob_text)
    assert after_bob_work_agenda.party_exists(bob_text) == False

    # WHEN
    bob_duty_agenda = bob_filehub.get_duty_agenda()
    bob_duty_agenda.add_partyunit(bob_text)
    bob_duty_agenda.set_party_pool(100)
    texas_text = "Texas"
    texas_road = bob_duty_agenda.make_l1_road(texas_text)
    elpaso_text = "el paso"
    elpaso_road = bob_duty_agenda.make_road(texas_road, elpaso_text)
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({bob_text}))
    bob_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    bob_duty_agenda.add_idea(elpaso_idea, texas_road)
    bob_filehub.save_duty_agenda(bob_duty_agenda)
    after_bob_work_agenda = music_real.generate_work_agenda(bob_text)

    # THEN
    assert after_bob_work_agenda.party_exists(bob_text)


def test_RealUnit_generate_all_work_agendas_SetsCorrectFiles(
    reals_dir_setup_cleanup,
):
    # GIVEN
    music_real = realunit_shop("music", get_test_reals_dir(), True)

    bob_text = "Bob"
    sue_text = "Sue"
    music_real.init_person_econs(bob_text)
    reals_dir = music_real.reals_dir
    bob_filehub = filehub_shop(reals_dir, music_real.real_id, bob_text, None)
    music_real.init_person_econs(sue_text)
    sue_filehub = filehub_shop(reals_dir, music_real.real_id, sue_text, None)
    bob_duty_agenda = music_real.generate_work_agenda(bob_text)
    sue_duty_agenda = music_real.generate_work_agenda(sue_text)

    texas_text = "Texas"
    texas_road = bob_duty_agenda.make_l1_road(texas_text)
    elpaso_text = "el paso"
    elpaso_road = bob_duty_agenda.make_road(texas_road, elpaso_text)
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({bob_text}))

    bob_duty_agenda = bob_filehub.get_duty_agenda()
    bob_duty_agenda.add_partyunit(bob_text)
    bob_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    bob_duty_agenda.add_idea(elpaso_idea, texas_road)
    bob_filehub.save_duty_agenda(bob_duty_agenda)

    sue_duty_agenda = sue_filehub.get_duty_agenda()
    sue_duty_agenda.add_partyunit(sue_text)
    sue_duty_agenda.add_partyunit(bob_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    sue_duty_agenda.add_idea(elpaso_idea, texas_road)
    sue_filehub.save_duty_agenda(sue_duty_agenda)

    before_bob_work_agenda = music_real.get_work_file_agenda(bob_text)
    before_sue_work_agenda = music_real.get_work_file_agenda(sue_text)
    assert before_bob_work_agenda.party_exists(bob_text) == False
    assert before_sue_work_agenda.party_exists(sue_text) == False

    # WHEN
    music_real.generate_all_work_agendas()

    # THEN
    after_bob_work_agenda = music_real.get_work_file_agenda(bob_text)
    after_sue_work_agenda = music_real.get_work_file_agenda(sue_text)
    assert after_bob_work_agenda.party_exists(bob_text)
    assert after_sue_work_agenda.party_exists(sue_text)
