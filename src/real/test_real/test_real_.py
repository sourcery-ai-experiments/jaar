from src._road.finance import default_planck_if_none
from src._road.road import default_road_delimiter_if_none
from src.agenda.healer import healerhold_shop
from src.agenda.idea import ideaunit_shop
from src.econ.job_creator import get_owner_file_name
from src.real.nook import nookunit_shop, save_duty_file, get_duty_file_agenda
from src.real.gift import get_gifts_folder
from src.real.duty_creator import create_person_econunits, get_econunit
from src.real.real import RealUnit, realunit_shop
from src.real.examples.real_env_kit import get_test_reals_dir, reals_dir_setup_cleanup
from os import path as os_path
from os.path import exists as os_path_exists


def test_RealUnit_exists(reals_dir_setup_cleanup):
    music_text = "music"
    music_real = RealUnit(real_id=music_text, reals_dir=get_test_reals_dir())
    assert music_real.real_id == music_text
    assert music_real.reals_dir == get_test_reals_dir()
    assert music_real._persons_dir is None
    assert music_real._journal_db is None
    assert music_real._gifts_dir is None
    assert music_real._road_delimiter is None
    assert music_real._planck is None


def test_realunit_shop_ReturnsRealUnit(reals_dir_setup_cleanup):
    # GIVEN
    music_text = "music"

    # WHEN
    music_real = realunit_shop(
        real_id=music_text, reals_dir=get_test_reals_dir(), in_memory_journal=True
    )

    # THEN
    assert music_real.real_id == music_text
    assert music_real.reals_dir == get_test_reals_dir()
    assert music_real._persons_dir != None
    assert music_real._gifts_dir != None
    assert music_real._road_delimiter == default_road_delimiter_if_none()
    assert music_real._planck == default_planck_if_none()


