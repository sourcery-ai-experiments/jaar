from src._road.road import default_road_delimiter_if_none
from src._road.finance import default_planck_if_none
from src.agenda.agenda import agendaunit_shop, get_from_json as agenda_get_from_json
from src.real.gift import init_gift_id, get_gifts_folder
from src.real.person import (
    PersonUnit,
    personunit_shop,
    get_gut_file_name,
    get_live_file_name,
)
from pytest import raises as pytest_raises
from src.real.examples.real_env_kit import (
    get_test_reals_dir,
    get_test_real_id,
    reals_dir_setup_cleanup,
)
from os.path import exists as os_path_exists
from src._instrument.file import open_file, save_file, delete_dir


def test_get_gut_file_name():
    assert get_gut_file_name() == "gut"


def test_get_live_file_name():
    assert get_live_file_name() == "live"


def test_PersonUnit_exists():
    # GIVEN / WHEN
    x_person = PersonUnit()

    # THEN
    assert x_person.person_id is None
    assert x_person.real_id is None
    assert x_person.reals_dir is None
    assert x_person.persons_dir is None
    assert x_person.person_dir is None
    assert x_person._econs_dir is None
    assert x_person._atoms_dir is None
    assert x_person._gifts_dir is None
    assert x_person._gut_obj is None
    assert x_person._gut_file_name is None
    assert x_person._gut_path is None
    assert x_person._live_obj is None
    assert x_person._live_file_name is None
    assert x_person._live_path is None
    assert x_person._econ_objs is None
    assert x_person._road_delimiter is None
    assert x_person._planck is None


def test_PersonUnit_set_person_id_CorrectlySetsAttr():
    # GIVEN / WHEN
    x_person = PersonUnit()
    assert x_person.person_id is None
    assert x_person.real_id is None
    assert x_person.reals_dir is None
    assert x_person.persons_dir is None
    assert x_person.person_dir is None
    assert x_person._gut_file_name is None
    assert x_person._gut_path is None
    assert x_person._live_file_name is None
    assert x_person._live_path is None
    assert x_person._econs_dir is None
    assert x_person._atoms_dir is None
    assert x_person._gifts_dir is None

    # GIVEN
    yao_text = "Yao"
    x_person.set_person_id(yao_text)

    # THEN
    assert x_person.person_id == yao_text
    assert x_person.real_id == get_test_real_id()
    assert x_person.reals_dir == get_test_reals_dir()
    assert x_person.persons_dir == f"{x_person.real_dir}/persons"
    assert x_person.person_dir == f"{x_person.persons_dir}/{yao_text}"
    assert x_person._gut_file_name == f"{get_gut_file_name()}.json"
    assert x_person._gut_path == f"{x_person.person_dir}/{x_person._gut_file_name}"
    assert x_person._live_file_name == f"{get_live_file_name()}.json"
    assert x_person._live_path == f"{x_person.person_dir}/{x_person._live_file_name}"
    assert x_person._econs_dir == f"{x_person.person_dir}/econs"
    assert x_person._atoms_dir == f"{x_person.person_dir}/atoms"
    assert x_person._gifts_dir == f"{x_person.person_dir}/{get_gifts_folder()}"


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
    assert sue_person.person_id == sue_text
    assert sue_person.real_id == x_real_id
    assert sue_person.reals_dir == x_reals_dir
    assert sue_person.real_dir == f"{sue_person.reals_dir}/{sue_person.real_id}"
    assert sue_person.persons_dir == f"{sue_person.real_dir}/persons"
    assert sue_person.person_dir == f"{sue_person.persons_dir}/{sue_text}"
    assert sue_person._econs_dir == f"{sue_person.person_dir}/econs"
    assert sue_person._gut_file_name == f"{get_gut_file_name()}.json"
    sue_gut_file_path = f"{sue_person.person_dir}/{sue_person._gut_file_name}"
    assert sue_person._gut_path == sue_gut_file_path
    assert sue_person._live_file_name == f"{get_live_file_name()}.json"
    sue_live_file_path = f"{sue_person.person_dir}/{sue_person._live_file_name}"
    assert sue_person._live_path == sue_live_file_path
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

    # THEN
    assert sue_person.person_id == sue_text
    assert sue_person.real_id == get_test_real_id()
    assert sue_person.reals_dir == get_test_reals_dir()
    assert sue_person.real_dir == f"{sue_person.reals_dir}/{sue_person.real_id}"
    assert sue_person.persons_dir == f"{sue_person.real_dir}/persons"
    assert sue_person.person_dir == f"{sue_person.persons_dir}/{sue_text}"
    assert sue_person._gut_file_name == f"{get_gut_file_name()}.json"
    sue_gut_file_path = f"{sue_person.person_dir}/{sue_person._gut_file_name}"
    assert sue_person._gut_path == sue_gut_file_path
    assert sue_person._live_file_name == f"{get_live_file_name()}.json"
    sue_live_file_path = f"{sue_person.person_dir}/{sue_person._live_file_name}"
    assert sue_person._live_path == sue_live_file_path
    assert sue_person._road_delimiter == slash_text
    assert sue_person._planck == two_int


