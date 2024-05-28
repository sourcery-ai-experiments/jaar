from src._instrument.file import open_file, dir_files, delete_dir, set_dir
from src.real.change import changeunit_shop, get_json_filename, init_change_id
from src.real.examples.example_atoms import get_atom_example_ideaunit_knee
from src.real.examples.example_changes import (
    get_sue_changeunit,
    sue_1atomunits_changeunit,
    sue_2atomunits_changeunit,
    sue_3atomunits_changeunit,
    sue_4atomunits_changeunit,
)
from src.real.userdir import userdir_shop
from src.real.admin_duty import (
    initialize_change_duty_files,
    get_duty_file_agenda,
    append_changes_to_duty_file,
    add_pledge_change,
)
from src.real.admin_change import (
    changeunit_file_exists,
    _get_next_change_file_number,
    get_max_change_file_number,
    get_changeunit,
    _merge_changes_into_agenda,
    validate_changeunit,
    save_changeunit_file,
    _create_new_changeunit,
    create_save_changeunit,
    del_changeunit_file,
)
from src.real.examples.real_env_kit import reals_dir_setup_cleanup
from os.path import exists as os_path_exists
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy


def test_save_changeunit_file_SaveCorrectObj(reals_dir_setup_cleanup):
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    two_int = 2
    six_int = 6
    two_filename = get_json_filename(two_int)
    six_filename = get_json_filename(six_int)
    sue_change2_path = f"{sue_userdir._changes_dir}/{two_filename}"
    sue_change0_path = f"{sue_userdir._changes_dir}/{six_filename}"
    print(f"{sue_change2_path=}")
    print(f"{sue_change0_path=}")
    x_change_id = two_int
    sue_changeunit = changeunit_shop(
        _giver=sue_text,
        _change_id=x_change_id,
        _atoms_dir=sue_userdir._atoms_dir,
        _changes_dir=sue_userdir._changes_dir,
    )
    assert os_path_exists(sue_change2_path) == False
    assert os_path_exists(sue_change0_path) == False

    # WHEN
    save_changeunit_file(sue_userdir, sue_changeunit, correct_invalid_attrs=False)

    # THEN
    assert os_path_exists(sue_change2_path)
    assert os_path_exists(sue_change0_path) == False
    two_file_json = open_file(sue_userdir._changes_dir, two_filename)
    assert two_file_json == sue_changeunit.get_bookmetric_json()


