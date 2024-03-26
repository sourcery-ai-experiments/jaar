from src._road.road import default_road_delimiter_if_none
from src._road.finance import default_planck_if_none
from src.agenda.agenda import agendaunit_shop, get_from_json as agenda_get_from_json
from src.world.person import (
    PersonUnit,
    personunit_shop,
    get_gut_file_name,
    get_live_file_name,
)
from pytest import raises as pytest_raises
from src.world.examples.world_env_kit import (
    get_test_worlds_dir,
    get_test_world_id,
    worlds_dir_setup_cleanup,
)
from os.path import exists as os_path_exists
from src.instrument.file import open_file, save_file, delete_dir


def test_get_gut_file_name():
    assert get_gut_file_name() == "gut"


def test_get_live_file_name():
    assert get_live_file_name() == "live"


def test_PersonUnit_exists():
    # GIVEN / WHEN
    x_person = PersonUnit()

    # THEN
    assert x_person.person_id is None
    assert x_person.world_id is None
    assert x_person.worlds_dir is None
    assert x_person.persons_dir is None
    assert x_person.person_dir is None
    assert x_person._econs_dir is None
    assert x_person._atoms_dir is None
    assert x_person._gifts_dir is None
    assert x_person._cycle_logs_dir is None
    assert x_person._save_cycle_logs is None
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
    assert x_person.world_id is None
    assert x_person.worlds_dir is None
    assert x_person.persons_dir is None
    assert x_person.person_dir is None
    assert x_person._gut_file_name is None
    assert x_person._gut_path is None
    assert x_person._live_file_name is None
    assert x_person._live_path is None
    assert x_person._econs_dir is None
    assert x_person._atoms_dir is None
    assert x_person._gifts_dir is None
    assert x_person._cycle_logs_dir is None
    assert x_person._save_cycle_logs is None

    # GIVEN
    yao_text = "Yao"
    x_person.set_person_id(yao_text)

    # THEN
    assert x_person.person_id == yao_text
    assert x_person.world_id == get_test_world_id()
    assert x_person.worlds_dir == get_test_worlds_dir()
    assert x_person.persons_dir == f"{x_person.world_dir}/persons"
    assert x_person.person_dir == f"{x_person.persons_dir}/{yao_text}"
    assert x_person._gut_file_name == f"{get_gut_file_name()}.json"
    assert x_person._gut_path == f"{x_person.person_dir}/{x_person._gut_file_name}"
    assert x_person._live_file_name == f"{get_live_file_name()}.json"
    assert x_person._live_path == f"{x_person.person_dir}/{x_person._live_file_name}"
    assert x_person._econs_dir == f"{x_person.person_dir}/econs"
    assert x_person._atoms_dir == f"{x_person.person_dir}/atoms"
    assert x_person._gifts_dir == f"{x_person.person_dir}/gifts"
    assert x_person._cycle_logs_dir == f"{x_person.person_dir}/cycle_logs"
    assert x_person._save_cycle_logs is None


