from src.agenda.book import bookunit_shop
from src.real.gift import (
    GiftUnit,
    giftunit_shop,
    create_giftunit_from_files,
    get_json_filename,
    init_gift_id,
)
from src.real.examples.example_atoms import get_atom_example_ideaunit_knee
from src.real.examples.example_gifts import (
    get_sue_giftunit,
    sue_1atomunits_giftunit,
    sue_2atomunits_giftunit,
    sue_3atomunits_giftunit,
    sue_4atomunits_giftunit,
)
from src.real.person import personunit_shop
from src.real.examples.real_env_kit import (
    get_test_reals_dir,
    get_test_real_id,
    reals_dir_setup_cleanup,
)
from src._instrument.file import open_file, dir_files, delete_dir, set_dir
from os.path import exists as os_path_exists
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy


def test_PersonUnit_save_giftunit_file_SaveCorrectObj(reals_dir_setup_cleanup):
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    two_int = 2
    six_int = 6
    two_filename = get_json_filename(two_int)
    six_filename = get_json_filename(six_int)
    sue_gift2_path = f"{sue_person._gifts_dir}/{two_filename}"
    sue_gift0_path = f"{sue_person._gifts_dir}/{six_filename}"
    print(f"{sue_gift2_path=}")
    print(f"{sue_gift0_path=}")
    x_gift_id = two_int
    sue_giftunit = giftunit_shop(
        _giver=sue_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_person._atoms_dir,
        _gifts_dir=sue_person._gifts_dir,
    )
    assert os_path_exists(sue_gift2_path) == False
    assert os_path_exists(sue_gift0_path) == False

    # WHEN
    sue_person.save_giftunit_file(sue_giftunit, change_invalid_attrs=False)

    # THEN
    assert os_path_exists(sue_gift2_path)
    assert os_path_exists(sue_gift0_path) == False
    two_file_json = open_file(sue_person._gifts_dir, two_filename)
    assert two_file_json == sue_giftunit.get_bookmetric_json()


