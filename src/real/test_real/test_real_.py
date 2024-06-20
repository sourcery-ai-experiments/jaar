from src._road.finance import default_planck_if_none, default_penny_if_none
from src._road.jaar_config import get_atoms_folder, get_json_filename
from src._road.road import default_road_delimiter_if_none
from src.agenda.healer import healerhold_shop
from src.agenda.idea import ideaunit_shop
from src.listen.userhub import userhub_shop
from src.real.real import RealUnit, realunit_shop
from src.real.examples.real_env import get_test_reals_dir, env_dir_setup_cleanup
from os.path import exists as os_path_exists, isdir as os_path_isdir


def test_RealUnit_exists(env_dir_setup_cleanup):
    music_text = "music"
    music_real = RealUnit(real_id=music_text, reals_dir=get_test_reals_dir())
    assert music_real.real_id == music_text
    assert music_real.reals_dir == get_test_reals_dir()
    assert music_real._persons_dir is None
    assert music_real._journal_db is None
    assert music_real._atoms_dir is None
    assert music_real._road_delimiter is None
    assert music_real._planck is None
    assert music_real._penny is None


def test_realunit_shop_ReturnsRealUnit(env_dir_setup_cleanup):
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
    assert music_real._atoms_dir != None
    assert music_real._road_delimiter == default_road_delimiter_if_none()
    assert music_real._planck == default_planck_if_none()
    assert music_real._penny == default_penny_if_none()


def test_realunit_shop_ReturnsRealUnitWith_road_delimiter(env_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    slash_text = "/"
    planck_float = 9
    penny_float = 3

    # WHEN
    music_real = realunit_shop(
        real_id=music_text,
        reals_dir=get_test_reals_dir(),
        in_memory_journal=True,
        _road_delimiter=slash_text,
        _planck=planck_float,
        _penny=penny_float,
    )

    # THEN
    assert music_real._road_delimiter == slash_text
    assert music_real._planck == planck_float
    assert music_real._penny == penny_float


def test_RealUnit_set_real_dirs_SetsCorrectDirsAndFiles(env_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    music_real = RealUnit(real_id=music_text, reals_dir=get_test_reals_dir())
    x_real_dir = f"{get_test_reals_dir()}/{music_text}"
    x_persons_dir = f"{x_real_dir}/persons"
    x_atoms_dir = f"{x_real_dir}/{get_atoms_folder()}"
    journal_file_name = "journal.db"
    journal_file_path = f"{x_real_dir}/{journal_file_name}"

    assert music_real._real_dir is None
    assert music_real._persons_dir is None
    assert music_real._atoms_dir is None
    assert os_path_exists(x_real_dir) is False
    assert os_path_isdir(x_real_dir) is False
    assert os_path_exists(x_persons_dir) is False
    assert os_path_exists(x_atoms_dir) is False
    assert os_path_exists(journal_file_path) is False

    # WHEN
    music_real._set_real_dirs()

    # THEN
    assert music_real._real_dir == x_real_dir
    assert music_real._persons_dir == x_persons_dir
    assert music_real._atoms_dir == x_atoms_dir
    assert os_path_exists(x_real_dir)
    assert os_path_isdir(x_real_dir)
    assert os_path_exists(x_persons_dir)
    assert os_path_exists(x_atoms_dir)
    assert os_path_exists(journal_file_path)


def test_realunit_shop_SetsRealsDirs(env_dir_setup_cleanup):
    # GIVEN
    music_text = "music"

    # WHEN
    music_real = realunit_shop(music_text, get_test_reals_dir(), in_memory_journal=True)

    # THEN
    assert music_real.real_id == music_text
    assert music_real._real_dir == f"{get_test_reals_dir()}/{music_text}"
    assert music_real._persons_dir == f"{music_real._real_dir}/persons"


def test_RealUnit_init_person_econs_CorrectlySetsDirAndFiles(env_dir_setup_cleanup):
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
    luca_userhub = userhub_shop(None, music_text, luca_text, None, planck=x_planck)
    assert os_path_exists(luca_userhub.work_path()) is False

    # WHEN
    music_real.init_person_econs(luca_text)

    # THEN
    print(f"{get_test_reals_dir()=}")
    assert os_path_exists(luca_userhub.work_path())


def test_RealUnit_get_person_duty_from_file_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), in_memory_journal=True)
    luca_text = "Luca"
    music_real.init_person_econs(luca_text)
    luca_userhub = userhub_shop(None, music_text, luca_text, None)
    bob_text = "Bob"
    luca_duty = luca_userhub.get_duty_agenda()
    luca_duty.add_otherunit(bob_text)
    luca_userhub.save_duty_agenda(luca_duty)

    # WHEN
    gen_luca_duty = music_real.get_person_duty_from_file(luca_text)

    # THEN
    assert gen_luca_duty != None
    assert gen_luca_duty.other_exists(bob_text)


