from src.agenda.agenda import (
    agendaunit_shop,
    get_from_json as agendaunit_get_from_json,
    duty_str,
    work_str,
)
from src.real.user import (
    userunit_shop,
    duty_file_exists,
    work_file_exists,
    _save_work_file,
    initialize_work_file,
    save_duty_file,
    get_duty_file_agenda,
    initialize_change_and_duty_files,
    userunit_create_core_dir_and_files,
    get_work_file_agenda,
)
from src.real.change import init_change_id
from src.real.examples.real_env_kit import (
    get_test_reals_dir,
    get_test_real_id,
    reals_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists
from src._instrument.file import open_file, save_file, delete_dir


def test_EngineUnit_duty_file_exists_ReturnsCorrectBool(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_duty_file_name = f"{duty_str()}.json"
    sue_duty_path = f"{sue_person_dir}/{sue_duty_file_name}"
    print(f"{sue_duty_path=}")
    assert os_path_exists(sue_duty_path) == False
    sue_userunit = userunit_shop(None, None, sue_text)
    userunit_create_core_dir_and_files(sue_userunit)
    assert os_path_exists(sue_duty_path)
    assert duty_file_exists(sue_userunit)
    delete_dir(sue_duty_path)
    assert os_path_exists(sue_duty_path) == False
    assert duty_file_exists(sue_userunit) == False

    # WHEN
    save_file(
        dest_dir=sue_userunit.person_dir,
        file_name=sue_userunit._duty_file_name,
        file_text=agendaunit_shop(sue_text).get_json(),
    )

    # THEN
    assert os_path_exists(sue_duty_path)
    assert duty_file_exists(sue_userunit)


def test_EngineUnit_save_duty_file_CorrectlySavesFile(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_duty_file_name = f"{duty_str()}.json"
    sue_duty_path = f"{sue_person_dir}/{sue_duty_file_name}"

    # WHEN
    sue_userunit = userunit_shop(None, None, sue_text)
    userunit_create_core_dir_and_files(sue_userunit)

    # THEN
    assert duty_file_exists(sue_userunit)

    # GIVEN
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    delete_dir(sue_duty_path)
    assert duty_file_exists(sue_userunit) == False

    # WHEN
    save_duty_file(sue_userunit, sue_agenda)

    # THEN
    assert duty_file_exists(sue_userunit)

    # GIVEN
    duty_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_duty_file_name)
    print(f"{duty_file_text=}")
    duty_agenda = agendaunit_get_from_json(duty_file_text)
    assert duty_agenda.get_party(bob_text) != None

    # WHEN
    sue2_agenda = agendaunit_shop(sue_text)
    zia_text = "Zia"
    sue2_agenda.add_partyunit(zia_text)
    save_duty_file(sue_userunit, sue2_agenda)

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
    sue_userunit = userunit_shop(None, None, sue_text)

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        save_duty_file(sue_userunit, agendaunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"AgendaUnit with owner_id '{yao_text}' cannot be saved as person_id '{sue_text}''s duty agenda."
    )


def test_EngineUnit_initialize_change_and_duty_files_CorrectlySavesDutyFileAndchangeFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userunit = userunit_shop(None, None, sue_text, None, planck=seven_int)
    userunit_create_core_dir_and_files(sue_userunit)
    assert duty_file_exists(sue_userunit)
    delete_dir(sue_userunit._duty_path)
    assert duty_file_exists(sue_userunit) == False
    init_change_file_path = f"{sue_userunit._changes_dir}/{init_change_id()}.json"
    delete_dir(sue_userunit._changes_dir)
    assert os_path_exists(init_change_file_path) == False

    # WHEN
    initialize_change_and_duty_files(sue_userunit)

    # THEN
    duty_agenda = get_duty_file_agenda(sue_userunit)
    assert duty_agenda._real_id == get_test_real_id()
    assert duty_agenda._owner_id == sue_text
    assert duty_agenda._planck == seven_int
    assert os_path_exists(init_change_file_path)


def test_EngineUnit_initialize_change_and_duty_files_CorrectlySavesOnlyDutyFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userunit = userunit_shop(None, None, sue_text, None, planck=seven_int)
    userunit_create_core_dir_and_files(sue_userunit)
    assert duty_file_exists(sue_userunit)
    delete_dir(sue_userunit._duty_path)
    assert duty_file_exists(sue_userunit) == False
    init_change_file_path = f"{sue_userunit._changes_dir}/{init_change_id()}.json"
    assert os_path_exists(init_change_file_path)

    # WHEN
    initialize_change_and_duty_files(sue_userunit)

    # THEN
    duty_agenda = get_duty_file_agenda(sue_userunit)
    assert duty_agenda._real_id == get_test_real_id()
    assert duty_agenda._owner_id == sue_text
    assert duty_agenda._planck == seven_int
    assert os_path_exists(init_change_file_path)


def test_EngineUnit_initialize_change_and_duty_files_CorrectlySavesOnlychangeFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userunit = userunit_shop(None, None, sue_text, None, planck=seven_int)
    userunit_create_core_dir_and_files(sue_userunit)
    sue_duty_agenda = get_duty_file_agenda(sue_userunit)
    bob_text = "Bob"
    sue_duty_agenda.add_partyunit(bob_text)
    save_duty_file(sue_userunit, sue_duty_agenda)
    assert duty_file_exists(sue_userunit)
    init_change_file_path = f"{sue_userunit._changes_dir}/{init_change_id()}.json"
    delete_dir(sue_userunit._changes_dir)
    assert os_path_exists(init_change_file_path) == False

    # WHEN
    initialize_change_and_duty_files(sue_userunit)

    # THEN
    assert sue_duty_agenda._real_id == get_test_real_id()
    assert sue_duty_agenda._owner_id == sue_text
    assert sue_duty_agenda._planck == seven_int
    assert sue_duty_agenda.get_party(bob_text) != None
    assert os_path_exists(init_change_file_path)


# def test_EngineUnit_initialize_change_and_duty_files_CorrectlyDoesNotOverwrite(
#     reals_dir_setup_cleanup,
# ):
#     # GIVEN
#     sue_text = "Sue"
#     sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
#     sue_userunit = userunit_shop(None, None, sue_text)
# sue_userunit = sue_userunit
#     assert sue_person.duty_file_exists()
#     delete_dir(sue_person._duty_path)
#     assert sue_person.duty_file_exists() == False

#     # WHEN
#     sue_agenda = agendaunit_shop(sue_text)
#     bob_text = "Bob"
#     sue_agenda.add_partyunit(bob_text)
#     initialize_change_and_duty_files()

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
    sue_userunit = userunit_shop(None, None, sue_text)
    userunit_create_core_dir_and_files(sue_userunit)
    assert work_file_exists(sue_userunit)
    delete_dir(sue_userunit._work_path)
    assert os_path_exists(sue_work_path) == False
    assert work_file_exists(sue_userunit) == False

    # WHEN
    save_file(
        dest_dir=sue_userunit.person_dir,
        file_name=sue_userunit._work_file_name,
        file_text=agendaunit_shop(sue_text).get_json(),
    )

    # THEN
    assert os_path_exists(sue_work_path)
    assert work_file_exists(sue_userunit)


def test_EngineUnit_save_work_file_CorrectlySavesFile(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userunit = userunit_shop(None, None, sue_text)
    userunit_create_core_dir_and_files(sue_userunit)
    assert work_file_exists(sue_userunit)
    delete_dir(sue_userunit._work_path)
    assert work_file_exists(sue_userunit) == False

    # WHEN
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    _save_work_file(sue_userunit, sue_agenda)

    # THEN
    assert work_file_exists(sue_userunit)

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
    _save_work_file(sue_userunit, sue2_agenda)

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
    sue_userunit = userunit_shop(None, None, sue_text)

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        _save_work_file(sue_userunit, agendaunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"AgendaUnit with owner_id '{yao_text}' cannot be saved as person_id '{sue_text}''s work agenda."
    )


def test_EngineUnit_initialize_work_file_CorrectlySavesFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userunit = userunit_shop(None, None, sue_text)
    userunit_create_core_dir_and_files(sue_userunit)
    assert work_file_exists(sue_userunit)
    delete_dir(sue_userunit._work_path)
    assert work_file_exists(sue_userunit) == False

    # WHEN
    initialize_work_file(sue_userunit)

    # THEN
    work_agenda = get_work_file_agenda(sue_userunit)
    assert work_agenda._real_id == get_test_real_id()
    assert work_agenda._owner_id == sue_text
    bob_text = "Bob"
    assert work_agenda.get_party(bob_text) is None

    # GIVEN
    sue_agenda = agendaunit_shop(sue_text)
    sue_agenda.add_partyunit(bob_text)
    _save_work_file(sue_userunit, sue_agenda)
    work_agenda = get_work_file_agenda(sue_userunit)
    assert work_agenda.get_party(bob_text)

    # WHEN
    initialize_work_file(sue_userunit)

    # THEN
    work_agenda = get_work_file_agenda(sue_userunit)
    assert work_agenda.get_party(bob_text)


def test_EngineUnit_initialize_work_file_CorrectlyDoesNotOverwrite(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_planck = 7
    sue_userunit = userunit_shop(None, None, sue_text, None, planck=sue_planck)
    userunit_create_core_dir_and_files(sue_userunit)
    assert work_file_exists(sue_userunit)
    delete_dir(sue_userunit._work_path)
    assert work_file_exists(sue_userunit) == False

    # WHEN
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    initialize_work_file(sue_userunit)

    # THEN
    assert work_file_exists(sue_userunit)

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
