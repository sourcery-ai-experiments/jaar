from src._road.road import default_road_delimiter_if_none
from src._road.finance import default_planck_if_none
from src.agenda.agenda import (
    agendaunit_shop,
    get_from_json as agendaunit_get_from_json,
    duty_str,
    work_str,
)
from src.real.nook import (
    nookunit_shop,
    duty_file_exists,
    work_file_exists,
    _save_work_file,
    initialize_work_file,
    save_duty_file,
    get_duty_file_agenda,
    initialize_gift_and_duty_files,
    nookunit_create_core_dir_and_files,
    get_work_file_agenda,
)
from src.real.gift import init_gift_id
from src.real.engine import EngineUnit, engineunit_shop
from src.real.examples.real_env_kit import (
    get_test_reals_dir,
    get_test_real_id,
    reals_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists
from src._instrument.file import open_file, save_file, delete_dir


def test_EngineUnit_Exists():
    # GIVEN / WHEN
    x_person = EngineUnit()

    # THEN
    assert x_person.nook is None
    assert x_person._duty_obj is None
    assert x_person._work_obj is None
    assert x_person._econ_objs is None


def test_EngineUnit_set_person_id_RaisesErrorIf_person_id_Contains_road_delimiter(
    reals_dir_setup_cleanup,
):
    # GIVEN
    slash_text = "/"
    bob_text = f"Bob{slash_text}Sue"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        engineunit_shop(person_id=bob_text, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{bob_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_engineunit_shop_ReturnsCorrectEngineUnit(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    x_reals_dir = get_test_reals_dir()
    x_real_id = "froopiland"

    # WHEN
    sue_person = engineunit_shop(sue_text, x_real_id, reals_dir=x_reals_dir)

    # THEN
    sue_nookunit = nookunit_shop(x_reals_dir, x_real_id, sue_text)
    assert sue_person.nook.person_id == sue_text
    assert sue_person.nook.real_id == x_real_id
    assert sue_person.nook.reals_dir == x_reals_dir
    assert sue_person.nook._econs_dir == f"{sue_nookunit.person_dir}/econs"
    assert sue_person.nook._work_file_name == f"{work_str()}.json"
    sue_work_file_path = f"{sue_nookunit.person_dir}/{sue_nookunit._work_file_name}"
    assert sue_person.nook._work_path == sue_work_file_path
    assert sue_person._econ_objs == {}
    assert sue_person.nook._road_delimiter == default_road_delimiter_if_none()
    assert sue_person.nook._planck == default_planck_if_none()


def test_engineunit_shop_ReturnsCorrectEngineUnitWhenGivenEmptyRealParameters(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    slash_text = "/"
    two_int = 2

    # WHEN
    sue_person = engineunit_shop(sue_text, _road_delimiter=slash_text, _planck=two_int)
    sue_nookunit = nookunit_shop(None, None, sue_text, slash_text, two_int)

    # THEN
    assert sue_person.nook.person_id == sue_text
    assert sue_person.nook._work_file_name == f"{work_str()}.json"
    sue_work_file_path = f"{sue_nookunit.person_dir}/{sue_nookunit._work_file_name}"
    assert sue_person.nook._work_path == sue_work_file_path
    assert sue_person.nook._road_delimiter == slash_text
    assert sue_person.nook._planck == two_int


def test_EngineUnit_duty_file_exists_ReturnsCorrectBool(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_duty_file_name = f"{duty_str()}.json"
    sue_duty_path = f"{sue_person_dir}/{sue_duty_file_name}"
    sue_nookunit = nookunit_shop(None, None, sue_text)
    print(f"{sue_duty_path=}")
    assert os_path_exists(sue_duty_path) == False
    sue_person = engineunit_shop(person_id=sue_text)
    sue_nookunit = sue_person.nook
    assert os_path_exists(sue_duty_path)
    assert duty_file_exists(sue_nookunit)
    delete_dir(sue_duty_path)
    assert os_path_exists(sue_duty_path) == False
    assert duty_file_exists(sue_nookunit) == False

    # WHEN
    save_file(
        dest_dir=sue_nookunit.person_dir,
        file_name=sue_nookunit._duty_file_name,
        file_text=agendaunit_shop(sue_text).get_json(),
    )

    # THEN
    assert os_path_exists(sue_duty_path)
    assert duty_file_exists(sue_nookunit)


def test_EngineUnit_save_duty_file_CorrectlySavesFile(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_duty_file_name = f"{duty_str()}.json"
    sue_duty_path = f"{sue_person_dir}/{sue_duty_file_name}"

    # WHEN
    sue_person = engineunit_shop(person_id=sue_text)
    sue_nookunit = sue_person.nook

    # THEN
    assert duty_file_exists(sue_nookunit)

    # GIVEN
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    delete_dir(sue_duty_path)
    assert duty_file_exists(sue_nookunit) == False

    # WHEN
    save_duty_file(sue_nookunit, sue_agenda)

    # THEN
    assert duty_file_exists(sue_nookunit)

    # GIVEN
    duty_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_duty_file_name)
    print(f"{duty_file_text=}")
    duty_agenda = agendaunit_get_from_json(duty_file_text)
    assert duty_agenda.get_party(bob_text) != None

    # WHEN
    sue2_agenda = agendaunit_shop(sue_text)
    zia_text = "Zia"
    sue2_agenda.add_partyunit(zia_text)
    save_duty_file(sue_nookunit, sue2_agenda)

    # THEN
    duty_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_duty_file_name)
    print(f"{duty_file_text=}")
    duty_agenda = agendaunit_get_from_json(duty_file_text)
    assert duty_agenda.get_party(zia_text) != None


def test_EngineUnit_save_duty_file_RaisesErrorWhenAgenda_work_id_IsWrong(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = engineunit_shop(person_id=sue_text)
    sue_nookunit = sue_person.nook

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        save_duty_file(sue_nookunit, agendaunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"AgendaUnit with owner_id '{yao_text}' cannot be saved as person_id '{sue_text}''s duty agenda."
    )


def test_EngineUnit_initialize_gift_and_duty_files_CorrectlySavesDutyFileAndGiftFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_person = engineunit_shop(person_id=sue_text, _planck=seven_int)
    sue_nookunit = sue_person.nook
    assert duty_file_exists(sue_nookunit)
    delete_dir(sue_nookunit._duty_path)
    assert duty_file_exists(sue_nookunit) == False
    init_gift_file_path = f"{sue_nookunit._gifts_dir}/{init_gift_id()}.json"
    delete_dir(sue_nookunit._gifts_dir)
    assert os_path_exists(init_gift_file_path) == False

    # WHEN
    initialize_gift_and_duty_files(sue_nookunit)

    # THEN
    duty_agenda = get_duty_file_agenda(sue_nookunit)
    assert duty_agenda._real_id == get_test_real_id()
    assert duty_agenda._owner_id == sue_text
    assert duty_agenda._planck == seven_int
    assert os_path_exists(init_gift_file_path)


def test_EngineUnit_initialize_gift_and_duty_files_CorrectlySavesOnlyDutyFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_person = engineunit_shop(person_id=sue_text, _planck=seven_int)
    sue_nookunit = sue_person.nook
    assert duty_file_exists(sue_nookunit)
    delete_dir(sue_nookunit._duty_path)
    assert duty_file_exists(sue_nookunit) == False
    init_gift_file_path = f"{sue_nookunit._gifts_dir}/{init_gift_id()}.json"
    assert os_path_exists(init_gift_file_path)

    # WHEN
    initialize_gift_and_duty_files(sue_nookunit)

    # THEN
    duty_agenda = get_duty_file_agenda(sue_nookunit)
    assert duty_agenda._real_id == get_test_real_id()
    assert duty_agenda._owner_id == sue_text
    assert duty_agenda._planck == seven_int
    assert os_path_exists(init_gift_file_path)


def test_EngineUnit_initialize_gift_and_duty_files_CorrectlySavesOnlyGiftFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_person = engineunit_shop(sue_text, _planck=seven_int)
    sue_nookunit = sue_person.nook
    sue_duty_agenda = get_duty_file_agenda(sue_nookunit)
    bob_text = "Bob"
    sue_duty_agenda.add_partyunit(bob_text)
    save_duty_file(sue_nookunit, sue_duty_agenda)
    assert duty_file_exists(sue_nookunit)
    init_gift_file_path = f"{sue_nookunit._gifts_dir}/{init_gift_id()}.json"
    delete_dir(sue_nookunit._gifts_dir)
    assert os_path_exists(init_gift_file_path) == False

    # WHEN
    initialize_gift_and_duty_files(sue_nookunit)

    # THEN
    assert sue_duty_agenda._real_id == get_test_real_id()
    assert sue_duty_agenda._owner_id == sue_text
    assert sue_duty_agenda._planck == seven_int
    assert sue_duty_agenda.get_party(bob_text) != None
    assert os_path_exists(init_gift_file_path)


# def test_EngineUnit_initialize_gift_and_duty_files_CorrectlyDoesNotOverwrite(
#     reals_dir_setup_cleanup,
# ):
#     # GIVEN
#     sue_text = "Sue"
#     sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
#     sue_person = engineunit_shop(person_id=sue_text)
# sue_nookunit = sue_person.nook
#     assert sue_person.duty_file_exists()
#     delete_dir(sue_person._duty_path)
#     assert sue_person.duty_file_exists() == False

#     # WHEN
#     sue_agenda = agendaunit_shop(sue_text)
#     bob_text = "Bob"
#     sue_agenda.add_partyunit(bob_text)
#     initialize_gift_and_duty_files()

#     # THEN
#     assert sue_person.duty_file_exists()

#     sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
#     sue_persons_dir = f"{sue_real_dir}/persons"
#     sue_person_dir = f"{sue_persons_dir}/{sue_text}"
#     sue_duty_file_name = f"{duty_str()}.json"
#     duty_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_duty_file_name)
#     print(f"{duty_file_text=}")
#     duty_agenda = agendaunit_get_from_json(duty_file_text)
#     assert duty_agenda._real_id == get_test_real_id()
#     assert duty_agenda._owner_id == sue_text


def test_EngineUnit_work_file_exists_ReturnsCorrectBool(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_work_file_name = f"{work_str()}.json"
    sue_work_path = f"{sue_person_dir}/{sue_work_file_name}"
    print(f"{sue_work_path=}")
    assert os_path_exists(sue_work_path) == False
    sue_person = engineunit_shop(person_id=sue_text)
    sue_nookunit = sue_person.nook
    assert work_file_exists(sue_nookunit)
    delete_dir(sue_person.nook._work_path)
    assert os_path_exists(sue_work_path) == False
    assert work_file_exists(sue_nookunit) == False

    # WHEN
    save_file(
        dest_dir=sue_nookunit.person_dir,
        file_name=sue_nookunit._work_file_name,
        file_text=agendaunit_shop(sue_text).get_json(),
    )

    # THEN
    assert os_path_exists(sue_work_path)
    assert work_file_exists(sue_nookunit)


def test_EngineUnit_save_work_file_CorrectlySavesFile(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_person = engineunit_shop(person_id=sue_text)
    sue_nookunit = sue_person.nook
    assert work_file_exists(sue_nookunit)
    delete_dir(sue_person.nook._work_path)
    assert work_file_exists(sue_nookunit) == False

    # WHEN
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    _save_work_file(sue_nookunit, sue_agenda)

    # THEN
    assert work_file_exists(sue_nookunit)

    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_work_file_name = f"{work_str()}.json"
    work_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_work_file_name)
    print(f"{work_file_text=}")
    work_agenda = agendaunit_get_from_json(work_file_text)
    assert work_agenda.get_party(bob_text) != None

    # # WHEN
    sue2_agenda = agendaunit_shop(sue_text)
    zia_text = "Zia"
    sue2_agenda.add_partyunit(zia_text)
    _save_work_file(sue_nookunit, sue2_agenda)

    # THEN
    work_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_work_file_name)
    print(f"{work_file_text=}")
    work_agenda = agendaunit_get_from_json(work_file_text)
    assert work_agenda.get_party(zia_text) != None


def test_EngineUnit_save_work_file_RaisesErrorWhenAgenda_work_id_IsWrong(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = engineunit_shop(person_id=sue_text)
    sue_nookunit = sue_person.nook

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        _save_work_file(sue_nookunit, agendaunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"AgendaUnit with owner_id '{yao_text}' cannot be saved as person_id '{sue_text}''s work agenda."
    )


def test_EngineUnit_initialize_work_file_CorrectlySavesFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = engineunit_shop(person_id=sue_text)
    sue_nookunit = sue_person.nook
    assert work_file_exists(sue_nookunit)
    delete_dir(sue_person.nook._work_path)
    assert work_file_exists(sue_nookunit) == False

    # WHEN
    initialize_work_file(sue_nookunit)

    # THEN
    work_agenda = get_work_file_agenda(sue_nookunit)
    assert work_agenda._real_id == get_test_real_id()
    assert work_agenda._owner_id == sue_text
    bob_text = "Bob"
    assert work_agenda.get_party(bob_text) is None

    # GIVEN
    sue_agenda = agendaunit_shop(sue_text)
    sue_agenda.add_partyunit(bob_text)
    _save_work_file(sue_nookunit, sue_agenda)
    work_agenda = get_work_file_agenda(sue_nookunit)
    assert work_agenda.get_party(bob_text)

    # WHEN
    initialize_work_file(sue_nookunit)

    # THEN
    work_agenda = get_work_file_agenda(sue_nookunit)
    assert work_agenda.get_party(bob_text)


def test_EngineUnit_initialize_work_file_CorrectlyDoesNotOverwrite(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_planck = 7
    sue_person = engineunit_shop(person_id=sue_text, _planck=sue_planck)
    sue_nookunit = sue_person.nook
    assert work_file_exists(sue_nookunit)
    delete_dir(sue_person.nook._work_path)
    assert work_file_exists(sue_nookunit) == False

    # WHEN
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    initialize_work_file(sue_nookunit)

    # THEN
    assert work_file_exists(sue_nookunit)

    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_work_file_name = f"{work_str()}.json"
    work_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_work_file_name)
    print(f"{work_file_text=}")
    work_agenda = agendaunit_get_from_json(work_file_text)
    assert work_agenda._real_id == get_test_real_id()
    assert work_agenda._owner_id == sue_text
    assert work_agenda._planck == sue_planck


def test_EngineUnit_create_core_dir_and_files_CreatesDirsAndFiles(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_nookunit = nookunit_shop(None, None, sue_text)
    delete_dir(sue_nookunit.real_dir)
    assert os_path_exists(sue_nookunit.real_dir) is False
    assert os_path_exists(sue_nookunit.persons_dir) is False
    assert os_path_exists(sue_nookunit.person_dir) is False
    assert os_path_exists(sue_nookunit._econs_dir) is False
    assert os_path_exists(sue_nookunit._atoms_dir) is False
    assert os_path_exists(sue_nookunit._gifts_dir) is False
    assert os_path_exists(sue_nookunit._duty_path) is False
    assert os_path_exists(sue_nookunit._work_path) is False

    # WHEN
    nookunit_create_core_dir_and_files(sue_nookunit)

    # THEN
    assert os_path_exists(sue_nookunit.real_dir)
    assert os_path_exists(sue_nookunit.persons_dir)
    assert os_path_exists(sue_nookunit.person_dir)
    assert os_path_exists(sue_nookunit._econs_dir)
    assert os_path_exists(sue_nookunit._atoms_dir)
    assert os_path_exists(sue_nookunit._gifts_dir)
    assert os_path_exists(sue_nookunit._duty_path)
    assert os_path_exists(sue_nookunit._work_path)
