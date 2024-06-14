from src._instrument.file import open_file, dir_files, delete_dir, set_dir, save_file
from src._road.jaar_config import init_atom_id, get_test_real_id as real_id
from src.atom.atom import atomunit_shop, get_json_filename
from src.listen.userhub import userhub_shop
from src.listen.examples.example_listen_quarks import get_quark_example_factunit_knee
from src.listen.examples.example_listen_atoms import (
    get_sue_atomunit,
    sue_1quarkunits_atomunit,
    sue_2quarkunits_atomunit,
    sue_3quarkunits_atomunit,
    sue_4quarkunits_atomunit,
)
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy


def test_UserHub_get_max_atom_file_number_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)

    # WHEN / THEN
    delete_dir(sue_userhub.atoms_dir())
    assert sue_userhub.get_max_atom_file_number() is None
    assert sue_userhub._get_next_atom_file_number() == init_atom_id()
    assert sue_userhub._get_next_atom_file_number() == 0

    # GIVEN
    six_int = 6
    save_file(sue_userhub.atoms_dir(), sue_userhub.atom_file_name(six_int), "x")

    # WHEN / THEN
    assert sue_userhub.get_max_atom_file_number() == six_int
    assert sue_userhub._get_next_atom_file_number() == 7


def test_UserHub_atom_file_exists_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    assert sue_userhub.atom_file_exists(None) is False
    assert sue_userhub.atom_file_exists(0) is False
    six_int = 6
    print(f"{sue_userhub.atom_file_path(six_int)=}")
    assert sue_userhub.atom_file_exists(six_int) is False

    # WHEN
    save_file(sue_userhub.atoms_dir(), sue_userhub.atom_file_name(six_int), "x")

    # THEN
    assert sue_userhub.atom_file_exists(None) is False
    assert sue_userhub.atom_file_exists(0) is False
    assert sue_userhub.atom_file_exists(six_int)


def test_UserHub_save_atom_file_SaveCorrectObj(env_dir_setup_cleanup):
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    two_int = 2
    six_int = 6
    two_filename = get_json_filename(two_int)
    six_filename = get_json_filename(six_int)
    sue_atom2_path = f"{sue_userhub.atoms_dir()}/{two_filename}"
    sue_atom0_path = f"{sue_userhub.atoms_dir()}/{six_filename}"
    print(f"{sue_atom2_path=}")
    print(f"{sue_atom0_path=}")
    sue_atomunit = atomunit_shop(
        person_id=sue_text,
        _atom_id=two_int,
        _quarks_dir=sue_userhub.quarks_dir(),
        _atoms_dir=sue_userhub.atoms_dir(),
    )
    assert sue_userhub.atom_file_exists(two_int) is False
    assert sue_userhub.atom_file_exists(six_int) is False

    # WHEN
    sue_userhub.save_atom_file(sue_atomunit, correct_invalid_attrs=False)

    # THEN
    assert sue_userhub.atom_file_exists(two_int)
    assert sue_userhub.atom_file_exists(six_int) is False
    two_file_json = open_file(sue_userhub.atoms_dir(), two_filename)
    assert two_file_json == sue_atomunit.get_nucmetric_json()


