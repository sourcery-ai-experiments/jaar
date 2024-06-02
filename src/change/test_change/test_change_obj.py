from src._road.jaar_config import init_change_id, get_changes_folder
from src.change.book import bookunit_shop
from src.change.change import ChangeUnit, changeunit_shop, get_init_change_id_if_None
from src.change.examples.example_books import (
    get_atom_example_ideaunit_sports,
    get_bookunit_carm_example,
)
from src._instrument.python import x_is_json


def test_get_changes_folder_ReturnsCorrectObj():
    # GIVEN / WHEN / THEN
    assert get_changes_folder() == "changes"


def test_init_change_id_ReturnsCorrectObj():
    # GIVEN / WHEN / THEN
    assert init_change_id() == 0


def test_get_init_change_id_if_None_ReturnsCorrectObj():
    # GIVEN / WHEN / THEN
    assert get_init_change_id_if_None() == init_change_id()
    assert get_init_change_id_if_None(None) == init_change_id()
    assert get_init_change_id_if_None(1) == 1


def test_ChangeUnit_exists():
    # GIVEN / WHEN
    x_changeunit = ChangeUnit()

    # THEN
    assert x_changeunit._change_id is None
    assert x_changeunit._giver is None
    assert x_changeunit._faces is None
    assert x_changeunit._bookunit is None
    assert x_changeunit._book_start is None
    assert x_changeunit._changes_dir is None
    assert x_changeunit._atoms_dir is None


def test_changeunit_shop_ReturnsCorrectObjGivenEmptyArgs():
    # GIVEN
    bob_text = "Bob"

    # WHEN
    farm_changeunit = changeunit_shop(_giver=bob_text)

    # THEN
    assert farm_changeunit._change_id == 0
    assert farm_changeunit._giver == bob_text
    assert farm_changeunit._faces == set()
    assert farm_changeunit._bookunit == bookunit_shop()
    assert farm_changeunit._book_start == 0
    assert farm_changeunit._changes_dir is None
    assert farm_changeunit._atoms_dir is None


def test_changeunit_shop_ReturnsCorrectObjGivenNonEmptyArgs():
    # GIVEN
    bob_text = "Bob"
    bob_change_id = 13
    bob_faces = {"Sue", "Yao"}
    bob_bookunit = get_bookunit_carm_example()
    bob_book_start = 6
    bob_changes_dir = "exampletext7"
    bob_atoms_dir = "exampletext9"

    # WHEN
    farm_changeunit = changeunit_shop(
        bob_text,
        _change_id=bob_change_id,
        _faces=bob_faces,
        _bookunit=bob_bookunit,
        _book_start=bob_book_start,
        _changes_dir=bob_changes_dir,
        _atoms_dir=bob_atoms_dir,
    )

    # THEN
    assert farm_changeunit._giver == bob_text
    assert farm_changeunit._change_id == bob_change_id
    assert farm_changeunit._faces == bob_faces
    assert farm_changeunit._bookunit == bob_bookunit
    assert farm_changeunit._book_start == bob_book_start
    assert farm_changeunit._changes_dir == bob_changes_dir
    assert farm_changeunit._atoms_dir == bob_atoms_dir


def test_changeunit_shop_ReturnsCorrectObjGivenSomeArgs_v1():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    x_faces = {bob_text, tim_text, yao_text}

    # WHEN
    farm_changeunit = changeunit_shop(_giver=bob_text, _faces=x_faces)

    # THEN
    assert farm_changeunit._giver == bob_text
    assert farm_changeunit._faces == x_faces


def test_ChangeUnit_set_face_SetsAttribute():
    # GIVEN
    bob_text = "Bob"
    farm_changeunit = changeunit_shop(_giver=bob_text)
    tim_text = "Tim"
    assert farm_changeunit._faces == set()
    assert tim_text not in farm_changeunit._faces

    # WHEN
    farm_changeunit.set_face(tim_text)

    # THEN
    assert tim_text in farm_changeunit._faces


def test_ChangeUnit_face_exists_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    farm_changeunit = changeunit_shop(_giver=bob_text)
    tim_text = "Tim"
    assert farm_changeunit._faces == set()
    assert tim_text not in farm_changeunit._faces

    # WHEN / THEN
    assert farm_changeunit.face_exists(tim_text) == False

    # WHEN / THEN
    farm_changeunit.set_face(tim_text)
    assert farm_changeunit.face_exists(tim_text)