def test_PersonUnit_gut_file_exists_ReturnsCorrectBool(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_gut_file_name = f"{get_gut_file_name()}.json"
    sue_gut_path = f"{sue_person_dir}/{sue_gut_file_name}"
    print(f"{sue_gut_path=}")
    assert os_path_exists(sue_gut_path) == False
    sue_person = personunit_shop(person_id=sue_text)
    assert os_path_exists(sue_gut_path)
    assert sue_person.gut_file_exists()
    delete_dir(sue_gut_path)
    assert os_path_exists(sue_gut_path) == False
    assert sue_person.gut_file_exists() == False

    # WHEN
    save_file(
        dest_dir=sue_person.person_dir,
        file_name=sue_person._gut_file_name,
        file_text=agendaunit_shop(sue_text).get_json(),
    )

    # THEN
    assert os_path_exists(sue_gut_path)
    assert sue_person.gut_file_exists()


def test_PersonUnitsave_gut_file_CorrectlySavesFile(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_gut_file_name = f"{get_gut_file_name()}.json"
    sue_gut_path = f"{sue_person_dir}/{sue_gut_file_name}"

    # WHEN
    sue_person = personunit_shop(person_id=sue_text)

    # THEN
    assert sue_person.gut_file_exists()

    # GIVEN
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    delete_dir(sue_gut_path)
    assert sue_person.gut_file_exists() == False

    # WHEN
    sue_person.save_gut_file(sue_agenda)

    # THEN
    assert sue_person.gut_file_exists()

    # GIVEN
    gut_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_gut_file_name)
    print(f"{gut_file_text=}")
    gut_agenda = agenda_get_from_json(gut_file_text)
    assert gut_agenda.get_party(bob_text) != None

    # WHEN
    sue2_agenda = agendaunit_shop(sue_text)
    zia_text = "Zia"
    sue2_agenda.add_partyunit(zia_text)
    sue_person.save_gut_file(sue2_agenda)

    # THEN
    gut_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_gut_file_name)
    print(f"{gut_file_text=}")
    gut_agenda = agenda_get_from_json(gut_file_text)
    assert gut_agenda.get_party(zia_text) != None


