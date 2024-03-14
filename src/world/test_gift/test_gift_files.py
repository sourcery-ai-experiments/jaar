from src._road.road import create_road_from_nodes as roadnodes
from src.agenda.book import bookunit_shop
from src.world.gift import GiftUnit, giftunit_shop, giftunit_get_from_dict
from src.world.examples.example_atoms import (
    get_atom_example_ideaunit_sports,
    get_atom_example_ideaunit_knee,
    get_bookunit_carm_example,
)
from src.world.examples.world_env_kit import (
    get_test_worlds_dir,
    get_test_world_id,
    worlds_dir_setup_cleanup,
)
from src.instrument.file import open_file
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_GiftUnit_save_atom_file_SavesCorrectFile(worlds_dir_setup_cleanup):
    # GIVEN
    x_world_dir = f"{get_test_worlds_dir()}/{get_test_world_id()}"
    x_persons_dir = f"{x_world_dir}/persons"
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
    farm_giftunit = giftunit_shop(sue_text, _atoms_dir=sue_atoms_dir)
    assert os_path_exists(sue_atom2_path) == False
    assert os_path_exists(sue_atom6_path) == False

    # WHEN
    sports_atom = get_atom_example_ideaunit_sports()
    farm_giftunit._save_atom_file(two_int, sports_atom)

    # THEN
    assert os_path_exists(sue_atom2_path)
    assert os_path_exists(sue_atom6_path) == False
    two_file_json = open_file(sue_atoms_dir, two_filename)
    assert two_file_json == sports_atom.get_json()


def test_GiftUnit_atom_file_exists_ReturnsCorrectObj(worlds_dir_setup_cleanup):
    # GIVEN
    x_world_dir = f"{get_test_worlds_dir()}/{get_test_world_id()}"
    x_persons_dir = f"{x_world_dir}/persons"
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
    farm_giftunit = giftunit_shop(sue_text, _atoms_dir=sue_atoms_dir)
    assert os_path_exists(sue_atom2_path) == False
    assert farm_giftunit.atom_file_exists(two_int) == False

    # WHEN
    sports_atom = get_atom_example_ideaunit_sports()
    farm_giftunit._save_atom_file(two_int, sports_atom)

    # THEN
    assert farm_giftunit.atom_file_exists(two_int)


def test_GiftUnit_open_atom_file_ReturnsCorrectObj(worlds_dir_setup_cleanup):
    # GIVEN
    x_world_dir = f"{get_test_worlds_dir()}/{get_test_world_id()}"
    x_persons_dir = f"{x_world_dir}/persons"
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
    farm_giftunit = giftunit_shop(sue_text, _atoms_dir=sue_atoms_dir)
    sports_atom = get_atom_example_ideaunit_sports()
    farm_giftunit._save_atom_file(two_int, sports_atom)
    assert farm_giftunit.atom_file_exists(two_int)

    # WHEN
    file_atom = farm_giftunit._open_atom_file(two_int)

    # THEN
    assert file_atom == sports_atom


def test_GiftUnit_save_files_CorrectlySavesFiles():
    # GIVEN
    x_world_dir = f"{get_test_worlds_dir()}/{get_test_world_id()}"
    x_persons_dir = f"{x_world_dir}/persons"
    sue_text = "Sue"
    sue_person_dir = f"{x_persons_dir}/{sue_text}"
    sue_atoms_dir = f"{sue_person_dir}/atoms"
    sue_gifts_dir = f"{sue_person_dir}/gifts"

    tim_text = "Tim"
    yao_text = "Yao"
    farm_book_start = 4
    farm_giftunit = giftunit_shop(
        sue_text, _atoms_dir=sue_atoms_dir, _gifts_dir=sue_gifts_dir
    )
    farm_giftunit.set_book_start(farm_book_start)
    farm_giftunit.set_giftee(tim_text)
    farm_giftunit.set_giftee(yao_text)
    four_int = 4
    five_int = 5
    four_atom = get_atom_example_ideaunit_sports()
    five_atom = get_atom_example_ideaunit_knee()
    farm_giftunit._bookunit.set_agendaatom(four_atom)
    farm_giftunit._bookunit.set_agendaatom(five_atom)
    assert farm_giftunit.gift_file_exists() == False
    assert farm_giftunit.atom_file_exists(four_int) == False
    assert farm_giftunit.atom_file_exists(five_int) == False

    # WHEN
    farm_dict = farm_giftunit.get_bookmetric_dict()

    # THEN
    assert farm_giftunit.gift_file_exists()
    assert farm_giftunit.atom_file_exists(four_int)
    assert farm_giftunit.atom_file_exists(five_int)