def test_RealUnit__set_all_healer_roles_CorrectlySetsroles(
    env_dir_setup_cleanup,
):
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), in_memory_journal=True)
    luca_text = "Luca"
    todd_text = "Todd"
    music_real.init_person_econs(luca_text)
    music_real.init_person_econs(todd_text)
    luca_userhub = userhub_shop(None, music_text, luca_text, None)
    todd_userhub = userhub_shop(None, music_text, todd_text, None)
    luca_duty_agenda = luca_userhub.get_duty_agenda()
    todd_duty_agenda = todd_userhub.get_duty_agenda()

    luca_duty_agenda.add_otherunit(luca_text)
    luca_duty_agenda.add_otherunit(todd_text)
    todd_duty_agenda.add_otherunit(luca_text)
    todd_duty_agenda.add_otherunit(todd_text)
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
    luca_userhub.save_duty_agenda(luca_duty_agenda)
    todd_userhub.save_duty_agenda(todd_duty_agenda)
    luca_file_name = get_json_filename(luca_text)
    todd_file_name = get_json_filename(todd_text)
    luca_dallas_userhub = userhub_shop(None, music_text, luca_text, dallas_road)
    todd_dallas_userhub = userhub_shop(None, music_text, todd_text, dallas_road)
    luca_roles_dir = luca_dallas_userhub.roles_dir()
    todd_roles_dir = todd_dallas_userhub.roles_dir()
    luca_dallas_luca_role_file_path = f"{luca_roles_dir}/{luca_file_name}"
    luca_dallas_todd_role_file_path = f"{luca_roles_dir}/{todd_file_name}"
    todd_dallas_luca_role_file_path = f"{todd_roles_dir}/{luca_file_name}"
    todd_dallas_todd_role_file_path = f"{todd_roles_dir}/{todd_file_name}"
    assert os_path_exists(luca_dallas_luca_role_file_path) is False
    assert os_path_exists(luca_dallas_todd_role_file_path) is False
    assert os_path_exists(todd_dallas_luca_role_file_path) is False
    assert os_path_exists(todd_dallas_todd_role_file_path) is False

    # WHEN
    music_real._set_all_healer_roles(luca_text)

    # THEN
    assert os_path_exists(luca_dallas_luca_role_file_path)
    assert os_path_exists(luca_dallas_todd_role_file_path) is False
    assert os_path_exists(todd_dallas_luca_role_file_path)
    assert os_path_exists(todd_dallas_todd_role_file_path) is False

    # WHEN
    music_real._set_all_healer_roles(todd_text)

    # THEN
    assert os_path_exists(luca_dallas_luca_role_file_path)
    assert os_path_exists(luca_dallas_todd_role_file_path)
    assert os_path_exists(todd_dallas_luca_role_file_path)
    assert os_path_exists(todd_dallas_todd_role_file_path)


def test_RealUnit_get_person_userhubs_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    music_real = realunit_shop("music", get_test_reals_dir(), in_memory_journal=True)
    luca_text = "Luca"
    todd_text = "Todd"

    # WHEN / THEN
    assert len(music_real.get_person_userhubs()) == 0

    # WHEN
    music_real.init_person_econs(luca_text)
    music_real.init_person_econs(todd_text)
    music_all_persons = music_real.get_person_userhubs()

    # THEN
    luca_userhub = userhub_shop(
        reals_dir=music_real.reals_dir,
        real_id=music_real.real_id,
        person_id=luca_text,
        econ_road=None,
        road_delimiter=music_real._road_delimiter,
        planck=music_real._planck,
    )
    todd_userhub = userhub_shop(
        reals_dir=music_real.reals_dir,
        real_id=music_real.real_id,
        person_id=todd_text,
        econ_road=None,
        road_delimiter=music_real._road_delimiter,
        planck=music_real._planck,
    )
    assert music_all_persons.get(luca_text) == luca_userhub
    assert music_all_persons.get(todd_text) == todd_userhub
    assert len(music_real.get_person_userhubs()) == 2
