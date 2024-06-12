from src._instrument.file import delete_dir
from src._road.jaar_config import init_atom_id, get_test_real_id as real_id
from src.listen.userhub import userhub_shop
from src.listen.examples.example_listen_atoms import sue_2quarkunits_atomunit
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from os.path import exists as os_path_exists


def test_UserHub_default_duty_agenda_ReturnsCorrectObj():
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
        nox_type=None,
        road_delimiter=slash_text,
        planck=point_five_float,
        penny=point_four_float,
    )

    # WHEN
    sue_default_duty = sue_userhub.default_duty_agenda()

    # THEN
    assert sue_default_duty._real_id == sue_userhub.real_id
    assert sue_default_duty._owner_id == sue_userhub.person_id
    assert sue_default_duty._road_delimiter == sue_userhub.road_delimiter
    assert sue_default_duty._planck == sue_userhub.planck
    assert sue_default_duty._penny == sue_userhub.penny


def test_UserHub_delete_duty_file_DeletesDutyFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    sue_userhub.save_duty_agenda(sue_userhub.default_duty_agenda())
    assert sue_userhub.duty_file_exists()

    # WHEN
    sue_userhub.delete_duty_file()

    # THEN
    assert sue_userhub.duty_file_exists() is False


def test_UserHub_create_initial_atom_files_from_default_CorrectlySavesAtomUnitFiles(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, planck=seven_int)
    init_atom_file_name = sue_userhub.atom_file_name(init_atom_id())
    init_atom_file_path = f"{sue_userhub.atoms_dir()}/{init_atom_file_name}"
    assert os_path_exists(init_atom_file_path) is False
    assert sue_userhub.duty_file_exists() is False

    # WHEN
    sue_userhub._create_initial_atom_files_from_default()

    # THEN
    assert os_path_exists(init_atom_file_path)
    assert sue_userhub.duty_file_exists() is False


def test_UserHub_create_duty_from_atoms_CreatesDutyFileFromAtomFiles(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, planck=seven_int)
    init_atom_file_name = sue_userhub.atom_file_name(init_atom_id())
    init_atom_file_path = f"{sue_userhub.atoms_dir()}/{init_atom_file_name}"
    sue_userhub._create_initial_atom_files_from_default()
    assert os_path_exists(init_atom_file_path)
    assert sue_userhub.duty_file_exists() is False

    # WHEN
    sue_userhub._create_duty_from_atoms()

    # THEN
    assert sue_userhub.duty_file_exists()
    static_sue_duty = sue_userhub._merge_any_atoms(sue_userhub.default_duty_agenda())
    assert sue_userhub.get_duty_agenda().get_dict() == static_sue_duty.get_dict()


def test_UserHub_create_initial_atom_and_duty_files_CreatesAtomFilesAndDutyFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, planck=seven_int)
    init_atom_file_name = sue_userhub.atom_file_name(init_atom_id())
    init_atom_file_path = f"{sue_userhub.atoms_dir()}/{init_atom_file_name}"
    assert os_path_exists(init_atom_file_path) is False
    assert sue_userhub.duty_file_exists() is False

    # WHEN
    sue_userhub._create_initial_atom_and_duty_files()

    # THEN
    assert os_path_exists(init_atom_file_path)
    assert sue_userhub.duty_file_exists()
    static_sue_duty = sue_userhub._merge_any_atoms(sue_userhub.default_duty_agenda())
    assert sue_userhub.get_duty_agenda().get_dict() == static_sue_duty.get_dict()


def test_UserHub_create_initial_atom_files_from_duty_SavesOnlyAtomFiles(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, planck=seven_int)
    sue_duty_agenda = sue_userhub.default_duty_agenda()
    bob_text = "Bob"
    sue_duty_agenda.add_partyunit(bob_text)
    assert sue_userhub.duty_file_exists() is False
    sue_userhub.save_duty_agenda(sue_duty_agenda)
    assert sue_userhub.duty_file_exists()
    init_atom_file_path = f"{sue_userhub.atoms_dir()}/{init_atom_id()}.json"
    assert os_path_exists(init_atom_file_path) is False

    # WHEN
    sue_userhub._create_initial_atom_files_from_duty()

    # THEN
    assert os_path_exists(init_atom_file_path)


def test_UserHub_initialize_atom_duty_files_CorrectlySavesDutyFileAndAtomFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, planck=seven_int)
    assert sue_userhub.duty_file_exists() is False
    init_atom_file_path = f"{sue_userhub.atoms_dir()}/{init_atom_id()}.json"
    delete_dir(sue_userhub.atoms_dir())
    assert os_path_exists(init_atom_file_path) is False

    # WHEN
    sue_userhub.initialize_atom_duty_files()

    # THEN
    duty_agenda = sue_userhub.get_duty_agenda()
    assert duty_agenda._real_id == real_id()
    assert duty_agenda._owner_id == sue_text
    assert duty_agenda._planck == seven_int
    assert os_path_exists(init_atom_file_path)


def test_UserHub_initialize_atom_duty_files_CorrectlySavesOnlyDutyFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, planck=seven_int)
    sue_userhub.initialize_atom_duty_files()
    assert sue_userhub.duty_file_exists()
    sue_userhub.delete_duty_file()
    assert sue_userhub.duty_file_exists() is False
    init_atom_file_path = f"{sue_userhub.atoms_dir()}/{init_atom_id()}.json"
    assert os_path_exists(init_atom_file_path)

    # WHEN
    sue_userhub.initialize_atom_duty_files()

    # THEN
    duty_agenda = sue_userhub.get_duty_agenda()
    assert duty_agenda._real_id == real_id()
    assert duty_agenda._owner_id == sue_text
    assert duty_agenda._planck == seven_int
    assert os_path_exists(init_atom_file_path)


def test_UserHub_initialize_atom_duty_files_CorrectlySavesOnlyatomFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    seven_int = 7
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, planck=seven_int)
    sue_userhub.initialize_atom_duty_files()
    sue_duty_agenda = sue_userhub.get_duty_agenda()
    bob_text = "Bob"
    sue_duty_agenda.add_partyunit(bob_text)
    sue_userhub.save_duty_agenda(sue_duty_agenda)
    assert sue_userhub.duty_file_exists()
    init_atom_file_path = f"{sue_userhub.atoms_dir()}/{init_atom_id()}.json"
    delete_dir(sue_userhub.atoms_dir())
    assert os_path_exists(init_atom_file_path) is False

    # WHEN
    sue_userhub.initialize_atom_duty_files()

    # THEN
    assert sue_duty_agenda._real_id == real_id()
    assert sue_duty_agenda._owner_id == sue_text
    assert sue_duty_agenda._planck == seven_int
    assert sue_duty_agenda.party_exists(bob_text)
    assert os_path_exists(init_atom_file_path)


def test_UserHub_append_atoms_to_duty_file_AddsatomsToDutyFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    sue_userhub.initialize_atom_duty_files()
    sue_userhub.save_atom_file(sue_2quarkunits_atomunit())
    duty_agenda = sue_userhub.get_duty_agenda()
    print(f"{duty_agenda._real_id=}")
    sports_text = "sports"
    sports_road = duty_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = duty_agenda.make_road(sports_road, knee_text)
    assert duty_agenda.idea_exists(sports_road) is False
    assert duty_agenda.idea_exists(knee_road) is False

    # WHEN
    new_agenda = sue_userhub.append_atoms_to_duty_file()

    # THEN
    assert new_agenda != duty_agenda
    assert new_agenda.idea_exists(sports_road)
    assert new_agenda.idea_exists(knee_road)
