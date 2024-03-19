from src.world.person import personunit_shop
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
from src.instrument.file import save_file
from os.path import exists as os_path_exists


def test_PersonUnit_get_max_atom_file_number_ReturnsCorrectObj(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    yao_person = personunit_shop("Yao")
    ten_int = 10
    save_file(yao_person._atoms_dir, f"{ten_int}.json", "filler text")
    assert os_path_exists(f"{yao_person._atoms_dir}/{ten_int}.json")

    # WHEN / THEN
    assert yao_person._get_max_atom_file_number() == ten_int


def test_PersonUnit_get_max_atom_file_number_ReturnsCorrectObjWhenDirIsEmpty(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    yao_person = personunit_shop("Yao")

    # WHEN / THEN
    assert yao_person._get_max_atom_file_number() is None


def test_PersonUnit_get_next_atom_file_number_ReturnsCorrectObj(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    yao_person = personunit_shop("Yao")
    # WHEN / THEN
    assert yao_person._get_next_atom_file_number() == 0

    ten_int = 10
    save_file(yao_person._atoms_dir, f"{ten_int}.json", "filler text")
    assert os_path_exists(f"{yao_person._atoms_dir}/{ten_int}.json")

    # WHEN / THEN
    assert yao_person._get_next_atom_file_number() == 11
