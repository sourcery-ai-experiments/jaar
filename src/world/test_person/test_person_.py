from src._prime.road import (
    default_road_delimiter_if_none,
    get_all_road_nodes,
)
from src.agenda.agenda import agendaunit_shop, get_from_json as agenda_get_from_json
from src.world.person import PersonUnit, personunit_shop
from pytest import raises as pytest_raises
from src.world.examples.world_env_kit import (
    get_test_worlds_dir,
    get_test_world_id,
    worlds_dir_setup_cleanup,
)
from os.path import exists as os_path_exists, isdir as os_path_isdir
from src.instrument.file import (
    delete_dir,
    dir_files,
    open_file,
    set_dir,
    save_file,
)


def test_PersonUnit_exists():
    # GIVEN / WHEN
    x_person = PersonUnit()

    # THEN
    assert x_person.person_id is None
    assert x_person.world_id is None
    assert x_person.worlds_dir is None
    assert x_person.persons_dir is None
    assert x_person.person_dir is None
    assert x_person._markets_dir is None
    assert x_person._gut_obj is None
    assert x_person._gut_file_name is None
    assert x_person._gut_path is None
    assert x_person._market_objs is None
    assert x_person._road_delimiter is None


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
    assert x_person._markets_dir is None

    # GIVEN
    yao_text = "Yao"
    x_person.set_person_id(yao_text)

    # THEN
    assert x_person.person_id == yao_text
    assert x_person.world_id == get_test_world_id()
    assert x_person.worlds_dir == get_test_worlds_dir()
    assert x_person.persons_dir == f"{x_person.world_dir}/persons"
    assert x_person.person_dir == f"{x_person.persons_dir}/{yao_text}"
    assert x_person._gut_file_name == "gut.json"
    assert x_person._gut_path == f"{x_person.person_dir}/{x_person._gut_file_name}"
    assert x_person._markets_dir == f"{x_person.person_dir}/markets"


def test_PersonUnit_set_person_id_RaisesErrorIf_person_id_Contains_road_delimiter():
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


def test_personunit_shop_ReturnsCorrectPersonUnit():
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
    assert sue_person._markets_dir == f"{sue_person.person_dir}/markets"
    assert sue_person._gut_file_name == "gut.json"
    sue_gut_file_path = f"{sue_person.person_dir}/{sue_person._gut_file_name}"
    assert sue_person._gut_path == sue_gut_file_path
    assert sue_person._market_objs == {}
    assert sue_person._road_delimiter == default_road_delimiter_if_none()


def test_personunit_shop_ReturnsCorrectPersonUnitWhenGivenEmptyWorldParameters():
    # GIVEN
    sue_text = "Sue"
    slash_text = "/"

    # WHEN
    sue_person = personunit_shop(person_id=sue_text, _road_delimiter=slash_text)

    # THEN
    assert sue_person.person_id == sue_text
    assert sue_person.world_id == get_test_world_id()
    assert sue_person.worlds_dir == get_test_worlds_dir()
    assert sue_person.world_dir == f"{sue_person.worlds_dir}/{sue_person.world_id}"
    assert sue_person.persons_dir == f"{sue_person.world_dir}/persons"
    assert sue_person.person_dir == f"{sue_person.persons_dir}/{sue_text}"
    assert sue_person._gut_file_name == "gut.json"
    sue_gut_file_path = f"{sue_person.person_dir}/{sue_person._gut_file_name}"
    assert sue_person._gut_path == sue_gut_file_path
    assert sue_person._road_delimiter == slash_text


def test_PersonUnit_gut_file_exists_ReturnsCorrectBool(worlds_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_world_dir = f"{get_test_worlds_dir()}/{get_test_world_id()}"
    sue_persons_dir = f"{sue_world_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_gut_file_name = "gut.json"
    sue_gut_path = f"{sue_person_dir}/{sue_gut_file_name}"
    print(f"{sue_gut_path=}")
    assert os_path_exists(sue_gut_path) == False
    sue_person = personunit_shop(person_id=sue_text)
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


def test_PersonUnit_save_agenda_to_gut_path_CorrectlySavesFile(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    assert sue_person.gut_file_exists() == False

    # WHEN
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    sue_person._save_agenda_to_gut_path(sue_agenda)

    # THEN
    assert sue_person.gut_file_exists()

    sue_world_dir = f"{get_test_worlds_dir()}/{get_test_world_id()}"
    sue_persons_dir = f"{sue_world_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_gut_file_name = "gut.json"
    gut_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_gut_file_name)
    print(f"{gut_file_text=}")
    gut_agenda = agenda_get_from_json(gut_file_text)
    assert gut_agenda.get_party(bob_text) != None

    # WHEN
    yao_agenda = agendaunit_shop("Yao")
    zia_text = "Zia"
    yao_agenda.add_partyunit(zia_text)
    sue_person._save_agenda_to_gut_path(yao_agenda)

    # THEN
    gut_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_gut_file_name)
    print(f"{gut_file_text=}")
    gut_agenda = agenda_get_from_json(gut_file_text)
    assert gut_agenda.get_party(zia_text) != None


