from src.agenda.book import bookunit_shop
from src.world.gift import GiftUnit, giftunit_shop
from src.world.examples.example_atoms import (
    get_atom_example_ideaunit_sports,
    get_bookunit_carm_example,
)
from src.instrument.python import x_is_json
from pytest import raises as pytest_raises


def test_GiftUnit_exists():
    # GIVEN / WHEN
    x_giftunit = GiftUnit()

    # THEN
    assert x_giftunit._gift_id is None
    assert x_giftunit._gifter is None
    assert x_giftunit._giftees is None
    assert x_giftunit._bookunit is None
    assert x_giftunit._book_start is None
    assert x_giftunit._person_dir is None
    assert x_giftunit._gifts_dir is None
    assert x_giftunit._atoms_dir is None


def test_giftunit_shop_ReturnsCorrectObjGivenEmptyArgs():
    # GIVEN
    bob_text = "Bob"

    # WHEN
    farm_giftunit = giftunit_shop(_gifter=bob_text)

    # THEN
    assert farm_giftunit._gift_id == 0
    assert farm_giftunit._gifter == bob_text
    assert farm_giftunit._giftees == set()
    assert farm_giftunit._bookunit == bookunit_shop()
    assert farm_giftunit._book_start == 0
    assert farm_giftunit._person_dir is None
    assert farm_giftunit._gifts_dir is None
    assert farm_giftunit._atoms_dir is None


def test_giftunit_shop_ReturnsCorrectObjGivenNonEmptyArgs():
    # GIVEN
    bob_text = "Bob"
    bob_gift_id = 13
    bob_giftees = {"Sue", "Yao"}
    bob_bookunit = get_bookunit_carm_example()
    bob_book_start = 6
    bob_person_dir = "exampletext5"
    bob_gifts_dir = "exampletext7"
    bob_atoms_dir = "exampletext9"

    # WHEN
    farm_giftunit = giftunit_shop(
        bob_text,
        _gift_id=bob_gift_id,
        _giftees=bob_giftees,
        _bookunit=bob_bookunit,
        _book_start=bob_book_start,
        _person_dir=bob_person_dir,
        _gifts_dir=bob_gifts_dir,
        _atoms_dir=bob_atoms_dir,
    )

    # THEN
    assert farm_giftunit._gifter == bob_text
    assert farm_giftunit._gift_id == bob_gift_id
    assert farm_giftunit._giftees == bob_giftees
    assert farm_giftunit._bookunit == bob_bookunit
    assert farm_giftunit._book_start == bob_book_start
    assert farm_giftunit._person_dir == bob_person_dir
    assert farm_giftunit._gifts_dir == bob_gifts_dir
    assert farm_giftunit._atoms_dir == bob_atoms_dir


def test_giftunit_shop_ReturnsCorrectObjGivenSomeArgs_v1():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    x_giftees = {bob_text, tim_text, yao_text}

    # WHEN
    farm_giftunit = giftunit_shop(_gifter=bob_text, _giftees=x_giftees)

    # THEN
    assert farm_giftunit._gifter == bob_text
    assert farm_giftunit._giftees == x_giftees


def test_GiftUnit_set_giftee_SetsAttribute():
    # GIVEN
    bob_text = "Bob"
    farm_giftunit = giftunit_shop(_gifter=bob_text)
    tim_text = "Tim"
    assert farm_giftunit._giftees == set()
    assert tim_text not in farm_giftunit._giftees

    # WHEN
    farm_giftunit.set_giftee(tim_text)

    # THEN
    assert tim_text in farm_giftunit._giftees


def test_GiftUnit_giftee_exists_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    farm_giftunit = giftunit_shop(_gifter=bob_text)
    tim_text = "Tim"
    assert farm_giftunit._giftees == set()
    assert tim_text not in farm_giftunit._giftees

    # WHEN / THEN
    assert farm_giftunit.giftee_exists(tim_text) == False

    # WHEN / THEN
    farm_giftunit.set_giftee(tim_text)
    assert farm_giftunit.giftee_exists(tim_text)


def test_GiftUnit_del_giftee_SetsAttribute():
    # GIVEN
    bob_text = "Bob"
    farm_giftunit = giftunit_shop(_gifter=bob_text)
    tim_text = "Tim"
    yao_text = "Yao"
    farm_giftunit.set_giftee(tim_text)
    farm_giftunit.set_giftee(yao_text)
    assert farm_giftunit.giftee_exists(tim_text)
    assert farm_giftunit.giftee_exists(yao_text)

    # WHEN
    farm_giftunit.del_giftee(yao_text)

    # THEN
    assert farm_giftunit.giftee_exists(tim_text)
    assert farm_giftunit.giftee_exists(yao_text) == False


def test_GiftUnit_set_bookunit_SetsAttribute():
    # GIVEN
    bob_text = "Bob"
    farm_giftunit = giftunit_shop(_gifter=bob_text)
    assert farm_giftunit._bookunit == bookunit_shop()

    # WHEN
    farm_bookunit = bookunit_shop()
    farm_bookunit.set_agendaatom(get_atom_example_ideaunit_sports())
    farm_giftunit.set_bookunit(farm_bookunit)

    # THEN
    assert farm_giftunit._bookunit == farm_bookunit


def test_GiftUnit_set_book_start_SetsAttribute():
    # GIVEN
    bob_text = "Bob"
    farm_giftunit = giftunit_shop(bob_text)
    assert farm_giftunit._book_start == 0

    # WHEN
    farm_book_start = 11
    farm_giftunit.set_book_start(farm_book_start)

    # THEN
    assert farm_giftunit._book_start == farm_book_start


