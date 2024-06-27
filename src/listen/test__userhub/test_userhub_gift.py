from src._instrument.file import open_file, dir_files, delete_dir, set_dir, save_file
from src._road.jaar_config import init_gift_id, get_test_real_id as real_id
from src.gift.gift import giftunit_shop, get_json_filename
from src.listen.userhub import userhub_shop
from src.listen.examples.example_listen_atoms import get_atom_example_ideaunit_knee
from src.listen.examples.example_listen_gifts import (
    get_sue_giftunit,
    sue_1atomunits_giftunit,
    sue_2atomunits_giftunit,
    sue_3atomunits_giftunit,
    sue_4atomunits_giftunit,
)
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy


def test_UserHub_get_max_gift_file_number_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)

    # WHEN / THEN
    delete_dir(sue_userhub.gifts_dir())
    assert sue_userhub.get_max_gift_file_number() is None
    assert sue_userhub._get_next_gift_file_number() == init_gift_id()
    assert sue_userhub._get_next_gift_file_number() == 0

    # GIVEN
    six_int = 6
    save_file(sue_userhub.gifts_dir(), sue_userhub.gift_file_name(six_int), "x")

    # WHEN / THEN
    assert sue_userhub.get_max_gift_file_number() == six_int
    assert sue_userhub._get_next_gift_file_number() == 7


def test_UserHub_gift_file_exists_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    assert sue_userhub.gift_file_exists(None) is False
    assert sue_userhub.gift_file_exists(0) is False
    six_int = 6
    print(f"{sue_userhub.gift_file_path(six_int)=}")
    assert sue_userhub.gift_file_exists(six_int) is False

    # WHEN
    save_file(sue_userhub.gifts_dir(), sue_userhub.gift_file_name(six_int), "x")

    # THEN
    assert sue_userhub.gift_file_exists(None) is False
    assert sue_userhub.gift_file_exists(0) is False
    assert sue_userhub.gift_file_exists(six_int)


def test_UserHub_save_gift_file_SaveCorrectObj(env_dir_setup_cleanup):
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    two_int = 2
    six_int = 6
    two_filename = get_json_filename(two_int)
    six_filename = get_json_filename(six_int)
    sue_gift2_path = f"{sue_userhub.gifts_dir()}/{two_filename}"
    sue_gift0_path = f"{sue_userhub.gifts_dir()}/{six_filename}"
    print(f"{sue_gift2_path=}")
    print(f"{sue_gift0_path=}")
    sue_giftunit = giftunit_shop(
        owner_id=sue_text,
        _gift_id=two_int,
        _atoms_dir=sue_userhub.atoms_dir(),
        _gifts_dir=sue_userhub.gifts_dir(),
    )
    assert sue_userhub.gift_file_exists(two_int) is False
    assert sue_userhub.gift_file_exists(six_int) is False

    # WHEN
    sue_userhub.save_gift_file(sue_giftunit, correct_invalid_attrs=False)

    # THEN
    assert sue_userhub.gift_file_exists(two_int)
    assert sue_userhub.gift_file_exists(six_int) is False
    two_file_json = open_file(sue_userhub.gifts_dir(), two_filename)
    assert two_file_json == sue_giftunit.get_changemetric_json()


