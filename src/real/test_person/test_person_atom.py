from src.real.person import (
    personunit_shop,
    chapunit_shop,
    _get_max_atom_file_number,
    _get_next_atom_file_number,
)
from src.real.examples.example_atoms import (
    get_atom_example_beliefunit_knee,
    get_atom_example_ideaunit_sports,
    get_atom_example_ideaunit_ball,
    get_atom_example_ideaunit_knee,
)
from src.real.examples.real_env_kit import (
    get_test_reals_dir,
    get_test_real_id,
    reals_dir_setup_cleanup,
)
from src._instrument.file import dir_files as file_dir_files
from os.path import exists as os_path_exists


def test_PersonUnit_save_valid_atom_file_CorrectlySavesFile(reals_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_person = personunit_shop(yao_text)
    yao_chapunit = chapunit_shop(None, None, yao_text)
    one_int = 1
    assert os_path_exists(f"{yao_person._atoms_dir}/{one_int}.json") == False

    # WHEN
    atom_num = yao_person._save_valid_atom_file(
        get_atom_example_beliefunit_knee(), one_int
    )

    # THEN
    assert os_path_exists(f"{yao_person._atoms_dir}/{one_int}.json")
    assert atom_num == one_int


def test_PersonUnit_atom_file_exists_ReturnsCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_person = personunit_shop(yao_text)
    yao_chapunit = chapunit_shop(None, None, yao_text)
    five_int = 5
    assert os_path_exists(f"{yao_person._atoms_dir}/{five_int}.json") == False
    assert yao_person.atom_file_exists(five_int) == False

    # WHEN
    yao_person._save_valid_atom_file(get_atom_example_beliefunit_knee(), five_int)

    # THEN
    assert os_path_exists(f"{yao_person._atoms_dir}/{five_int}.json")
    assert yao_person.atom_file_exists(five_int)


def test_PersonUnit_delete_atom_file_CorrectlyDeletesFile(reals_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_person = personunit_shop(yao_text)
    yao_chapunit = chapunit_shop(None, None, yao_text)
    ten_int = 10
    yao_person._save_valid_atom_file(get_atom_example_beliefunit_knee(), ten_int)
    assert os_path_exists(f"{yao_person._atoms_dir}/{ten_int}.json")

    # WHEN
    yao_person._delete_atom_file(ten_int)

    # THEN
    assert os_path_exists(f"{yao_person._atoms_dir}/{ten_int}.json") == False


def test_PersonUnit_get_max_atom_file_number_ReturnsCorrectObj(
    reals_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_person = personunit_shop(yao_text)
    yao_chapunit = chapunit_shop(None, None, yao_text)
    ten_int = 10
    yao_person._save_valid_atom_file(get_atom_example_beliefunit_knee(), ten_int)
    assert os_path_exists(f"{yao_person._atoms_dir}/{ten_int}.json")

    # WHEN / THEN
    assert _get_max_atom_file_number(yao_chapunit) == ten_int


def test_PersonUnit_get_max_atom_file_number_ReturnsCorrectObjWhenDirIsEmpty(
    reals_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_person = personunit_shop(yao_text)
    yao_chapunit = chapunit_shop(None, None, yao_text)

    # WHEN / THEN
    assert _get_max_atom_file_number(yao_chapunit) is None


def test_PersonUnit_get_next_atom_file_number_ReturnsCorrectObj(
    reals_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_person = personunit_shop(yao_text)
    yao_chapunit = chapunit_shop(None, None, yao_text)
    # WHEN / THEN
    assert _get_next_atom_file_number(yao_chapunit) == 0

    ten_int = 10
    yao_person._save_valid_atom_file(get_atom_example_beliefunit_knee(), ten_int)
    assert os_path_exists(f"{yao_person._atoms_dir}/{ten_int}.json")

    # WHEN / THEN
    assert _get_next_atom_file_number(yao_chapunit) == 11


def test_PersonUnit_save_atom_file_CorrectlySavesFile(reals_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_person = personunit_shop(yao_text)
    yao_chapunit = chapunit_shop(None, None, yao_text)
    ten_int = 10
    yao_person._save_valid_atom_file(get_atom_example_beliefunit_knee(), ten_int)
    assert _get_max_atom_file_number(yao_chapunit) == ten_int
    eleven_int = ten_int + 1
    assert os_path_exists(f"{yao_person._atoms_dir}/{eleven_int}.json") == False

    # WHEN
    atom_num1 = yao_person.save_atom_file(
        yao_chapunit, get_atom_example_beliefunit_knee()
    )

    # THEN
    assert _get_max_atom_file_number(yao_chapunit) != ten_int
    assert _get_max_atom_file_number(yao_chapunit) == eleven_int
    assert os_path_exists(f"{yao_person._atoms_dir}/{eleven_int}.json")
    assert atom_num1 == eleven_int
    atom_num2 = yao_person.save_atom_file(
        yao_chapunit, get_atom_example_beliefunit_knee()
    )
    assert atom_num2 == 12


def test_PersonUnit_get_agenda_from_atom_files_ReturnsCorrectFile_ZeroAtoms(
    reals_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_person = personunit_shop(yao_text)
    yao_chapunit = chapunit_shop(None, None, yao_text)

    # WHEN
    yao_agenda = yao_person._get_agenda_from_atom_files(yao_chapunit)

    # THEN
    assert yao_agenda._owner_id == yao_text
    assert yao_agenda._real_id == yao_person.real_id
    assert yao_agenda._road_delimiter == yao_person._road_delimiter
    assert yao_agenda._planck == yao_person._planck


def test_PersonUnit_get_agenda_from_atom_files_ReturnsCorrectFile_SimpleIdea(
    reals_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_person = personunit_shop(yao_text)
    yao_chapunit = chapunit_shop(None, None, yao_text)
    # save atom files
    yao_person.save_atom_file(
        yao_chapunit, get_atom_example_ideaunit_sports(yao_person.real_id)
    )

    # WHEN
    yao_agenda = yao_person._get_agenda_from_atom_files(yao_chapunit)

    # THEN
    assert yao_agenda._owner_id == yao_text
    assert yao_agenda._real_id == yao_person.real_id
    assert yao_agenda._road_delimiter == yao_person._road_delimiter
    sports_text = "sports"
    sports_road = yao_agenda.make_l1_road(sports_text)

    assert yao_agenda.idea_exists(sports_road)


def test_PersonUnit_get_agenda_from_atom_files_ReturnsCorrectFile_WithBeliefUnit(
    reals_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_person = personunit_shop(yao_text)
    yao_chapunit = chapunit_shop(None, None, yao_text)
    # save atom files
    yao_person.save_atom_file(
        yao_chapunit, get_atom_example_ideaunit_sports(yao_person.real_id)
    )
    yao_person.save_atom_file(
        yao_chapunit, get_atom_example_ideaunit_ball(yao_person.real_id)
    )
    yao_person.save_atom_file(
        yao_chapunit, get_atom_example_ideaunit_knee(yao_person.real_id)
    )
    yao_person.save_atom_file(
        yao_chapunit, get_atom_example_beliefunit_knee(yao_person.real_id)
    )
    print(f"{file_dir_files(yao_person._atoms_dir).keys()=}")

    # WHEN
    yao_agenda = yao_person._get_agenda_from_atom_files(yao_chapunit)

    # THEN
    assert yao_agenda._owner_id == yao_text
    assert yao_agenda._real_id == yao_person.real_id
    assert yao_agenda._road_delimiter == yao_person._road_delimiter
    sports_text = "sports"
    sports_road = yao_agenda.make_l1_road(sports_text)

    assert yao_agenda.idea_exists(sports_road)