def test_PersonUnit_set_person_id_RaisesErrorIf_person_id_Contains_road_delimiter(
    worlds_dir_setup_cleanup,
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


def test_personunit_shop_ReturnsCorrectPersonUnit(worlds_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    x_worlds_dir = "/worlds1"
    x_world_id = "froopiland"

    # WHEN
    sue_person = personunit_shop(
        person_id=sue_text, world_id=x_world_id, worlds_dir=x_worlds_dir
    )

    # THEN
    assert sue_person.person_id == sue_text
    assert sue_person.world_id == x_world_id
    assert sue_person.worlds_dir == x_worlds_dir
    assert sue_person.world_dir == f"{sue_person.worlds_dir}/{sue_person.world_id}"
    assert sue_person.persons_dir == f"{sue_person.world_dir}/persons"
    assert sue_person.person_dir == f"{sue_person.persons_dir}/{sue_text}"
    assert sue_person._econs_dir == f"{sue_person.person_dir}/econs"
    assert sue_person._gut_file_name == f"{get_gut_file_name()}.json"
    sue_gut_file_path = f"{sue_person.person_dir}/{sue_person._gut_file_name}"
    assert sue_person._gut_path == sue_gut_file_path
    assert sue_person._live_file_name == f"{get_live_file_name()}.json"
    sue_live_file_path = f"{sue_person.person_dir}/{sue_person._live_file_name}"
    assert sue_person._live_path == sue_live_file_path
    assert sue_person._cycle_logs_dir != None
    assert sue_person._save_cycle_logs == False
    assert sue_person._econ_objs == {}
    assert sue_person._road_delimiter == default_road_delimiter_if_none()
    assert sue_person._planck == default_planck_if_none()


def test_personunit_shop_ReturnsCorrectPersonUnitWhenGivenEmptyWorldParameters(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    slash_text = "/"
    two_int = 2

    # WHEN
    sue_person = personunit_shop(
        person_id=sue_text, _road_delimiter=slash_text, _planck=two_int
    )

    # THEN
    assert sue_person.person_id == sue_text
    assert sue_person.world_id == get_test_world_id()
    assert sue_person.worlds_dir == get_test_worlds_dir()
    assert sue_person.world_dir == f"{sue_person.worlds_dir}/{sue_person.world_id}"
    assert sue_person.persons_dir == f"{sue_person.world_dir}/persons"
    assert sue_person.person_dir == f"{sue_person.persons_dir}/{sue_text}"
    assert sue_person._gut_file_name == f"{get_gut_file_name()}.json"
    sue_gut_file_path = f"{sue_person.person_dir}/{sue_person._gut_file_name}"
    assert sue_person._gut_path == sue_gut_file_path
    assert sue_person._live_file_name == f"{get_live_file_name()}.json"
    sue_live_file_path = f"{sue_person.person_dir}/{sue_person._live_file_name}"
    assert sue_person._live_path == sue_live_file_path
    assert sue_person._road_delimiter == slash_text
    assert sue_person._planck == two_int


def test_PersonUnit_gut_file_exists_ReturnsCorrectBool(worlds_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_world_dir = f"{get_test_worlds_dir()}/{get_test_world_id()}"
    sue_persons_dir = f"{sue_world_dir}/persons"
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


def test_PersonUnit_save_gut_file_CorrectlySavesFile(worlds_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_world_dir = f"{get_test_worlds_dir()}/{get_test_world_id()}"
    sue_persons_dir = f"{sue_world_dir}/persons"
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
    sue_person._save_gut_file(sue_agenda)

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
    sue_person._save_gut_file(sue2_agenda)

    # THEN
    gut_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_gut_file_name)
    print(f"{gut_file_text=}")
    gut_agenda = agenda_get_from_json(gut_file_text)
    assert gut_agenda.get_party(zia_text) != None


def test_PersonUnit_save_gut_file_RaisesErrorWhenAgenda_live_id_IsWrong(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        sue_person._save_gut_file(agendaunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"AgendaUnit with owner_id '{yao_text}' cannot be saved as person_id '{sue_text}''s gut agenda."
    )


def test_PersonUnit_load_gut_file_CorrectlyLoads_gut_obj(worlds_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    sue_person._save_gut_file(sue_agenda)
    assert sue_person._gut_obj is None

    # WHEN
    sue_person.load_gut_file()

    # THEN
    assert sue_person._gut_obj != None
    assert sue_person._gut_obj.get_party(bob_text) != None
    assert sue_person._gut_obj.get_party("Zia") is None


def test_PersonUnit_create_gut_file_if_does_not_exist_CorrectlySavesFile(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    assert sue_person.gut_file_exists()
    delete_dir(sue_person._gut_path)
    assert sue_person.gut_file_exists() == False

    # WHEN
    sue_person.create_gut_file_if_does_not_exist()

    # THEN
    gut_agenda = sue_person.get_gut_file_agenda()
    assert gut_agenda._world_id == get_test_world_id()
    assert gut_agenda._owner_id == sue_text
    bob_text = "Bob"
    assert gut_agenda.get_party(bob_text) is None

    # GIVEN
    sue_agenda = agendaunit_shop(sue_text)
    sue_agenda.add_partyunit(bob_text)
    sue_person._save_gut_file(sue_agenda)
    gut_agenda = sue_person.get_gut_file_agenda()
    assert gut_agenda.get_party(bob_text)

    # WHEN
    sue_person.create_gut_file_if_does_not_exist()

    # THEN
    gut_agenda = sue_person.get_gut_file_agenda()
    assert gut_agenda.get_party(bob_text)


def test_PersonUnit_create_gut_file_if_does_not_exist_CorrectlyDoesNotOverwrite(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_world_dir = f"{get_test_worlds_dir()}/{get_test_world_id()}"
    sue_person = personunit_shop(person_id=sue_text)
    assert sue_person.gut_file_exists()
    delete_dir(sue_person._gut_path)
    assert sue_person.gut_file_exists() == False

    # WHEN
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    sue_person.create_gut_file_if_does_not_exist()

    # THEN
    assert sue_person.gut_file_exists()

    sue_world_dir = f"{get_test_worlds_dir()}/{get_test_world_id()}"
    sue_persons_dir = f"{sue_world_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_gut_file_name = f"{get_gut_file_name()}.json"
    gut_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_gut_file_name)
    print(f"{gut_file_text=}")
    gut_agenda = agenda_get_from_json(gut_file_text)
    assert gut_agenda._world_id == get_test_world_id()
    assert gut_agenda._owner_id == sue_text


def test_PersonUnit_live_file_exists_ReturnsCorrectBool(worlds_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_world_dir = f"{get_test_worlds_dir()}/{get_test_world_id()}"
    sue_persons_dir = f"{sue_world_dir}/persons"
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


def test_PersonUnit_save_live_file_CorrectlySavesFile(
    worlds_dir_setup_cleanup,
):
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

    sue_world_dir = f"{get_test_worlds_dir()}/{get_test_world_id()}"
    sue_persons_dir = f"{sue_world_dir}/persons"
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
    worlds_dir_setup_cleanup,
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
    worlds_dir_setup_cleanup,
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
    worlds_dir_setup_cleanup,
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
    assert live_agenda._world_id == get_test_world_id()
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
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_world_dir = f"{get_test_worlds_dir()}/{get_test_world_id()}"
    sue_person = personunit_shop(person_id=sue_text)
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

    sue_world_dir = f"{get_test_worlds_dir()}/{get_test_world_id()}"
    sue_persons_dir = f"{sue_world_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_live_file_name = f"{get_live_file_name()}.json"
    live_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_live_file_name)
    print(f"{live_file_text=}")
    live_agenda = agenda_get_from_json(live_file_text)
    assert live_agenda._world_id == get_test_world_id()
    assert live_agenda._owner_id == sue_text


def test_PersonUnit_create_core_dir_and_files_CreatesDirsAndFiles(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    delete_dir(sue_person.world_dir)
    assert os_path_exists(sue_person.world_dir) is False
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
    assert os_path_exists(sue_person.world_dir)
    assert os_path_exists(sue_person.persons_dir)
    assert os_path_exists(sue_person.person_dir)
    assert os_path_exists(sue_person._econs_dir)
    assert os_path_exists(sue_person._atoms_dir)
    assert os_path_exists(sue_person._gifts_dir)
    assert os_path_exists(sue_person._gut_path)
    assert os_path_exists(sue_person._live_path)