def test_GiftUnit_agendaatom_exists_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    farm_bookunit = bookunit_shop()
    farm_giftunit = giftunit_shop(_gifter=bob_text)
    farm_giftunit.set_bookunit(farm_bookunit)

    # WHEN
    sports_agendaatom = get_atom_example_ideaunit_sports()

    # THEN
    assert farm_giftunit.agendaatom_exists(sports_agendaatom) == False

    # WHEN
    farm_bookunit.set_agendaatom(sports_agendaatom)
    farm_giftunit.set_bookunit(farm_bookunit)

    # THEN
    assert farm_giftunit.agendaatom_exists(sports_agendaatom)


def test_GiftUnit_del_bookunit_SetsAttribute():
    # GIVEN
    bob_text = "Bob"
    farm_bookunit = bookunit_shop()
    farm_bookunit.set_agendaatom(get_atom_example_ideaunit_sports())
    farm_giftunit = giftunit_shop(_gifter=bob_text, _bookunit=farm_bookunit)
    assert farm_giftunit._bookunit != bookunit_shop()
    assert farm_giftunit._bookunit == farm_bookunit

    # WHEN
    farm_giftunit.del_bookunit()

    # THEN
    assert farm_giftunit._bookunit == bookunit_shop()


def test_GiftUnit_get_step_dict_ReturnsCorrectObj_Simple():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    farm_giftunit = giftunit_shop(_gifter=bob_text)
    farm_giftunit.set_giftee(tim_text)
    farm_giftunit.set_giftee(yao_text)

    # WHEN
    x_dict = farm_giftunit.get_step_dict()

    # THEN
    gifter_text = "gifter"
    assert x_dict.get(gifter_text) != None
    assert x_dict.get(gifter_text) == bob_text

    giftees_text = "giftees"
    assert x_dict.get(giftees_text) != None
    giftees_dict = x_dict.get(giftees_text)
    assert giftees_dict.get(bob_text) is None
    assert giftees_dict.get(tim_text) != None
    assert giftees_dict.get(yao_text) != None

    book_text = "book"
    assert x_dict.get(book_text) != None
    assert x_dict.get(book_text) == bookunit_shop().get_ordered_agendaatoms()
    assert x_dict.get(book_text) == {}


def test_GiftUnit_get_step_dict_ReturnsCorrectObj_WithBookPopulated():
    # GIVEN
    bob_text = "Bob"
    carm_bookunit = get_bookunit_carm_example()
    farm_giftunit = giftunit_shop(bob_text, _bookunit=carm_bookunit)

    # WHEN
    x_dict = farm_giftunit.get_step_dict()

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


def test_GiftUnit_get_step_dict_ReturnsCorrectObj_book_start():
    # GIVEN
    bob_text = "Bob"
    carm_bookunit = get_bookunit_carm_example()
    farm_book_start = 7
    farm_giftunit = giftunit_shop(
        bob_text, _bookunit=carm_bookunit, _book_start=farm_book_start
    )

    # WHEN
    x_dict = farm_giftunit.get_step_dict()

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


def test_GiftUnit_get_book_atom_numbers_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    carm_bookunit = get_bookunit_carm_example()
    farm_book_start = 7
    farm_giftunit = giftunit_shop(bob_text)
    farm_giftunit.set_bookunit(carm_bookunit)
    farm_giftunit.set_book_start(farm_book_start)
    farm_giftunit.set_giftee(tim_text)
    farm_giftunit.set_giftee(yao_text)
    farm_dict = farm_giftunit.get_step_dict()

    # WHEN
    farm_book_atom_numbers = farm_giftunit.get_book_atom_numbers(farm_dict)
    # THEN
    assert farm_book_atom_numbers == [farm_book_start, farm_book_start + 1]


def test_GiftUnit_get_giftmetric_dict_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    carm_bookunit = get_bookunit_carm_example()
    farm_book_start = 7
    farm_giftunit = giftunit_shop(bob_text)
    farm_giftunit.set_bookunit(carm_bookunit)
    farm_giftunit.set_book_start(farm_book_start)
    farm_giftunit.set_giftee(tim_text)
    farm_giftunit.set_giftee(yao_text)

    # WHEN
    x_dict = farm_giftunit.get_giftmetric_dict()

    # THEN
    gifter_text = "gifter"
    assert x_dict.get(gifter_text) != None
    assert x_dict.get(gifter_text) == bob_text

    giftees_text = "giftees"
    assert x_dict.get(giftees_text) != None
    giftees_dict = x_dict.get(giftees_text)
    assert giftees_dict.get(bob_text) is None
    assert giftees_dict.get(tim_text) != None
    assert giftees_dict.get(yao_text) != None

    book_atom_numbers_text = "book_atom_numbers"
    assert x_dict.get(book_atom_numbers_text) != None
    assert x_dict.get(book_atom_numbers_text) == [7, 8]

    book_min_text = "book_min"
    assert x_dict.get(book_min_text) is None
    book_max_text = "book_max"
    assert x_dict.get(book_max_text) is None


def test_GiftUnit_get_bookmetric_json_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    carm_bookunit = get_bookunit_carm_example()
    farm_book_start = 7
    farm_giftunit = giftunit_shop(bob_text)
    farm_giftunit.set_bookunit(carm_bookunit)
    farm_giftunit.set_book_start(farm_book_start)
    farm_giftunit.set_giftee(tim_text)
    farm_giftunit.set_giftee(yao_text)

    # WHEN
    farm_json = farm_giftunit.get_bookmetric_json()

    # THEN
    assert x_is_json(farm_json)