def test_PersonUnit_load_gut_file_CorrectlyLoads_gut_obj(worlds_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    sue_person._save_agenda_to_gut_path(sue_agenda)
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
    assert sue_person.gut_file_exists() == False

    # WHEN
    sue_person.create_gut_file_if_does_not_exist()

    # THEN
    gut_agenda = sue_person.get_gut_file_agenda()
    assert gut_agenda._world_id == get_test_world_id()
    assert gut_agenda._agent_id == sue_text
    bob_text = "Bob"
    assert gut_agenda.get_party(bob_text) is None

    # GIVEN
    sue_agenda = agendaunit_shop(sue_text)
    sue_agenda.add_partyunit(bob_text)
    sue_person._save_agenda_to_gut_path(sue_agenda)
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
    sue_gut_file_name = "gut.json"
    gut_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_gut_file_name)
    print(f"{gut_file_text=}")
    gut_agenda = agenda_get_from_json(gut_file_text)
    assert gut_agenda._world_id == get_test_world_id()
    assert gut_agenda._agent_id == sue_text


def test_PersonUnit_create_core_dir_and_files_CreatesDirsAndFiles(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    assert os_path_exists(sue_person.world_dir) is False
    assert os_path_exists(sue_person.persons_dir) is False
    assert os_path_exists(sue_person.person_dir) is False
    assert os_path_exists(sue_person._markets_dir) is False
    assert os_path_exists(sue_person._gut_path) is False

    # WHEN
    sue_person.create_core_dir_and_files()

    # THEN
    assert os_path_exists(sue_person.world_dir)
    assert os_path_exists(sue_person.persons_dir)
    assert os_path_exists(sue_person.person_dir)
    assert os_path_exists(sue_person._gut_path)
    assert os_path_exists(sue_person._markets_dir)


def test_PersonUnit_get_market_path_ReturnsCorrectObj():
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    texas_text = "texas"
    dallas_text = "dallas"
    elpaso_text = "el paso"
    kern_text = "kern"

    # WHEN
    texas_path = sue_person._get_market_path([texas_text])
    dallas_path = sue_person._get_market_path([texas_text, dallas_text])
    elpaso_path = sue_person._get_market_path([texas_text, elpaso_text])
    kern_path = sue_person._get_market_path([texas_text, elpaso_text, kern_text])

    # THEN
    idearoot_dir = f"{sue_person._markets_dir}/idearoot"
    assert texas_path == f"{idearoot_dir}/{texas_text}"
    assert dallas_path == f"{idearoot_dir}/{texas_text}/{dallas_text}"
    assert elpaso_path == f"{idearoot_dir}/{texas_text}/{elpaso_text}"
    assert kern_path == f"{idearoot_dir}/{texas_text}/{elpaso_text}/{kern_text}"


def test_PersonUnit_create_market_dir_CreatesDir(worlds_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_person.create_core_dir_and_files()
    assert os_path_exists(sue_person._markets_dir)
    dallas_text = "dallas"
    dallas_list = [dallas_text]
    dallas_dir = sue_person._get_market_path(dallas_list)
    print(f"{dallas_dir=}")
    assert os_path_exists(dallas_dir) == False

    # WHEN
    sue_person._create_market_dir(dallas_text)

    # THEN
    print(f"{dallas_dir=}")
    assert os_path_exists(dallas_dir)


def test_PersonUnit_create_marketunit_CreatesMarketUnit(worlds_dir_setup_cleanup):
    # GIVEN
    pound_text = "#"
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text, _road_delimiter=pound_text)
    sue_person.create_core_dir_and_files()
    sue_gut = sue_person.get_gut_file_agenda()
    texas_text = "Texas"
    texas_road = sue_gut.make_l1_road(texas_text)
    dallas_text = "dallas"
    dallas_road = sue_gut.make_road(texas_road, dallas_text)
    dallas_nodes = get_all_road_nodes(dallas_road, delimiter=pound_text)
    dallas_dir = sue_person._get_market_path(dallas_nodes)
    dallas_db_path = f"{dallas_dir}/bank.db"
    print(f"{dallas_dir=}")
    print(f"{dallas_db_path=}")
    assert os_path_exists(dallas_db_path) == False
    assert sue_person._market_objs == {}

    # WHEN
    sue_person._create_marketunit(dallas_road)

    # THEN
    assert os_path_exists(dallas_db_path)
    assert sue_person._market_objs != {}
    assert sue_person._market_objs.get(dallas_road) != None
    dallas_marketunit = sue_person._market_objs.get(dallas_road)
    assert dallas_marketunit.market_id == dallas_text
    assert dallas_marketunit.market_dir == dallas_dir
    assert dallas_marketunit._manager_person_id == sue_text
    assert dallas_marketunit._road_delimiter == sue_person._road_delimiter
