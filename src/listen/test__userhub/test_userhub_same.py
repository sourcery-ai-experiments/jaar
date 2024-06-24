from src._instrument.file import delete_dir
from src._road.jaar_config import init_atom_id, get_test_real_id as real_id
from src.listen.userhub import userhub_shop
from src.listen.examples.example_listen_atoms import sue_2quarkunits_atomunit
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from os.path import exists as os_path_exists


def test_UserHub_default_same_agenda_ReturnsCorrectObj():
    # GIVEN
    sue_text = "Sue"
    slash_text = "/"
    point_five_float = 0.5
    point_four_float = 0.4
    sue_userhub = userhub_shop(
        env_dir(),
        real_id(),
        sue_text,
        econ_road=None,
        road_delimiter=slash_text,
        pixel=point_five_float,
        penny=point_four_float,
    )

    # WHEN
    sue_default_same = sue_userhub.default_same_agenda()

    # THEN
    assert sue_default_same._real_id == sue_userhub.real_id
    assert sue_default_same._owner_id == sue_userhub.person_id
    assert sue_default_same._road_delimiter == sue_userhub.road_delimiter
    assert sue_default_same._pixel == sue_userhub.pixel
    assert sue_default_same._penny == sue_userhub.penny


def test_UserHub_delete_same_file_DeletesSameFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    sue_userhub.save_same_agenda(sue_userhub.default_same_agenda())
    assert sue_userhub.same_file_exists()

    # WHEN
    sue_userhub.delete_same_file()

    # THEN
    assert sue_userhub.same_file_exists() is False


def test_UserHub_create_initial_atom_files_from_default_CorrectlySavesAtomUnitFiles(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    init_atom_file_name = sue_userhub.atom_file_name(init_atom_id())
    init_atom_file_path = f"{sue_userhub.atoms_dir()}/{init_atom_file_name}"
    assert os_path_exists(init_atom_file_path) is False
    assert sue_userhub.same_file_exists() is False

    # WHEN
    sue_userhub._create_initial_atom_files_from_default()

    # THEN
    assert os_path_exists(init_atom_file_path)
    assert sue_userhub.same_file_exists() is False


def test_UserHub_create_same_from_atoms_CreatesSameFileFromAtomFiles(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    init_atom_file_name = sue_userhub.atom_file_name(init_atom_id())
    init_atom_file_path = f"{sue_userhub.atoms_dir()}/{init_atom_file_name}"
    sue_userhub._create_initial_atom_files_from_default()
    assert os_path_exists(init_atom_file_path)
    assert sue_userhub.same_file_exists() is False

    # WHEN
    sue_userhub._create_same_from_atoms()

    # THEN
    assert sue_userhub.same_file_exists()
    static_sue_same = sue_userhub._merge_any_atoms(sue_userhub.default_same_agenda())
    assert sue_userhub.get_same_agenda().get_dict() == static_sue_same.get_dict()


def test_UserHub_create_initial_atom_and_same_files_CreatesAtomFilesAndSameFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    init_atom_file_name = sue_userhub.atom_file_name(init_atom_id())
    init_atom_file_path = f"{sue_userhub.atoms_dir()}/{init_atom_file_name}"
    assert os_path_exists(init_atom_file_path) is False
    assert sue_userhub.same_file_exists() is False

    # WHEN
    sue_userhub._create_initial_atom_and_same_files()

    # THEN
    assert os_path_exists(init_atom_file_path)
    assert sue_userhub.same_file_exists()
    static_sue_same = sue_userhub._merge_any_atoms(sue_userhub.default_same_agenda())
    assert sue_userhub.get_same_agenda().get_dict() == static_sue_same.get_dict()


def test_UserHub_create_initial_atom_files_from_same_SavesOnlyAtomFiles(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    sue_same_agenda = sue_userhub.default_same_agenda()
    bob_text = "Bob"
    sue_same_agenda.add_otherunit(bob_text)
    assert sue_userhub.same_file_exists() is False
    sue_userhub.save_same_agenda(sue_same_agenda)
    assert sue_userhub.same_file_exists()
    init_atom_file_path = f"{sue_userhub.atoms_dir()}/{init_atom_id()}.json"
    assert os_path_exists(init_atom_file_path) is False

    # WHEN
    sue_userhub._create_initial_atom_files_from_same()

    # THEN
    assert os_path_exists(init_atom_file_path)


def test_UserHub_initialize_atom_same_files_CorrectlySavesSameFileAndAtomFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    assert sue_userhub.same_file_exists() is False
    init_atom_file_path = f"{sue_userhub.atoms_dir()}/{init_atom_id()}.json"
    delete_dir(sue_userhub.atoms_dir())
    assert os_path_exists(init_atom_file_path) is False

    # WHEN
    sue_userhub.initialize_atom_same_files()

    # THEN
    same_agenda = sue_userhub.get_same_agenda()
    assert same_agenda._real_id == real_id()
    assert same_agenda._owner_id == sue_text
    assert same_agenda._pixel == seven_int
    assert os_path_exists(init_atom_file_path)


def test_UserHub_initialize_atom_same_files_CorrectlySavesOnlySameFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    sue_userhub.initialize_atom_same_files()
    assert sue_userhub.same_file_exists()
    sue_userhub.delete_same_file()
    assert sue_userhub.same_file_exists() is False
    init_atom_file_path = f"{sue_userhub.atoms_dir()}/{init_atom_id()}.json"
    assert os_path_exists(init_atom_file_path)

    # WHEN
    sue_userhub.initialize_atom_same_files()

    # THEN
    same_agenda = sue_userhub.get_same_agenda()
    assert same_agenda._real_id == real_id()
    assert same_agenda._owner_id == sue_text
    assert same_agenda._pixel == seven_int
    assert os_path_exists(init_atom_file_path)


def test_UserHub_initialize_atom_same_files_CorrectlySavesOnlyatomFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, pixel=seven_int)
    sue_userhub.initialize_atom_same_files()
    sue_same_agenda = sue_userhub.get_same_agenda()
    bob_text = "Bob"
    sue_same_agenda.add_otherunit(bob_text)
    sue_userhub.save_same_agenda(sue_same_agenda)
    assert sue_userhub.same_file_exists()
    init_atom_file_path = f"{sue_userhub.atoms_dir()}/{init_atom_id()}.json"
    delete_dir(sue_userhub.atoms_dir())
    assert os_path_exists(init_atom_file_path) is False

    # WHEN
    sue_userhub.initialize_atom_same_files()

    # THEN
    assert sue_same_agenda._real_id == real_id()
    assert sue_same_agenda._owner_id == sue_text
    assert sue_same_agenda._pixel == seven_int
    assert sue_same_agenda.other_exists(bob_text)
    assert os_path_exists(init_atom_file_path)


def test_UserHub_append_atoms_to_same_file_AddsatomsToSameFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    sue_userhub.initialize_atom_same_files()
    sue_userhub.save_atom_file(sue_2quarkunits_atomunit())
    same_agenda = sue_userhub.get_same_agenda()
    print(f"{same_agenda._real_id=}")
    sports_text = "sports"
    sports_road = same_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = same_agenda.make_road(sports_road, knee_text)
    assert same_agenda.idea_exists(sports_road) is False
    assert same_agenda.idea_exists(knee_road) is False

    # WHEN
    new_agenda = sue_userhub.append_atoms_to_same_file()

    # THEN
    assert new_agenda != same_agenda
    assert new_agenda.idea_exists(sports_road)
    assert new_agenda.idea_exists(knee_road)
