from src._instrument.python import x_is_json
from src._road.jaar_config import init_atom_id, get_atoms_folder
from src._road.road import get_default_real_id_roadnode as root_label
from src.atom.nuc import nucunit_shop
from src.atom.atom import AtomUnit, atomunit_shop, get_init_atom_id_if_None
from src.atom.examples.example_quarks import get_quark_example_ideaunit_sports
from src.atom.examples.example_nucs import get_nucunit_carm_example


def test_get_atoms_folder_ReturnsCorrectObj():
    # GIVEN / WHEN / THEN
    assert get_atoms_folder() == "atoms"


def test_init_atom_id_ReturnsCorrectObj():
    # GIVEN / WHEN / THEN
    assert init_atom_id() == 0


def test_get_init_atom_id_if_None_ReturnsCorrectObj():
    # GIVEN / WHEN / THEN
    assert get_init_atom_id_if_None() == init_atom_id()
    assert get_init_atom_id_if_None(None) == init_atom_id()
    assert get_init_atom_id_if_None(1) == 1


def test_AtomUnit_exists():
    # GIVEN / WHEN
    x_atomunit = AtomUnit()

    # THEN
    assert x_atomunit.real_id is None
    assert x_atomunit.person_id is None
    assert x_atomunit._atom_id is None
    assert x_atomunit._faces is None
    assert x_atomunit._nucunit is None
    assert x_atomunit._nuc_start is None
    assert x_atomunit._atoms_dir is None
    assert x_atomunit._quarks_dir is None


def test_atomunit_shop_ReturnsCorrectObjGivenEmptyArgs():
    # GIVEN
    bob_text = "Bob"

    # WHEN
    farm_atomunit = atomunit_shop(person_id=bob_text)

    # THEN
    assert farm_atomunit.real_id == root_label()
    assert farm_atomunit.person_id == bob_text
    assert farm_atomunit._atom_id == 0
    assert farm_atomunit._faces == set()
    assert farm_atomunit._nucunit == nucunit_shop()
    assert farm_atomunit._nuc_start == 0
    assert farm_atomunit._atoms_dir is None
    assert farm_atomunit._quarks_dir is None


def test_atomunit_shop_ReturnsCorrectObjGivenNonEmptyArgs():
    # GIVEN
    bob_text = "Bob"
    bob_atom_id = 13
    bob_faces = {"Sue", "Yao"}
    bob_nucunit = get_nucunit_carm_example()
    bob_nuc_start = 6
    bob_atoms_dir = "exampletext7"
    bob_quarks_dir = "exampletext9"
    music_text = "music"

    # WHEN
    farm_atomunit = atomunit_shop(
        real_id=music_text,
        person_id=bob_text,
        _atom_id=bob_atom_id,
        _faces=bob_faces,
        _nucunit=bob_nucunit,
        _nuc_start=bob_nuc_start,
        _atoms_dir=bob_atoms_dir,
        _quarks_dir=bob_quarks_dir,
    )

    # THEN
    assert farm_atomunit.real_id == music_text
    assert farm_atomunit.person_id == bob_text
    assert farm_atomunit._atom_id == bob_atom_id
    assert farm_atomunit._faces == bob_faces
    assert farm_atomunit._nucunit == bob_nucunit
    assert farm_atomunit._nuc_start == bob_nuc_start
    assert farm_atomunit._atoms_dir == bob_atoms_dir
    assert farm_atomunit._quarks_dir == bob_quarks_dir


def test_atomunit_shop_ReturnsCorrectObjGivenSomeArgs_v1():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    x_faces = {bob_text, tim_text, yao_text}

    # WHEN
    farm_atomunit = atomunit_shop(person_id=bob_text, _faces=x_faces)

    # THEN
    assert farm_atomunit.person_id == bob_text
    assert farm_atomunit._faces == x_faces


def test_AtomUnit_set_face_SetsAttribute():
    # GIVEN
    bob_text = "Bob"
    farm_atomunit = atomunit_shop(person_id=bob_text)
    tim_text = "Tim"
    assert farm_atomunit._faces == set()
    assert tim_text not in farm_atomunit._faces

    # WHEN
    farm_atomunit.set_face(tim_text)

    # THEN
    assert tim_text in farm_atomunit._faces


def test_AtomUnit_face_exists_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    farm_atomunit = atomunit_shop(person_id=bob_text)
    tim_text = "Tim"
    assert farm_atomunit._faces == set()
    assert tim_text not in farm_atomunit._faces

    # WHEN / THEN
    assert farm_atomunit.face_exists(tim_text) is False

    # WHEN / THEN
    farm_atomunit.set_face(tim_text)
    assert farm_atomunit.face_exists(tim_text)


