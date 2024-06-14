from src._instrument.file import open_file
from src._instrument.python import get_dict_from_json
from src._road.jaar_config import get_atoms_folder, get_test_real_id as real_id
from src.atom.nuc import nucunit_shop
from src.atom.atom import atomunit_shop, create_atomunit_from_files
from src.atom.examples.example_quarks import (
    get_quark_example_ideaunit_sports,
    get_quark_example_ideaunit_knee,
    get_quark_example_ideaunit_ball,
)
from src.atom.examples.atom_env import (
    get_atom_temp_env_dir as reals_dir,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_AtomUnit_save_quark_file_SavesCorrectFile(env_dir_setup_cleanup):
    # GIVEN
    x_real_dir = f"{reals_dir()}/{real_id()}"
    x_persons_dir = f"{x_real_dir}/persons"
    sue_text = "Sue"
    sue_person_dir = f"{x_persons_dir}/{sue_text}"
    sue_quarks_dir = f"{sue_person_dir}/quarks"
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_quark2_path = f"{sue_quarks_dir}/{two_filename}"
    sue_quark6_path = f"{sue_quarks_dir}/{six_filename}"
    print(f"{sue_quark2_path=}")
    print(f"{sue_quark6_path=}")
    farm_atomunit = atomunit_shop(sue_text, _quarks_dir=sue_quarks_dir)
    assert os_path_exists(sue_quark2_path) is False
    assert os_path_exists(sue_quark6_path) is False

    # WHEN
    sports_quark = get_quark_example_ideaunit_sports()
    farm_atomunit._save_quark_file(two_int, sports_quark)

    # THEN
    assert os_path_exists(sue_quark2_path)
    assert os_path_exists(sue_quark6_path) is False
    two_file_json = open_file(sue_quarks_dir, two_filename)
    assert two_file_json == sports_quark.get_json()


def test_AtomUnit_quark_file_exists_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    x_real_dir = f"{reals_dir()}/{real_id()}"
    x_persons_dir = f"{x_real_dir}/persons"
    sue_text = "Sue"
    sue_person_dir = f"{x_persons_dir}/{sue_text}"
    sue_quarks_dir = f"{sue_person_dir}/quarks"
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_quark2_path = f"{sue_quarks_dir}/{two_filename}"
    sue_quark6_path = f"{sue_quarks_dir}/{six_filename}"
    print(f"{sue_quark2_path=}")
    print(f"{sue_quark6_path=}")
    farm_atomunit = atomunit_shop(sue_text, _quarks_dir=sue_quarks_dir)
    assert os_path_exists(sue_quark2_path) is False
    assert farm_atomunit.quark_file_exists(two_int) is False

    # WHEN
    sports_quark = get_quark_example_ideaunit_sports()
    farm_atomunit._save_quark_file(two_int, sports_quark)

    # THEN
    assert farm_atomunit.quark_file_exists(two_int)


def test_AtomUnit_open_quark_file_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    x_real_dir = f"{reals_dir()}/{real_id()}"
    x_persons_dir = f"{x_real_dir}/persons"
    sue_text = "Sue"
    sue_person_dir = f"{x_persons_dir}/{sue_text}"
    sue_quarks_dir = f"{sue_person_dir}/quarks"
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_quark2_path = f"{sue_quarks_dir}/{two_filename}"
    sue_quark6_path = f"{sue_quarks_dir}/{six_filename}"
    print(f"{sue_quark2_path=}")
    print(f"{sue_quark6_path=}")
    farm_atomunit = atomunit_shop(sue_text, _quarks_dir=sue_quarks_dir)
    sports_quark = get_quark_example_ideaunit_sports()
    farm_atomunit._save_quark_file(two_int, sports_quark)
    assert farm_atomunit.quark_file_exists(two_int)

    # WHEN
    file_quark = farm_atomunit._open_quark_file(two_int)

    # THEN
    assert file_quark == sports_quark


def test_AtomUnit_save_atom_file_SavesCorrectFile(env_dir_setup_cleanup):
    # GIVEN
    x_real_dir = f"{reals_dir()}/{real_id()}"
    x_persons_dir = f"{x_real_dir}/persons"
    sue_text = "Sue"
    sue_atom_id = 2
    sue_person_dir = f"{x_persons_dir}/{sue_text}"
    sue_atoms_dir = f"{sue_person_dir}/{get_atoms_folder()}"
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = f"{sue_atoms_dir}/{two_filename}"
    sue_atom6_path = f"{sue_atoms_dir}/{six_filename}"
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    farm_atomunit = atomunit_shop(sue_text, None, sue_atom_id, _atoms_dir=sue_atoms_dir)
    assert os_path_exists(sue_atom2_path) is False
    assert os_path_exists(sue_atom6_path) is False

    # WHEN
    farm_atomunit._save_atom_file()

    # THEN
    assert os_path_exists(sue_atom2_path)
    assert os_path_exists(sue_atom6_path) is False
    atom_file_json = open_file(sue_atoms_dir, two_filename)
    atom_file_dict = get_dict_from_json(atom_file_json)
    print(f"{atom_file_dict=}")
    assert atom_file_dict.get("nuc_quark_numbers") == []
    assert atom_file_dict.get("person_id") == sue_text
    assert atom_file_dict.get("faces") == {}


def test_AtomUnit_atom_file_exists_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    x_real_dir = f"{reals_dir()}/{real_id()}"
    x_persons_dir = f"{x_real_dir}/persons"
    sue_text = "Sue"
    sue_person_dir = f"{x_persons_dir}/{sue_text}"
    sue_atoms_dir = f"{sue_person_dir}/{get_atoms_folder()}"
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = f"{sue_atoms_dir}/{two_filename}"
    sue_atom6_path = f"{sue_atoms_dir}/{six_filename}"
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    farm_atomunit = atomunit_shop(sue_text, _atoms_dir=sue_atoms_dir)
    assert os_path_exists(sue_atom2_path) is False
    assert farm_atomunit.atom_file_exists() is False

    # WHEN
    farm_atomunit._save_atom_file()

    # THEN
    assert farm_atomunit.atom_file_exists()


def test_AtomUnit_save_files_CorrectlySavesFiles(env_dir_setup_cleanup):
    # GIVEN
    x_real_dir = f"{reals_dir()}/{real_id()}"
    x_persons_dir = f"{x_real_dir}/persons"
    sue_text = "Sue"
    sue_person_dir = f"{x_persons_dir}/{sue_text}"
    sue_quarks_dir = f"{sue_person_dir}/quarks"
    sue_atoms_dir = f"{sue_person_dir}/{get_atoms_folder()}"

    tim_text = "Tim"
    yao_text = "Yao"
    farm_nuc_start = 4
    farm_atomunit = atomunit_shop(
        sue_text, _quarks_dir=sue_quarks_dir, _atoms_dir=sue_atoms_dir
    )
    farm_atomunit.set_nuc_start(farm_nuc_start)
    farm_atomunit.set_face(tim_text)
    farm_atomunit.set_face(yao_text)
    four_int = 4
    five_int = 5
    four_quark = get_quark_example_ideaunit_sports()
    five_quark = get_quark_example_ideaunit_knee()
    farm_atomunit._nucunit.set_quarkunit(four_quark)
    farm_atomunit._nucunit.set_quarkunit(five_quark)
    assert farm_atomunit.atom_file_exists() is False
    assert farm_atomunit.quark_file_exists(four_int) is False
    assert farm_atomunit.quark_file_exists(five_int) is False

    # WHEN
    farm_atomunit.save_files()

    # THEN
    assert farm_atomunit.atom_file_exists()
    assert farm_atomunit.quark_file_exists(four_int)
    assert farm_atomunit.quark_file_exists(five_int)


def test_AtomUnit_create_nucunit_from_quark_files_SetsAttr(env_dir_setup_cleanup):
    # GIVEN
    x_real_dir = f"{reals_dir()}/{real_id()}"
    x_persons_dir = f"{x_real_dir}/persons"
    sue_text = "Sue"
    sue_person_dir = f"{x_persons_dir}/{sue_text}"
    sue_quarks_dir = f"{sue_person_dir}/quarks"

    sue_atomunit = atomunit_shop(sue_text, _quarks_dir=sue_quarks_dir)
    four_int = 4
    five_int = 5
    nine_int = 9
    four_quark = get_quark_example_ideaunit_sports()
    five_quark = get_quark_example_ideaunit_knee()
    nine_quark = get_quark_example_ideaunit_ball()
    sue_atomunit._save_quark_file(four_int, four_quark)
    sue_atomunit._save_quark_file(five_int, five_quark)
    sue_atomunit._save_quark_file(nine_int, nine_quark)
    assert sue_atomunit._nucunit == nucunit_shop()

    # WHEN
    quarks_list = [four_int, five_int, nine_int]
    sue_atomunit._create_nucunit_from_quark_files(quarks_list)

    # THEN
    static_nucunit = nucunit_shop()
    static_nucunit.set_quarkunit(four_quark)
    static_nucunit.set_quarkunit(five_quark)
    static_nucunit.set_quarkunit(nine_quark)
    assert sue_atomunit._nucunit != nucunit_shop()
    assert sue_atomunit._nucunit == static_nucunit


def test_create_atomunit_from_files_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    x_real_dir = f"{reals_dir()}/{real_id()}"
    x_persons_dir = f"{x_real_dir}/persons"
    sue_text = "Sue"
    sue_person_dir = f"{x_persons_dir}/{sue_text}"
    sue_quarks_dir = f"{sue_person_dir}/quarks"
    sue_atoms_dir = f"{sue_person_dir}/{get_atoms_folder()}"

    tim_text = "Tim"
    yao_text = "Yao"
    sue_nuc_start = 4
    src_sue_atomunit = atomunit_shop(
        sue_text, _quarks_dir=sue_quarks_dir, _atoms_dir=sue_atoms_dir
    )
    src_sue_atomunit.set_nuc_start(sue_nuc_start)
    src_sue_atomunit.set_face(tim_text)
    src_sue_atomunit.set_face(yao_text)
    sports_quark = get_quark_example_ideaunit_sports()
    knee_quark = get_quark_example_ideaunit_knee()
    ball_quark = get_quark_example_ideaunit_ball()
    src_sue_atomunit._nucunit.set_quarkunit(sports_quark)
    src_sue_atomunit._nucunit.set_quarkunit(knee_quark)
    src_sue_atomunit._nucunit.set_quarkunit(ball_quark)
    src_sue_atomunit.save_files()

    # WHEN
    new_sue_atomunit = create_atomunit_from_files(
        atoms_dir=sue_atoms_dir,
        atom_id=src_sue_atomunit._atom_id,
        quarks_dir=sue_quarks_dir,
    )

    # THEN
    assert src_sue_atomunit.person_id == new_sue_atomunit.person_id
    assert src_sue_atomunit._faces == new_sue_atomunit._faces
    assert src_sue_atomunit._nucunit == new_sue_atomunit._nucunit