def test_PersonUnit_save_giftunit_file_RaisesErrorIfGiftUnit_atoms_dir_IsWrong(
    reals_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_gift0_path = f"{sue_person._gifts_dir}/{six_filename}"
    print(f"{sue_gift0_path=}")
    sue_giftunit = giftunit_shop(
        _giver=sue_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_person.person_dir,
        _gifts_dir=sue_person._gifts_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_person.save_giftunit_file(sue_giftunit, change_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"GiftUnit file cannot be saved because giftunit._atoms_dir is incorrect: {sue_giftunit._atoms_dir}. It must be {sue_person._atoms_dir}."
    )


def test_PersonUnit_save_giftunit_file_RaisesErrorIfGiftUnit_gifts_dir_IsWrong(
    reals_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_gift0_path = f"{sue_person._gifts_dir}/{six_filename}"
    print(f"{sue_gift0_path=}")
    sue_giftunit = giftunit_shop(
        _giver=sue_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_person._atoms_dir,
        _gifts_dir=sue_person.person_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_person.save_giftunit_file(sue_giftunit, change_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"GiftUnit file cannot be saved because giftunit._gifts_dir is incorrect: {sue_giftunit._gifts_dir}. It must be {sue_person._gifts_dir}."
    )


def test_PersonUnit_giftunit_file_exists_ReturnsCorrectObj(reals_dir_setup_cleanup):
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    x_gift_id = 2
    six_int = 6
    two_filename = get_json_filename(x_gift_id)
    six_filename = get_json_filename(six_int)
    sue_gift2_path = f"{sue_person._gifts_dir}/{two_filename}"
    sue_gift0_path = f"{sue_person._gifts_dir}/{six_filename}"
    print(f"{sue_gift2_path=}")
    sue_giftunit = giftunit_shop(
        _giver=sue_person.person_id,
        _gift_id=x_gift_id,
        _atoms_dir=sue_person._atoms_dir,
        _gifts_dir=sue_person._gifts_dir,
    )
    assert os_path_exists(sue_gift2_path) == False
    assert os_path_exists(sue_gift0_path) == False
    assert sue_person.giftunit_file_exists(x_gift_id) == False
    assert sue_person.giftunit_file_exists(six_int) == False

    # WHEN
    sue_person.save_giftunit_file(sue_giftunit, change_invalid_attrs=False)

    # THEN
    assert os_path_exists(sue_gift2_path)
    assert os_path_exists(sue_gift0_path) == False
    assert sue_person.giftunit_file_exists(x_gift_id)
    assert sue_person.giftunit_file_exists(six_int) == False
    two_file_json = open_file(sue_person._gifts_dir, two_filename)
    assert two_file_json == sue_giftunit.get_bookmetric_json()


def test_PersonUnit_save_giftunit_file_RaisesErrorIfGiftUnit_giver_IsWrong(
    reals_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_gift0_path = f"{sue_person._gifts_dir}/{six_filename}"
    print(f"{sue_gift0_path=}")
    bob_text = "Bob"
    sue_giftunit = giftunit_shop(
        _giver=bob_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_person._atoms_dir,
        _gifts_dir=sue_person._gifts_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_person.save_giftunit_file(sue_giftunit, change_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"GiftUnit file cannot be saved because giftunit._giver is incorrect: {sue_giftunit._giver}. It must be {sue_person.person_id}."
    )


def test_PersonUnit_save_giftunit_file_RaisesErrorIf_replace_IsFalse(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    x_gift_id = 1
    six_filename = get_json_filename(x_gift_id)
    sue_giftunit = giftunit_shop(
        _giver=sue_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_person._atoms_dir,
        _gifts_dir=sue_person._gifts_dir,
    )
    saved_giftunit = sue_person.save_giftunit_file(sue_giftunit)

    sue_gift0_path = f"{sue_person._gifts_dir}/{six_filename}"
    print(f"{sue_gift0_path=}")
    assert os_path_exists(sue_gift0_path)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_person.save_giftunit_file(
            saved_giftunit, replace=False, change_invalid_attrs=False
        )
    assert (
        str(excinfo.value)
        == f"GiftUnit file {six_filename} already exists and cannot be saved over."
    )


def test_PersonUnit_validate_giftunit_ReturnsObjWithAttributesFixed(
    reals_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    two_int = 2
    two_filename = get_json_filename(two_int)
    sue_gift2_path = f"{sue_person._gifts_dir}/{two_filename}"
    print(f"{sue_gift2_path=}")

    # WHEN
    invalid_sue_giftunit = giftunit_shop(
        _giver="Bob",
        _gift_id=sue_person._get_next_gift_file_number() - 5,
        _atoms_dir=f"{sue_person.person_dir}/swimming",
        _gifts_dir=f"{sue_person.person_dir}/swimming",
    )
    valid_giftunit = sue_person.validate_giftunit(invalid_sue_giftunit)

    # THEN
    assert valid_giftunit._atoms_dir == sue_person._atoms_dir
    assert valid_giftunit._gifts_dir == sue_person._gifts_dir
    assert valid_giftunit._gift_id == sue_person._get_next_gift_file_number()
    correct_sue_giftunit = giftunit_shop(
        _giver=sue_text,
        _gift_id=sue_person._get_next_gift_file_number(),
        _atoms_dir=sue_person._atoms_dir,
        _gifts_dir=sue_person._gifts_dir,
    )
    assert valid_giftunit == correct_sue_giftunit


def test_PersonUnit_save_giftunit_file_SaveCorrectObj_change_invalid_attrs_IsTrue(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    next_int = sue_person._get_next_gift_file_number()
    next_filename = get_json_filename(next_int)
    sue_gift2_path = f"{sue_person._gifts_dir}/{next_filename}"
    print(f"{sue_gift2_path=}")
    assert os_path_exists(sue_gift2_path) == False

    # WHEN
    invalid_sue_giftunit = giftunit_shop(
        _giver="Bob",
        _gift_id=sue_person._get_next_gift_file_number() - 5,
        _atoms_dir=f"{sue_person.person_dir}/swimming",
        _gifts_dir=f"{sue_person.person_dir}/swimming",
    )
    sue_person.save_giftunit_file(invalid_sue_giftunit)

    # THEN
    assert os_path_exists(sue_gift2_path)
    two_file_json = open_file(sue_person._gifts_dir, next_filename)


def test_PersonUnit_get_max_gift_file_number_ReturnsCorrectObj(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)

    # WHEN / THEN
    delete_dir(sue_person._gifts_dir)
    assert sue_person.get_max_gift_file_number() is None
    assert sue_person._get_next_gift_file_number() == init_gift_id()
    assert sue_person._get_next_gift_file_number() == 0

    # GIVEN
    six_int = 6
    sue6_giftunit = giftunit_shop(
        _giver=sue_text,
        _gift_id=six_int,
        _atoms_dir=sue_person._atoms_dir,
        _gifts_dir=sue_person._gifts_dir,
    )
    sue2_giftunit = giftunit_shop(
        _giver=sue_text,
        _gift_id=2,
        _atoms_dir=sue_person._atoms_dir,
        _gifts_dir=sue_person._gifts_dir,
    )
    sue_person.save_giftunit_file(sue6_giftunit, change_invalid_attrs=False)
    sue_person.save_giftunit_file(sue2_giftunit, change_invalid_attrs=False)

    # WHEN / THEN
    assert sue_person.get_max_gift_file_number() == six_int
    assert sue_person._get_next_gift_file_number() == 7


def test_PersonUnit__create_new_giftunit_ReturnsObjWithCorrect_gift_id_WhenNoGiftFilesExist(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)

    # WHEN
    delete_dir(sue_person._gifts_dir)
    sue_giftunit = sue_person._create_new_giftunit()

    # THEN
    assert sue_giftunit._giver == sue_person.person_id
    assert sue_giftunit._gift_id == init_gift_id()
    assert sue_giftunit._gift_id == 0
    assert sue_giftunit._gift_id == sue_person._get_next_gift_file_number()
    assert sue_giftunit._takers == set()
    assert sue_giftunit._atoms_dir == sue_person._atoms_dir
    assert sue_giftunit._gifts_dir == sue_person._gifts_dir


def test_PersonUnit__create_new_giftunit_ReturnsObjWithCorrect_gift_id_WhenGiftFilesExist(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    delete_dir(sue_person._gifts_dir)

    zero_giftunit = get_sue_giftunit()
    zero_giftunit._gift_id = sue_person._get_next_gift_file_number()
    zero_giftunit._atoms_dir = sue_person._atoms_dir
    zero_giftunit._gifts_dir = sue_person._gifts_dir
    sue_person.save_giftunit_file(zero_giftunit)

    # WHEN
    sue_giftunit = sue_person._create_new_giftunit()

    # THEN
    assert sue_giftunit._giver == sue_person.person_id
    assert sue_giftunit._gift_id == init_gift_id() + 1
    assert sue_giftunit._gift_id == 1
    assert sue_giftunit._gift_id == sue_person._get_next_gift_file_number()
    assert sue_giftunit._takers == set()
    assert sue_giftunit._atoms_dir == sue_person._atoms_dir
    assert sue_giftunit._gifts_dir == sue_person._gifts_dir


def test_PersonUnit_get_giftunit_ReturnsCorrectObjWhenFilesDoesExist(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    yao_text = "yao"
    x0_giftunit = sue_person._create_new_giftunit()
    x0_giftunit.set_taker(yao_text)
    sue_person.save_giftunit_file(x0_giftunit)
    bob_text = "Bob"
    x1_giftunit = sue_person._create_new_giftunit()
    x1_giftunit.set_taker(bob_text)
    sue_person.save_giftunit_file(x1_giftunit)

    # WHEN
    y0_giftunit = sue_person.get_giftunit(x0_giftunit._gift_id)
    y1_giftunit = sue_person.get_giftunit(x1_giftunit._gift_id)

    # THEN
    assert y0_giftunit != None
    assert y1_giftunit != None
    assert yao_text in y0_giftunit._takers
    assert bob_text not in y0_giftunit._takers
    assert bob_text in y1_giftunit._takers


def test_PersonUnit_get_giftunit_RaisesExceptionWhenFileDoesNotExist(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    yao_text = "yao"
    x0_giftunit = sue_person._create_new_giftunit()
    x0_giftunit.set_taker(yao_text)
    sue_person.save_giftunit_file(x0_giftunit)
    bob_text = "Bob"
    x1_giftunit = sue_person._create_new_giftunit()
    x1_giftunit.set_taker(bob_text)
    sue_person.save_giftunit_file(x1_giftunit)

    # WHEN / THEN
    six_file_number = 6
    with pytest_raises(Exception) as excinfo:
        sue_person.get_giftunit(six_file_number)
    assert (
        str(excinfo.value) == f"GiftUnit file_number {six_file_number} does not exist."
    )


def test_PersonUnit_del_giftunit_DeletesGiftjsonAndNotAgendaAtomjsons(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_giftunit = giftunit_shop(
        _giver=sue_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_person._atoms_dir,
        _gifts_dir=sue_person._gifts_dir,
    )
    sue_giftunit._bookunit.set_agendaatom(get_atom_example_ideaunit_knee())
    atom0_filename = sue_giftunit._get_num_filename(0)
    sue_gift0_path = f"{sue_person._gifts_dir}/{six_filename}"
    sue_atom0_path = f"{sue_person._atoms_dir}/{atom0_filename}"
    assert os_path_exists(sue_gift0_path) == False
    assert os_path_exists(sue_atom0_path) == False

    sue_person.save_giftunit_file(sue_giftunit, change_invalid_attrs=False)

    print(f"{dir_files(sue_person._atoms_dir)}")
    assert os_path_exists(sue_gift0_path)
    assert os_path_exists(sue_atom0_path)

    # WHEN
    sue_person.del_giftunit_file(sue_giftunit._gift_id)

    # THEN
    assert os_path_exists(sue_gift0_path) == False
    assert os_path_exists(sue_atom0_path)


def test_PersonUnit_save_giftunit_file_CanCreateAndChange3Giftunits(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    delete_dir(sue_person._gifts_dir)
    delete_dir(sue_person._atoms_dir)
    set_dir(sue_person._gifts_dir)
    set_dir(sue_person._atoms_dir)
    assert len(dir_files(sue_person._gifts_dir)) == 0
    assert len(dir_files(sue_person._atoms_dir)) == 0

    # WHEN
    sue_person.save_giftunit_file(sue_2atomunits_giftunit())
    sue_person.save_giftunit_file(sue_3atomunits_giftunit())
    sue_person.save_giftunit_file(sue_4atomunits_giftunit())

    # THEN
    assert len(dir_files(sue_person._gifts_dir)) == 3
    assert len(dir_files(sue_person._atoms_dir)) == 9


def test_PersonUnit_save_giftunit_file_ReturnsValidObj(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    sue2_giftunit = sue_2atomunits_giftunit()
    sue2_giftunit._atoms_dir = f"{sue_person.person_dir}/swimming"
    sue2_giftunit._gifts_dir = f"{sue_person.person_dir}/swimming"
    sue2_giftunit._giver = "Bob"
    sue2_giftunit._gift_id = sue_person._get_next_gift_file_number() - 5
    prev_sue2_giftunit = copy_deepcopy(sue2_giftunit)

    # WHEN
    valid_giftunit = sue_person.save_giftunit_file(sue2_giftunit)

    # THEN
    assert valid_giftunit._gifts_dir != prev_sue2_giftunit._gifts_dir
    assert valid_giftunit._gifts_dir == sue_person._gifts_dir
    assert valid_giftunit._atoms_dir == sue_person._atoms_dir
    assert valid_giftunit._gift_id != prev_sue2_giftunit._gift_id


def test_PersonUnit_create_save_giftunit_SaveCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    two_int = 2
    three_int = 3
    two_filename = get_json_filename(two_int)
    three_filename = get_json_filename(three_int)
    sue_gift2_path = f"{sue_person._gifts_dir}/{two_filename}"
    sue_gift3_path = f"{sue_person._gifts_dir}/{three_filename}"
    print(f"{sue_gift2_path=}")
    print(f"{sue_gift3_path=}")
    sue_giftunit = giftunit_shop(
        _giver=sue_text,
        _gift_id=two_int,
        _atoms_dir=sue_person._atoms_dir,
        _gifts_dir=sue_person._gifts_dir,
    )
    sue_person.save_giftunit_file(sue_giftunit, change_invalid_attrs=False)
    assert os_path_exists(sue_gift2_path)
    assert os_path_exists(sue_gift3_path) == False

    # WHEN
    before_agenda = sue_person.get_gut_file_agenda()
    bob_text = "Bob"
    after_agenda = copy_deepcopy(before_agenda)
    after_agenda.add_partyunit(bob_text)
    sue_person.create_save_giftunit(before_agenda, after_agenda)

    # THEN
    assert os_path_exists(sue_gift3_path)


def test_PersonUnit_merge_gifts_into_agenda_ReturnsObj_NoChange(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    gut_agenda = sue_person.get_gut_file_agenda()
    gut_agenda._last_gift_id is None

    # WHEN
    new_agenda = sue_person._merge_gifts_into_agenda(gut_agenda)

    # THEN
    assert new_agenda == gut_agenda


def test_PersonUnit_merge_gifts_into_agenda_ReturnsObj_WithSingleGiftChanges_1atom(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    sue_person.save_giftunit_file(sue_1atomunits_giftunit())
    # sue_person.save_giftunit_file(sue_3atomunits_giftunit())
    # sue_person.save_giftunit_file(sue_4atomunits_giftunit())
    gut_agenda = sue_person.get_gut_file_agenda()
    print(f"{gut_agenda._real_id=}")
    sports_text = "sports"
    sports_road = gut_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = gut_agenda.make_road(sports_road, knee_text)
    assert gut_agenda.idea_exists(sports_road) == False

    # WHEN
    new_agenda = sue_person._merge_gifts_into_agenda(gut_agenda)

    # THEN
    assert new_agenda != gut_agenda
    assert new_agenda.idea_exists(sports_road)


def test_PersonUnit_merge_gifts_into_agenda_ReturnsObj_WithSingleGiftChanges_2atoms(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    sue_person.save_giftunit_file(sue_2atomunits_giftunit())
    # sue_person.save_giftunit_file(sue_3atomunits_giftunit())
    # sue_person.save_giftunit_file(sue_4atomunits_giftunit())
    gut_agenda = sue_person.get_gut_file_agenda()
    print(f"{gut_agenda._real_id=}")
    sports_text = "sports"
    sports_road = gut_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = gut_agenda.make_road(sports_road, knee_text)
    assert gut_agenda.idea_exists(sports_road) == False
    assert gut_agenda.idea_exists(knee_road) == False

    # WHEN
    new_agenda = sue_person._merge_gifts_into_agenda(gut_agenda)

    # THEN
    assert new_agenda != gut_agenda
    assert new_agenda.idea_exists(sports_road)
    assert new_agenda.idea_exists(knee_road)


def test_PersonUnit_append_gifts_to_gut_file_AddsGiftsToGutFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    sue_person.save_giftunit_file(sue_2atomunits_giftunit())
    gut_agenda = sue_person.get_gut_file_agenda()
    print(f"{gut_agenda._real_id=}")
    sports_text = "sports"
    sports_road = gut_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = gut_agenda.make_road(sports_road, knee_text)
    assert gut_agenda.idea_exists(sports_road) == False
    assert gut_agenda.idea_exists(knee_road) == False

    # WHEN
    new_agenda = sue_person.append_gifts_to_gut_file()

    # THEN
    assert new_agenda != gut_agenda
    assert new_agenda.idea_exists(sports_road)
    assert new_agenda.idea_exists(knee_road)


# def test_PersonUnit_build_agenda_ReturnsObjGivenBeginAgendaAndGiftRange(
#     reals_dir_setup_cleanup,
# ):
#     assert 1 == 2


# def test_PersonUnit_save_valid_atom_file_CorrectlySavesFile(reals_dir_setup_cleanup):
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


# def test_PersonUnit_atom_file_exists_ReturnsCorrectObj(reals_dir_setup_cleanup):
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


# def test_PersonUnit_delete_atom_file_CorrectlyDeletesFile(reals_dir_setup_cleanup):
#     # GIVEN
#     yao_person = personunit_shop("Yao")
#     ten_int = 10
#     yao_person._save_valid_atom_file(get_atom_example_beliefunit_knee(), ten_int)
#     assert os_path_exists(f"{yao_person._atoms_dir}/{ten_int}.json")

#     # WHEN
#     yao_person._delete_atom_file(ten_int)

#     # THEN
#     assert os_path_exists(f"{yao_person._atoms_dir}/{ten_int}.json") == False


# def test_PersonUnit_get_max_atom_file_number_ReturnsCorrectObj(reals_dir_setup_cleanup):
#     # GIVEN
#     yao_person = personunit_shop("Yao")
#     ten_int = 10
#     yao_person._save_valid_atom_file(get_atom_example_beliefunit_knee(), ten_int)
#     assert os_path_exists(f"{yao_person._atoms_dir}/{ten_int}.json")

#     # WHEN / THEN
#     assert yao_person._get_max_atom_file_number() == ten_int


# def test_PersonUnit_get_max_atom_file_number_ReturnsCorrectObjWhenDirIsEmpty(
#     reals_dir_setup_cleanup,
# ):
#     # GIVEN
#     yao_person = personunit_shop("Yao")

#     # WHEN / THEN
#     assert yao_person._get_max_atom_file_number() == 0


# def test_PersonUnit_get_next_atom_file_number_ReturnsCorrectObj(reals_dir_setup_cleanup):
#     # GIVEN
#     yao_person = personunit_shop("Yao")
#     ten_int = 10
#     yao_person._save_valid_atom_file(get_atom_example_beliefunit_knee(), ten_int)
#     assert os_path_exists(f"{yao_person._atoms_dir}/{ten_int}.json")

#     # WHEN / THEN
#     assert yao_person._get_next_atom_file_number() == "11.json"


# def test_PersonUnit_save_atom_file_CorrectlySavesFile(reals_dir_setup_cleanup):
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
#     reals_dir_setup_cleanup,
# ):
#     # GIVEN
#     yao_text = "Yao"
#     yao_person = personunit_shop(yao_text)

#     # WHEN
#     yao_agenda = yao_person._get_agenda_from_atom_files()

#     # THEN
#     assert yao_agenda._owner_id == yao_text
#     assert yao_agenda._real_id == yao_person.real_id
#     assert yao_agenda._road_delimiter == yao_person._road_delimiter
#     assert yao_agenda._planck == yao_person._planck


# def test_PersonUnit_get_agenda_from_atom_files_ReturnsCorrectFile_SimpleIdea(
#     reals_dir_setup_cleanup,
# ):
#     # GIVEN
#     yao_text = "Yao"
#     yao_person = personunit_shop(yao_text)
#     # save atom files
#     yao_person.save_atom_file(get_atom_example_ideaunit_sports(yao_person.real_id))

#     # WHEN
#     yao_agenda = yao_person._get_agenda_from_atom_files()

#     # THEN
#     assert yao_agenda._owner_id == yao_text
#     assert yao_agenda._real_id == yao_person.real_id
#     assert yao_agenda._road_delimiter == yao_person._road_delimiter
#     sports_text = "sports"
#     sports_road = yao_agenda.make_l1_road(sports_text)

#     assert yao_agenda.idea_exists(sports_road)


# def test_PersonUnit_get_agenda_from_atom_files_ReturnsCorrectFile_WithBeliefUnit(
#     reals_dir_setup_cleanup,
# ):
#     # GIVEN
#     yao_text = "Yao"
#     yao_person = personunit_shop(yao_text)
#     # save atom files
#     yao_person.save_atom_file(get_atom_example_ideaunit_sports(yao_person.real_id))
#     yao_person.save_atom_file(get_atom_example_ideaunit_ball(yao_person.real_id))
#     yao_person.save_atom_file(get_atom_example_ideaunit_knee(yao_person.real_id))
#     yao_person.save_atom_file(get_atom_example_beliefunit_knee(yao_person.real_id))

#     # WHEN
#     yao_agenda = yao_person._get_agenda_from_atom_files()

#     # THEN
#     assert yao_agenda._owner_id == yao_text
#     assert yao_agenda._real_id == yao_person.real_id
#     assert yao_agenda._road_delimiter == yao_person._road_delimiter
#     sports_text = "sports"
#     sports_road = yao_agenda.make_l1_road(sports_text)

#     assert yao_agenda.idea_exists(sports_road)


def test_PersonUnit_add_promise_gift_AddsPromiseGift(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    old_sue_gut = sue_person.get_gut_file_agenda()
    clean_text = "clean"
    clean_road = old_sue_gut.make_l1_road(clean_text)
    gift_filename = get_json_filename(1)
    sue_gift_path = f"{sue_person._gifts_dir}/{gift_filename}"
    print(f"{sue_gift_path=}")
    assert os_path_exists(sue_gift_path) == False
    old_sue_gut = sue_person.get_gut_file_agenda()
    assert old_sue_gut.idea_exists(clean_road) == False

    # WHEN
    sue_person.add_promise_gift(clean_road)

    # THEN
    assert os_path_exists(sue_gift_path)
    new_sue_gut = sue_person.get_gut_file_agenda()
    assert new_sue_gut.idea_exists(clean_road)


def test_PersonUnit_add_promise_gift_SetsGutAgendaPromiseIdea_suffgroup(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    old_sue_gut = sue_person.get_gut_file_agenda()
    clean_text = "clean"
    clean_road = old_sue_gut.make_l1_road(clean_text)
    assert old_sue_gut.idea_exists(clean_road) == False

    # WHEN
    bob_text = "Bob"
    sue_person.add_promise_gift(clean_road, x_suffgroup=bob_text)

    # THEN
    new_sue_gut = sue_person.get_gut_file_agenda()
    assert new_sue_gut.idea_exists(clean_road)
    clean_idea = new_sue_gut.get_idea_obj(clean_road)
    print(f"{clean_idea._assignedunit._suffgroups=}")
    assert clean_idea._assignedunit.suffgroup_exists(bob_text)