def test_UserHub_save_gift_file_RaisesErrorIfGiftUnit_atoms_dir_IsWrong(
    env_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_gift0_path = f"{sue_userhub.gifts_dir()}/{six_filename}"
    print(f"{sue_gift0_path=}")
    sue_giftunit = giftunit_shop(
        owner_id=sue_text,
        _gift_id=x_gift_id,
        _atoms_dir="src/incorrect_directory",
        _gifts_dir=sue_userhub.gifts_dir(),
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_userhub.save_gift_file(sue_giftunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"GiftUnit file cannot be saved because giftunit._atoms_dir is incorrect: {sue_giftunit._atoms_dir}. It must be {sue_userhub.atoms_dir()}."
    )


def test_UserHub_save_gift_file_RaisesErrorIfGiftUnit_gifts_dir_IsWrong(
    env_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_gift0_path = f"{sue_userhub.gifts_dir()}/{six_filename}"
    print(f"{sue_gift0_path=}")
    sue_giftunit = giftunit_shop(
        owner_id=sue_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_userhub.atoms_dir(),
        _gifts_dir="src/incorrect_directory",
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_userhub.save_gift_file(sue_giftunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"GiftUnit file cannot be saved because giftunit._gifts_dir is incorrect: {sue_giftunit._gifts_dir}. It must be {sue_userhub.gifts_dir()}."
    )


def test_UserHub_save_gift_file_RaisesErrorIfGiftUnit_owner_id_IsWrong(
    env_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_gift0_path = f"{sue_userhub.gifts_dir()}/{six_filename}"
    print(f"{sue_gift0_path=}")
    bob_text = "Bob"
    sue_giftunit = giftunit_shop(
        owner_id=bob_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_userhub.atoms_dir(),
        _gifts_dir=sue_userhub.gifts_dir(),
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_userhub.save_gift_file(sue_giftunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"GiftUnit file cannot be saved because giftunit.owner_id is incorrect: {sue_giftunit.owner_id}. It must be {sue_text}."
    )


def test_UserHub_save_gift_file_RaisesErrorIf_replace_IsFalse(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    x_gift_id = 0
    six_filename = get_json_filename(x_gift_id)
    sue_giftunit = giftunit_shop(
        owner_id=sue_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_userhub.atoms_dir(),
        _gifts_dir=sue_userhub.gifts_dir(),
    )
    saved_giftunit = sue_userhub.save_gift_file(sue_giftunit)

    print(f"{sue_userhub.gift_file_path(x_gift_id)=}")
    assert sue_userhub.gift_file_exists(x_gift_id)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_userhub.save_gift_file(
            saved_giftunit, replace=False, correct_invalid_attrs=False
        )
    assert (
        str(excinfo.value)
        == f"GiftUnit file {six_filename} already exists and cannot be saved over."
    )


def test_UserHub_validate_giftunit_ReturnsObjWithAttributesFixed(
    env_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    two_int = 2
    two_filename = get_json_filename(two_int)
    sue_gift2_path = f"{sue_userhub.gifts_dir()}/{two_filename}"
    print(f"{sue_gift2_path=}")

    # WHEN
    invalid_sue_giftunit = giftunit_shop(
        owner_id="Bob",
        _gift_id=sue_userhub._get_next_gift_file_number() - 5,
        _atoms_dir=f"{sue_userhub.econs_dir()}/swimming",
        _gifts_dir=f"{sue_userhub.econs_dir()}/swimming",
    )
    valid_giftunit = sue_userhub.validate_giftunit(invalid_sue_giftunit)

    # THEN
    assert valid_giftunit._atoms_dir == sue_userhub.atoms_dir()
    assert valid_giftunit._gifts_dir == sue_userhub.gifts_dir()
    assert valid_giftunit._gift_id == sue_userhub._get_next_gift_file_number()
    correct_sue_giftunit = giftunit_shop(
        owner_id=sue_text,
        _gift_id=sue_userhub._get_next_gift_file_number(),
        _atoms_dir=sue_userhub.atoms_dir(),
        _gifts_dir=sue_userhub.gifts_dir(),
    )
    assert valid_giftunit == correct_sue_giftunit


def test_UserHub_save_gift_file_SaveCorrectObj_correct_invalid_attrs_IsTrue(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    next_int = sue_userhub._get_next_gift_file_number()
    next_filename = get_json_filename(next_int)
    sue_gift2_path = f"{sue_userhub.gifts_dir()}/{next_filename}"
    print(f"{sue_gift2_path=}")
    assert sue_userhub.gift_file_exists(next_int) is False

    # WHEN
    invalid_sue_giftunit = giftunit_shop(
        owner_id="Bob",
        _gift_id=sue_userhub._get_next_gift_file_number() - 5,
        _atoms_dir=f"{sue_userhub.econs_dir()}/swimming",
        _gifts_dir=f"{sue_userhub.econs_dir()}/swimming",
    )
    sue_userhub.save_gift_file(invalid_sue_giftunit)

    # THEN
    assert sue_userhub.gift_file_exists(next_int)
    two_file_json = open_file(sue_userhub.gifts_dir(), next_filename)


def test_UserHub_default_giftunit_ReturnsObjWithCorrect_gift_id_WhenNogiftFilesExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)

    # WHEN
    delete_dir(sue_userhub.gifts_dir())
    sue_giftunit = sue_userhub._default_giftunit()

    # THEN
    assert sue_giftunit.owner_id == sue_text
    assert sue_giftunit._gift_id == init_gift_id()
    assert sue_giftunit._gift_id == 0
    assert sue_giftunit._gift_id == sue_userhub._get_next_gift_file_number()
    assert sue_giftunit._faces == set()
    assert sue_giftunit._atoms_dir == sue_userhub.atoms_dir()
    assert sue_giftunit._gifts_dir == sue_userhub.gifts_dir()


def test_UserHub_default_giftunit_ReturnsObjWithCorrect_gift_id_WhengiftFilesExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    delete_dir(sue_userhub.gifts_dir())

    zero_giftunit = get_sue_giftunit()
    zero_giftunit._gift_id = sue_userhub._get_next_gift_file_number()
    zero_giftunit._atoms_dir = sue_userhub.atoms_dir()
    zero_giftunit._gifts_dir = sue_userhub.gifts_dir()
    sue_userhub.save_gift_file(zero_giftunit)

    # WHEN
    sue_giftunit = sue_userhub._default_giftunit()

    # THEN
    assert sue_giftunit.owner_id == sue_text
    assert sue_giftunit._gift_id == init_gift_id() + 1
    assert sue_giftunit._gift_id == 1
    assert sue_giftunit._gift_id == sue_userhub._get_next_gift_file_number()
    assert sue_giftunit._faces == set()
    assert sue_giftunit._atoms_dir == sue_userhub.atoms_dir()
    assert sue_giftunit._gifts_dir == sue_userhub.gifts_dir()


def test_UserHub_get_giftunit_ReturnsCorrectObjWhenFilesDoesExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    yao_text = "yao"
    x0_giftunit = sue_userhub._default_giftunit()
    x0_giftunit.set_face(yao_text)
    sue_userhub.save_gift_file(x0_giftunit)
    bob_text = "Bob"
    x1_giftunit = sue_userhub._default_giftunit()
    x1_giftunit.set_face(bob_text)
    sue_userhub.save_gift_file(x1_giftunit)

    # WHEN
    y0_giftunit = sue_userhub.get_giftunit(x0_giftunit._gift_id)
    y1_giftunit = sue_userhub.get_giftunit(x1_giftunit._gift_id)

    # THEN
    assert y0_giftunit != None
    assert y1_giftunit != None
    assert yao_text in y0_giftunit._faces
    assert bob_text not in y0_giftunit._faces
    assert bob_text in y1_giftunit._faces


def test_UserHub_get_giftunit_RaisesExceptionWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    yao_text = "yao"
    x0_giftunit = sue_userhub._default_giftunit()
    x0_giftunit.set_face(yao_text)
    sue_userhub.save_gift_file(x0_giftunit)
    bob_text = "Bob"
    x1_giftunit = sue_userhub._default_giftunit()
    x1_giftunit.set_face(bob_text)
    sue_userhub.save_gift_file(x1_giftunit)

    # WHEN / THEN
    six_file_number = 6
    with pytest_raises(Exception) as excinfo:
        sue_userhub.get_giftunit(six_file_number)
    assert (
        str(excinfo.value) == f"GiftUnit file_number {six_file_number} does not exist."
    )


def test_UserHub_del_gift_file_DeletesgiftjsonAndNotAtomUnitjsons(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    six_int = 6
    sue_giftunit = giftunit_shop(
        owner_id=sue_text,
        _gift_id=six_int,
        _atoms_dir=sue_userhub.atoms_dir(),
        _gifts_dir=sue_userhub.gifts_dir(),
    )
    sue_giftunit._changeunit.set_atomunit(get_atom_example_ideaunit_knee())
    zero_int = 0
    assert sue_userhub.gift_file_exists(six_int) is False
    assert sue_userhub.atom_file_exists(zero_int) is False

    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    sue_userhub.save_gift_file(sue_giftunit, correct_invalid_attrs=False)

    print(f"{dir_files(sue_userhub.atoms_dir())}")
    assert sue_userhub.gift_file_exists(six_int)
    assert sue_userhub.atom_file_exists(zero_int)

    # WHEN
    sue_userhub._del_gift_file(sue_giftunit._gift_id)

    # THEN
    assert sue_userhub.gift_file_exists(six_int) is False
    assert sue_userhub.atom_file_exists(zero_int)


def test_UserHub_save_gift_file_CanCreateAndModify3giftunits(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    delete_dir(sue_userhub.gifts_dir())
    delete_dir(sue_userhub.atoms_dir())
    set_dir(sue_userhub.gifts_dir())
    set_dir(sue_userhub.atoms_dir())
    assert len(dir_files(sue_userhub.gifts_dir())) == 0
    assert len(dir_files(sue_userhub.atoms_dir())) == 0

    # WHEN
    sue_userhub.save_gift_file(sue_2atomunits_giftunit())
    sue_userhub.save_gift_file(sue_3atomunits_giftunit())
    sue_userhub.save_gift_file(sue_4atomunits_giftunit())

    # THEN
    assert len(dir_files(sue_userhub.gifts_dir())) == 3
    assert len(dir_files(sue_userhub.atoms_dir())) == 9


def test_UserHub_save_gift_file_ReturnsValidObj(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    sue2_giftunit = sue_2atomunits_giftunit()
    sue2_giftunit._atoms_dir = f"{sue_userhub.econs_dir()}/swimming"
    sue2_giftunit._gifts_dir = f"{sue_userhub.econs_dir()}/swimming"
    sue2_giftunit.owner_id = "Bob"
    sue2_giftunit._gift_id = sue_userhub._get_next_gift_file_number() - 5
    prev_sue2_giftunit = copy_deepcopy(sue2_giftunit)

    # WHEN
    valid_giftunit = sue_userhub.save_gift_file(sue2_giftunit)

    # THEN
    assert valid_giftunit._gifts_dir != prev_sue2_giftunit._gifts_dir
    assert valid_giftunit._gifts_dir == sue_userhub.gifts_dir()
    assert valid_giftunit._atoms_dir == sue_userhub.atoms_dir()
    assert valid_giftunit._gift_id != prev_sue2_giftunit._gift_id


def test_UserHub_create_save_gift_file_SaveCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    two_int = 2
    three_int = 3
    print(f"{sue_userhub.gift_file_path(two_int)=}")
    print(f"{sue_userhub.gift_file_path(three_int)=}")
    sue_giftunit = giftunit_shop(
        owner_id=sue_text,
        _gift_id=two_int,
        _atoms_dir=sue_userhub.atoms_dir(),
        _gifts_dir=sue_userhub.gifts_dir(),
    )
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    sue_userhub.save_gift_file(sue_giftunit, correct_invalid_attrs=False)
    assert sue_userhub.gift_file_exists(two_int)
    assert sue_userhub.gift_file_exists(three_int) is False

    # WHEN
    before_world = sue_userhub.default_same_world()
    bob_text = "Bob"
    after_world = copy_deepcopy(before_world)
    after_world.add_charunit(bob_text)
    sue_userhub.create_save_gift_file(before_world, after_world)

    # THEN
    assert sue_userhub.gift_file_exists(three_int)


def test_UserHub_merge_any_gifts_ReturnsEqualObj(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    sue_userhub.save_same_world(sue_userhub.default_same_world())
    same_world = sue_userhub.get_same_world()
    same_world._last_gift_id is None

    # WHEN
    new_world = sue_userhub._merge_any_gifts(same_world)

    # THEN
    assert new_world == same_world


def test_UserHub_merge_any_gifts_ReturnsObj_WithSinglegiftModifies_1atom(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    sue_userhub.save_gift_file(sue_1atomunits_giftunit())
    sue_userhub.save_same_world(sue_userhub.default_same_world())
    same_world = sue_userhub.get_same_world()
    print(f"{same_world._real_id=}")
    print(f"{sue_userhub.real_id=}")
    sports_text = "sports"
    sports_road = same_world.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = same_world.make_road(sports_road, knee_text)
    assert same_world.idea_exists(sports_road) is False

    # WHEN
    new_world = sue_userhub._merge_any_gifts(same_world)

    # THEN
    assert new_world != same_world
    assert new_world.idea_exists(sports_road)


def test_UserHub_merge_any_gifts_ReturnsObj_WithSinglegiftModifies_2atoms(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)
    sue_userhub.save_gift_file(sue_2atomunits_giftunit())
    sue_userhub.save_same_world(sue_userhub.default_same_world())
    same_world = sue_userhub.get_same_world()
    print(f"{same_world._real_id=}")
    sports_text = "sports"
    sports_road = same_world.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = same_world.make_road(sports_road, knee_text)
    assert same_world.idea_exists(sports_road) is False
    assert same_world.idea_exists(knee_road) is False

    # WHEN
    new_world = sue_userhub._merge_any_gifts(same_world)

    # THEN
    assert new_world != same_world
    assert new_world.idea_exists(sports_road)
    assert new_world.idea_exists(knee_road)
