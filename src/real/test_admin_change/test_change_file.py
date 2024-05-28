from src.agenda.book import bookunit_shop
from src.agenda.change import (
    changeunit_shop,
    create_changeunit_from_files,
    get_changes_folder,
)
from src.real.examples.example_atoms import (
    get_atom_example_ideaunit_sports,
    get_atom_example_ideaunit_knee,
    get_atom_example_ideaunit_ball,
)
from src.real.examples.real_env_kit import (
    get_test_reals_dir,
    get_test_real_id,
    reals_dir_setup_cleanup,
)
from src._instrument.python import get_dict_from_json
from src._instrument.file import open_file
from os.path import exists as os_path_exists


def test_ChangeUnit_save_atom_file_SavesCorrectFile(reals_dir_setup_cleanup):
    # GIVEN
    x_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    x_persons_dir = f"{x_real_dir}/persons"
    sue_text = "Sue"
    sue_person_dir = f"{x_persons_dir}/{sue_text}"
    sue_atoms_dir = f"{sue_person_dir}/atoms"
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = f"{sue_atoms_dir}/{two_filename}"
    sue_atom6_path = f"{sue_atoms_dir}/{six_filename}"
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    farm_changeunit = changeunit_shop(sue_text, _atoms_dir=sue_atoms_dir)
    assert os_path_exists(sue_atom2_path) == False
    assert os_path_exists(sue_atom6_path) == False

    # WHEN
    sports_atom = get_atom_example_ideaunit_sports()
    farm_changeunit._save_atom_file(two_int, sports_atom)

    # THEN
    assert os_path_exists(sue_atom2_path)
    assert os_path_exists(sue_atom6_path) == False
    two_file_json = open_file(sue_atoms_dir, two_filename)
    assert two_file_json == sports_atom.get_json()


def test_ChangeUnit_atom_file_exists_ReturnsCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    x_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    x_persons_dir = f"{x_real_dir}/persons"
    sue_text = "Sue"
    sue_person_dir = f"{x_persons_dir}/{sue_text}"
    sue_atoms_dir = f"{sue_person_dir}/atoms"
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = f"{sue_atoms_dir}/{two_filename}"
    sue_atom6_path = f"{sue_atoms_dir}/{six_filename}"
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    farm_changeunit = changeunit_shop(sue_text, _atoms_dir=sue_atoms_dir)
    assert os_path_exists(sue_atom2_path) == False
    assert farm_changeunit.atom_file_exists(two_int) == False

    # WHEN
    sports_atom = get_atom_example_ideaunit_sports()
    farm_changeunit._save_atom_file(two_int, sports_atom)

    # THEN
    assert farm_changeunit.atom_file_exists(two_int)


def test_ChangeUnit_open_atom_file_ReturnsCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    x_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    x_persons_dir = f"{x_real_dir}/persons"
    sue_text = "Sue"
    sue_person_dir = f"{x_persons_dir}/{sue_text}"
    sue_atoms_dir = f"{sue_person_dir}/atoms"
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_atom2_path = f"{sue_atoms_dir}/{two_filename}"
    sue_atom6_path = f"{sue_atoms_dir}/{six_filename}"
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom6_path=}")
    farm_changeunit = changeunit_shop(sue_text, _atoms_dir=sue_atoms_dir)
    sports_atom = get_atom_example_ideaunit_sports()
    farm_changeunit._save_atom_file(two_int, sports_atom)
    assert farm_changeunit.atom_file_exists(two_int)

    # WHEN
    file_atom = farm_changeunit._open_atom_file(two_int)

    # THEN
    assert file_atom == sports_atom


def test_ChangeUnit_save_change_file_SavesCorrectFile(reals_dir_setup_cleanup):
    # GIVEN
    x_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    x_persons_dir = f"{x_real_dir}/persons"
    sue_text = "Sue"
    sue_change_id = 2
    sue_person_dir = f"{x_persons_dir}/{sue_text}"
    sue_changes_dir = f"{sue_person_dir}/{get_changes_folder()}"
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_change2_path = f"{sue_changes_dir}/{two_filename}"
    sue_change6_path = f"{sue_changes_dir}/{six_filename}"
    print(f"{sue_change2_path=}")
    print(f"{sue_change6_path=}")
    farm_changeunit = changeunit_shop(
        sue_text, sue_change_id, _changes_dir=sue_changes_dir
    )
    assert os_path_exists(sue_change2_path) == False
    assert os_path_exists(sue_change6_path) == False

    # WHEN
    farm_changeunit._save_change_file()

    # THEN
    assert os_path_exists(sue_change2_path)
    assert os_path_exists(sue_change6_path) == False
    change_file_json = open_file(sue_changes_dir, two_filename)
    change_file_dict = get_dict_from_json(change_file_json)
    print(f"{change_file_dict=}")
    assert change_file_dict.get("book_atom_numbers") == []
    assert change_file_dict.get("giver") == sue_text
    assert change_file_dict.get("faces") == {}