def test_UserHub_save_atom_file_RaisesErrorIfAtomUnit_quarks_dir_IsWrong(
    env_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    x_atom_id = 6
    six_filename = get_json_filename(x_atom_id)
    sue_atom0_path = f"{sue_userhub.atoms_dir()}/{six_filename}"
    print(f"{sue_atom0_path=}")
    sue_atomunit = atomunit_shop(
        person_id=sue_text,
        _atom_id=x_atom_id,
        _quarks_dir="src/world",
        _atoms_dir=sue_userhub.atoms_dir(),
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_userhub.save_atom_file(sue_atomunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"AtomUnit file cannot be saved because atomunit._quarks_dir is incorrect: {sue_atomunit._quarks_dir}. It must be {sue_userhub.quarks_dir()}."
    )


def test_UserHub_save_atom_file_RaisesErrorIfAtomUnit_atoms_dir_IsWrong(
    env_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    x_atom_id = 6
    six_filename = get_json_filename(x_atom_id)
    sue_atom0_path = f"{sue_userhub.atoms_dir()}/{six_filename}"
    print(f"{sue_atom0_path=}")
    sue_atomunit = atomunit_shop(
        person_id=sue_text,
        _atom_id=x_atom_id,
        _quarks_dir=sue_userhub.quarks_dir(),
        _atoms_dir="src/world",
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_userhub.save_atom_file(sue_atomunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"AtomUnit file cannot be saved because atomunit._atoms_dir is incorrect: {sue_atomunit._atoms_dir}. It must be {sue_userhub.atoms_dir()}."
    )


def test_UserHub_save_atom_file_RaisesErrorIfAtomUnit_person_id_IsWrong(
    env_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    x_atom_id = 6
    six_filename = get_json_filename(x_atom_id)
    sue_atom0_path = f"{sue_userhub.atoms_dir()}/{six_filename}"
    print(f"{sue_atom0_path=}")
    bob_text = "Bob"
    sue_atomunit = atomunit_shop(
        person_id=bob_text,
        _atom_id=x_atom_id,
        _quarks_dir=sue_userhub.quarks_dir(),
        _atoms_dir=sue_userhub.atoms_dir(),
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_userhub.save_atom_file(sue_atomunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"AtomUnit file cannot be saved because atomunit.person_id is incorrect: {sue_atomunit.person_id}. It must be {sue_text}."
    )


def test_UserHub_save_atom_file_RaisesErrorIf_replace_IsFalse(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    x_atom_id = 0
    six_filename = get_json_filename(x_atom_id)
    sue_atomunit = atomunit_shop(
        person_id=sue_text,
        _atom_id=x_atom_id,
        _quarks_dir=sue_userhub.quarks_dir(),
        _atoms_dir=sue_userhub.atoms_dir(),
    )
    saved_atomunit = sue_userhub.save_atom_file(sue_atomunit)

    print(f"{sue_userhub.atom_file_path(x_atom_id)=}")
    assert sue_userhub.atom_file_exists(x_atom_id)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_userhub.save_atom_file(
            saved_atomunit, replace=False, correct_invalid_attrs=False
        )
    assert (
        str(excinfo.value)
        == f"AtomUnit file {six_filename} already exists and cannot be saved over."
    )


def test_UserHub_validate_atomunit_ReturnsObjWithAttributesFixed(
    env_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    two_int = 2
    two_filename = get_json_filename(two_int)
    sue_atom2_path = f"{sue_userhub.atoms_dir()}/{two_filename}"
    print(f"{sue_atom2_path=}")

    # WHEN
    invalid_sue_atomunit = atomunit_shop(
        person_id="Bob",
        _atom_id=sue_userhub._get_next_atom_file_number() - 5,
        _quarks_dir=f"{sue_userhub.econs_dir()}/swimming",
        _atoms_dir=f"{sue_userhub.econs_dir()}/swimming",
    )
    valid_atomunit = sue_userhub.validate_atomunit(invalid_sue_atomunit)

    # THEN
    assert valid_atomunit._quarks_dir == sue_userhub.quarks_dir()
    assert valid_atomunit._atoms_dir == sue_userhub.atoms_dir()
    assert valid_atomunit._atom_id == sue_userhub._get_next_atom_file_number()
    correct_sue_atomunit = atomunit_shop(
        person_id=sue_text,
        _atom_id=sue_userhub._get_next_atom_file_number(),
        _quarks_dir=sue_userhub.quarks_dir(),
        _atoms_dir=sue_userhub.atoms_dir(),
    )
    assert valid_atomunit == correct_sue_atomunit


def test_UserHub_save_atom_file_SaveCorrectObj_correct_invalid_attrs_IsTrue(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    next_int = sue_userhub._get_next_atom_file_number()
    next_filename = get_json_filename(next_int)
    sue_atom2_path = f"{sue_userhub.atoms_dir()}/{next_filename}"
    print(f"{sue_atom2_path=}")
    assert sue_userhub.atom_file_exists(next_int) is False

    # WHEN
    invalid_sue_atomunit = atomunit_shop(
        person_id="Bob",
        _atom_id=sue_userhub._get_next_atom_file_number() - 5,
        _quarks_dir=f"{sue_userhub.econs_dir()}/swimming",
        _atoms_dir=f"{sue_userhub.econs_dir()}/swimming",
    )
    sue_userhub.save_atom_file(invalid_sue_atomunit)

    # THEN
    assert sue_userhub.atom_file_exists(next_int)
    two_file_json = open_file(sue_userhub.atoms_dir(), next_filename)


def test_UserHub_default_atomunit_ReturnsObjWithCorrect_atom_id_WhenNoatomFilesExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)

    # WHEN
    delete_dir(sue_userhub.atoms_dir())
    sue_atomunit = sue_userhub._default_atomunit()

    # THEN
    assert sue_atomunit.person_id == sue_text
    assert sue_atomunit._atom_id == init_atom_id()
    assert sue_atomunit._atom_id == 0
    assert sue_atomunit._atom_id == sue_userhub._get_next_atom_file_number()
    assert sue_atomunit._faces == set()
    assert sue_atomunit._quarks_dir == sue_userhub.quarks_dir()
    assert sue_atomunit._atoms_dir == sue_userhub.atoms_dir()


def test_UserHub_default_atomunit_ReturnsObjWithCorrect_atom_id_WhenatomFilesExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    delete_dir(sue_userhub.atoms_dir())

    zero_atomunit = get_sue_atomunit()
    zero_atomunit._atom_id = sue_userhub._get_next_atom_file_number()
    zero_atomunit._quarks_dir = sue_userhub.quarks_dir()
    zero_atomunit._atoms_dir = sue_userhub.atoms_dir()
    sue_userhub.save_atom_file(zero_atomunit)

    # WHEN
    sue_atomunit = sue_userhub._default_atomunit()

    # THEN
    assert sue_atomunit.person_id == sue_text
    assert sue_atomunit._atom_id == init_atom_id() + 1
    assert sue_atomunit._atom_id == 1
    assert sue_atomunit._atom_id == sue_userhub._get_next_atom_file_number()
    assert sue_atomunit._faces == set()
    assert sue_atomunit._quarks_dir == sue_userhub.quarks_dir()
    assert sue_atomunit._atoms_dir == sue_userhub.atoms_dir()


def test_UserHub_get_atomunit_ReturnsCorrectObjWhenFilesDoesExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    yao_text = "yao"
    x0_atomunit = sue_userhub._default_atomunit()
    x0_atomunit.set_face(yao_text)
    sue_userhub.save_atom_file(x0_atomunit)
    bob_text = "Bob"
    x1_atomunit = sue_userhub._default_atomunit()
    x1_atomunit.set_face(bob_text)
    sue_userhub.save_atom_file(x1_atomunit)

    # WHEN
    y0_atomunit = sue_userhub.get_atomunit(x0_atomunit._atom_id)
    y1_atomunit = sue_userhub.get_atomunit(x1_atomunit._atom_id)

    # THEN
    assert y0_atomunit != None
    assert y1_atomunit != None
    assert yao_text in y0_atomunit._faces
    assert bob_text not in y0_atomunit._faces
    assert bob_text in y1_atomunit._faces


def test_UserHub_get_atomunit_RaisesExceptionWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    yao_text = "yao"
    x0_atomunit = sue_userhub._default_atomunit()
    x0_atomunit.set_face(yao_text)
    sue_userhub.save_atom_file(x0_atomunit)
    bob_text = "Bob"
    x1_atomunit = sue_userhub._default_atomunit()
    x1_atomunit.set_face(bob_text)
    sue_userhub.save_atom_file(x1_atomunit)

    # WHEN / THEN
    six_file_number = 6
    with pytest_raises(Exception) as excinfo:
        sue_userhub.get_atomunit(six_file_number)
    assert (
        str(excinfo.value) == f"AtomUnit file_number {six_file_number} does not exist."
    )


def test_UserHub_del_atom_file_DeletesatomjsonAndNotQuarkUnitjsons(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    six_int = 6
    sue_atomunit = atomunit_shop(
        person_id=sue_text,
        _atom_id=six_int,
        _quarks_dir=sue_userhub.quarks_dir(),
        _atoms_dir=sue_userhub.atoms_dir(),
    )
    sue_atomunit._nucunit.set_quarkunit(get_quark_example_factunit_knee())
    zero_int = 0
    assert sue_userhub.atom_file_exists(six_int) is False
    assert sue_userhub.quark_file_exists(zero_int) is False

    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    sue_userhub.save_atom_file(sue_atomunit, correct_invalid_attrs=False)

    print(f"{dir_files(sue_userhub.quarks_dir())}")
    assert sue_userhub.atom_file_exists(six_int)
    assert sue_userhub.quark_file_exists(zero_int)

    # WHEN
    sue_userhub._del_atom_file(sue_atomunit._atom_id)

    # THEN
    assert sue_userhub.atom_file_exists(six_int) is False
    assert sue_userhub.quark_file_exists(zero_int)


def test_UserHub_save_atom_file_CanCreateAndModify3atomunits(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    delete_dir(sue_userhub.atoms_dir())
    delete_dir(sue_userhub.quarks_dir())
    set_dir(sue_userhub.atoms_dir())
    set_dir(sue_userhub.quarks_dir())
    assert len(dir_files(sue_userhub.atoms_dir())) == 0
    assert len(dir_files(sue_userhub.quarks_dir())) == 0

    # WHEN
    sue_userhub.save_atom_file(sue_2quarkunits_atomunit())
    sue_userhub.save_atom_file(sue_3quarkunits_atomunit())
    sue_userhub.save_atom_file(sue_4quarkunits_atomunit())

    # THEN
    assert len(dir_files(sue_userhub.atoms_dir())) == 3
    assert len(dir_files(sue_userhub.quarks_dir())) == 9


def test_UserHub_save_atom_file_ReturnsValidObj(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    sue2_atomunit = sue_2quarkunits_atomunit()
    sue2_atomunit._quarks_dir = f"{sue_userhub.econs_dir()}/swimming"
    sue2_atomunit._atoms_dir = f"{sue_userhub.econs_dir()}/swimming"
    sue2_atomunit.person_id = "Bob"
    sue2_atomunit._atom_id = sue_userhub._get_next_atom_file_number() - 5
    prev_sue2_atomunit = copy_deepcopy(sue2_atomunit)

    # WHEN
    valid_atomunit = sue_userhub.save_atom_file(sue2_atomunit)

    # THEN
    assert valid_atomunit._atoms_dir != prev_sue2_atomunit._atoms_dir
    assert valid_atomunit._atoms_dir == sue_userhub.atoms_dir()
    assert valid_atomunit._quarks_dir == sue_userhub.quarks_dir()
    assert valid_atomunit._atom_id != prev_sue2_atomunit._atom_id


def test_UserHub_create_save_atom_file_SaveCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    two_int = 2
    three_int = 3
    print(f"{sue_userhub.atom_file_path(two_int)=}")
    print(f"{sue_userhub.atom_file_path(three_int)=}")
    sue_atomunit = atomunit_shop(
        person_id=sue_text,
        _atom_id=two_int,
        _quarks_dir=sue_userhub.quarks_dir(),
        _atoms_dir=sue_userhub.atoms_dir(),
    )
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    sue_userhub.save_atom_file(sue_atomunit, correct_invalid_attrs=False)
    assert sue_userhub.atom_file_exists(two_int)
    assert sue_userhub.atom_file_exists(three_int) is False

    # WHEN
    before_agenda = sue_userhub.default_duty_agenda()
    bob_text = "Bob"
    after_agenda = copy_deepcopy(before_agenda)
    after_agenda.add_partyunit(bob_text)
    sue_userhub.create_save_atom_file(before_agenda, after_agenda)

    # THEN
    assert sue_userhub.atom_file_exists(three_int)


def test_UserHub_merge_any_atoms_ReturnsSameObj(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    sue_userhub.save_duty_agenda(sue_userhub.default_duty_agenda())
    duty_agenda = sue_userhub.get_duty_agenda()
    duty_agenda._last_atom_id is None

    # WHEN
    new_agenda = sue_userhub._merge_any_atoms(duty_agenda)

    # THEN
    assert new_agenda == duty_agenda


def test_UserHub_merge_any_atoms_ReturnsObj_WithSingleatomModifies_1quark(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    sue_userhub.save_atom_file(sue_1quarkunits_atomunit())
    sue_userhub.save_duty_agenda(sue_userhub.default_duty_agenda())
    duty_agenda = sue_userhub.get_duty_agenda()
    print(f"{duty_agenda._real_id=}")
    print(f"{sue_userhub.real_id=}")
    sports_text = "sports"
    sports_road = duty_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = duty_agenda.make_road(sports_road, knee_text)
    assert duty_agenda.fact_exists(sports_road) is False

    # WHEN
    new_agenda = sue_userhub._merge_any_atoms(duty_agenda)

    # THEN
    assert new_agenda != duty_agenda
    assert new_agenda.fact_exists(sports_road)


def test_UserHub_merge_any_atoms_ReturnsObj_WithSingleatomModifies_2quarks(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    sue_userhub.save_atom_file(sue_2quarkunits_atomunit())
    sue_userhub.save_duty_agenda(sue_userhub.default_duty_agenda())
    duty_agenda = sue_userhub.get_duty_agenda()
    print(f"{duty_agenda._real_id=}")
    sports_text = "sports"
    sports_road = duty_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = duty_agenda.make_road(sports_road, knee_text)
    assert duty_agenda.fact_exists(sports_road) is False
    assert duty_agenda.fact_exists(knee_road) is False

    # WHEN
    new_agenda = sue_userhub._merge_any_atoms(duty_agenda)

    # THEN
    assert new_agenda != duty_agenda
    assert new_agenda.fact_exists(sports_road)
    assert new_agenda.fact_exists(knee_road)
