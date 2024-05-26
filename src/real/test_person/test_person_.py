from src._road.road import default_road_delimiter_if_none
from src._road.finance import default_planck_if_none
from src.agenda.agenda import (
    agendaunit_shop,
    get_from_json as agendaunit_get_from_json,
    duty_str,
    work_str,
)
from src.world.gift import init_gift_id, get_gifts_folder
from src.real.person import (
    PersonUnit,
    personunit_shop,
    chapunit_shop,
    duty_file_exists,
    work_file_exists,
    ChapUnit,
    _save_work_file,
    initialize_work_file,
    save_duty_file,
    get_duty_file_agenda,
    initialize_gift_and_duty_files,
    chap_create_core_dir_and_files,
    get_work_file_agenda,
)
from pytest import raises as pytest_raises
from src.real.examples.real_env_kit import (
    get_test_reals_dir,
    get_test_real_id,
    reals_dir_setup_cleanup,
)
from os.path import exists as os_path_exists
from src._instrument.file import open_file, save_file, delete_dir


def test_duty_str():
    assert duty_str() == "duty"


def test_work_str():
    assert work_str() == "work"


def test_ChapUnit_Exists():
    # GIVEN / WHEN
    x_chap = ChapUnit()

    # THEN
    assert x_chap.person_id is None
    assert x_chap.real_id is None
    assert x_chap.real_dir is None
    assert x_chap.reals_dir is None
    assert x_chap.persons_dir is None
    assert x_chap.person_dir is None
    assert x_chap._econs_dir is None
    assert x_chap._atoms_dir is None
    assert x_chap._gifts_dir is None
    assert x_chap._duty_obj is None
    assert x_chap._duty_file_name is None
    assert x_chap._duty_path is None
    assert x_chap._work_obj is None
    assert x_chap._work_file_name is None
    assert x_chap._work_path is None
    assert x_chap._econ_objs is None
    assert x_chap._road_delimiter is None
    assert x_chap._planck is None


def test_ChapUnit_Exists():
    # GIVEN
    x_reals_dir = "src/real/examples"
    x_real_id = "music"
    x_person_id = "Sue"
    x_road_delimiter = "/"
    x_planck = 3

    # WHEN
    x_chapunit = chapunit_shop(
        x_reals_dir, x_real_id, x_person_id, x_road_delimiter, x_planck
    )

    # THEN
    assert x_chapunit._road_delimiter == x_road_delimiter
    assert x_chapunit.real_dir == f"{x_reals_dir}/{x_real_id}"
    assert x_chapunit.persons_dir == f"{x_chapunit.real_dir}/persons"
    assert x_chapunit.person_id == x_person_id
    assert x_chapunit.person_dir == f"{x_chapunit.persons_dir}/{x_person_id}"
    assert x_chapunit._econs_dir == f"{x_chapunit.person_dir}/econs"
    assert x_chapunit._atoms_dir == f"{x_chapunit.person_dir}/atoms"
    assert x_chapunit._gifts_dir == f"{x_chapunit.person_dir}/{get_gifts_folder()}"
    assert x_chapunit._duty_file_name == f"{duty_str()}.json"
    x_duty_path = f"{x_chapunit.person_dir}/{x_chapunit._duty_file_name}"
    assert x_chapunit._duty_path == x_duty_path
    assert x_chapunit._work_file_name == f"{work_str()}.json"
    x_workpath = f"{x_chapunit.person_dir}/{x_chapunit._work_file_name}"
    assert x_chapunit._work_path == x_workpath


def test_PersonUnit_Exists():
    # GIVEN / WHEN
    x_person = PersonUnit()

    # THEN
    assert x_person.person_id is None
    assert x_person.real_id is None
    assert x_person.reals_dir is None
    assert x_person.persons_dir is None
    assert x_person.person_dir is None
    assert x_person._econs_dir is None
    assert x_person._duty_obj is None
    assert x_person._work_obj is None
    assert x_person._econ_objs is None
    assert x_person._road_delimiter is None
    assert x_person._planck is None


def test_PersonUnit_set_person_id_CorrectlySetsAttr():
    # GIVEN / WHEN
    x_person = PersonUnit()
    assert x_person.person_id is None
    assert x_person.real_id is None
    assert x_person._econs_dir is None

    # GIVEN
    yao_text = "Yao"
    x_chapunit = chapunit_shop(None, None, yao_text)
    x_person.set_person_id(x_chapunit)

    # THEN
    assert x_person.person_id == yao_text
    assert x_person._work_file_name == f"{work_str()}.json"
    assert x_person._econs_dir == f"{x_chapunit.person_dir}/econs"