def test_ChangeUnit_change_file_exists_ReturnsCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    x_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    x_persons_dir = f"{x_real_dir}/persons"
    sue_text = "Sue"
    sue_person_dir = f"{x_persons_dir}/{sue_text}"
    sue_changes_dir = f"{sue_person_dir}/{get_changes_folder()}"
    two_int = 2
    six_int = 6
    two_filename = f"{two_int}.json"
    six_filename = f"{six_int}.json"
    sue_change2_path = f"{sue_changes_dir}/{two_filename}"
    sue_change6_path = f"{sue_changes_dir}/{six_filename}"
    print(f"{sue_change2_path=}")
    print(f"{sue_change6_path=}")
    farm_changeunit = changeunit_shop(sue_text, _changes_dir=sue_changes_dir)
    assert os_path_exists(sue_change2_path) == False
    assert farm_changeunit.change_file_exists() == False

    # WHEN
    farm_changeunit._save_change_file()

    # THEN
    assert farm_changeunit.change_file_exists()


def test_ChangeUnit_save_files_CorrectlySavesFiles(reals_dir_setup_cleanup):
    # GIVEN
    x_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    x_persons_dir = f"{x_real_dir}/persons"
    sue_text = "Sue"
    sue_person_dir = f"{x_persons_dir}/{sue_text}"
    sue_atoms_dir = f"{sue_person_dir}/atoms"
    sue_changes_dir = f"{sue_person_dir}/{get_changes_folder()}"

    tim_text = "Tim"
    yao_text = "Yao"
    farm_book_start = 4
    farm_changeunit = changeunit_shop(
        sue_text, _atoms_dir=sue_atoms_dir, _changes_dir=sue_changes_dir
    )
    farm_changeunit.set_book_start(farm_book_start)
    farm_changeunit.set_face(tim_text)
    farm_changeunit.set_face(yao_text)
    four_int = 4
    five_int = 5
    four_atom = get_atom_example_ideaunit_sports()
    five_atom = get_atom_example_ideaunit_knee()
    farm_changeunit._bookunit.set_agendaatom(four_atom)
    farm_changeunit._bookunit.set_agendaatom(five_atom)
    assert farm_changeunit.change_file_exists() == False
    assert farm_changeunit.atom_file_exists(four_int) == False
    assert farm_changeunit.atom_file_exists(five_int) == False

    # WHEN
    farm_changeunit.save_files()

    # THEN
    assert farm_changeunit.change_file_exists()
    assert farm_changeunit.atom_file_exists(four_int)
    assert farm_changeunit.atom_file_exists(five_int)


def test_ChangeUnit_create_bookunit_from_atom_files_SetsAttr(reals_dir_setup_cleanup):
    # GIVEN
    x_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    x_persons_dir = f"{x_real_dir}/persons"
    sue_text = "Sue"
    sue_person_dir = f"{x_persons_dir}/{sue_text}"
    sue_atoms_dir = f"{sue_person_dir}/atoms"

    sue_changeunit = changeunit_shop(sue_text, _atoms_dir=sue_atoms_dir)
    four_int = 4
    five_int = 5
    nine_int = 9
    four_atom = get_atom_example_ideaunit_sports()
    five_atom = get_atom_example_ideaunit_knee()
    nine_atom = get_atom_example_ideaunit_ball()
    sue_changeunit._save_atom_file(four_int, four_atom)
    sue_changeunit._save_atom_file(five_int, five_atom)
    sue_changeunit._save_atom_file(nine_int, nine_atom)
    assert sue_changeunit._bookunit == bookunit_shop()

    # WHEN
    atoms_list = [four_int, five_int, nine_int]
    sue_changeunit._create_bookunit_from_atom_files(atoms_list)

    # THEN
    static_bookunit = bookunit_shop()
    static_bookunit.set_agendaatom(four_atom)
    static_bookunit.set_agendaatom(five_atom)
    static_bookunit.set_agendaatom(nine_atom)
    assert sue_changeunit._bookunit != bookunit_shop()
    assert sue_changeunit._bookunit == static_bookunit


def test_create_changeunit_from_files_ReturnsCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    x_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    x_persons_dir = f"{x_real_dir}/persons"
    sue_text = "Sue"
    sue_person_dir = f"{x_persons_dir}/{sue_text}"
    sue_atoms_dir = f"{sue_person_dir}/atoms"
    sue_changes_dir = f"{sue_person_dir}/{get_changes_folder()}"

    tim_text = "Tim"
    yao_text = "Yao"
    sue_book_start = 4
    src_sue_changeunit = changeunit_shop(
        sue_text, _atoms_dir=sue_atoms_dir, _changes_dir=sue_changes_dir
    )
    src_sue_changeunit.set_book_start(sue_book_start)
    src_sue_changeunit.set_face(tim_text)
    src_sue_changeunit.set_face(yao_text)
    sports_atom = get_atom_example_ideaunit_sports()
    knee_atom = get_atom_example_ideaunit_knee()
    ball_atom = get_atom_example_ideaunit_ball()
    src_sue_changeunit._bookunit.set_agendaatom(sports_atom)
    src_sue_changeunit._bookunit.set_agendaatom(knee_atom)
    src_sue_changeunit._bookunit.set_agendaatom(ball_atom)
    src_sue_changeunit.save_files()

    # WHEN
    new_sue_changeunit = create_changeunit_from_files(
        changes_dir=sue_changes_dir,
        change_id=src_sue_changeunit._change_id,
        atoms_dir=sue_atoms_dir,
    )

    # THEN
    assert src_sue_changeunit._giver == new_sue_changeunit._giver
    assert src_sue_changeunit._faces == new_sue_changeunit._faces
    assert src_sue_changeunit._bookunit == new_sue_changeunit._bookunit