def test_giftunit_get_from_dict_ReturnsCorrectObj():
    # GIVEN
    x_world_dir = f"{get_test_worlds_dir()}/{get_test_world_id()}"
    x_persons_dir = f"{x_world_dir}/persons"
    sue_text = "Sue"
    sue_person_dir = f"{x_persons_dir}/{sue_text}"
    sue_atoms_dir = f"{sue_person_dir}/atoms"

    tim_text = "Tim"
    yao_text = "Yao"
    farm_book_start = 4
    src_farm_giftunit = giftunit_shop(sue_text, _atoms_dir=sue_atoms_dir)
    src_farm_giftunit.set_book_start(farm_book_start)
    src_farm_giftunit.set_giftee(tim_text)
    src_farm_giftunit.set_giftee(yao_text)
    four_int = 4
    five_int = 5
    four_atom = get_atom_example_ideaunit_sports()
    five_atom = get_atom_example_ideaunit_knee()
    src_farm_giftunit._bookunit.set_agendaatom(four_atom)
    src_farm_giftunit._bookunit.set_agendaatom(five_atom)
    src_farm_giftunit._save_atom_file(four_int, four_atom)
    src_farm_giftunit._save_atom_file(five_int, five_atom)

    # WHEN
    farm_dict = src_farm_giftunit.get_bookmetric_dict()
    built_farm_giftunit = giftunit_get_from_dict(farm_dict)

    # THEN
    assert src_farm_giftunit._gifter == built_farm_giftunit._gifter
    assert src_farm_giftunit._giftees == built_farm_giftunit._giftees
    assert src_farm_giftunit._bookunit == built_farm_giftunit._bookunit


# def test_GiftUnit_save_bookmetric_file_SavesCorrectFile(worlds_dir_setup_cleanup):
#     # GIVEN
#     sue_text = "Sue"
#     sue_world_dir = f"{get_test_worlds_dir()}/{get_test_world_id()}"
#     sue_persons_dir = f"{sue_world_dir}/persons"
#     sue_person_dir = f"{sue_persons_dir}/{sue_text}"
#     sue_gut_file_name = f"{get_gut_file_name()}.json"
#     sue_gut_path = f"{sue_person_dir}/{sue_gut_file_name}"
#     print(f"{sue_gut_path=}")
#     assert os_path_exists(sue_gut_path) == False
#     sue_person = personunit_shop(person_id=sue_text)
#     assert os_path_exists(sue_gut_path) == False
#     assert sue_person.gut_file_exists() == False

#     # WHEN
#     save_file(
#         dest_dir=sue_person.person_dir,
#         file_name=sue_person._gut_file_name,
#         file_text=agendaunit_shop(sue_text).get_json(),
#     )

#     # THEN
#     assert os_path_exists(sue_gut_path)
#     assert sue_person.gut_file_exists()


# def test_GiftUnit_exists():
#     # GIVEN / WHEN
#     x_giftunit = GiftUnit()

#     # THEN
#     assert x_giftunit._gifter is None
#     assert x_giftunit._giftees is None
#     assert x_giftunit._bookunit is None
#     assert x_giftunit._book_start is None


# def test_giftunit_shop_ReturnsCorrectObjGivenEmptyArgs():
#     # GIVEN
#     bob_text = "Bob"

#     # WHEN
#     farm_giftunit = giftunit_shop(_gifter=bob_text)

#     # THEN
#     assert farm_giftunit._gifter == bob_text
#     assert farm_giftunit._bookunit == bookunit_shop()
#     assert farm_giftunit._book_start == 0


# def test_giftunit_shop_ReturnsCorrectObjGivenEmptyArgs():
#     # GIVEN
#     bob_text = "Bob"
#     bob_bookunit = get_bookunit_carm_example()
#     bob_book_start = 6

#     # WHEN
#     farm_giftunit = giftunit_shop(
#         bob_text, _bookunit=bob_bookunit, _book_start=bob_book_start
#     )

