from src._road.finance import default_planck_if_none
from src._road.road import default_road_delimiter_if_none
from src.agenda.healer import healerhold_shop
from src.agenda.idea import ideaunit_shop
from src.econ.job_creator import get_owner_file_name
from src.real.nook import nookunit_shop, save_duty_file, get_duty_file_agenda
from src.real.gift import get_gifts_folder
from src.real.engine import engineunit_shop
from src.real.real import RealUnit, realunit_shop
from src.real.examples.real_env_kit import get_test_reals_dir, reals_dir_setup_cleanup
from os import path as os_path
from os.path import exists as os_path_exists
from pytest import raises as pytest_raises


def test_RealUnit_exists(reals_dir_setup_cleanup):
    music_text = "music"
    music_real = RealUnit(real_id=music_text, reals_dir=get_test_reals_dir())
    assert music_real.real_id == music_text
    assert music_real.reals_dir == get_test_reals_dir()
    assert music_real._persons_dir is None
    assert music_real._journal_db is None
    assert music_real._engineunits is None
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
    assert music_real._engineunits == {}
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


def test_RealUnit__set_real_dirs_SetsPersonDir(reals_dir_setup_cleanup):
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


def test_RealUnit__set_engineunit_in_memory_CorrectlySetsPerson(
    reals_dir_setup_cleanup,
):
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(
        real_id=music_text, reals_dir=get_test_reals_dir(), in_memory_journal=True
    )
    assert music_real._engineunits == {}

    # WHEN
    luca_text = "Luca"
    luca_person = engineunit_shop(person_id=luca_text)
    music_real._set_engineunit_in_memory(engineunit=luca_person)

    # THEN
    assert music_real._engineunits != {}
    assert len(music_real._engineunits) == 1
    assert music_real._engineunits[luca_text] == luca_person
    assert music_real._real_dir == f"{get_test_reals_dir()}/{music_text}"
    assert music_real._persons_dir == f"{music_real._real_dir}/persons"


def test_RealUnit_engineunit_exists_in_memory_ReturnsCorrectBool(
    reals_dir_setup_cleanup,
):
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(
        real_id=music_text, reals_dir=get_test_reals_dir(), in_memory_journal=True
    )
    assert music_real._engineunits == {}

    # WHEN / THEN
    luca_text = "Luca"
    assert music_real.engineunit_exists_in_memory(luca_text) == False

    # WHEN / THEN
    luca_person = engineunit_shop(person_id=luca_text)
    music_real._set_engineunit_in_memory(engineunit=luca_person)
    assert music_real.engineunit_exists_in_memory(luca_text)


def test_RealUnit_add_engineunit_CorrectlySetsPerson(reals_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    slash_text = "/"
    music_real = realunit_shop(
        music_text,
        get_test_reals_dir(),
        _road_delimiter=slash_text,
        in_memory_journal=True,
    )
    luca_text = "Luca"
    luca_person_dir = f"{music_real._persons_dir}/{luca_text}"

    # WHEN
    music_real.add_engineunit(luca_text)

    # THEN
    assert music_real._engineunits[luca_text] != None
    print(f"{get_test_reals_dir()=}")
    print(f"      {luca_person_dir=}")
    assert music_real._engineunits[luca_text].nook._road_delimiter == slash_text
    luca_person_obj = engineunit_shop(
        person_id=luca_text,
        real_id=music_text,
        reals_dir=music_real.reals_dir,
        _road_delimiter=slash_text,
    )
    assert (
        music_real._engineunits[luca_text].nook.reals_dir
        == luca_person_obj.nook.reals_dir
    )
    assert (
        music_real._engineunits[luca_text].nook.real_id == luca_person_obj.nook.real_id
    )
    assert music_real._engineunits[luca_text] == luca_person_obj


def test_RealUnit_add_engineunit_RaisesErrorIfPersonExists(reals_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(
        real_id=music_text, reals_dir=get_test_reals_dir(), in_memory_journal=True
    )
    luca_text = "Luca"
    luca_person_dir = f"{music_real._persons_dir}/{luca_text}"
    luca_person_obj = engineunit_shop(
        person_id=luca_text,
        real_id=music_text,
        reals_dir=music_real.reals_dir,
    )
    music_real.add_engineunit(luca_text)
    assert music_real._engineunits[luca_text] != None
    assert music_real._engineunits[luca_text] == luca_person_obj

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        music_real.add_engineunit(luca_text)
    assert str(excinfo.value) == f"add_engineunit fail: {luca_text} already exists"


def test_RealUnit__set_engineunit_in_memory_CorrectlyCreatesObj(
    reals_dir_setup_cleanup,
):
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(
        real_id=music_text, reals_dir=get_test_reals_dir(), in_memory_journal=True
    )
    luca_text = "Luca"
    assert music_real.engineunit_exists_in_memory(luca_text) == False

    # WHEN
    luca_person_dir = f"{music_real._persons_dir}/{luca_text}"
    luca_person_obj = engineunit_shop(
        person_id=luca_text,
        real_id=music_real.real_id,
        reals_dir=music_real.reals_dir,
    )
    music_real._set_engineunit_in_memory(luca_person_obj)

    # THEN
    assert music_real.engineunit_exists_in_memory(luca_text)
    assert music_real._engineunits.get(luca_text) == luca_person_obj


def test_RealUnit_get_engineunit_ReturnsPerson(reals_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(
        real_id=music_text, reals_dir=get_test_reals_dir(), in_memory_journal=True
    )
    luca_text = "Luca"
    luca_person_dir = f"{music_real._persons_dir}/{luca_text}"
    luca_person_obj = engineunit_shop(
        person_id=luca_text,
        real_id=music_real.real_id,
        reals_dir=music_real.reals_dir,
    )
    music_real.add_engineunit(luca_text)

    # WHEN
    luca_gotten_obj = music_real.get_engineunit_from_memory(luca_text)

    # THEN
    assert luca_gotten_obj != None
    assert luca_gotten_obj == luca_person_obj


def test_RealUnit_get_engineunit_ReturnsNone(reals_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(
        real_id=music_text, reals_dir=get_test_reals_dir(), in_memory_journal=True
    )
    luca_text = "Luca"

    # WHEN
    luca_gotten_obj = music_real.get_engineunit_from_memory(luca_text)

    # THEN
    assert luca_gotten_obj is None


def test_RealUnit_get_person_duty_from_file_ReturnsCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), in_memory_journal=True)
    luca_text = "Luca"
    music_real.add_engineunit(luca_text)
    luca_person = music_real.get_engineunit_from_memory(luca_text)
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
    luca_person = music_real.add_engineunit(luca_text)
    todd_person = music_real.add_engineunit(todd_text)
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
    luca_person.create_person_econunits(luca_nookunit)
    todd_person.create_person_econunits(todd_nookunit)
    luca_dallas_econ = luca_person.get_econ(dallas_road)
    todd_dallas_econ = todd_person.get_econ(dallas_road)
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
    sue_text = "Sue"
    music_real.add_engineunit(luca_text)
    music_real.add_engineunit(todd_text)
    music_real.add_engineunit(sue_text)
    assert len(music_real._engineunits) == 3
    music_real._engineunits.pop(sue_text)
    assert len(music_real._engineunits) == 2

    # WHEN
    music_all_persons = music_real.get_person_paths()

    # THEN
    assert f"{music_real._persons_dir}/{luca_text}" in music_all_persons
    assert f"{music_real._persons_dir}/{todd_text}" in music_all_persons
    assert f"{music_real._persons_dir}/{sue_text}" in music_all_persons
