from src.agenda.book import bookunit_shop
from src.world.gift import (
    GiftUnit,
    giftunit_shop,
    create_giftunit_from_files,
    get_json_filename,
)
from src.world.examples.example_atoms import get_atom_example_ideaunit_knee
from src.world.examples.example_gifts import (
    get_sue_giftunit,
    sue_2atomunits_giftunit,
    sue_3atomunits_giftunit,
    sue_4atomunits_giftunit,
)
from src.world.person import personunit_shop
from src.world.examples.world_env_kit import (
    get_test_worlds_dir,
    get_test_world_id,
    worlds_dir_setup_cleanup,
)
from src.instrument.file import open_file, dir_files
from os.path import exists as os_path_exists
from pytest import raises as pytest_raises


def test_PersonUnit_save_giftunit_file_SaveCorrectObj(worlds_dir_setup_cleanup):
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    two_int = 2
    six_int = 6
    two_filename = get_json_filename(two_int)
    six_filename = get_json_filename(six_int)
    sue_gift2_path = f"{sue_person._gifts_dir}/{two_filename}"
    sue_gift6_path = f"{sue_person._gifts_dir}/{six_filename}"
    print(f"{sue_gift2_path=}")
    print(f"{sue_gift6_path=}")
    x_gift_id = two_int
    sue_giftunit = giftunit_shop(
        _gifter=sue_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_person._atoms_dir,
        _gifts_dir=sue_person._gifts_dir,
    )
    assert os_path_exists(sue_gift2_path) == False
    assert os_path_exists(sue_gift6_path) == False

    # WHEN
    sue_person.save_giftunit_file(sue_giftunit)

    # THEN
    assert os_path_exists(sue_gift2_path)
    assert os_path_exists(sue_gift6_path) == False
    two_file_json = open_file(sue_person._gifts_dir, two_filename)
    assert two_file_json == sue_giftunit.get_bookmetric_json()