def test_PersonUnit_set_person_id_RaisesErrorIf_person_id_Contains_road_delimiter(
    reals_dir_setup_cleanup,
):
    # GIVEN
    slash_text = "/"
    bob_text = f"Bob{slash_text}Sue"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        personunit_shop(person_id=bob_text, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{bob_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_personunit_shop_ReturnsCorrectPersonUnit(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    x_reals_dir = get_test_reals_dir()
    x_real_id = "froopiland"

    # WHEN
    sue_person = personunit_shop(sue_text, x_real_id, reals_dir=x_reals_dir)

    # THEN
    sue_chapunit = chapunit_shop(x_reals_dir, x_real_id, sue_text)
    assert sue_person.person_id == sue_text
    assert sue_person.real_id == x_real_id
    assert sue_person.reals_dir == x_reals_dir
    assert sue_person._econs_dir == f"{sue_chapunit.person_dir}/econs"
    assert sue_person._work_file_name == f"{work_str()}.json"
    sue_work_file_path = f"{sue_chapunit.person_dir}/{sue_chapunit._work_file_name}"
    assert sue_person._work_path == sue_work_file_path
    assert sue_person._econ_objs == {}
    assert sue_person._road_delimiter == default_road_delimiter_if_none()
    assert sue_person._planck == default_planck_if_none()


def test_personunit_shop_ReturnsCorrectPersonUnitWhenGivenEmptyRealParameters(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    slash_text = "/"
    two_int = 2

    # WHEN
    sue_person = personunit_shop(sue_text, _road_delimiter=slash_text, _planck=two_int)
    sue_chapunit = chapunit_shop(None, None, sue_text, slash_text, two_int)

    # THEN
    assert sue_person.person_id == sue_text
    assert sue_person._work_file_name == f"{work_str()}.json"
    sue_work_file_path = f"{sue_chapunit.person_dir}/{sue_chapunit._work_file_name}"
    assert sue_person._work_path == sue_work_file_path
    assert sue_person._road_delimiter == slash_text
    assert sue_person._planck == two_int


def test_PersonUnit_duty_file_exists_ReturnsCorrectBool(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_duty_file_name = f"{duty_str()}.json"
    sue_duty_path = f"{sue_person_dir}/{sue_duty_file_name}"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    print(f"{sue_duty_path=}")
    assert os_path_exists(sue_duty_path) == False
    sue_person = personunit_shop(person_id=sue_text)
    sue_chapunit = chapunit_shop(None, None, sue_text)
    assert os_path_exists(sue_duty_path)
    assert duty_file_exists(sue_chapunit)
    delete_dir(sue_duty_path)
    assert os_path_exists(sue_duty_path) == False
    assert duty_file_exists(sue_chapunit) == False

    # WHEN
    save_file(
        dest_dir=sue_chapunit.person_dir,
        file_name=sue_chapunit._duty_file_name,
        file_text=agendaunit_shop(sue_text).get_json(),
    )

    # THEN
    assert os_path_exists(sue_duty_path)
    assert duty_file_exists(sue_chapunit)


def test_PersonUnit_save_duty_file_CorrectlySavesFile(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_duty_file_name = f"{duty_str()}.json"
    sue_duty_path = f"{sue_person_dir}/{sue_duty_file_name}"

    # WHEN
    sue_person = personunit_shop(person_id=sue_text)
    sue_chapunit = chapunit_shop(None, None, sue_text)

    # THEN
    assert duty_file_exists(sue_chapunit)

    # GIVEN
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    delete_dir(sue_duty_path)
    assert duty_file_exists(sue_chapunit) == False

    # WHEN
    save_duty_file(sue_chapunit, sue_agenda)

    # THEN
    assert duty_file_exists(sue_chapunit)

    # GIVEN
    duty_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_duty_file_name)
    print(f"{duty_file_text=}")
    duty_agenda = agendaunit_get_from_json(duty_file_text)
    assert duty_agenda.get_party(bob_text) != None

    # WHEN
    sue2_agenda = agendaunit_shop(sue_text)
    zia_text = "Zia"
    sue2_agenda.add_partyunit(zia_text)
    save_duty_file(sue_chapunit, sue2_agenda)

    # THEN
    duty_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_duty_file_name)
    print(f"{duty_file_text=}")
    duty_agenda = agendaunit_get_from_json(duty_file_text)
    assert duty_agenda.get_party(zia_text) != None


def test_PersonUnit_save_duty_file_RaisesErrorWhenAgenda_work_id_IsWrong(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_chapunit = chapunit_shop(None, None, sue_text)

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        save_duty_file(sue_chapunit, agendaunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"AgendaUnit with owner_id '{yao_text}' cannot be saved as person_id '{sue_text}''s duty agenda."
    )


def test_PersonUnit_initialize_gift_and_duty_files_CorrectlySavesDutyFileAndGiftFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_person = personunit_shop(person_id=sue_text, _planck=seven_int)
    sue_chapunit = chapunit_shop(None, None, sue_text, x_planck=seven_int)
    assert duty_file_exists(sue_chapunit)
    delete_dir(sue_chapunit._duty_path)
    assert duty_file_exists(sue_chapunit) == False
    init_gift_file_path = f"{sue_chapunit._gifts_dir}/{init_gift_id()}.json"
    delete_dir(sue_chapunit._gifts_dir)
    assert os_path_exists(init_gift_file_path) == False

    # WHEN
    initialize_gift_and_duty_files(sue_chapunit)

    # THEN
    duty_agenda = get_duty_file_agenda(sue_chapunit)
    assert duty_agenda._real_id == get_test_real_id()
    assert duty_agenda._owner_id == sue_text
    assert duty_agenda._planck == seven_int
    assert os_path_exists(init_gift_file_path)


def test_PersonUnit_initialize_gift_and_duty_files_CorrectlySavesOnlyDutyFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_person = personunit_shop(person_id=sue_text, _planck=seven_int)
    sue_chapunit = chapunit_shop(None, None, sue_text)
    assert duty_file_exists(sue_chapunit)
    delete_dir(sue_chapunit._duty_path)
    assert duty_file_exists(sue_chapunit) == False
    init_gift_file_path = f"{sue_chapunit._gifts_dir}/{init_gift_id()}.json"
    assert os_path_exists(init_gift_file_path)

    # WHEN
    initialize_gift_and_duty_files(sue_chapunit)

    # THEN
    duty_agenda = get_duty_file_agenda(sue_chapunit)
    assert duty_agenda._real_id == get_test_real_id()
    assert duty_agenda._owner_id == sue_text
    assert duty_agenda._planck == seven_int
    assert os_path_exists(init_gift_file_path)


def test_PersonUnit_initialize_gift_and_duty_files_CorrectlySavesOnlyGiftFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_person = personunit_shop(sue_text, _planck=seven_int)
    sue_chapunit = chapunit_shop(None, None, sue_text)
    sue_duty_agenda = get_duty_file_agenda(sue_chapunit)
    bob_text = "Bob"
    sue_duty_agenda.add_partyunit(bob_text)
    save_duty_file(sue_chapunit, sue_duty_agenda)
    assert duty_file_exists(sue_chapunit)
    init_gift_file_path = f"{sue_chapunit._gifts_dir}/{init_gift_id()}.json"
    delete_dir(sue_chapunit._gifts_dir)
    assert os_path_exists(init_gift_file_path) == False

    # WHEN
    initialize_gift_and_duty_files(sue_chapunit)

    # THEN
    assert sue_duty_agenda._real_id == get_test_real_id()
    assert sue_duty_agenda._owner_id == sue_text
    assert sue_duty_agenda._planck == seven_int
    assert sue_duty_agenda.get_party(bob_text) != None
    assert os_path_exists(init_gift_file_path)


# def test_PersonUnit_initialize_gift_and_duty_files_CorrectlyDoesNotOverwrite(
#     reals_dir_setup_cleanup,
# ):
#     # GIVEN
#     sue_text = "Sue"
#     sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
#     sue_person = personunit_shop(person_id=sue_text)
# sue_chapunit = chapunit_shop(None, None, sue_text)
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


def test_PersonUnit_work_file_exists_ReturnsCorrectBool(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_work_file_name = f"{work_str()}.json"
    sue_work_path = f"{sue_person_dir}/{sue_work_file_name}"
    print(f"{sue_work_path=}")
    assert os_path_exists(sue_work_path) == False
    sue_person = personunit_shop(person_id=sue_text)
    sue_chapunit = chapunit_shop(None, None, sue_text)
    sue_chapunit = chapunit_shop(None, None, sue_text)
    assert work_file_exists(sue_chapunit)
    delete_dir(sue_person._work_path)
    assert os_path_exists(sue_work_path) == False
    assert work_file_exists(sue_chapunit) == False

    # WHEN
    save_file(
        dest_dir=sue_chapunit.person_dir,
        file_name=sue_chapunit._work_file_name,
        file_text=agendaunit_shop(sue_text).get_json(),
    )

    # THEN
    assert os_path_exists(sue_work_path)
    assert work_file_exists(sue_chapunit)


def test_PersonUnit_save_work_file_CorrectlySavesFile(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_chapunit = chapunit_shop(None, None, sue_text)
    sue_chapunit = chapunit_shop(None, None, sue_text)
    assert work_file_exists(sue_chapunit)
    delete_dir(sue_person._work_path)
    assert work_file_exists(sue_chapunit) == False

    # WHEN
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    _save_work_file(sue_chapunit, sue_agenda)

    # THEN
    assert work_file_exists(sue_chapunit)

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
    _save_work_file(sue_chapunit, sue2_agenda)

    # THEN
    work_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_work_file_name)
    print(f"{work_file_text=}")
    work_agenda = agendaunit_get_from_json(work_file_text)
    assert work_agenda.get_party(zia_text) != None


def test_PersonUnit_save_work_file_RaisesErrorWhenAgenda_work_id_IsWrong(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_chapunit = chapunit_shop(None, None, sue_text)

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        _save_work_file(sue_chapunit, agendaunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"AgendaUnit with owner_id '{yao_text}' cannot be saved as person_id '{sue_text}''s work agenda."
    )


def test_PersonUnit_initialize_work_file_CorrectlySavesFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_chapunit = chapunit_shop(None, None, sue_text)
    assert work_file_exists(sue_chapunit)
    delete_dir(sue_person._work_path)
    assert work_file_exists(sue_chapunit) == False

    # WHEN
    initialize_work_file(sue_chapunit)

    # THEN
    work_agenda = get_work_file_agenda(sue_chapunit)
    assert work_agenda._real_id == get_test_real_id()
    assert work_agenda._owner_id == sue_text
    bob_text = "Bob"
    assert work_agenda.get_party(bob_text) is None

    # GIVEN
    sue_agenda = agendaunit_shop(sue_text)
    sue_agenda.add_partyunit(bob_text)
    _save_work_file(sue_chapunit, sue_agenda)
    work_agenda = get_work_file_agenda(sue_chapunit)
    assert work_agenda.get_party(bob_text)

    # WHEN
    initialize_work_file(sue_chapunit)

    # THEN
    work_agenda = get_work_file_agenda(sue_chapunit)
    assert work_agenda.get_party(bob_text)


def test_PersonUnit_initialize_work_file_CorrectlyDoesNotOverwrite(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_planck = 7
    sue_person = personunit_shop(person_id=sue_text, _planck=sue_planck)
    sue_chapunit = chapunit_shop(None, None, sue_text, x_planck=sue_planck)
    assert work_file_exists(sue_chapunit)
    delete_dir(sue_person._work_path)
    assert work_file_exists(sue_chapunit) == False

    # WHEN
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    initialize_work_file(sue_chapunit)

    # THEN
    assert work_file_exists(sue_chapunit)

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


def test_PersonUnit_create_core_dir_and_files_CreatesDirsAndFiles(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    delete_dir(sue_chapunit.real_dir)
    assert os_path_exists(sue_chapunit.real_dir) is False
    assert os_path_exists(sue_chapunit.persons_dir) is False
    assert os_path_exists(sue_chapunit.person_dir) is False
    assert os_path_exists(sue_chapunit._econs_dir) is False
    assert os_path_exists(sue_chapunit._atoms_dir) is False
    assert os_path_exists(sue_chapunit._gifts_dir) is False
    assert os_path_exists(sue_chapunit._duty_path) is False
    assert os_path_exists(sue_chapunit._work_path) is False

    # WHEN
    chap_create_core_dir_and_files(sue_chapunit)

    # THEN
    assert os_path_exists(sue_chapunit.real_dir)
    assert os_path_exists(sue_chapunit.persons_dir)
    assert os_path_exists(sue_chapunit.person_dir)
    assert os_path_exists(sue_chapunit._econs_dir)
    assert os_path_exists(sue_chapunit._atoms_dir)
    assert os_path_exists(sue_chapunit._gifts_dir)
    assert os_path_exists(sue_chapunit._duty_path)
    assert os_path_exists(sue_chapunit._work_path)