def test_save_changeunit_file_RaisesErrorIfChangeUnit_atoms_dir_IsWrong(
    reals_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    x_change_id = 6
    six_filename = get_json_filename(x_change_id)
    sue_change0_path = f"{sue_userdir._changes_dir}/{six_filename}"
    print(f"{sue_change0_path=}")
    sue_changeunit = changeunit_shop(
        _giver=sue_text,
        _change_id=x_change_id,
        _atoms_dir="src/world",
        _changes_dir=sue_userdir._changes_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        save_changeunit_file(sue_userdir, sue_changeunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"ChangeUnit file cannot be saved because changeunit._atoms_dir is incorrect: {sue_changeunit._atoms_dir}. It must be {sue_userdir._atoms_dir}."
    )


def test_save_changeunit_file_RaisesErrorIfChangeUnit_changes_dir_IsWrong(
    reals_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    x_change_id = 6
    six_filename = get_json_filename(x_change_id)
    sue_change0_path = f"{sue_userdir._changes_dir}/{six_filename}"
    print(f"{sue_change0_path=}")
    sue_changeunit = changeunit_shop(
        _giver=sue_text,
        _change_id=x_change_id,
        _atoms_dir=sue_userdir._atoms_dir,
        _changes_dir="src/world",
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        save_changeunit_file(sue_userdir, sue_changeunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"ChangeUnit file cannot be saved because changeunit._changes_dir is incorrect: {sue_changeunit._changes_dir}. It must be {sue_userdir._changes_dir}."
    )


def test_changeunit_file_exists_ReturnsCorrectObj(reals_dir_setup_cleanup):
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    x_change_id = 2
    six_int = 6
    two_filename = get_json_filename(x_change_id)
    six_filename = get_json_filename(six_int)
    sue_change2_path = f"{sue_userdir._changes_dir}/{two_filename}"
    sue_change0_path = f"{sue_userdir._changes_dir}/{six_filename}"
    print(f"{sue_change2_path=}")
    sue_changeunit = changeunit_shop(
        _giver=sue_text,
        _change_id=x_change_id,
        _atoms_dir=sue_userdir._atoms_dir,
        _changes_dir=sue_userdir._changes_dir,
    )
    assert os_path_exists(sue_change2_path) == False
    assert os_path_exists(sue_change0_path) == False
    assert changeunit_file_exists(sue_userdir, x_change_id) == False
    assert changeunit_file_exists(sue_userdir, six_int) == False

    # WHEN
    save_changeunit_file(sue_userdir, sue_changeunit, correct_invalid_attrs=False)

    # THEN
    assert os_path_exists(sue_change2_path)
    assert os_path_exists(sue_change0_path) == False
    assert changeunit_file_exists(sue_userdir, x_change_id)
    assert changeunit_file_exists(sue_userdir, six_int) == False
    two_file_json = open_file(sue_userdir._changes_dir, two_filename)
    assert two_file_json == sue_changeunit.get_bookmetric_json()


def test_save_changeunit_file_RaisesErrorIfChangeUnit_giver_IsWrong(
    reals_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    x_change_id = 6
    six_filename = get_json_filename(x_change_id)
    sue_change0_path = f"{sue_userdir._changes_dir}/{six_filename}"
    print(f"{sue_change0_path=}")
    bob_text = "Bob"
    sue_changeunit = changeunit_shop(
        _giver=bob_text,
        _change_id=x_change_id,
        _atoms_dir=sue_userdir._atoms_dir,
        _changes_dir=sue_userdir._changes_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        save_changeunit_file(sue_userdir, sue_changeunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"ChangeUnit file cannot be saved because changeunit._giver is incorrect: {sue_changeunit._giver}. It must be {sue_text}."
    )


def test_save_changeunit_file_RaisesErrorIf_replace_IsFalse(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    initialize_change_duty_files(sue_userdir)
    x_change_id = 1
    six_filename = get_json_filename(x_change_id)
    sue_changeunit = changeunit_shop(
        _giver=sue_text,
        _change_id=x_change_id,
        _atoms_dir=sue_userdir._atoms_dir,
        _changes_dir=sue_userdir._changes_dir,
    )
    saved_changeunit = save_changeunit_file(sue_userdir, sue_changeunit)

    sue_change0_path = f"{sue_userdir._changes_dir}/{six_filename}"
    print(f"{sue_change0_path=}")
    assert os_path_exists(sue_change0_path)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        save_changeunit_file(
            sue_userdir, saved_changeunit, replace=False, correct_invalid_attrs=False
        )
    assert (
        str(excinfo.value)
        == f"ChangeUnit file {six_filename} already exists and cannot be saved over."
    )


def test_validate_changeunit_ReturnsObjWithAttributesFixed(
    reals_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    two_int = 2
    two_filename = get_json_filename(two_int)
    sue_change2_path = f"{sue_userdir._changes_dir}/{two_filename}"
    print(f"{sue_change2_path=}")

    # WHEN
    invalid_sue_changeunit = changeunit_shop(
        _giver="Bob",
        _change_id=_get_next_change_file_number(sue_userdir) - 5,
        _atoms_dir=f"{sue_userdir._econs_dir}/swimming",
        _changes_dir=f"{sue_userdir._econs_dir}/swimming",
    )
    valid_changeunit = validate_changeunit(sue_userdir, invalid_sue_changeunit)

    # THEN
    assert valid_changeunit._atoms_dir == sue_userdir._atoms_dir
    assert valid_changeunit._changes_dir == sue_userdir._changes_dir
    assert valid_changeunit._change_id == _get_next_change_file_number(sue_userdir)
    correct_sue_changeunit = changeunit_shop(
        _giver=sue_text,
        _change_id=_get_next_change_file_number(sue_userdir),
        _atoms_dir=sue_userdir._atoms_dir,
        _changes_dir=sue_userdir._changes_dir,
    )
    assert valid_changeunit == correct_sue_changeunit


def test_save_changeunit_file_SaveCorrectObj_correct_invalid_attrs_IsTrue(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    next_int = _get_next_change_file_number(sue_userdir)
    next_filename = get_json_filename(next_int)
    sue_change2_path = f"{sue_userdir._changes_dir}/{next_filename}"
    print(f"{sue_change2_path=}")
    assert os_path_exists(sue_change2_path) == False

    # WHEN
    invalid_sue_changeunit = changeunit_shop(
        _giver="Bob",
        _change_id=_get_next_change_file_number(sue_userdir) - 5,
        _atoms_dir=f"{sue_userdir._econs_dir}/swimming",
        _changes_dir=f"{sue_userdir._econs_dir}/swimming",
    )
    save_changeunit_file(sue_userdir, invalid_sue_changeunit)

    # THEN
    assert os_path_exists(sue_change2_path)
    two_file_json = open_file(sue_userdir._changes_dir, next_filename)


def test_get_max_change_file_number_ReturnsCorrectObj(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)

    # WHEN / THEN
    delete_dir(sue_userdir._changes_dir)
    assert get_max_change_file_number(sue_userdir) is None
    assert _get_next_change_file_number(sue_userdir) == init_change_id()
    assert _get_next_change_file_number(sue_userdir) == 0

    # GIVEN
    six_int = 6
    sue6_changeunit = changeunit_shop(
        _giver=sue_text,
        _change_id=six_int,
        _atoms_dir=sue_userdir._atoms_dir,
        _changes_dir=sue_userdir._changes_dir,
    )
    sue2_changeunit = changeunit_shop(
        _giver=sue_text,
        _change_id=2,
        _atoms_dir=sue_userdir._atoms_dir,
        _changes_dir=sue_userdir._changes_dir,
    )
    save_changeunit_file(sue_userdir, sue6_changeunit, correct_invalid_attrs=False)
    save_changeunit_file(sue_userdir, sue2_changeunit, correct_invalid_attrs=False)

    # WHEN / THEN
    assert get_max_change_file_number(sue_userdir) == six_int
    assert _get_next_change_file_number(sue_userdir) == 7


def test__create_new_changeunit_ReturnsObjWithCorrect_change_id_WhenNochangeFilesExist(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)

    # WHEN
    delete_dir(sue_userdir._changes_dir)
    sue_changeunit = _create_new_changeunit(sue_userdir)

    # THEN
    assert sue_changeunit._giver == sue_text
    assert sue_changeunit._change_id == init_change_id()
    assert sue_changeunit._change_id == 0
    assert sue_changeunit._change_id == _get_next_change_file_number(sue_userdir)
    assert sue_changeunit._faces == set()
    assert sue_changeunit._atoms_dir == sue_userdir._atoms_dir
    assert sue_changeunit._changes_dir == sue_userdir._changes_dir


def test__create_new_changeunit_ReturnsObjWithCorrect_change_id_WhenchangeFilesExist(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    delete_dir(sue_userdir._changes_dir)

    zero_changeunit = get_sue_changeunit()
    zero_changeunit._change_id = _get_next_change_file_number(sue_userdir)
    zero_changeunit._atoms_dir = sue_userdir._atoms_dir
    zero_changeunit._changes_dir = sue_userdir._changes_dir
    save_changeunit_file(sue_userdir, zero_changeunit)

    # WHEN
    sue_changeunit = _create_new_changeunit(sue_userdir)

    # THEN
    assert sue_changeunit._giver == sue_text
    assert sue_changeunit._change_id == init_change_id() + 1
    assert sue_changeunit._change_id == 1
    assert sue_changeunit._change_id == _get_next_change_file_number(sue_userdir)
    assert sue_changeunit._faces == set()
    assert sue_changeunit._atoms_dir == sue_userdir._atoms_dir
    assert sue_changeunit._changes_dir == sue_userdir._changes_dir


def test_get_changeunit_ReturnsCorrectObjWhenFilesDoesExist(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    yao_text = "yao"
    x0_changeunit = _create_new_changeunit(sue_userdir)
    x0_changeunit.set_face(yao_text)
    save_changeunit_file(sue_userdir, x0_changeunit)
    bob_text = "Bob"
    x1_changeunit = _create_new_changeunit(sue_userdir)
    x1_changeunit.set_face(bob_text)
    save_changeunit_file(sue_userdir, x1_changeunit)

    # WHEN
    y0_changeunit = get_changeunit(sue_userdir, x0_changeunit._change_id)
    y1_changeunit = get_changeunit(sue_userdir, x1_changeunit._change_id)

    # THEN
    assert y0_changeunit != None
    assert y1_changeunit != None
    assert yao_text in y0_changeunit._faces
    assert bob_text not in y0_changeunit._faces
    assert bob_text in y1_changeunit._faces


def test_get_changeunit_RaisesExceptionWhenFileDoesNotExist(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    yao_text = "yao"
    x0_changeunit = _create_new_changeunit(sue_userdir)
    x0_changeunit.set_face(yao_text)
    save_changeunit_file(sue_userdir, x0_changeunit)
    bob_text = "Bob"
    x1_changeunit = _create_new_changeunit(sue_userdir)
    x1_changeunit.set_face(bob_text)
    save_changeunit_file(sue_userdir, x1_changeunit)

    # WHEN / THEN
    six_file_number = 6
    with pytest_raises(Exception) as excinfo:
        get_changeunit(sue_userdir, six_file_number)
    assert (
        str(excinfo.value)
        == f"ChangeUnit file_number {six_file_number} does not exist."
    )


def test_del_changeunit_DeleteschangejsonAndNotAgendaAtomjsons(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    x_change_id = 6
    six_filename = get_json_filename(x_change_id)
    sue_changeunit = changeunit_shop(
        _giver=sue_text,
        _change_id=x_change_id,
        _atoms_dir=sue_userdir._atoms_dir,
        _changes_dir=sue_userdir._changes_dir,
    )
    sue_changeunit._bookunit.set_agendaatom(get_atom_example_ideaunit_knee())
    atom0_filename = sue_changeunit._get_num_filename(0)
    sue_change0_path = f"{sue_userdir._changes_dir}/{six_filename}"
    sue_atom0_path = f"{sue_userdir._atoms_dir}/{atom0_filename}"
    assert os_path_exists(sue_change0_path) == False
    assert os_path_exists(sue_atom0_path) == False

    sue_userdir = userdir_shop(None, None, sue_text)
    save_changeunit_file(sue_userdir, sue_changeunit, correct_invalid_attrs=False)

    print(f"{dir_files(sue_userdir._atoms_dir)}")
    assert os_path_exists(sue_change0_path)
    assert os_path_exists(sue_atom0_path)

    # WHEN
    del_changeunit_file(sue_userdir, sue_changeunit._change_id)

    # THEN
    assert os_path_exists(sue_change0_path) == False
    assert os_path_exists(sue_atom0_path)


def test_save_changeunit_file_CanCreateAndModify3changeunits(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    delete_dir(sue_userdir._changes_dir)
    delete_dir(sue_userdir._atoms_dir)
    set_dir(sue_userdir._changes_dir)
    set_dir(sue_userdir._atoms_dir)
    assert len(dir_files(sue_userdir._changes_dir)) == 0
    assert len(dir_files(sue_userdir._atoms_dir)) == 0

    # WHEN
    save_changeunit_file(sue_userdir, sue_2atomunits_changeunit())
    save_changeunit_file(sue_userdir, sue_3atomunits_changeunit())
    save_changeunit_file(sue_userdir, sue_4atomunits_changeunit())

    # THEN
    assert len(dir_files(sue_userdir._changes_dir)) == 3
    assert len(dir_files(sue_userdir._atoms_dir)) == 9


def test_save_changeunit_file_ReturnsValidObj(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    sue2_changeunit = sue_2atomunits_changeunit()
    sue2_changeunit._atoms_dir = f"{sue_userdir._econs_dir}/swimming"
    sue2_changeunit._changes_dir = f"{sue_userdir._econs_dir}/swimming"
    sue2_changeunit._giver = "Bob"
    sue2_changeunit._change_id = _get_next_change_file_number(sue_userdir) - 5
    prev_sue2_changeunit = copy_deepcopy(sue2_changeunit)

    # WHEN
    valid_changeunit = save_changeunit_file(sue_userdir, sue2_changeunit)

    # THEN
    assert valid_changeunit._changes_dir != prev_sue2_changeunit._changes_dir
    assert valid_changeunit._changes_dir == sue_userdir._changes_dir
    assert valid_changeunit._atoms_dir == sue_userdir._atoms_dir
    assert valid_changeunit._change_id != prev_sue2_changeunit._change_id


def test_create_save_changeunit_SaveCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    initialize_change_duty_files(sue_userdir)
    two_int = 2
    three_int = 3
    two_filename = get_json_filename(two_int)
    three_filename = get_json_filename(three_int)
    sue_change2_path = f"{sue_userdir._changes_dir}/{two_filename}"
    sue_change3_path = f"{sue_userdir._changes_dir}/{three_filename}"
    print(f"{sue_change2_path=}")
    print(f"{sue_change3_path=}")
    sue_changeunit = changeunit_shop(
        _giver=sue_text,
        _change_id=two_int,
        _atoms_dir=sue_userdir._atoms_dir,
        _changes_dir=sue_userdir._changes_dir,
    )
    sue_userdir = userdir_shop(None, None, sue_text)
    save_changeunit_file(sue_userdir, sue_changeunit, correct_invalid_attrs=False)
    assert os_path_exists(sue_change2_path)
    assert os_path_exists(sue_change3_path) == False

    # WHEN
    before_agenda = get_duty_file_agenda(sue_userdir)
    bob_text = "Bob"
    after_agenda = copy_deepcopy(before_agenda)
    after_agenda.add_partyunit(bob_text)
    create_save_changeunit(sue_userdir, before_agenda, after_agenda)

    # THEN
    assert os_path_exists(sue_change3_path)


def test_merge_changes_into_agenda_ReturnsSameObj(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    initialize_change_duty_files(sue_userdir)
    duty_agenda = get_duty_file_agenda(sue_userdir)
    duty_agenda._last_change_id is None

    # WHEN
    new_agenda = _merge_changes_into_agenda(sue_userdir, duty_agenda)

    # THEN
    assert new_agenda == duty_agenda


def test_merge_changes_into_agenda_ReturnsObj_WithSinglechangeModifys_1atom(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    initialize_change_duty_files(sue_userdir)
    save_changeunit_file(sue_userdir, sue_1atomunits_changeunit())
    # save_changeunit_file(sue_3atomunits_changeunit())
    # save_changeunit_file(sue_4atomunits_changeunit())
    duty_agenda = get_duty_file_agenda(sue_userdir)
    print(f"{duty_agenda._real_id=}")
    sports_text = "sports"
    sports_road = duty_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = duty_agenda.make_road(sports_road, knee_text)
    assert duty_agenda.idea_exists(sports_road) == False

    # WHEN
    new_agenda = _merge_changes_into_agenda(sue_userdir, duty_agenda)

    # THEN
    assert new_agenda != duty_agenda
    assert new_agenda.idea_exists(sports_road)


def test_merge_changes_into_agenda_ReturnsObj_WithSinglechangeModifys_2atoms(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    initialize_change_duty_files(sue_userdir)
    save_changeunit_file(sue_userdir, sue_2atomunits_changeunit())
    # save_changeunit_file(sue_3atomunits_changeunit())
    # save_changeunit_file(sue_4atomunits_changeunit())
    duty_agenda = get_duty_file_agenda(sue_userdir)
    print(f"{duty_agenda._real_id=}")
    sports_text = "sports"
    sports_road = duty_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = duty_agenda.make_road(sports_road, knee_text)
    assert duty_agenda.idea_exists(sports_road) == False
    assert duty_agenda.idea_exists(knee_road) == False

    # WHEN
    new_agenda = _merge_changes_into_agenda(sue_userdir, duty_agenda)

    # THEN
    assert new_agenda != duty_agenda
    assert new_agenda.idea_exists(sports_road)
    assert new_agenda.idea_exists(knee_road)


def test_append_changes_to_duty_file_AddschangesToDutyFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    initialize_change_duty_files(sue_userdir)
    save_changeunit_file(sue_userdir, sue_2atomunits_changeunit())
    duty_agenda = get_duty_file_agenda(sue_userdir)
    print(f"{duty_agenda._real_id=}")
    sports_text = "sports"
    sports_road = duty_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = duty_agenda.make_road(sports_road, knee_text)
    assert duty_agenda.idea_exists(sports_road) == False
    assert duty_agenda.idea_exists(knee_road) == False

    # WHEN
    new_agenda = append_changes_to_duty_file(sue_userdir)

    # THEN
    assert new_agenda != duty_agenda
    assert new_agenda.idea_exists(sports_road)
    assert new_agenda.idea_exists(knee_road)


def test_add_pledge_change_Addspledgechange(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    initialize_change_duty_files(sue_userdir)
    old_sue_duty = get_duty_file_agenda(sue_userdir)
    clean_text = "clean"
    clean_road = old_sue_duty.make_l1_road(clean_text)
    change_filename = get_json_filename(1)
    sue_change_path = f"{sue_userdir._changes_dir}/{change_filename}"
    print(f"{sue_change_path=}")
    assert os_path_exists(sue_change_path) == False
    old_sue_duty = get_duty_file_agenda(sue_userdir)
    assert old_sue_duty.idea_exists(clean_road) == False

    # WHEN
    add_pledge_change(sue_userdir, clean_road)

    # THEN
    assert os_path_exists(sue_change_path)
    new_sue_duty = get_duty_file_agenda(sue_userdir)
    assert new_sue_duty.idea_exists(clean_road)


def test_add_pledge_change_SetsDutyAgendapledgeIdea_suffgroup(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userdir = userdir_shop(None, None, sue_text)
    initialize_change_duty_files(sue_userdir)
    old_sue_duty = get_duty_file_agenda(sue_userdir)
    clean_text = "clean"
    clean_road = old_sue_duty.make_l1_road(clean_text)
    assert old_sue_duty.idea_exists(clean_road) == False

    # WHEN
    bob_text = "Bob"
    add_pledge_change(sue_userdir, clean_road, x_suffgroup=bob_text)

    # THEN
    new_sue_duty = get_duty_file_agenda(sue_userdir)
    assert new_sue_duty.idea_exists(clean_road)
    clean_idea = new_sue_duty.get_idea_obj(clean_road)
    print(f"{clean_idea._assignedunit._suffgroups=}")
    assert clean_idea._assignedunit.suffgroup_exists(bob_text)
