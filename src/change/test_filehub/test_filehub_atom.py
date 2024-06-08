from src.change.filehub import filehub_shop
from src.change.examples.example_atoms import (
    get_atom_example_beliefunit_knee,
    get_atom_example_ideaunit_sports,
    get_atom_example_ideaunit_ball,
    get_atom_example_ideaunit_knee,
)
from src.change.examples.change_env import (
    get_change_temp_env_dir as reals_dir,
    get_default_real_id_roadnode as real_id,
    env_dir_setup_cleanup,
)
from src._instrument.file import dir_files as file_dir_files
from os.path import exists as os_path_exists


def test_FileHub_atom_file_name_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)
    one_int = 1

    # WHEN
    one_atom_file_name = yao_filehub.atom_file_name(one_int)

    # THEN
    assert one_atom_file_name == f"{one_int}.json"


def test_FileHub_atom_file_path_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)
    one_int = 1

    # WHEN
    one_atom_file_path = yao_filehub.atom_file_path(one_int)

    # THEN
    one_atom_file_name = yao_filehub.atom_file_name(one_int)
    assert one_atom_file_path == f"{yao_filehub.atoms_dir()}/{one_atom_file_name}"


def test_FileHub_save_valid_atom_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)
    one_int = 1
    assert os_path_exists(yao_filehub.atom_file_path(one_int)) == False

    # WHEN
    knee_atom = get_atom_example_beliefunit_knee()
    atom_num = yao_filehub._save_valid_atom_file(knee_atom, one_int)

    # THEN
    assert os_path_exists(yao_filehub.atom_file_path(one_int))
    assert atom_num == one_int


def test_FileHub_atom_file_exists_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)
    five_int = 5
    assert os_path_exists(yao_filehub.atom_file_path(five_int)) == False
    assert yao_filehub.atom_file_exists(five_int) == False

    # WHEN
    yao_filehub._save_valid_atom_file(get_atom_example_beliefunit_knee(), five_int)

    # THEN
    assert os_path_exists(yao_filehub.atom_file_path(five_int))
    assert yao_filehub.atom_file_exists(five_int)


def test_FileHub_delete_atom_file_CorrectlyDeletesFile(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)
    ten_int = 10
    yao_filehub._save_valid_atom_file(get_atom_example_beliefunit_knee(), ten_int)
    assert yao_filehub.atom_file_exists(ten_int)

    # WHEN
    yao_filehub.delete_atom_file(ten_int)

    # THEN
    assert yao_filehub.atom_file_exists(ten_int) == False


def test_FileHub_get_max_atom_file_number_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)
    ten_int = 10
    yao_filehub._save_valid_atom_file(get_atom_example_beliefunit_knee(), ten_int)
    assert yao_filehub.atom_file_exists(ten_int)

    # WHEN / THEN
    assert yao_filehub.get_max_atom_file_number() == ten_int


def test_FileHub_get_max_atom_file_number_ReturnsCorrectObjWhenDirIsEmpty(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)

    # WHEN / THEN
    assert yao_filehub.get_max_atom_file_number() is None


def test_FileHub_get_next_atom_file_number_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)
    # WHEN / THEN
    assert yao_filehub._get_next_atom_file_number() == 0

    ten_int = 10
    yao_filehub._save_valid_atom_file(get_atom_example_beliefunit_knee(), ten_int)
    assert yao_filehub.atom_file_exists(ten_int)

    # WHEN / THEN
    assert yao_filehub._get_next_atom_file_number() == 11


def test_FileHub_save_atom_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)
    ten_int = 10
    yao_filehub._save_valid_atom_file(get_atom_example_beliefunit_knee(), ten_int)
    assert yao_filehub.get_max_atom_file_number() == ten_int
    eleven_int = ten_int + 1
    assert yao_filehub.atom_file_exists(eleven_int) == False

    # WHEN
    atom_num1 = yao_filehub.save_atom_file(get_atom_example_beliefunit_knee())

    # THEN
    assert yao_filehub.get_max_atom_file_number() != ten_int
    assert yao_filehub.get_max_atom_file_number() == eleven_int
    assert yao_filehub.atom_file_exists(eleven_int)
    assert atom_num1 == eleven_int
    atom_num2 = yao_filehub.save_atom_file(get_atom_example_beliefunit_knee())
    assert atom_num2 == 12


# def test_FileHub_get_agenda_from_atom_files_ReturnsFileWithZeroAtoms(
#     env_dir_setup_cleanup,
# ):
#     # GIVEN
#     yao_text = "Yao"
#     yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)
#     # initialize_change_duty_files(yao_filehub)

#     # WHEN
#     yao_agenda = yao_filehub._get_agenda_from_atom_files()

#     # THEN
#     assert yao_agenda._owner_id == yao_text
#     assert yao_agenda._real_id == yao_filehub.real_id
#     assert yao_agenda._road_delimiter == yao_filehub.road_delimiter
#     assert yao_agenda._planck == yao_filehub.planck


def test_FileHub_get_agenda_from_atom_files_ReturnsCorrectFile_SimpleIdea(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)

    # save atom files
    sports_atom = get_atom_example_ideaunit_sports(yao_filehub.real_id)
    yao_filehub.save_atom_file(sports_atom)

    # WHEN
    yao_agenda = yao_filehub._get_agenda_from_atom_files()

    # THEN
    assert yao_agenda._owner_id == yao_text
    assert yao_agenda._real_id == yao_filehub.real_id
    assert yao_agenda._road_delimiter == yao_filehub.road_delimiter
    sports_text = "sports"
    sports_road = yao_agenda.make_l1_road(sports_text)

    assert yao_agenda.idea_exists(sports_road)


# def test_FileHub_get_agenda_from_atom_files_ReturnsCorrectFile_WithBeliefUnit(
#     env_dir_setup_cleanup,
# ):
#     # GIVEN
#     yao_text = "Yao"
#     yao_filehub = filehub_shop(reals_dir(), real_id(), yao_text)
#     initialize_change_duty_files(yao_filehub)

#     # save atom files
#     x_real_id = yao_filehub.real_id
#     yao_filehub.save_atom_file(get_atom_example_ideaunit_sports(x_real_id))
#     yao_filehub.save_atom_file(get_atom_example_ideaunit_ball(x_real_id))
#     yao_filehub.save_atom_file(get_atom_example_ideaunit_knee(x_real_id))
#     yao_filehub.save_atom_file(get_atom_example_beliefunit_knee(x_real_id))
#     print(f"{file_dir_files(yao_filehub.atoms_dir()).keys()=}")

#     # WHEN
#     yao_agenda = yao_filehub._get_agenda_from_atom_files()

#     # THEN
#     assert yao_agenda._owner_id == yao_text
#     assert yao_agenda._real_id == yao_filehub.real_id
#     assert yao_agenda._road_delimiter == yao_filehub.road_delimiter
#     sports_text = "sports"
#     sports_road = yao_agenda.make_l1_road(sports_text)

#     assert yao_agenda.idea_exists(sports_road)