def test_PersonUnitsave_gut_file_RaisesErrorWhenAgenda_live_id_IsWrong(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        sue_person.save_gut_file(agendaunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"AgendaUnit with owner_id '{yao_text}' cannot be saved as person_id '{sue_text}''s gut agenda."
    )


def test_PersonUnit_load_gut_file_CorrectlyLoads_gut_obj(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    sue_person.save_gut_file(sue_agenda)
    assert sue_person._gut_obj is None

    # WHEN
    sue_person.load_gut_file()

    # THEN
    assert sue_person._gut_obj != None
    assert sue_person._gut_obj.get_party(bob_text) != None
    assert sue_person._gut_obj.get_party("Zia") is None


def test_PersonUnit_initialize_gift_and_gut_files_CorrectlySavesGutFileAndGiftFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_person = personunit_shop(person_id=sue_text, _planck=seven_int)
    assert sue_person.gut_file_exists()
    delete_dir(sue_person._gut_path)
    assert sue_person.gut_file_exists() == False
    init_gift_file_path = f"{sue_person._gifts_dir}/{init_gift_id()}.json"
    delete_dir(sue_person._gifts_dir)
    assert os_path_exists(init_gift_file_path) == False

    # WHEN
    sue_person.initialize_gift_and_gut_files()

    # THEN
    gut_agenda = sue_person.get_gut_file_agenda()
    assert gut_agenda._real_id == get_test_real_id()
    assert gut_agenda._owner_id == sue_text
    assert gut_agenda._planck == seven_int
    assert os_path_exists(init_gift_file_path)


def test_PersonUnit_initialize_gift_and_gut_files_CorrectlySavesOnlyGutFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_person = personunit_shop(person_id=sue_text, _planck=seven_int)
    assert sue_person.gut_file_exists()
    delete_dir(sue_person._gut_path)
    assert sue_person.gut_file_exists() == False
    init_gift_file_path = f"{sue_person._gifts_dir}/{init_gift_id()}.json"
    assert os_path_exists(init_gift_file_path)

    # WHEN
    sue_person.initialize_gift_and_gut_files()

    # THEN
    gut_agenda = sue_person.get_gut_file_agenda()
    assert gut_agenda._real_id == get_test_real_id()
    assert gut_agenda._owner_id == sue_text
    assert gut_agenda._planck == seven_int
    assert os_path_exists(init_gift_file_path)


def test_PersonUnit_initialize_gift_and_gut_files_CorrectlySavesOnlyGiftFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_person = personunit_shop(sue_text, _planck=seven_int)
    sue_gut_agenda = sue_person.get_gut_file_agenda()
    bob_text = "Bob"
    sue_gut_agenda.add_partyunit(bob_text)
    sue_person.save_gut_file(sue_gut_agenda)
    assert sue_person.gut_file_exists()
    init_gift_file_path = f"{sue_person._gifts_dir}/{init_gift_id()}.json"
    delete_dir(sue_person._gifts_dir)
    assert os_path_exists(init_gift_file_path) == False

    # WHEN
    sue_person.initialize_gift_and_gut_files()

    # THEN
    assert sue_gut_agenda._real_id == get_test_real_id()
    assert sue_gut_agenda._owner_id == sue_text
    assert sue_gut_agenda._planck == seven_int
    assert sue_gut_agenda.get_party(bob_text) != None
    assert os_path_exists(init_gift_file_path)


# def test_PersonUnit_initialize_gift_and_gut_files_CorrectlyDoesNotOverwrite(
#     reals_dir_setup_cleanup,
# ):
#     # GIVEN
#     sue_text = "Sue"
#     sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
#     sue_person = personunit_shop(person_id=sue_text)
#     assert sue_person.gut_file_exists()
#     delete_dir(sue_person._gut_path)
#     assert sue_person.gut_file_exists() == False

#     # WHEN
#     sue_agenda = agendaunit_shop(sue_text)
#     bob_text = "Bob"
#     sue_agenda.add_partyunit(bob_text)
#     sue_person.initialize_gift_and_gut_files()

#     # THEN
#     assert sue_person.gut_file_exists()

#     sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
#     sue_persons_dir = f"{sue_real_dir}/persons"
#     sue_person_dir = f"{sue_persons_dir}/{sue_text}"
#     sue_gut_file_name = f"{get_gut_file_name()}.json"
#     gut_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_gut_file_name)
#     print(f"{gut_file_text=}")
#     gut_agenda = agenda_get_from_json(gut_file_text)
#     assert gut_agenda._real_id == get_test_real_id()
#     assert gut_agenda._owner_id == sue_text


def test_PersonUnit_live_file_exists_ReturnsCorrectBool(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_live_file_name = f"{get_live_file_name()}.json"
    sue_live_path = f"{sue_person_dir}/{sue_live_file_name}"
    print(f"{sue_live_path=}")
    assert os_path_exists(sue_live_path) == False
    sue_person = personunit_shop(person_id=sue_text)
    assert sue_person.live_file_exists()
    delete_dir(sue_person._live_path)
    assert os_path_exists(sue_live_path) == False
    assert sue_person.live_file_exists() == False

    # WHEN
    save_file(
        dest_dir=sue_person.person_dir,
        file_name=sue_person._live_file_name,
        file_text=agendaunit_shop(sue_text).get_json(),
    )

    # THEN
    assert os_path_exists(sue_live_path)
    assert sue_person.live_file_exists()


def test_PersonUnit_save_live_file_CorrectlySavesFile(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    assert sue_person.live_file_exists()
    delete_dir(sue_person._live_path)
    assert sue_person.live_file_exists() == False

    # WHEN
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    sue_person._save_live_file(sue_agenda)

    # THEN
    assert sue_person.live_file_exists()

    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_live_file_name = f"{get_live_file_name()}.json"
    live_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_live_file_name)
    print(f"{live_file_text=}")
    live_agenda = agenda_get_from_json(live_file_text)
    assert live_agenda.get_party(bob_text) != None

    # # WHEN
    sue2_agenda = agendaunit_shop(sue_text)
    zia_text = "Zia"
    sue2_agenda.add_partyunit(zia_text)
    sue_person._save_live_file(sue2_agenda)

    # THEN
    live_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_live_file_name)
    print(f"{live_file_text=}")
    live_agenda = agenda_get_from_json(live_file_text)
    assert live_agenda.get_party(zia_text) != None


def test_PersonUnit_save_live_file_RaisesErrorWhenAgenda_live_id_IsWrong(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        sue_person._save_live_file(agendaunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"AgendaUnit with owner_id '{yao_text}' cannot be saved as person_id '{sue_text}''s live agenda."
    )


def test_PersonUnit_load_live_file_CorrectlyLoads_live_obj(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    sue_person._save_live_file(sue_agenda)
    assert sue_person._live_obj is None

    # WHEN
    sue_person.load_live_file()

    # THEN
    assert sue_person._live_obj != None
    assert sue_person._live_obj.get_party(bob_text) != None
    assert sue_person._live_obj.get_party("Zia") is None


def test_PersonUnit_create_live_file_if_does_not_exist_CorrectlySavesFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    assert sue_person.live_file_exists()
    delete_dir(sue_person._live_path)
    assert sue_person.live_file_exists() == False

    # WHEN
    sue_person.create_live_file_if_does_not_exist()

    # THEN
    live_agenda = sue_person.get_live_file_agenda()
    assert live_agenda._real_id == get_test_real_id()
    assert live_agenda._owner_id == sue_text
    bob_text = "Bob"
    assert live_agenda.get_party(bob_text) is None

    # GIVEN
    sue_agenda = agendaunit_shop(sue_text)
    sue_agenda.add_partyunit(bob_text)
    sue_person._save_live_file(sue_agenda)
    live_agenda = sue_person.get_live_file_agenda()
    assert live_agenda.get_party(bob_text)

    # WHEN
    sue_person.create_live_file_if_does_not_exist()

    # THEN
    live_agenda = sue_person.get_live_file_agenda()
    assert live_agenda.get_party(bob_text)


def test_PersonUnit_create_live_file_if_does_not_exist_CorrectlyDoesNotOverwrite(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_planck = 7
    sue_person = personunit_shop(person_id=sue_text, _planck=sue_planck)
    assert sue_person.live_file_exists()
    delete_dir(sue_person._live_path)
    assert sue_person.live_file_exists() == False

    # WHEN
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    sue_person.create_live_file_if_does_not_exist()

    # THEN
    assert sue_person.live_file_exists()

    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_live_file_name = f"{get_live_file_name()}.json"
    live_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_live_file_name)
    print(f"{live_file_text=}")
    live_agenda = agenda_get_from_json(live_file_text)
    assert live_agenda._real_id == get_test_real_id()
    assert live_agenda._owner_id == sue_text
    assert live_agenda._planck == sue_planck


def test_PersonUnit_create_core_dir_and_files_CreatesDirsAndFiles(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    delete_dir(sue_person.real_dir)
    assert os_path_exists(sue_person.real_dir) is False
    assert os_path_exists(sue_person.persons_dir) is False
    assert os_path_exists(sue_person.person_dir) is False
    assert os_path_exists(sue_person._econs_dir) is False
    assert os_path_exists(sue_person._atoms_dir) is False
    assert os_path_exists(sue_person._gifts_dir) is False
    assert os_path_exists(sue_person._gut_path) is False
    assert os_path_exists(sue_person._live_path) is False

    # WHEN
    sue_person.create_core_dir_and_files()

    # THEN
    assert os_path_exists(sue_person.real_dir)
    assert os_path_exists(sue_person.persons_dir)
    assert os_path_exists(sue_person.person_dir)
    assert os_path_exists(sue_person._econs_dir)
    assert os_path_exists(sue_person._atoms_dir)
    assert os_path_exists(sue_person._gifts_dir)
    assert os_path_exists(sue_person._gut_path)
    assert os_path_exists(sue_person._live_path)