def test_AtomUnit_del_face_SetsAttribute():
    # GIVEN
    bob_text = "Bob"
    farm_atomunit = atomunit_shop(person_id=bob_text)
    tim_text = "Tim"
    yao_text = "Yao"
    farm_atomunit.set_face(tim_text)
    farm_atomunit.set_face(yao_text)
    assert farm_atomunit.face_exists(tim_text)
    assert farm_atomunit.face_exists(yao_text)

    # WHEN
    farm_atomunit.del_face(yao_text)

    # THEN
    assert farm_atomunit.face_exists(tim_text)
    assert farm_atomunit.face_exists(yao_text) is False


def test_AtomUnit_set_nucunit_SetsAttribute():
    # GIVEN
    bob_text = "Bob"
    farm_atomunit = atomunit_shop(person_id=bob_text)
    assert farm_atomunit._nucunit == nucunit_shop()

    # WHEN
    farm_nucunit = nucunit_shop()
    farm_nucunit.set_quarkunit(get_quark_example_ideaunit_sports())
    farm_atomunit.set_nucunit(farm_nucunit)

    # THEN
    assert farm_atomunit._nucunit == farm_nucunit


def test_AtomUnit_set_nuc_start_SetsAttribute():
    # GIVEN
    bob_text = "Bob"
    farm_atomunit = atomunit_shop(bob_text)
    assert farm_atomunit._nuc_start == 0

    # WHEN
    farm_nuc_start = 11
    farm_atomunit.set_nuc_start(farm_nuc_start)

    # THEN
    assert farm_atomunit._nuc_start == farm_nuc_start


def test_AtomUnit_quarkunit_exists_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    farm_nucunit = nucunit_shop()
    farm_atomunit = atomunit_shop(person_id=bob_text)
    farm_atomunit.set_nucunit(farm_nucunit)

    # WHEN
    sports_quarkunit = get_quark_example_ideaunit_sports()

    # THEN
    assert farm_atomunit.quarkunit_exists(sports_quarkunit) is False

    # WHEN
    farm_nucunit.set_quarkunit(sports_quarkunit)
    farm_atomunit.set_nucunit(farm_nucunit)

    # THEN
    assert farm_atomunit.quarkunit_exists(sports_quarkunit)


def test_AtomUnit_del_nucunit_SetsAttribute():
    # GIVEN
    bob_text = "Bob"
    farm_nucunit = nucunit_shop()
    farm_nucunit.set_quarkunit(get_quark_example_ideaunit_sports())
    farm_atomunit = atomunit_shop(person_id=bob_text, _nucunit=farm_nucunit)
    assert farm_atomunit._nucunit != nucunit_shop()
    assert farm_atomunit._nucunit == farm_nucunit

    # WHEN
    farm_atomunit.del_nucunit()

    # THEN
    assert farm_atomunit._nucunit == nucunit_shop()


def test_AtomUnit_get_step_dict_ReturnsCorrectObj_Simple():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    music_text = "music"
    farm_atomunit = atomunit_shop(real_id=music_text, person_id=bob_text)
    farm_atomunit.set_face(tim_text)
    farm_atomunit.set_face(yao_text)

    # WHEN
    x_dict = farm_atomunit.get_step_dict()

    # THEN
    real_id_text = "real_id"
    assert x_dict.get(real_id_text) != None
    assert x_dict.get(real_id_text) == music_text

    person_id_text = "person_id"
    assert x_dict.get(person_id_text) != None
    assert x_dict.get(person_id_text) == bob_text

    faces_text = "faces"
    assert x_dict.get(faces_text) != None
    faces_dict = x_dict.get(faces_text)
    assert faces_dict.get(bob_text) is None
    assert faces_dict.get(tim_text) != None
    assert faces_dict.get(yao_text) != None

    nuc_text = "nuc"
    assert x_dict.get(nuc_text) != None
    assert x_dict.get(nuc_text) == nucunit_shop().get_ordered_quarkunits()
    assert x_dict.get(nuc_text) == {}