#     # THEN
#     assert farm_giftunit._gifter == bob_text
#     assert farm_giftunit._bookunit == bob_bookunit
#     assert farm_giftunit._book_start == bob_book_start


# def test_giftunit_shop_ReturnsCorrectObjGivenSomeArgs_v1():
#     # GIVEN
#     bob_text = "Bob"
#     tim_text = "Tim"
#     yao_text = "Yao"
#     x_giftees = {bob_text, tim_text, yao_text}

#     # WHEN
#     farm_giftunit = giftunit_shop(_gifter=bob_text, _giftees=x_giftees)

#     # THEN
#     assert farm_giftunit._gifter == bob_text
#     assert farm_giftunit._giftees == x_giftees


# def test_GiftUnit_set_giftee_SetsAttribute():
#     # GIVEN
#     bob_text = "Bob"
#     farm_giftunit = giftunit_shop(_gifter=bob_text)
#     tim_text = "Tim"
#     assert farm_giftunit._giftees == set()
#     assert tim_text not in farm_giftunit._giftees

#     # WHEN
#     farm_giftunit.set_giftee(tim_text)

#     # THEN
#     assert tim_text in farm_giftunit._giftees


# def test_GiftUnit_giftee_exists_ReturnsCorrectObj():
#     # GIVEN
#     bob_text = "Bob"
#     farm_giftunit = giftunit_shop(_gifter=bob_text)
#     tim_text = "Tim"
#     assert farm_giftunit._giftees == set()
#     assert tim_text not in farm_giftunit._giftees

#     # WHEN / THEN
#     assert farm_giftunit.giftee_exists(tim_text) == False

#     # WHEN / THEN
#     farm_giftunit.set_giftee(tim_text)
#     assert farm_giftunit.giftee_exists(tim_text)


# def test_GiftUnit_del_giftee_SetsAttribute():
#     # GIVEN
#     bob_text = "Bob"
#     farm_giftunit = giftunit_shop(_gifter=bob_text)
#     tim_text = "Tim"
#     yao_text = "Yao"
#     farm_giftunit.set_giftee(tim_text)
#     farm_giftunit.set_giftee(yao_text)
#     assert farm_giftunit.giftee_exists(tim_text)
#     assert farm_giftunit.giftee_exists(yao_text)

#     # WHEN
#     farm_giftunit.del_giftee(yao_text)

#     # THEN
#     assert farm_giftunit.giftee_exists(tim_text)
#     assert farm_giftunit.giftee_exists(yao_text) == False


# def test_GiftUnit_set_bookunit_SetsAttribute():
#     # GIVEN
#     bob_text = "Bob"
#     farm_giftunit = giftunit_shop(_gifter=bob_text)
#     assert farm_giftunit._bookunit == bookunit_shop()

#     # WHEN
#     farm_bookunit = bookunit_shop()
#     farm_bookunit.set_agendaatom(get_atom_example_ideaunit_sports())
#     farm_giftunit.set_bookunit(farm_bookunit)

#     # THEN
#     assert farm_giftunit._bookunit == farm_bookunit


# def test_GiftUnit_agendaatom_exists_ReturnsCorrectObj():
#     # GIVEN
#     bob_text = "Bob"
#     farm_bookunit = bookunit_shop()
#     farm_giftunit = giftunit_shop(_gifter=bob_text)
#     farm_giftunit.set_bookunit(farm_bookunit)

#     # WHEN
#     sports_agendaatom = get_atom_example_ideaunit_sports()

#     # THEN
#     assert farm_giftunit.agendaatom_exists(sports_agendaatom) == False

#     # WHEN
#     farm_bookunit.set_agendaatom(sports_agendaatom)
#     farm_giftunit.set_bookunit(farm_bookunit)

#     # THEN
#     assert farm_giftunit.agendaatom_exists(sports_agendaatom)


# def test_GiftUnit_del_bookunit_SetsAttribute():
#     # GIVEN
#     bob_text = "Bob"
#     farm_bookunit = bookunit_shop()
#     farm_bookunit.set_agendaatom(get_atom_example_ideaunit_sports())
#     farm_giftunit = giftunit_shop(_gifter=bob_text, _bookunit=farm_bookunit)
#     assert farm_giftunit._bookunit != bookunit_shop()
#     assert farm_giftunit._bookunit == farm_bookunit

