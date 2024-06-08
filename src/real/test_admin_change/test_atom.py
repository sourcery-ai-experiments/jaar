from src.change.filehub import filehub_shop
from src.real.admin_duty import initialize_change_duty_files
from src.real.admin_change import (
    filehub_save_atom_file,
    _save_valid_atom_file,
    filehub_atom_file_exists,
    _get_max_atom_file_number,
    _get_next_atom_file_number,
    _delete_atom_file,
    _get_agenda_from_atom_files,
)
from src.real.examples.example_atoms import (
    get_atom_example_beliefunit_knee,
    get_atom_example_ideaunit_sports,
    get_atom_example_ideaunit_ball,
    get_atom_example_ideaunit_knee,
)
from src.real.examples.real_env_kit import (
    get_test_reals_dir as reals_dir,
    get_test_real_id as real_id,
    reals_dir_setup_cleanup,
)
from src._instrument.file import dir_files as file_dir_files
from os.path import exists as os_path_exists


def test_save_valid_atom_file_CorrectlySavesFile(reals_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)
    one_int = 1
    assert os_path_exists(f"{yao_filehub.atoms_dir()}/{one_int}.json") == False

    # WHEN
    knee_atom = get_atom_example_beliefunit_knee()
    atom_num = _save_valid_atom_file(yao_filehub, knee_atom, one_int)

    # THEN
    assert os_path_exists(f"{yao_filehub.atoms_dir()}/{one_int}.json")
    assert atom_num == one_int


def test_filehub_atom_file_exists_ReturnsCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)
    five_int = 5
    assert os_path_exists(f"{yao_filehub.atoms_dir()}/{five_int}.json") == False
    assert filehub_atom_file_exists(yao_filehub, five_int) == False

    # WHEN
    _save_valid_atom_file(yao_filehub, get_atom_example_beliefunit_knee(), five_int)

    # THEN
    assert os_path_exists(f"{yao_filehub.atoms_dir()}/{five_int}.json")
    assert filehub_atom_file_exists(yao_filehub, five_int)


def test_delete_atom_file_CorrectlyDeletesFile(reals_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)
    ten_int = 10
    _save_valid_atom_file(yao_filehub, get_atom_example_beliefunit_knee(), ten_int)
    assert os_path_exists(f"{yao_filehub.atoms_dir()}/{ten_int}.json")

    # WHEN
    _delete_atom_file(yao_filehub, ten_int)

    # THEN
    assert os_path_exists(f"{yao_filehub.atoms_dir()}/{ten_int}.json") == False


def test_get_max_atom_file_number_ReturnsCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)
    ten_int = 10
    _save_valid_atom_file(yao_filehub, get_atom_example_beliefunit_knee(), ten_int)
    assert os_path_exists(f"{yao_filehub.atoms_dir()}/{ten_int}.json")

    # WHEN / THEN
    assert _get_max_atom_file_number(yao_filehub) == ten_int


def test_get_max_atom_file_number_ReturnsCorrectObjWhenDirIsEmpty(
    reals_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)

    # WHEN / THEN
    assert _get_max_atom_file_number(yao_filehub) is None


def test_get_next_atom_file_number_ReturnsCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)
    # WHEN / THEN
    assert _get_next_atom_file_number(yao_filehub) == 0

    ten_int = 10
    _save_valid_atom_file(yao_filehub, get_atom_example_beliefunit_knee(), ten_int)
    assert os_path_exists(f"{yao_filehub.atoms_dir()}/{ten_int}.json")

    # WHEN / THEN
    assert _get_next_atom_file_number(yao_filehub) == 11


def test_filehub_save_atom_file_CorrectlySavesFile(reals_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)
    ten_int = 10
    _save_valid_atom_file(yao_filehub, get_atom_example_beliefunit_knee(), ten_int)
    assert _get_max_atom_file_number(yao_filehub) == ten_int
    eleven_int = ten_int + 1
    assert os_path_exists(f"{yao_filehub.atoms_dir()}/{eleven_int}.json") == False

    # WHEN
    atom_num1 = filehub_save_atom_file(yao_filehub, get_atom_example_beliefunit_knee())

    # THEN
    assert _get_max_atom_file_number(yao_filehub) != ten_int
    assert _get_max_atom_file_number(yao_filehub) == eleven_int
    assert os_path_exists(f"{yao_filehub.atoms_dir()}/{eleven_int}.json")
    assert atom_num1 == eleven_int
    atom_num2 = filehub_save_atom_file(yao_filehub, get_atom_example_beliefunit_knee())
    assert atom_num2 == 12


def test_get_agenda_from_atom_files_ReturnsFileWithZeroAtoms(reals_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)
    initialize_change_duty_files(yao_filehub)

    # WHEN
    yao_agenda = _get_agenda_from_atom_files(yao_filehub)

    # THEN
    assert yao_agenda._owner_id == yao_text
    assert yao_agenda._real_id == yao_filehub.real_id
    assert yao_agenda._road_delimiter == yao_filehub.road_delimiter
    assert yao_agenda._planck == yao_filehub.planck


def test_get_agenda_from_atom_files_ReturnsCorrectFile_SimpleIdea(
    reals_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)

    # save atom files
    sports_atom = get_atom_example_ideaunit_sports(yao_filehub.real_id)
    filehub_save_atom_file(yao_filehub, sports_atom)

    # WHEN
    yao_agenda = _get_agenda_from_atom_files(yao_filehub)

    # THEN
    assert yao_agenda._owner_id == yao_text
    assert yao_agenda._real_id == yao_filehub.real_id
    assert yao_agenda._road_delimiter == yao_filehub.road_delimiter
    sports_text = "sports"
    sports_road = yao_agenda.make_l1_road(sports_text)

    assert yao_agenda.idea_exists(sports_road)


def test_get_agenda_from_atom_files_ReturnsCorrectFile_WithBeliefUnit(
    reals_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)
    initialize_change_duty_files(yao_filehub)

    # save atom files
    x_real_id = yao_filehub.real_id
    filehub_save_atom_file(yao_filehub, get_atom_example_ideaunit_sports(x_real_id))
    filehub_save_atom_file(yao_filehub, get_atom_example_ideaunit_ball(x_real_id))
    filehub_save_atom_file(yao_filehub, get_atom_example_ideaunit_knee(x_real_id))
    filehub_save_atom_file(yao_filehub, get_atom_example_beliefunit_knee(x_real_id))
    print(f"{file_dir_files(yao_filehub.atoms_dir()).keys()=}")

    # WHEN
    yao_agenda = _get_agenda_from_atom_files(yao_filehub)

    # THEN
    assert yao_agenda._owner_id == yao_text
    assert yao_agenda._real_id == yao_filehub.real_id
    assert yao_agenda._road_delimiter == yao_filehub.road_delimiter
    sports_text = "sports"
    sports_road = yao_agenda.make_l1_road(sports_text)

    assert yao_agenda.idea_exists(sports_road)