def test_AtomUnit_get_step_dict_ReturnsCorrectObj_WithNucPopulated():
    # GIVEN
    bob_text = "Bob"
    carm_nucunit = get_nucunit_carm_example()
    farm_atomunit = atomunit_shop(bob_text, _nucunit=carm_nucunit)

    # WHEN
    x_dict = farm_atomunit.get_step_dict()

    # THEN
    nuc_text = "nuc"
    assert x_dict.get(nuc_text) != None
    assert x_dict.get(nuc_text) == carm_nucunit.get_ordered_quarkunits()
    carm_quarkunits_dict = x_dict.get(nuc_text)
    print(f"{len(carm_nucunit.get_sorted_quarkunits())=}")
    print(f"{carm_quarkunits_dict.keys()=}")
    # print(f"{carm_quarkunits_dict.get(0)=}")
    assert carm_quarkunits_dict.get(2) is None
    assert carm_quarkunits_dict.get(0) != None
    assert carm_quarkunits_dict.get(1) != None


def test_AtomUnit_get_step_dict_ReturnsCorrectObj_nuc_start():
    # GIVEN
    bob_text = "Bob"
    carm_nucunit = get_nucunit_carm_example()
    farm_nuc_start = 7
    farm_atomunit = atomunit_shop(
        bob_text, _nucunit=carm_nucunit, _nuc_start=farm_nuc_start
    )

    # WHEN
    x_dict = farm_atomunit.get_step_dict()

    # THEN
    nuc_text = "nuc"
    assert x_dict.get(nuc_text) != None
    assert x_dict.get(nuc_text) == carm_nucunit.get_ordered_quarkunits(farm_nuc_start)
    carm_quarkunits_dict = x_dict.get(nuc_text)
    print(f"{len(carm_nucunit.get_sorted_quarkunits())=}")
    print(f"{carm_quarkunits_dict.keys()=}")
    # print(f"{carm_quarkunits_dict.get(0)=}")
    assert carm_quarkunits_dict.get(farm_nuc_start + 2) is None
    assert carm_quarkunits_dict.get(farm_nuc_start + 0) != None
    assert carm_quarkunits_dict.get(farm_nuc_start + 1) != None


def test_AtomUnit_get_nuc_quark_numbers_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    carm_nucunit = get_nucunit_carm_example()
    farm_nuc_start = 7
    farm_atomunit = atomunit_shop(bob_text)
    farm_atomunit.set_nucunit(carm_nucunit)
    farm_atomunit.set_nuc_start(farm_nuc_start)
    farm_atomunit.set_face(tim_text)
    farm_atomunit.set_face(yao_text)
    farm_dict = farm_atomunit.get_step_dict()

    # WHEN
    farm_nuc_quark_numbers = farm_atomunit.get_nuc_quark_numbers(farm_dict)
    # THEN
    assert farm_nuc_quark_numbers == [farm_nuc_start, farm_nuc_start + 1]


def test_AtomUnit_get_nucmetric_dict_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    carm_nucunit = get_nucunit_carm_example()
    farm_nuc_start = 7
    farm_atomunit = atomunit_shop(bob_text)
    farm_atomunit.set_nucunit(carm_nucunit)
    farm_atomunit.set_nuc_start(farm_nuc_start)
    farm_atomunit.set_face(tim_text)
    farm_atomunit.set_face(yao_text)

    # WHEN
    x_dict = farm_atomunit.get_nucmetric_dict()

    # THEN
    person_id_text = "person_id"
    assert x_dict.get(person_id_text) != None
    assert x_dict.get(person_id_text) == bob_text

    faces_text = "faces"
    assert x_dict.get(faces_text) != None
    faces_dict = x_dict.get(faces_text)
    assert faces_dict.get(bob_text) is None
    assert faces_dict.get(tim_text) != None
    assert faces_dict.get(yao_text) != None

    nuc_quark_numbers_text = "nuc_quark_numbers"
    assert x_dict.get(nuc_quark_numbers_text) != None
    assert x_dict.get(nuc_quark_numbers_text) == [7, 8]

    nuc_min_text = "nuc_min"
    assert x_dict.get(nuc_min_text) is None
    nuc_max_text = "nuc_max"
    assert x_dict.get(nuc_max_text) is None


def test_AtomUnit_get_nucmetric_json_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    tim_text = "Tim"
    yao_text = "Yao"
    carm_nucunit = get_nucunit_carm_example()
    farm_nuc_start = 7
    farm_atomunit = atomunit_shop(bob_text)
    farm_atomunit.set_nucunit(carm_nucunit)
    farm_atomunit.set_nuc_start(farm_nuc_start)
    farm_atomunit.set_face(tim_text)
    farm_atomunit.set_face(yao_text)

    # WHEN
    farm_json = farm_atomunit.get_nucmetric_json()

    # THEN
    assert x_is_json(farm_json)
