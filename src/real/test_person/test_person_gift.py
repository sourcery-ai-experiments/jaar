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
from src.real.person import (
    chap_create_core_dir_and_files,
    chapunit_shop,
    giftunit_file_exists,
    get_duty_file_agenda,
    _get_next_gift_file_number,
    get_max_gift_file_number,
    get_giftunit,
    _merge_gifts_into_agenda,
    append_gifts_to_duty_file,
    validate_giftunit,
    save_giftunit_file,
    _create_new_giftunit,
    create_save_giftunit,
    add_pledge_gift,
    del_giftunit_file,
)
from src.real.examples.real_env_kit import (
    get_test_reals_dir,
    get_test_real_id,
    reals_dir_setup_cleanup,
)
from src._instrument.file import open_file, dir_files, delete_dir, set_dir
from os.path import exists as os_path_exists
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy


def test_save_giftunit_file_SaveCorrectObj(reals_dir_setup_cleanup):
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    two_int = 2
    six_int = 6
    two_filename = get_json_filename(two_int)
    six_filename = get_json_filename(six_int)
    sue_gift2_path = f"{sue_chapunit._gifts_dir}/{two_filename}"
    sue_gift0_path = f"{sue_chapunit._gifts_dir}/{six_filename}"
    print(f"{sue_gift2_path=}")
    print(f"{sue_gift0_path=}")
    x_gift_id = two_int
    sue_giftunit = giftunit_shop(
        _giver=sue_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_chapunit._atoms_dir,
        _gifts_dir=sue_chapunit._gifts_dir,
    )
    assert os_path_exists(sue_gift2_path) == False
    assert os_path_exists(sue_gift0_path) == False

    # WHEN
    save_giftunit_file(sue_chapunit, sue_giftunit, change_invalid_attrs=False)

    # THEN
    assert os_path_exists(sue_gift2_path)
    assert os_path_exists(sue_gift0_path) == False
    two_file_json = open_file(sue_chapunit._gifts_dir, two_filename)
    assert two_file_json == sue_giftunit.get_bookmetric_json()


