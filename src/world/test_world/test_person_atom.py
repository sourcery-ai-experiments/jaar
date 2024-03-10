from src._road.road import default_road_delimiter_if_none
from src.agenda.agenda import agendaunit_shop, get_from_json as agenda_get_from_json
from src.agenda.atom import agendaatom_shop, get_from_json as agendaatom_get_from_json
from src.world.person import (
    PersonUnit,
    personunit_shop,
    get_gut_file_name,
    get_life_file_name,
)
from pytest import raises as pytest_raises
from src.world.examples.example_atoms import (
    get_atom_example_beliefunit_knee,
    get_atom_example_ideaunit_sports,
    get_atom_example_ideaunit_ball,
    get_atom_example_ideaunit_knee,
)
from src.world.examples.world_env_kit import (
    get_test_worlds_dir,
    get_test_world_id,
    worlds_dir_setup_cleanup,
)
from os.path import exists as os_path_exists
from src.instrument.file import open_file, save_file, dir_files


def test_get_gut_file_name():
    assert get_gut_file_name() == "gut"


def test_get_life_file_name():
    assert get_life_file_name() == "life"


def test_PersonUnit_save_valid_atom_file_CorrectlySavesFile(worlds_dir_setup_cleanup):
    # GIVEN
    yao_person = personunit_shop("Yao")
    one_int = 1
    assert os_path_exists(f"{yao_person._atoms_dir}/{one_int}.json") == False

    # WHEN
    atom_num = yao_person._save_valid_atom_file(
        get_atom_example_beliefunit_knee(), one_int
    )

    # THEN
    assert os_path_exists(f"{yao_person._atoms_dir}/{one_int}.json")
    assert atom_num == one_int


def test_PersonUnit_atom_file_exists_ReturnsCorrectObj(worlds_dir_setup_cleanup):
    # GIVEN
    yao_person = personunit_shop("Yao")
    five_int = 5
    assert os_path_exists(f"{yao_person._atoms_dir}/{five_int}.json") == False
    assert yao_person.atom_file_exists(five_int) == False

    # WHEN
    yao_person._save_valid_atom_file(get_atom_example_beliefunit_knee(), five_int)

    # THEN
    assert os_path_exists(f"{yao_person._atoms_dir}/{five_int}.json")
    assert yao_person.atom_file_exists(five_int)


def test_PersonUnit_delete_atom_file_CorrectlyDeletesFile(worlds_dir_setup_cleanup):
    # GIVEN
    yao_person = personunit_shop("Yao")
    ten_int = 10
    yao_person._save_valid_atom_file(get_atom_example_beliefunit_knee(), ten_int)
    assert os_path_exists(f"{yao_person._atoms_dir}/{ten_int}.json")

    # WHEN
    yao_person._delete_atom_file(ten_int)

    # THEN
    assert os_path_exists(f"{yao_person._atoms_dir}/{ten_int}.json") == False


def test_PersonUnit_get_max_atom_filename_ReturnsCorrectObj(worlds_dir_setup_cleanup):
    # GIVEN
    yao_person = personunit_shop("Yao")
    ten_int = 10
    yao_person._save_valid_atom_file(get_atom_example_beliefunit_knee(), ten_int)
    assert os_path_exists(f"{yao_person._atoms_dir}/{ten_int}.json")

    # WHEN / THEN
    assert yao_person._get_max_atom_filename() == ten_int


def test_PersonUnit_get_max_atom_filename_ReturnsCorrectObjWhenDirIsEmpty(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    yao_person = personunit_shop("Yao")

    # WHEN / THEN
    assert yao_person._get_max_atom_filename() == 0


def test_PersonUnit_get_next_atom_filename_ReturnsCorrectObj(worlds_dir_setup_cleanup):
    # GIVEN
    yao_person = personunit_shop("Yao")
    ten_int = 10
    yao_person._save_valid_atom_file(get_atom_example_beliefunit_knee(), ten_int)
    assert os_path_exists(f"{yao_person._atoms_dir}/{ten_int}.json")

    # WHEN / THEN
    assert yao_person._get_next_atom_filename() == "11.json"


def test_PersonUnit_save_atom_file_CorrectlySavesFile(worlds_dir_setup_cleanup):
    # GIVEN
    yao_person = personunit_shop("Yao")
    ten_int = 10
    yao_person._save_valid_atom_file(get_atom_example_beliefunit_knee(), ten_int)
    assert yao_person._get_max_atom_filename() == ten_int
    eleven_int = ten_int + 1
    assert os_path_exists(f"{yao_person._atoms_dir}/{eleven_int}.json") == False

    # WHEN
    atom_num1 = yao_person.save_atom_file(get_atom_example_beliefunit_knee())

    # THEN
    assert yao_person._get_max_atom_filename() != ten_int
    assert yao_person._get_max_atom_filename() == eleven_int
    assert os_path_exists(f"{yao_person._atoms_dir}/{eleven_int}.json")
    assert atom_num1 == eleven_int
    atom_num2 = yao_person.save_atom_file(get_atom_example_beliefunit_knee())
    assert atom_num2 == 12


def test_PersonUnit_get_agenda_from_atom_files_ReturnsCorrectFile_ZeroAtoms(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_person = personunit_shop(yao_text)
    yao_person.create_core_dir_and_files()

    # WHEN
    yao_agenda = yao_person._get_agenda_from_atom_files()

    # THEN
    assert yao_agenda._worker_id == yao_text
    assert yao_agenda._world_id == yao_person.world_id
    assert yao_agenda._road_delimiter == yao_person._road_delimiter
    assert yao_agenda._planck == yao_person._planck


def test_PersonUnit_get_agenda_from_atom_files_ReturnsCorrectFile_SimpleIdea(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_person = personunit_shop(yao_text)
    # save atom files
    yao_person.save_atom_file(get_atom_example_ideaunit_sports(yao_person.world_id))

    # WHEN
    yao_agenda = yao_person._get_agenda_from_atom_files()

    # THEN
    assert yao_agenda._worker_id == yao_text
    assert yao_agenda._world_id == yao_person.world_id
    assert yao_agenda._road_delimiter == yao_person._road_delimiter
    sports_text = "sports"
    sports_road = yao_agenda.make_l1_road(sports_text)

    assert yao_agenda.idea_exists(sports_road)


def test_PersonUnit_get_agenda_from_atom_files_ReturnsCorrectFile_WithBeliefUnit(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_person = personunit_shop(yao_text)
    # save atom files
    yao_person.save_atom_file(get_atom_example_ideaunit_sports(yao_person.world_id))
    yao_person.save_atom_file(get_atom_example_ideaunit_ball(yao_person.world_id))
    yao_person.save_atom_file(get_atom_example_ideaunit_knee(yao_person.world_id))
    yao_person.save_atom_file(get_atom_example_beliefunit_knee(yao_person.world_id))

    # WHEN
    yao_agenda = yao_person._get_agenda_from_atom_files()

    # THEN
    assert yao_agenda._worker_id == yao_text
    assert yao_agenda._world_id == yao_person.world_id
    assert yao_agenda._road_delimiter == yao_person._road_delimiter
    sports_text = "sports"
    sports_road = yao_agenda.make_l1_road(sports_text)

    assert yao_agenda.idea_exists(sports_road)