def test_realunit_shop_ReturnsRealUnitWith_road_delimiter(reals_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    slash_text = "/"
    three_int = 3

    # WHEN
    music_real = realunit_shop(
        real_id=music_text,
        reals_dir=get_test_reals_dir(),
        in_memory_journal=True,
        _road_delimiter=slash_text,
        _planck=three_int,
    )

    # THEN
    assert music_real._road_delimiter == slash_text
    assert music_real._planck == three_int


def test_RealUnit__set_real_dirs_SetsEngineDir(reals_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    music_real = RealUnit(real_id=music_text, reals_dir=get_test_reals_dir())
    x_real_dir = f"{get_test_reals_dir()}/{music_text}"
    x_persons_dir = f"{x_real_dir}/persons"
    x_gifts_dir = f"{x_real_dir}/{get_gifts_folder()}"
    journal_file_name = "journal.db"
    journal_file_path = f"{x_real_dir}/{journal_file_name}"

    assert music_real._real_dir is None
    assert music_real._persons_dir is None
    assert music_real._gifts_dir is None
    assert os_path.exists(x_real_dir) is False
    assert os_path.isdir(x_real_dir) is False
    assert os_path.exists(x_persons_dir) is False
    assert os_path.exists(x_gifts_dir) is False
    assert os_path.exists(journal_file_path) is False

    # WHEN
    music_real._set_real_dirs()

    # THEN
    assert music_real._real_dir == x_real_dir
    assert music_real._persons_dir == x_persons_dir
    assert music_real._gifts_dir == x_gifts_dir
    assert os_path.exists(x_real_dir)
    assert os_path.isdir(x_real_dir)
    assert os_path.exists(x_persons_dir)
    assert os_path.exists(x_gifts_dir)
    assert os_path.exists(journal_file_path)


def test_realunit_shop_SetsRealsDirs(reals_dir_setup_cleanup):
    # GIVEN
    music_text = "music"

    # WHEN
    music_real = realunit_shop(music_text, get_test_reals_dir(), in_memory_journal=True)

    # THEN
    assert music_real.real_id == music_text
    assert music_real._real_dir == f"{get_test_reals_dir()}/{music_text}"
    assert music_real._persons_dir == f"{music_real._real_dir}/persons"


def test_RealUnit_init_person_econs_CorrectlySetsEngine(reals_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    slash_text = "/"
    x_planck = 5
    music_real = realunit_shop(
        music_text,
        get_test_reals_dir(),
        _road_delimiter=slash_text,
        _planck=x_planck,
        in_memory_journal=True,
    )
    luca_text = "Luca"
    luca_nookunit = nookunit_shop(None, music_text, luca_text, planck=x_planck)
    assert os_path_exists(luca_nookunit._work_path) == False

    # WHEN
    music_real.init_person_econs(luca_text)

    # THEN
    print(f"{get_test_reals_dir()=}")
    assert os_path_exists(luca_nookunit._work_path)


def test_RealUnit_get_person_duty_from_file_ReturnsCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), in_memory_journal=True)
    luca_text = "Luca"
    music_real.init_person_econs(luca_text)
    luca_nookunit = nookunit_shop(None, music_text, luca_text)
    bob_text = "Bob"
    luca_duty = get_duty_file_agenda(luca_nookunit)
    luca_duty.add_partyunit(bob_text)
    save_duty_file(luca_nookunit, luca_duty)

    # WHEN
    gen_luca_duty = music_real.get_person_duty_from_file(luca_text)

    # THEN
    assert gen_luca_duty != None
    assert gen_luca_duty.get_party(bob_text) != None


def test_RealUnit_set_person_econunits_dirs_CorrectlySetsroles(
    reals_dir_setup_cleanup,
):
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), in_memory_journal=True)
    luca_text = "Luca"
    todd_text = "Todd"
    music_real.init_person_econs(luca_text)
    music_real.init_person_econs(todd_text)
    luca_nookunit = nookunit_shop(None, music_text, luca_text)
    todd_nookunit = nookunit_shop(None, music_text, todd_text)
    luca_duty_agenda = get_duty_file_agenda(luca_nookunit)
    todd_duty_agenda = get_duty_file_agenda(todd_nookunit)

    luca_duty_agenda.add_partyunit(luca_text)
    luca_duty_agenda.add_partyunit(todd_text)
    todd_duty_agenda.add_partyunit(luca_text)
    todd_duty_agenda.add_partyunit(todd_text)
    texas_text = "Texas"
    texas_road = luca_duty_agenda.make_l1_road(texas_text)
    luca_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    todd_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    dallas_road = luca_duty_agenda.make_road(texas_road, dallas_text)
    dallas_healerhold = healerhold_shop({luca_text, todd_text})
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=dallas_healerhold)
    elpaso_text = "el paso"
    elpaso_road = luca_duty_agenda.make_road(texas_road, elpaso_text)
    elpaso_healerhold = healerhold_shop({luca_text})
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=elpaso_healerhold)

    luca_duty_agenda.add_idea(dallas_idea, texas_road)
    luca_duty_agenda.add_idea(elpaso_idea, texas_road)
    todd_duty_agenda.add_idea(dallas_idea, texas_road)
    todd_duty_agenda.add_idea(elpaso_idea, texas_road)
    # display_ideatree(luca_duty_agenda.calc_agenda_metrics(), mode="Econ").show()
    save_duty_file(luca_nookunit, luca_duty_agenda)
    save_duty_file(todd_nookunit, todd_duty_agenda)
    create_person_econunits(luca_nookunit)
    create_person_econunits(todd_nookunit)
    luca_dallas_econ = get_econunit(luca_nookunit, dallas_road)
    todd_dallas_econ = get_econunit(todd_nookunit, dallas_road)
    luca_file_name = get_owner_file_name(luca_text)
    todd_file_name = get_owner_file_name(todd_text)
    luca_roles_dir = luca_dallas_econ.get_roles_dir()
    todd_roles_dir = todd_dallas_econ.get_roles_dir()
    luca_dallas_luca_role_file_path = f"{luca_roles_dir}/{luca_file_name}"
    luca_dallas_todd_role_file_path = f"{luca_roles_dir}/{todd_file_name}"
    todd_dallas_luca_role_file_path = f"{todd_roles_dir}/{luca_file_name}"
    todd_dallas_todd_role_file_path = f"{todd_roles_dir}/{todd_file_name}"
    assert os_path_exists(luca_dallas_luca_role_file_path) == False
    assert os_path_exists(luca_dallas_todd_role_file_path) == False
    assert os_path_exists(todd_dallas_luca_role_file_path) == False
    assert os_path_exists(todd_dallas_todd_role_file_path) == False

    # WHEN
    music_real.set_person_econunits_dirs(luca_text)

    # THEN
    assert os_path_exists(luca_dallas_luca_role_file_path)
    assert os_path_exists(luca_dallas_todd_role_file_path) == False
    assert os_path_exists(todd_dallas_luca_role_file_path)
    assert os_path_exists(todd_dallas_todd_role_file_path) == False

    # WHEN
    music_real.set_person_econunits_dirs(todd_text)

    # THEN
    assert os_path_exists(luca_dallas_luca_role_file_path)
    assert os_path_exists(luca_dallas_todd_role_file_path)
    assert os_path_exists(todd_dallas_luca_role_file_path)
    assert os_path_exists(todd_dallas_todd_role_file_path)


def test_RealUnit_get_person_paths_ReturnsCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    music_real = realunit_shop("music", get_test_reals_dir(), in_memory_journal=True)
    luca_text = "Luca"
    todd_text = "Todd"

    # WHEN / THEN
    assert len(music_real.get_person_paths()) == 0

    # WHEN
    music_real.init_person_econs(luca_text)
    music_real.init_person_econs(todd_text)
    music_all_persons = music_real.get_person_paths()

    # THEN
    assert f"{music_real._persons_dir}/{luca_text}" in music_all_persons
    assert f"{music_real._persons_dir}/{todd_text}" in music_all_persons
    assert len(music_real.get_person_paths()) == 2