#     # WHEN
#     farm_giftunit.del_bookunit()

#     # THEN
#     assert farm_giftunit._bookunit == bookunit_shop()


# def test_GiftUnit_get_dict_ReturnsCorrectObj_Simple():
#     # GIVEN
#     bob_text = "Bob"
#     tim_text = "Tim"
#     yao_text = "Yao"
#     farm_giftunit = giftunit_shop(_gifter=bob_text)
#     farm_giftunit.set_giftee(tim_text)
#     farm_giftunit.set_giftee(yao_text)

#     # WHEN
#     x_dict = farm_giftunit.get_dict()

#     # THEN
#     gifter_text = "gifter"
#     assert x_dict.get(gifter_text) != None
#     assert x_dict.get(gifter_text) == bob_text

#     giftees_text = "giftees"
#     assert x_dict.get(giftees_text) != None
#     giftees_dict = x_dict.get(giftees_text)
#     assert giftees_dict.get(bob_text) is None
#     assert giftees_dict.get(tim_text) != None
#     assert giftees_dict.get(yao_text) != None

#     book_text = "book"
#     assert x_dict.get(book_text) != None
#     assert x_dict.get(book_text) == bookunit_shop().get_dict()
#     assert x_dict.get(book_text) == {}


# def test_GiftUnit_get_dict_ReturnsCorrectObj_WithBookPopulated():
#     # GIVEN
#     bob_text = "Bob"
#     carm_bookunit = get_bookunit_carm_example()
#     farm_giftunit = giftunit_shop(bob_text, _bookunit=carm_bookunit)

#     # WHEN
#     x_dict = farm_giftunit.get_dict()

#     # THEN
#     book_text = "book"
#     assert x_dict.get(book_text) != None
#     assert x_dict.get(book_text) == carm_bookunit.get_dict()
#     carm_agendaatoms_dict = x_dict.get(book_text)
#     print(f"{len(carm_bookunit.get_sorted_agendaatoms())=}")
#     print(f"{carm_agendaatoms_dict.keys()=}")
#     # print(f"{carm_agendaatoms_dict.get(0)=}")
#     assert carm_agendaatoms_dict.get(2) is None
#     assert carm_agendaatoms_dict.get(0) != None
#     assert carm_agendaatoms_dict.get(1) != None


# def test_GiftUnit_get_dict_ReturnsCorrectObj_book_start():
#     # GIVEN
#     bob_text = "Bob"
#     carm_bookunit = get_bookunit_carm_example()
#     farm_book_start = 7
#     farm_giftunit = giftunit_shop(
#         bob_text, _bookunit=carm_bookunit, _book_start=farm_book_start
#     )

#     # WHEN
#     x_dict = farm_giftunit.get_dict()

#     # THEN
#     book_text = "book"
#     assert x_dict.get(book_text) != None
#     assert x_dict.get(book_text) == carm_bookunit.get_dict(farm_book_start)
#     carm_agendaatoms_dict = x_dict.get(book_text)
#     print(f"{len(carm_bookunit.get_sorted_agendaatoms())=}")
#     print(f"{carm_agendaatoms_dict.keys()=}")
#     # print(f"{carm_agendaatoms_dict.get(0)=}")
#     assert carm_agendaatoms_dict.get(farm_book_start + 2) is None
#     assert carm_agendaatoms_dict.get(farm_book_start + 0) != None
#     assert carm_agendaatoms_dict.get(farm_book_start + 1) != None


# def test_GiftUnit__ReturnsCorrectObj_book_start(worlds_dir_setup_cleanup):
#     # GIVEN
#     sue_text = "Sue"
#     sue_world_dir = f"{get_test_worlds_dir()}/{get_test_world_id()}"
#     sue_persons_dir = f"{sue_world_dir}/persons"
#     sue_person_dir = f"{sue_persons_dir}/{sue_text}"
#     sue_gut_file_name = f"{get_gut_file_name()}.json"
#     sue_gut_path = f"{sue_person_dir}/{sue_gut_file_name}"
#     print(f"{sue_gut_path=}")
#     assert os_path_exists(sue_gut_path) == False
#     sue_person = personunit_shop(person_id=sue_text)
#     assert os_path_exists(sue_gut_path) == False
#     assert sue_person.gut_file_exists() == False