def test_ChangeUnit_del_face_SetsAttribute():
    # GIVEN
    bob_text = "Bob"
    farm_changeunit = changeunit_shop(_giver=bob_text)
    tim_text = "Tim"
    yao_text = "Yao"
    farm_changeunit.set_face(tim_text)
    farm_changeunit.set_face(yao_text)
    assert farm_changeunit.face_exists(tim_text)
    assert farm_changeunit.face_exists(yao_text)

    # WHEN
    farm_changeunit.del_face(yao_text)

    # THEN
    assert farm_changeunit.face_exists(tim_text)
    assert farm_changeunit.face_exists(yao_text) == False


def test_ChangeUnit_set_bookunit_SetsAttribute():
    # GIVEN
    bob_text = "Bob"
    farm_changeunit = changeunit_shop(_giver=bob_text)
    assert farm_changeunit._bookunit == bookunit_shop()

    # WHEN
    farm_bookunit = bookunit_shop()
    farm_bookunit.set_agendaatom(get_atom_example_ideaunit_sports())
    farm_changeunit.set_bookunit(farm_bookunit)

    # THEN
    assert farm_changeunit._bookunit == farm_bookunit


def test_ChangeUnit_set_book_start_SetsAttribute():
    # GIVEN
    bob_text = "Bob"
    farm_changeunit = changeunit_shop(bob_text)
    assert farm_changeunit._book_start == 0

    # WHEN
    farm_book_start = 11
    farm_changeunit.set_book_start(farm_book_start)

    # THEN
    assert farm_changeunit._book_start == farm_book_start


def test_ChangeUnit_agendaatom_exists_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    farm_bookunit = bookunit_shop()
    farm_changeunit = changeunit_shop(_giver=bob_text)
    farm_changeunit.set_bookunit(farm_bookunit)

    # WHEN
    sports_agendaatom = get_atom_example_ideaunit_sports()

    # THEN
    assert farm_changeunit.agendaatom_exists(sports_agendaatom) == False

    # WHEN
    farm_bookunit.set_agendaatom(sports_agendaatom)
    farm_changeunit.set_bookunit(farm_bookunit)

    # THEN
    assert farm_changeunit.agendaatom_exists(sports_agendaatom)


def test_ChangeUnit_del_bookunit_SetsAttribute():
    # GIVEN
    bob_text = "Bob"
    farm_bookunit = bookunit_shop()
    farm_bookunit.set_agendaatom(get_atom_example_ideaunit_sports())
    farm_changeunit = changeunit_shop(_giver=bob_text, _bookunit=farm_bookunit)
    assert farm_changeunit._bookunit != bookunit_shop()
    assert farm_changeunit._bookunit == farm_bookunit

    # WHEN
    farm_changeunit.del_bookunit()

    # THEN
    assert farm_changeunit._bookunit == bookunit_shop()


def test_ChangeUnit_get_step_dict_ReturnsCorrectObj_Simple():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    farm_changeunit = changeunit_shop(_giver=bob_text)
    farm_changeunit.set_face(tim_text)
    farm_changeunit.set_face(yao_text)

    # WHEN
    x_dict = farm_changeunit.get_step_dict()

    # THEN
    giver_text = "giver"
    assert x_dict.get(giver_text) != None
    assert x_dict.get(giver_text) == bob_text

    faces_text = "faces"
    assert x_dict.get(faces_text) != None
    faces_dict = x_dict.get(faces_text)
    assert faces_dict.get(bob_text) is None
    assert faces_dict.get(tim_text) != None
    assert faces_dict.get(yao_text) != None

    book_text = "book"
    assert x_dict.get(book_text) != None
    assert x_dict.get(book_text) == bookunit_shop().get_ordered_agendaatoms()
    assert x_dict.get(book_text) == {}