def test_save_giftunit_file_RaisesErrorIfGiftUnit_atoms_dir_IsWrong(
    reals_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_gift0_path = f"{sue_chapunit._gifts_dir}/{six_filename}"
    print(f"{sue_gift0_path=}")
    sue_giftunit = giftunit_shop(
        _giver=sue_text,
        _gift_id=x_gift_id,
        _atoms_dir="src/world",
        _gifts_dir=sue_chapunit._gifts_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        save_giftunit_file(sue_chapunit, sue_giftunit, change_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"GiftUnit file cannot be saved because giftunit._atoms_dir is incorrect: {sue_giftunit._atoms_dir}. It must be {sue_chapunit._atoms_dir}."
    )


def test_save_giftunit_file_RaisesErrorIfGiftUnit_gifts_dir_IsWrong(
    reals_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_gift0_path = f"{sue_chapunit._gifts_dir}/{six_filename}"
    print(f"{sue_gift0_path=}")
    sue_giftunit = giftunit_shop(
        _giver=sue_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_chapunit._atoms_dir,
        _gifts_dir="src/world",
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        save_giftunit_file(sue_chapunit, sue_giftunit, change_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"GiftUnit file cannot be saved because giftunit._gifts_dir is incorrect: {sue_giftunit._gifts_dir}. It must be {sue_chapunit._gifts_dir}."
    )


def test_giftunit_file_exists_ReturnsCorrectObj(reals_dir_setup_cleanup):
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    x_gift_id = 2
    six_int = 6
    two_filename = get_json_filename(x_gift_id)
    six_filename = get_json_filename(six_int)
    sue_gift2_path = f"{sue_chapunit._gifts_dir}/{two_filename}"
    sue_gift0_path = f"{sue_chapunit._gifts_dir}/{six_filename}"
    print(f"{sue_gift2_path=}")
    sue_giftunit = giftunit_shop(
        _giver=sue_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_chapunit._atoms_dir,
        _gifts_dir=sue_chapunit._gifts_dir,
    )
    assert os_path_exists(sue_gift2_path) == False
    assert os_path_exists(sue_gift0_path) == False
    assert giftunit_file_exists(sue_chapunit, x_gift_id) == False
    assert giftunit_file_exists(sue_chapunit, six_int) == False

    # WHEN
    save_giftunit_file(sue_chapunit, sue_giftunit, change_invalid_attrs=False)

    # THEN
    assert os_path_exists(sue_gift2_path)
    assert os_path_exists(sue_gift0_path) == False
    assert giftunit_file_exists(sue_chapunit, x_gift_id)
    assert giftunit_file_exists(sue_chapunit, six_int) == False
    two_file_json = open_file(sue_chapunit._gifts_dir, two_filename)
    assert two_file_json == sue_giftunit.get_bookmetric_json()


def test_save_giftunit_file_RaisesErrorIfGiftUnit_giver_IsWrong(
    reals_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_gift0_path = f"{sue_chapunit._gifts_dir}/{six_filename}"
    print(f"{sue_gift0_path=}")
    bob_text = "Bob"
    sue_giftunit = giftunit_shop(
        _giver=bob_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_chapunit._atoms_dir,
        _gifts_dir=sue_chapunit._gifts_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        save_giftunit_file(sue_chapunit, sue_giftunit, change_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"GiftUnit file cannot be saved because giftunit._giver is incorrect: {sue_giftunit._giver}. It must be {sue_text}."
    )


def test_save_giftunit_file_RaisesErrorIf_replace_IsFalse(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    chap_create_core_dir_and_files(sue_chapunit)
    x_gift_id = 1
    six_filename = get_json_filename(x_gift_id)
    sue_giftunit = giftunit_shop(
        _giver=sue_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_chapunit._atoms_dir,
        _gifts_dir=sue_chapunit._gifts_dir,
    )
    saved_giftunit = save_giftunit_file(sue_chapunit, sue_giftunit)

    sue_gift0_path = f"{sue_chapunit._gifts_dir}/{six_filename}"
    print(f"{sue_gift0_path=}")
    assert os_path_exists(sue_gift0_path)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        save_giftunit_file(
            sue_chapunit, saved_giftunit, replace=False, change_invalid_attrs=False
        )
    assert (
        str(excinfo.value)
        == f"GiftUnit file {six_filename} already exists and cannot be saved over."
    )


def test_validate_giftunit_ReturnsObjWithAttributesFixed(
    reals_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    two_int = 2
    two_filename = get_json_filename(two_int)
    sue_gift2_path = f"{sue_chapunit._gifts_dir}/{two_filename}"
    print(f"{sue_gift2_path=}")

    # WHEN
    invalid_sue_giftunit = giftunit_shop(
        _giver="Bob",
        _gift_id=_get_next_gift_file_number(sue_chapunit) - 5,
        _atoms_dir=f"{sue_chapunit._econs_dir}/swimming",
        _gifts_dir=f"{sue_chapunit._econs_dir}/swimming",
    )
    valid_giftunit = validate_giftunit(sue_chapunit, invalid_sue_giftunit)

    # THEN
    assert valid_giftunit._atoms_dir == sue_chapunit._atoms_dir
    assert valid_giftunit._gifts_dir == sue_chapunit._gifts_dir
    assert valid_giftunit._gift_id == _get_next_gift_file_number(sue_chapunit)
    correct_sue_giftunit = giftunit_shop(
        _giver=sue_text,
        _gift_id=_get_next_gift_file_number(sue_chapunit),
        _atoms_dir=sue_chapunit._atoms_dir,
        _gifts_dir=sue_chapunit._gifts_dir,
    )
    assert valid_giftunit == correct_sue_giftunit


def test_save_giftunit_file_SaveCorrectObj_change_invalid_attrs_IsTrue(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    next_int = _get_next_gift_file_number(sue_chapunit)
    next_filename = get_json_filename(next_int)
    sue_gift2_path = f"{sue_chapunit._gifts_dir}/{next_filename}"
    print(f"{sue_gift2_path=}")
    assert os_path_exists(sue_gift2_path) == False

    # WHEN
    invalid_sue_giftunit = giftunit_shop(
        _giver="Bob",
        _gift_id=_get_next_gift_file_number(sue_chapunit) - 5,
        _atoms_dir=f"{sue_chapunit._econs_dir}/swimming",
        _gifts_dir=f"{sue_chapunit._econs_dir}/swimming",
    )
    save_giftunit_file(sue_chapunit, invalid_sue_giftunit)

    # THEN
    assert os_path_exists(sue_gift2_path)
    two_file_json = open_file(sue_chapunit._gifts_dir, next_filename)


def test_get_max_gift_file_number_ReturnsCorrectObj(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)

    # WHEN / THEN
    delete_dir(sue_chapunit._gifts_dir)
    assert get_max_gift_file_number(sue_chapunit) is None
    assert _get_next_gift_file_number(sue_chapunit) == init_gift_id()
    assert _get_next_gift_file_number(sue_chapunit) == 0

    # GIVEN
    six_int = 6
    sue6_giftunit = giftunit_shop(
        _giver=sue_text,
        _gift_id=six_int,
        _atoms_dir=sue_chapunit._atoms_dir,
        _gifts_dir=sue_chapunit._gifts_dir,
    )
    sue2_giftunit = giftunit_shop(
        _giver=sue_text,
        _gift_id=2,
        _atoms_dir=sue_chapunit._atoms_dir,
        _gifts_dir=sue_chapunit._gifts_dir,
    )
    save_giftunit_file(sue_chapunit, sue6_giftunit, change_invalid_attrs=False)
    save_giftunit_file(sue_chapunit, sue2_giftunit, change_invalid_attrs=False)

    # WHEN / THEN
    assert get_max_gift_file_number(sue_chapunit) == six_int
    assert _get_next_gift_file_number(sue_chapunit) == 7


def test__create_new_giftunit_ReturnsObjWithCorrect_gift_id_WhenNoGiftFilesExist(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)

    # WHEN
    delete_dir(sue_chapunit._gifts_dir)
    sue_giftunit = _create_new_giftunit(sue_chapunit)

    # THEN
    assert sue_giftunit._giver == sue_text
    assert sue_giftunit._gift_id == init_gift_id()
    assert sue_giftunit._gift_id == 0
    assert sue_giftunit._gift_id == _get_next_gift_file_number(sue_chapunit)
    assert sue_giftunit._takers == set()
    assert sue_giftunit._atoms_dir == sue_chapunit._atoms_dir
    assert sue_giftunit._gifts_dir == sue_chapunit._gifts_dir


def test__create_new_giftunit_ReturnsObjWithCorrect_gift_id_WhenGiftFilesExist(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    delete_dir(sue_chapunit._gifts_dir)

    zero_giftunit = get_sue_giftunit()
    zero_giftunit._gift_id = _get_next_gift_file_number(sue_chapunit)
    zero_giftunit._atoms_dir = sue_chapunit._atoms_dir
    zero_giftunit._gifts_dir = sue_chapunit._gifts_dir
    save_giftunit_file(sue_chapunit, zero_giftunit)

    # WHEN
    sue_giftunit = _create_new_giftunit(sue_chapunit)

    # THEN
    assert sue_giftunit._giver == sue_text
    assert sue_giftunit._gift_id == init_gift_id() + 1
    assert sue_giftunit._gift_id == 1
    assert sue_giftunit._gift_id == _get_next_gift_file_number(sue_chapunit)
    assert sue_giftunit._takers == set()
    assert sue_giftunit._atoms_dir == sue_chapunit._atoms_dir
    assert sue_giftunit._gifts_dir == sue_chapunit._gifts_dir


def test_get_giftunit_ReturnsCorrectObjWhenFilesDoesExist(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    yao_text = "yao"
    x0_giftunit = _create_new_giftunit(sue_chapunit)
    x0_giftunit.set_taker(yao_text)
    save_giftunit_file(sue_chapunit, x0_giftunit)
    bob_text = "Bob"
    x1_giftunit = _create_new_giftunit(sue_chapunit)
    x1_giftunit.set_taker(bob_text)
    save_giftunit_file(sue_chapunit, x1_giftunit)

    # WHEN
    y0_giftunit = get_giftunit(sue_chapunit, x0_giftunit._gift_id)
    y1_giftunit = get_giftunit(sue_chapunit, x1_giftunit._gift_id)

    # THEN
    assert y0_giftunit != None
    assert y1_giftunit != None
    assert yao_text in y0_giftunit._takers
    assert bob_text not in y0_giftunit._takers
    assert bob_text in y1_giftunit._takers


def test_get_giftunit_RaisesExceptionWhenFileDoesNotExist(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    yao_text = "yao"
    x0_giftunit = _create_new_giftunit(sue_chapunit)
    x0_giftunit.set_taker(yao_text)
    save_giftunit_file(sue_chapunit, x0_giftunit)
    bob_text = "Bob"
    x1_giftunit = _create_new_giftunit(sue_chapunit)
    x1_giftunit.set_taker(bob_text)
    save_giftunit_file(sue_chapunit, x1_giftunit)

    # WHEN / THEN
    six_file_number = 6
    with pytest_raises(Exception) as excinfo:
        get_giftunit(sue_chapunit, six_file_number)
    assert (
        str(excinfo.value) == f"GiftUnit file_number {six_file_number} does not exist."
    )


def test_del_giftunit_DeletesGiftjsonAndNotAgendaAtomjsons(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_giftunit = giftunit_shop(
        _giver=sue_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_chapunit._atoms_dir,
        _gifts_dir=sue_chapunit._gifts_dir,
    )
    sue_giftunit._bookunit.set_agendaatom(get_atom_example_ideaunit_knee())
    atom0_filename = sue_giftunit._get_num_filename(0)
    sue_gift0_path = f"{sue_chapunit._gifts_dir}/{six_filename}"
    sue_atom0_path = f"{sue_chapunit._atoms_dir}/{atom0_filename}"
    assert os_path_exists(sue_gift0_path) == False
    assert os_path_exists(sue_atom0_path) == False

    sue_chapunit = chapunit_shop(None, None, sue_text)
    save_giftunit_file(sue_chapunit, sue_giftunit, change_invalid_attrs=False)

    print(f"{dir_files(sue_chapunit._atoms_dir)}")
    assert os_path_exists(sue_gift0_path)
    assert os_path_exists(sue_atom0_path)

    # WHEN
    del_giftunit_file(sue_chapunit, sue_giftunit._gift_id)

    # THEN
    assert os_path_exists(sue_gift0_path) == False
    assert os_path_exists(sue_atom0_path)


def test_save_giftunit_file_CanCreateAndChange3Giftunits(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    delete_dir(sue_chapunit._gifts_dir)
    delete_dir(sue_chapunit._atoms_dir)
    set_dir(sue_chapunit._gifts_dir)
    set_dir(sue_chapunit._atoms_dir)
    assert len(dir_files(sue_chapunit._gifts_dir)) == 0
    assert len(dir_files(sue_chapunit._atoms_dir)) == 0

    # WHEN
    save_giftunit_file(sue_chapunit, sue_2atomunits_giftunit())
    save_giftunit_file(sue_chapunit, sue_3atomunits_giftunit())
    save_giftunit_file(sue_chapunit, sue_4atomunits_giftunit())

    # THEN
    assert len(dir_files(sue_chapunit._gifts_dir)) == 3
    assert len(dir_files(sue_chapunit._atoms_dir)) == 9


def test_save_giftunit_file_ReturnsValidObj(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    sue2_giftunit = sue_2atomunits_giftunit()
    sue2_giftunit._atoms_dir = f"{sue_chapunit._econs_dir}/swimming"
    sue2_giftunit._gifts_dir = f"{sue_chapunit._econs_dir}/swimming"
    sue2_giftunit._giver = "Bob"
    sue2_giftunit._gift_id = _get_next_gift_file_number(sue_chapunit) - 5
    prev_sue2_giftunit = copy_deepcopy(sue2_giftunit)

    # WHEN
    valid_giftunit = save_giftunit_file(sue_chapunit, sue2_giftunit)

    # THEN
    assert valid_giftunit._gifts_dir != prev_sue2_giftunit._gifts_dir
    assert valid_giftunit._gifts_dir == sue_chapunit._gifts_dir
    assert valid_giftunit._atoms_dir == sue_chapunit._atoms_dir
    assert valid_giftunit._gift_id != prev_sue2_giftunit._gift_id


def test_create_save_giftunit_SaveCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    chap_create_core_dir_and_files(sue_chapunit)
    two_int = 2
    three_int = 3
    two_filename = get_json_filename(two_int)
    three_filename = get_json_filename(three_int)
    sue_gift2_path = f"{sue_chapunit._gifts_dir}/{two_filename}"
    sue_gift3_path = f"{sue_chapunit._gifts_dir}/{three_filename}"
    print(f"{sue_gift2_path=}")
    print(f"{sue_gift3_path=}")
    sue_giftunit = giftunit_shop(
        _giver=sue_text,
        _gift_id=two_int,
        _atoms_dir=sue_chapunit._atoms_dir,
        _gifts_dir=sue_chapunit._gifts_dir,
    )
    sue_chapunit = chapunit_shop(None, None, sue_text)
    save_giftunit_file(sue_chapunit, sue_giftunit, change_invalid_attrs=False)
    assert os_path_exists(sue_gift2_path)
    assert os_path_exists(sue_gift3_path) == False

    # WHEN
    before_agenda = get_duty_file_agenda(sue_chapunit)
    bob_text = "Bob"
    after_agenda = copy_deepcopy(before_agenda)
    after_agenda.add_partyunit(bob_text)
    create_save_giftunit(sue_chapunit, before_agenda, after_agenda)

    # THEN
    assert os_path_exists(sue_gift3_path)


def test_merge_gifts_into_agenda_ReturnsObj_NoChange(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    chap_create_core_dir_and_files(sue_chapunit)
    duty_agenda = get_duty_file_agenda(sue_chapunit)
    duty_agenda._last_gift_id is None

    # WHEN
    new_agenda = _merge_gifts_into_agenda(sue_chapunit, duty_agenda)

    # THEN
    assert new_agenda == duty_agenda


def test_merge_gifts_into_agenda_ReturnsObj_WithSingleGiftChanges_1atom(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    chap_create_core_dir_and_files(sue_chapunit)
    save_giftunit_file(sue_chapunit, sue_1atomunits_giftunit())
    # save_giftunit_file(sue_3atomunits_giftunit())
    # save_giftunit_file(sue_4atomunits_giftunit())
    duty_agenda = get_duty_file_agenda(sue_chapunit)
    print(f"{duty_agenda._real_id=}")
    sports_text = "sports"
    sports_road = duty_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = duty_agenda.make_road(sports_road, knee_text)
    assert duty_agenda.idea_exists(sports_road) == False

    # WHEN
    new_agenda = _merge_gifts_into_agenda(sue_chapunit, duty_agenda)

    # THEN
    assert new_agenda != duty_agenda
    assert new_agenda.idea_exists(sports_road)


def test_merge_gifts_into_agenda_ReturnsObj_WithSingleGiftChanges_2atoms(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    chap_create_core_dir_and_files(sue_chapunit)
    save_giftunit_file(sue_chapunit, sue_2atomunits_giftunit())
    # save_giftunit_file(sue_3atomunits_giftunit())
    # save_giftunit_file(sue_4atomunits_giftunit())
    duty_agenda = get_duty_file_agenda(sue_chapunit)
    print(f"{duty_agenda._real_id=}")
    sports_text = "sports"
    sports_road = duty_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = duty_agenda.make_road(sports_road, knee_text)
    assert duty_agenda.idea_exists(sports_road) == False
    assert duty_agenda.idea_exists(knee_road) == False

    # WHEN
    new_agenda = _merge_gifts_into_agenda(sue_chapunit, duty_agenda)

    # THEN
    assert new_agenda != duty_agenda
    assert new_agenda.idea_exists(sports_road)
    assert new_agenda.idea_exists(knee_road)


def test_append_gifts_to_duty_file_AddsGiftsToDutyFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    chap_create_core_dir_and_files(sue_chapunit)
    save_giftunit_file(sue_chapunit, sue_2atomunits_giftunit())
    duty_agenda = get_duty_file_agenda(sue_chapunit)
    print(f"{duty_agenda._real_id=}")
    sports_text = "sports"
    sports_road = duty_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = duty_agenda.make_road(sports_road, knee_text)
    assert duty_agenda.idea_exists(sports_road) == False
    assert duty_agenda.idea_exists(knee_road) == False

    # WHEN
    new_agenda = append_gifts_to_duty_file(sue_chapunit)

    # THEN
    assert new_agenda != duty_agenda
    assert new_agenda.idea_exists(sports_road)
    assert new_agenda.idea_exists(knee_road)


def test_add_pledge_gift_AddspledgeGift(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    chap_create_core_dir_and_files(sue_chapunit)
    old_sue_duty = get_duty_file_agenda(sue_chapunit)
    clean_text = "clean"
    clean_road = old_sue_duty.make_l1_road(clean_text)
    gift_filename = get_json_filename(1)
    sue_gift_path = f"{sue_chapunit._gifts_dir}/{gift_filename}"
    print(f"{sue_gift_path=}")
    assert os_path_exists(sue_gift_path) == False
    old_sue_duty = get_duty_file_agenda(sue_chapunit)
    assert old_sue_duty.idea_exists(clean_road) == False

    # WHEN
    add_pledge_gift(sue_chapunit, clean_road)

    # THEN
    assert os_path_exists(sue_gift_path)
    new_sue_duty = get_duty_file_agenda(sue_chapunit)
    assert new_sue_duty.idea_exists(clean_road)


def test_add_pledge_gift_SetsDutyAgendapledgeIdea_suffgroup(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_chapunit = chapunit_shop(None, None, sue_text)
    chap_create_core_dir_and_files(sue_chapunit)
    old_sue_duty = get_duty_file_agenda(sue_chapunit)
    clean_text = "clean"
    clean_road = old_sue_duty.make_l1_road(clean_text)
    assert old_sue_duty.idea_exists(clean_road) == False

    # WHEN
    bob_text = "Bob"
    add_pledge_gift(sue_chapunit, clean_road, x_suffgroup=bob_text)

    # THEN
    new_sue_duty = get_duty_file_agenda(sue_chapunit)
    assert new_sue_duty.idea_exists(clean_road)
    clean_idea = new_sue_duty.get_idea_obj(clean_road)
    print(f"{clean_idea._assignedunit._suffgroups=}")
    assert clean_idea._assignedunit.suffgroup_exists(bob_text)