def test_PersonUnit_save_giftunit_file_RaisesErrorIfGiftUnit_atoms_dir_IsWrong(
    worlds_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_gift6_path = f"{sue_person._gifts_dir}/{six_filename}"
    print(f"{sue_gift6_path=}")
    sue_giftunit = giftunit_shop(
        _gifter=sue_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_person.person_dir,
        _gifts_dir=sue_person._gifts_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_person.save_giftunit_file(sue_giftunit)
    assert (
        str(excinfo.value)
        == f"GiftUnit file cannot be saved because giftunit._atoms_dir is incorrect: {sue_giftunit._atoms_dir}. It must be {sue_person._atoms_dir}."
    )


def test_PersonUnit_save_giftunit_file_RaisesErrorIfGiftUnit_gifts_dir_IsWrong(
    worlds_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_gift6_path = f"{sue_person._gifts_dir}/{six_filename}"
    print(f"{sue_gift6_path=}")
    sue_giftunit = giftunit_shop(
        _gifter=sue_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_person._atoms_dir,
        _gifts_dir=sue_person.person_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_person.save_giftunit_file(sue_giftunit)
    assert (
        str(excinfo.value)
        == f"GiftUnit file cannot be saved because giftunit._gifts_dir is incorrect: {sue_giftunit._gifts_dir}. It must be {sue_person._gifts_dir}."
    )


def test_PersonUnit_giftunit_file_exists_ReturnsCorrectObj(worlds_dir_setup_cleanup):
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    x_gift_id = 2
    six_int = 6
    two_filename = get_json_filename(x_gift_id)
    six_filename = get_json_filename(six_int)
    sue_gift2_path = f"{sue_person._gifts_dir}/{two_filename}"
    sue_gift6_path = f"{sue_person._gifts_dir}/{six_filename}"
    print(f"{sue_gift2_path=}")
    sue_giftunit = giftunit_shop(
        _gifter=sue_person.person_id,
        _gift_id=x_gift_id,
        _atoms_dir=sue_person._atoms_dir,
        _gifts_dir=sue_person._gifts_dir,
    )
    assert os_path_exists(sue_gift2_path) == False
    assert os_path_exists(sue_gift6_path) == False
    assert sue_person.giftunit_file_exists(x_gift_id) == False
    assert sue_person.giftunit_file_exists(six_int) == False

    # WHEN
    sue_person.save_giftunit_file(sue_giftunit)

    # THEN
    assert os_path_exists(sue_gift2_path)
    assert os_path_exists(sue_gift6_path) == False
    assert sue_person.giftunit_file_exists(x_gift_id)
    assert sue_person.giftunit_file_exists(six_int) == False
    two_file_json = open_file(sue_person._gifts_dir, two_filename)
    assert two_file_json == sue_giftunit.get_bookmetric_json()


def test_PersonUnit_save_giftunit_file_RaisesErrorIfGiftUnit_gifter_IsWrong(
    worlds_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_gift6_path = f"{sue_person._gifts_dir}/{six_filename}"
    print(f"{sue_gift6_path=}")
    bob_text = "Bob"
    sue_giftunit = giftunit_shop(
        _gifter=bob_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_person._atoms_dir,
        _gifts_dir=sue_person._gifts_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_person.save_giftunit_file(sue_giftunit)
    assert (
        str(excinfo.value)
        == f"GiftUnit file cannot be saved because giftunit._gifter is incorrect: {sue_giftunit._gifter}. It must be {sue_person.person_id}."
    )


def test_PersonUnit_save_giftunit_file_RaisesErrorIf_replace_IsFalse(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_giftunit = giftunit_shop(
        _gifter=sue_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_person._atoms_dir,
        _gifts_dir=sue_person._gifts_dir,
    )
    sue_person.save_giftunit_file(sue_giftunit)

    sue_gift6_path = f"{sue_person._gifts_dir}/{six_filename}"
    print(f"{sue_gift6_path=}")
    assert os_path_exists(sue_gift6_path)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_person.save_giftunit_file(sue_giftunit, replace=False)
    assert (
        str(excinfo.value)
        == f"GiftUnit file {six_filename} already exists and cannot be saved over."
    )


def test_PersonUnit_get_valid_giftunit_ReturnsObjWithAttributesFixed(
    worlds_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    two_int = 2
    two_filename = get_json_filename(two_int)
    sue_gift2_path = f"{sue_person._gifts_dir}/{two_filename}"
    print(f"{sue_gift2_path=}")

    # WHEN
    invalid_sue_giftunit = giftunit_shop(
        _gifter="Bob",
        _gift_id=sue_person.get_next_gift_file_number() - 5,
        _atoms_dir=f"{sue_person.person_dir}/swimming",
        _gifts_dir=f"{sue_person.person_dir}/swimming",
    )
    valid_giftunit = sue_person.get_valid_giftunit(invalid_sue_giftunit)

    # THEN
    assert valid_giftunit._atoms_dir == sue_person._atoms_dir
    assert valid_giftunit._gifts_dir == sue_person._gifts_dir
    assert valid_giftunit._gift_id == sue_person.get_next_gift_file_number()
    correct_sue_giftunit = giftunit_shop(
        _gifter=sue_text,
        _gift_id=sue_person.get_next_gift_file_number(),
        _atoms_dir=sue_person._atoms_dir,
        _gifts_dir=sue_person._gifts_dir,
    )
    assert valid_giftunit == correct_sue_giftunit


def test_PersonUnit_save_giftunit_file_SaveCorrectObj_change_invalid_attrs_IsTrue(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    next_int = sue_person.get_next_gift_file_number()
    next_filename = get_json_filename(next_int)
    sue_gift2_path = f"{sue_person._gifts_dir}/{next_filename}"
    print(f"{sue_gift2_path=}")
    assert os_path_exists(sue_gift2_path) == False

    # WHEN
    invalid_sue_giftunit = giftunit_shop(
        _gifter="Bob",
        _gift_id=sue_person.get_next_gift_file_number() - 5,
        _atoms_dir=f"{sue_person.person_dir}/swimming",
        _gifts_dir=f"{sue_person.person_dir}/swimming",
    )
    sue_person.save_giftunit_file(invalid_sue_giftunit, change_invalid_attrs=True)

    # THEN
    assert os_path_exists(sue_gift2_path)
    two_file_json = open_file(sue_person._gifts_dir, next_filename)


def test_PersonUnit_get_max_gift_file_number_ReturnsCorrectObj(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)

    # WHEN / THEN
    assert sue_person.get_max_gift_file_number() is None
    assert sue_person.get_next_gift_file_number() == 0

    # GIVEN
    six_int = 6
    sue6_giftunit = giftunit_shop(
        _gifter=sue_text,
        _gift_id=six_int,
        _atoms_dir=sue_person._atoms_dir,
        _gifts_dir=sue_person._gifts_dir,
    )
    sue2_giftunit = giftunit_shop(
        _gifter=sue_text,
        _gift_id=2,
        _atoms_dir=sue_person._atoms_dir,
        _gifts_dir=sue_person._gifts_dir,
    )
    sue_person.save_giftunit_file(sue6_giftunit)
    sue_person.save_giftunit_file(sue2_giftunit)

    # WHEN / THEN
    assert sue_person.get_max_gift_file_number() == six_int
    assert sue_person.get_next_gift_file_number() == 7


def test_PersonUnit_get_new_giftunit_ReturnsObjWithCorrect_gift_id_WhenNoGiftFilesExist(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)

    # WHEN
    sue_giftunit = sue_person.get_new_giftunit()

    # THEN
    assert sue_giftunit._gifter == sue_person.person_id
    assert sue_giftunit._gift_id == 0
    assert sue_giftunit._gift_id == sue_person.get_next_gift_file_number()
    assert sue_giftunit._giftees == set()
    assert sue_giftunit._atoms_dir == sue_person._atoms_dir
    assert sue_giftunit._gifts_dir == sue_person._gifts_dir


def test_PersonUnit_get_new_giftunit_ReturnsObjWithCorrect_gift_id_WhenGiftFilesExist(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    zero_giftunit = get_sue_giftunit()
    zero_giftunit._gift_id = sue_person.get_next_gift_file_number()
    zero_giftunit._atoms_dir = sue_person._atoms_dir
    zero_giftunit._gifts_dir = sue_person._gifts_dir
    sue_person.save_giftunit_file(zero_giftunit)

    # WHEN
    sue_giftunit = sue_person.get_new_giftunit()

    # THEN
    assert sue_giftunit._gifter == sue_person.person_id
    assert sue_giftunit._gift_id == 1
    assert sue_giftunit._gift_id == sue_person.get_next_gift_file_number()
    assert sue_giftunit._giftees == set()
    assert sue_giftunit._atoms_dir == sue_person._atoms_dir
    assert sue_giftunit._gifts_dir == sue_person._gifts_dir


def test_PersonUnit_get_giftunit_ReturnsCorrectObjWhenFilesDoesExist(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    yao_text = "yao"
    x0_giftunit = sue_person.get_new_giftunit()
    x0_giftunit.set_giftee(yao_text)
    sue_person.save_giftunit_file(x0_giftunit)
    bob_text = "Bob"
    x1_giftunit = sue_person.get_new_giftunit()
    x1_giftunit.set_giftee(bob_text)
    sue_person.save_giftunit_file(x1_giftunit)

    # WHEN
    y0_giftunit = sue_person.get_giftunit(x0_giftunit._gift_id)
    y1_giftunit = sue_person.get_giftunit(x1_giftunit._gift_id)

    # THEN
    assert y0_giftunit != None
    assert y1_giftunit != None
    assert yao_text in y0_giftunit._giftees
    assert bob_text not in y0_giftunit._giftees
    assert bob_text in y1_giftunit._giftees


def test_PersonUnit_get_giftunit_RaisesExceptionWhenFileDoesNotExist(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    yao_text = "yao"
    x0_giftunit = sue_person.get_new_giftunit()
    x0_giftunit.set_giftee(yao_text)
    sue_person.save_giftunit_file(x0_giftunit)
    bob_text = "Bob"
    x1_giftunit = sue_person.get_new_giftunit()
    x1_giftunit.set_giftee(bob_text)
    sue_person.save_giftunit_file(x1_giftunit)

    # WHEN / THEN
    six_file_number = 6
    with pytest_raises(Exception) as excinfo:
        sue_person.get_giftunit(six_file_number)
    assert (
        str(excinfo.value) == f"GiftUnit file_number {six_file_number} does not exist."
    )


def test_PersonUnit_del_giftunit_DeletesGiftjsonAndNotAgendaAtomjsons(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_giftunit = giftunit_shop(
        _gifter=sue_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_person._atoms_dir,
        _gifts_dir=sue_person._gifts_dir,
    )
    sue_giftunit._bookunit.set_agendaatom(get_atom_example_ideaunit_knee())
    atom0_filename = sue_giftunit._get_num_filename(0)
    sue_gift6_path = f"{sue_person._gifts_dir}/{six_filename}"
    sue_atom0_path = f"{sue_person._atoms_dir}/{atom0_filename}"
    assert os_path_exists(sue_gift6_path) == False
    assert os_path_exists(sue_atom0_path) == False

    sue_person.save_giftunit_file(sue_giftunit)

    print(f"{dir_files(sue_person._atoms_dir)}")
    assert os_path_exists(sue_gift6_path)
    assert os_path_exists(sue_atom0_path)

    # WHEN
    sue_person.del_giftunit_file(sue_giftunit._gift_id)

    # THEN
    assert os_path_exists(sue_gift6_path) == False
    assert os_path_exists(sue_atom0_path)


def test_PersonUnit_CanCreateAndChange3Giftunits(worlds_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    assert len(dir_files(sue_person._gifts_dir)) == 0
    assert len(dir_files(sue_person._atoms_dir)) == 0

    # WHEN
    sue_person.save_giftunit_file(sue_2atomunits_giftunit(), change_invalid_attrs=True)
    sue_person.save_giftunit_file(sue_3atomunits_giftunit(), change_invalid_attrs=True)
    sue_person.save_giftunit_file(sue_4atomunits_giftunit(), change_invalid_attrs=True)

    # THEN
    assert len(dir_files(sue_person._gifts_dir)) == 3
    assert len(dir_files(sue_person._atoms_dir)) == 9


# def test_PersonUnit_build_agenda_ReturnsObjGivenOnlyLastGiftNumber(
#     worlds_dir_setup_cleanup,
# ):

#     assert 1 == 2


# def test_PersonUnit_build_agenda_ReturnsObjGivenBeginAgendaAndGiftRange(
#     worlds_dir_setup_cleanup,
# ):
#     assert 1 == 2


# def test_PersonUnit_save_valid_atom_file_CorrectlySavesFile(worlds_dir_setup_cleanup):
#     # GIVEN
#     yao_person = personunit_shop("Yao")
#     one_int = 1
#     assert os_path_exists(f"{yao_person._atoms_dir}/{one_int}.json") == False

#     # WHEN
#     atom_num = yao_person._save_valid_atom_file(
#         get_atom_example_beliefunit_knee(), one_int
#     )

#     # THEN
#     assert os_path_exists(f"{yao_person._atoms_dir}/{one_int}.json")
#     assert atom_num == one_int


# def test_PersonUnit_atom_file_exists_ReturnsCorrectObj(worlds_dir_setup_cleanup):
#     # GIVEN
#     yao_person = personunit_shop("Yao")
#     five_int = 5
#     assert os_path_exists(f"{yao_person._atoms_dir}/{five_int}.json") == False
#     assert yao_person.atom_file_exists(five_int) == False

#     # WHEN
#     yao_person._save_valid_atom_file(get_atom_example_beliefunit_knee(), five_int)

#     # THEN
#     assert os_path_exists(f"{yao_person._atoms_dir}/{five_int}.json")
#     assert yao_person.atom_file_exists(five_int)


# def test_PersonUnit_delete_atom_file_CorrectlyDeletesFile(worlds_dir_setup_cleanup):
#     # GIVEN
#     yao_person = personunit_shop("Yao")
#     ten_int = 10
#     yao_person._save_valid_atom_file(get_atom_example_beliefunit_knee(), ten_int)
#     assert os_path_exists(f"{yao_person._atoms_dir}/{ten_int}.json")

#     # WHEN
#     yao_person._delete_atom_file(ten_int)

#     # THEN
#     assert os_path_exists(f"{yao_person._atoms_dir}/{ten_int}.json") == False


# def test_PersonUnit_get_max_atom_file_number_ReturnsCorrectObj(worlds_dir_setup_cleanup):
#     # GIVEN
#     yao_person = personunit_shop("Yao")
#     ten_int = 10
#     yao_person._save_valid_atom_file(get_atom_example_beliefunit_knee(), ten_int)
#     assert os_path_exists(f"{yao_person._atoms_dir}/{ten_int}.json")

#     # WHEN / THEN
#     assert yao_person._get_max_atom_file_number() == ten_int


# def test_PersonUnit_get_max_atom_file_number_ReturnsCorrectObjWhenDirIsEmpty(
#     worlds_dir_setup_cleanup,
# ):
#     # GIVEN
#     yao_person = personunit_shop("Yao")

#     # WHEN / THEN
#     assert yao_person._get_max_atom_file_number() == 0


# def test_PersonUnit_get_next_atom_file_number_ReturnsCorrectObj(worlds_dir_setup_cleanup):
#     # GIVEN
#     yao_person = personunit_shop("Yao")
#     ten_int = 10
#     yao_person._save_valid_atom_file(get_atom_example_beliefunit_knee(), ten_int)
#     assert os_path_exists(f"{yao_person._atoms_dir}/{ten_int}.json")

#     # WHEN / THEN
#     assert yao_person._get_next_atom_file_number() == "11.json"


# def test_PersonUnit_save_atom_file_CorrectlySavesFile(worlds_dir_setup_cleanup):
#     # GIVEN
#     yao_person = personunit_shop("Yao")
#     ten_int = 10
#     yao_person._save_valid_atom_file(get_atom_example_beliefunit_knee(), ten_int)
#     assert yao_person._get_max_atom_file_number() == ten_int
#     eleven_int = ten_int + 1
#     assert os_path_exists(f"{yao_person._atoms_dir}/{eleven_int}.json") == False

#     # WHEN
#     atom_num1 = yao_person.save_atom_file(get_atom_example_beliefunit_knee())

#     # THEN
#     assert yao_person._get_max_atom_file_number() != ten_int
#     assert yao_person._get_max_atom_file_number() == eleven_int
#     assert os_path_exists(f"{yao_person._atoms_dir}/{eleven_int}.json")
#     assert atom_num1 == eleven_int
#     atom_num2 = yao_person.save_atom_file(get_atom_example_beliefunit_knee())
#     assert atom_num2 == 12


# def test_PersonUnit_get_agenda_from_atom_files_ReturnsCorrectFile_ZeroAtoms(
#     worlds_dir_setup_cleanup,
# ):
#     # GIVEN
#     yao_text = "Yao"
#     yao_person = personunit_shop(yao_text)

#     # WHEN
#     yao_agenda = yao_person._get_agenda_from_atom_files()

#     # THEN
#     assert yao_agenda._owner_id == yao_text
#     assert yao_agenda._world_id == yao_person.world_id
#     assert yao_agenda._road_delimiter == yao_person._road_delimiter
#     assert yao_agenda._planck == yao_person._planck


# def test_PersonUnit_get_agenda_from_atom_files_ReturnsCorrectFile_SimpleIdea(
#     worlds_dir_setup_cleanup,
# ):
#     # GIVEN
#     yao_text = "Yao"
#     yao_person = personunit_shop(yao_text)
#     # save atom files
#     yao_person.save_atom_file(get_atom_example_ideaunit_sports(yao_person.world_id))

#     # WHEN
#     yao_agenda = yao_person._get_agenda_from_atom_files()

#     # THEN
#     assert yao_agenda._owner_id == yao_text
#     assert yao_agenda._world_id == yao_person.world_id
#     assert yao_agenda._road_delimiter == yao_person._road_delimiter
#     sports_text = "sports"
#     sports_road = yao_agenda.make_l1_road(sports_text)

#     assert yao_agenda.idea_exists(sports_road)


# def test_PersonUnit_get_agenda_from_atom_files_ReturnsCorrectFile_WithBeliefUnit(
#     worlds_dir_setup_cleanup,
# ):
#     # GIVEN
#     yao_text = "Yao"
#     yao_person = personunit_shop(yao_text)
#     # save atom files
#     yao_person.save_atom_file(get_atom_example_ideaunit_sports(yao_person.world_id))
#     yao_person.save_atom_file(get_atom_example_ideaunit_ball(yao_person.world_id))
#     yao_person.save_atom_file(get_atom_example_ideaunit_knee(yao_person.world_id))
#     yao_person.save_atom_file(get_atom_example_beliefunit_knee(yao_person.world_id))

#     # WHEN
#     yao_agenda = yao_person._get_agenda_from_atom_files()

#     # THEN
#     assert yao_agenda._owner_id == yao_text
#     assert yao_agenda._world_id == yao_person.world_id
#     assert yao_agenda._road_delimiter == yao_person._road_delimiter
#     sports_text = "sports"
#     sports_road = yao_agenda.make_l1_road(sports_text)

#     assert yao_agenda.idea_exists(sports_road)