def test_ChangeUnit_get_step_dict_ReturnsCorrectObj_WithBookPopulated():
    # GIVEN
    bob_text = "Bob"
    carm_bookunit = get_bookunit_carm_example()
    farm_changeunit = changeunit_shop(bob_text, _bookunit=carm_bookunit)

    # WHEN
    x_dict = farm_changeunit.get_step_dict()

    # THEN
    book_text = "book"
    assert x_dict.get(book_text) != None
    assert x_dict.get(book_text) == carm_bookunit.get_ordered_agendaatoms()
    carm_agendaatoms_dict = x_dict.get(book_text)
    print(f"{len(carm_bookunit.get_sorted_agendaatoms())=}")
    print(f"{carm_agendaatoms_dict.keys()=}")
    # print(f"{carm_agendaatoms_dict.get(0)=}")
    assert carm_agendaatoms_dict.get(2) is None
    assert carm_agendaatoms_dict.get(0) != None
    assert carm_agendaatoms_dict.get(1) != None


def test_ChangeUnit_get_step_dict_ReturnsCorrectObj_book_start():
    # GIVEN
    bob_text = "Bob"
    carm_bookunit = get_bookunit_carm_example()
    farm_book_start = 7
    farm_changeunit = changeunit_shop(
        bob_text, _bookunit=carm_bookunit, _book_start=farm_book_start
    )

    # WHEN
    x_dict = farm_changeunit.get_step_dict()

    # THEN
    book_text = "book"
    assert x_dict.get(book_text) != None
    assert x_dict.get(book_text) == carm_bookunit.get_ordered_agendaatoms(
        farm_book_start
    )
    carm_agendaatoms_dict = x_dict.get(book_text)
    print(f"{len(carm_bookunit.get_sorted_agendaatoms())=}")
    print(f"{carm_agendaatoms_dict.keys()=}")
    # print(f"{carm_agendaatoms_dict.get(0)=}")
    assert carm_agendaatoms_dict.get(farm_book_start + 2) is None
    assert carm_agendaatoms_dict.get(farm_book_start + 0) != None
    assert carm_agendaatoms_dict.get(farm_book_start + 1) != None


def test_ChangeUnit_get_book_atom_numbers_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    carm_bookunit = get_bookunit_carm_example()
    farm_book_start = 7
    farm_changeunit = changeunit_shop(bob_text)
    farm_changeunit.set_bookunit(carm_bookunit)
    farm_changeunit.set_book_start(farm_book_start)
    farm_changeunit.set_face(tim_text)
    farm_changeunit.set_face(yao_text)
    farm_dict = farm_changeunit.get_step_dict()

    # WHEN
    farm_book_atom_numbers = farm_changeunit.get_book_atom_numbers(farm_dict)
    # THEN
    assert farm_book_atom_numbers == [farm_book_start, farm_book_start + 1]


def test_ChangeUnit_get_bookmetric_dict_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    carm_bookunit = get_bookunit_carm_example()
    farm_book_start = 7
    farm_changeunit = changeunit_shop(bob_text)
    farm_changeunit.set_bookunit(carm_bookunit)
    farm_changeunit.set_book_start(farm_book_start)
    farm_changeunit.set_face(tim_text)
    farm_changeunit.set_face(yao_text)

    # WHEN
    x_dict = farm_changeunit.get_bookmetric_dict()

    # THEN
    giver_text = "giver"
    assert x_dict.get(giver_text) != None
    assert x_dict.get(giver_text) == bob_text

    faces_text = "faces"
    assert x_dict.get(faces_text) != None
    faces_dict = x_dict.get(faces_text)
    assert faces_dict.get(bob_text) is None
    assert faces_dict.get(tim_text) != None
    assert faces_dict.get(yao_text) != None

    book_atom_numbers_text = "book_atom_numbers"
    assert x_dict.get(book_atom_numbers_text) != None
    assert x_dict.get(book_atom_numbers_text) == [7, 8]

    book_min_text = "book_min"
    assert x_dict.get(book_min_text) is None
    book_max_text = "book_max"
    assert x_dict.get(book_max_text) is None


def test_ChangeUnit_get_bookmetric_json_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    carm_bookunit = get_bookunit_carm_example()
    farm_book_start = 7
    farm_changeunit = changeunit_shop(bob_text)
    farm_changeunit.set_bookunit(carm_bookunit)
    farm_changeunit.set_book_start(farm_book_start)
    farm_changeunit.set_face(tim_text)
    farm_changeunit.set_face(yao_text)

    # WHEN
    farm_json = farm_changeunit.get_bookmetric_json()

    # THEN
    assert x_is_json(farm_json)
