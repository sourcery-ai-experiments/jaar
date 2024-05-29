from src._road.userdir import userdir_shop
from src.agenda.healer import healerhold_shop
from src.agenda.group import groupunit_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop, AgendaUnit
from src.real.admin_duty import save_duty_file, get_duty_file_agenda
from src.real.admin_work import (
    save_work_file,
    get_work_file_agenda,
    get_default_work_agenda,
)
from src.real.real import realunit_shop
from src.real.examples.real_env_kit import get_test_reals_dir, reals_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_get_default_work_agenda_ReturnsCorrectObj():
    # GIVEN
    sue_text = "Sue"
    blue_text = "blue"
    slash_text = "/"
    five_planck = 5
    sue_party_pool = 800
    casa_text = "casa"
    bob_text = "Bob"
    last_change_id = 7
    sue_max_tree_traverse = 9
    sue_agendaunit = agendaunit_shop(sue_text, blue_text, slash_text, five_planck)
    sue_agendaunit.set_last_change_id(last_change_id)
    sue_agendaunit.add_partyunit(bob_text, 3, 4)
    swim_text = "/swimmers"
    swim_groupunit = groupunit_shop(swim_text, _road_delimiter=slash_text)
    swim_groupunit.edit_partylink(bob_text)
    sue_agendaunit.set_groupunit(swim_groupunit)
    sue_agendaunit.set_party_pool(sue_party_pool)
    sue_agendaunit.add_l1_idea(ideaunit_shop(casa_text))
    sue_agendaunit.set_max_tree_traverse(sue_max_tree_traverse)

    # WHEN
    default_work_agenda = get_default_work_agenda(sue_agendaunit)

    # THEN
    default_work_agenda.calc_agenda_metrics()
    assert default_work_agenda._owner_id == sue_agendaunit._owner_id
    assert default_work_agenda._owner_id == sue_text
    assert default_work_agenda._real_id == sue_agendaunit._real_id
    assert default_work_agenda._real_id == blue_text
    assert default_work_agenda._road_delimiter == slash_text
    assert default_work_agenda._planck == five_planck
    assert default_work_agenda._party_creditor_pool is None
    assert default_work_agenda._party_debtor_pool is None
    assert default_work_agenda._max_tree_traverse == sue_max_tree_traverse
    assert len(default_work_agenda.get_partys_dict()) == 0
    assert len(default_work_agenda.get_groupunits_dict()) == 0
    assert len(default_work_agenda._idea_dict) == 1


def test_RealUnit_generate_work_agenda_Sets_work_AgendaFile(reals_dir_setup_cleanup):
    # GIVEN
    music_text = "Music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), True)
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, music_text, sue_text)
    x_sue_work_path = f"{music_real._persons_dir}/{sue_text}/work.json"
    assert os_path_exists(x_sue_work_path) == False
    music_real.init_person_econs(sue_text)
    assert sue_userdir._work_path == x_sue_work_path
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
    sue_userdir = userdir_shop(music_real.reals_dir, music_real.real_id, sue_text)
    before_sue_agenda = get_work_file_agenda(sue_userdir)
    bob_text = "Bob"
    before_sue_agenda.add_partyunit(bob_text)
    save_work_file(sue_userdir, before_sue_agenda)
    assert get_work_file_agenda(sue_userdir).get_party(bob_text) != None

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
    music_real.init_person_econs(bob_text)
    bob_userdir = userdir_shop(music_real.reals_dir, music_real.real_id, bob_text)
    before_bob_work_agenda = music_real.generate_work_agenda(bob_text)
    sue_text = "Sue"
    assert before_bob_work_agenda.get_party(sue_text) is None

    # WHEN
    bob_duty_agenda = get_duty_file_agenda(bob_userdir)
    bob_duty_agenda.add_partyunit(sue_text)
    save_duty_file(bob_userdir, bob_duty_agenda)

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
    music_real.init_person_econs(bob_text)
    bob_userdir = userdir_shop(music_real.reals_dir, music_real.real_id, bob_text)
    after_bob_work_agenda = music_real.generate_work_agenda(bob_text)
    assert after_bob_work_agenda.get_party(bob_text) is None

    # WHEN
    bob_duty_agenda = get_duty_file_agenda(bob_userdir)
    bob_duty_agenda.add_partyunit(bob_text)
    texas_text = "Texas"
    texas_road = bob_duty_agenda.make_l1_road(texas_text)
    elpaso_text = "el paso"
    elpaso_road = bob_duty_agenda.make_road(texas_road, elpaso_text)
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({bob_text}))
    bob_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    bob_duty_agenda.add_idea(elpaso_idea, texas_road)
    save_duty_file(bob_userdir, bob_duty_agenda)
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
    music_real.init_person_econs(bob_text)
    bob_userdir = userdir_shop(music_real.reals_dir, music_real.real_id, bob_text)
    music_real.init_person_econs(sue_text)
    sue_userdir = userdir_shop(music_real.reals_dir, music_real.real_id, sue_text)
    bob_duty_agenda = music_real.generate_work_agenda(bob_text)
    sue_duty_agenda = music_real.generate_work_agenda(sue_text)

    texas_text = "Texas"
    texas_road = bob_duty_agenda.make_l1_road(texas_text)
    elpaso_text = "el paso"
    elpaso_road = bob_duty_agenda.make_road(texas_road, elpaso_text)
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({bob_text}))

    bob_duty_agenda = get_duty_file_agenda(bob_userdir)
    bob_duty_agenda.add_partyunit(bob_text)
    bob_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    bob_duty_agenda.add_idea(elpaso_idea, texas_road)
    save_duty_file(bob_userdir, bob_duty_agenda)

    sue_duty_agenda = get_duty_file_agenda(sue_userdir)
    sue_duty_agenda.add_partyunit(sue_text)
    sue_duty_agenda.add_partyunit(bob_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    sue_duty_agenda.add_idea(elpaso_idea, texas_road)
    save_duty_file(sue_userdir, sue_duty_agenda)

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
