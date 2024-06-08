from src._instrument.file import open_file, dir_files, delete_dir, set_dir, save_file
from src._road.jaar_config import init_change_id
from src._road.road import get_default_real_id_roadnode as root_label
from src.change.change import changeunit_shop, get_json_filename
from src.change.filehub import filehub_shop
from src.change.examples.example_change_atoms import get_atom_example_ideaunit_knee
from src.change.examples.example_change_changes import (
    get_sue_changeunit,
    sue_1atomunits_changeunit,
    sue_2atomunits_changeunit,
    sue_3atomunits_changeunit,
    sue_4atomunits_changeunit,
)
from src.change.examples.change_env import (
    env_dir_setup_cleanup,
    get_change_temp_env_dir as env_dir,
)
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy


def test_FileHub_get_max_change_file_number_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)

    # WHEN / THEN
    delete_dir(sue_filehub.changes_dir())
    assert sue_filehub.get_max_change_file_number() is None
    assert sue_filehub._get_next_change_file_number() == init_change_id()
    assert sue_filehub._get_next_change_file_number() == 0

    # GIVEN
    six_int = 6
    save_file(sue_filehub.changes_dir(), sue_filehub.change_file_name(six_int), "x")

    # WHEN / THEN
    assert sue_filehub.get_max_change_file_number() == six_int
    assert sue_filehub._get_next_change_file_number() == 7


def test_FileHub_change_file_exists_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    assert sue_filehub.change_file_exists(None) == False
    assert sue_filehub.change_file_exists(0) == False
    six_int = 6
    print(f"{sue_filehub.change_file_path(six_int)=}")
    assert sue_filehub.change_file_exists(six_int) == False

    # WHEN
    save_file(sue_filehub.changes_dir(), sue_filehub.change_file_name(six_int), "x")

    # THEN
    assert sue_filehub.change_file_exists(None) == False
    assert sue_filehub.change_file_exists(0) == False
    assert sue_filehub.change_file_exists(six_int)


def test_FileHub_save_change_file_SaveCorrectObj(env_dir_setup_cleanup):
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    two_int = 2
    six_int = 6
    two_filename = get_json_filename(two_int)
    six_filename = get_json_filename(six_int)
    sue_change2_path = f"{sue_filehub.changes_dir()}/{two_filename}"
    sue_change0_path = f"{sue_filehub.changes_dir()}/{six_filename}"
    print(f"{sue_change2_path=}")
    print(f"{sue_change0_path=}")
    sue_changeunit = changeunit_shop(
        _giver=sue_text,
        _change_id=two_int,
        _atoms_dir=sue_filehub.atoms_dir(),
        _changes_dir=sue_filehub.changes_dir(),
    )
    assert sue_filehub.change_file_exists(two_int) == False
    assert sue_filehub.change_file_exists(six_int) == False

    # WHEN
    sue_filehub.save_change_file(sue_changeunit, correct_invalid_attrs=False)

    # THEN
    assert sue_filehub.change_file_exists(two_int)
    assert sue_filehub.change_file_exists(six_int) == False
    two_file_json = open_file(sue_filehub.changes_dir(), two_filename)
    assert two_file_json == sue_changeunit.get_bookmetric_json()


def test_FileHub_save_change_file_RaisesErrorIfChangeUnit_atoms_dir_IsWrong(
    env_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    x_change_id = 6
    six_filename = get_json_filename(x_change_id)
    sue_change0_path = f"{sue_filehub.changes_dir()}/{six_filename}"
    print(f"{sue_change0_path=}")
    sue_changeunit = changeunit_shop(
        _giver=sue_text,
        _change_id=x_change_id,
        _atoms_dir="src/world",
        _changes_dir=sue_filehub.changes_dir(),
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_filehub.save_change_file(sue_changeunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"ChangeUnit file cannot be saved because changeunit._atoms_dir is incorrect: {sue_changeunit._atoms_dir}. It must be {sue_filehub.atoms_dir()}."
    )


def test_FileHub_save_change_file_RaisesErrorIfChangeUnit_changes_dir_IsWrong(
    env_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    x_change_id = 6
    six_filename = get_json_filename(x_change_id)
    sue_change0_path = f"{sue_filehub.changes_dir()}/{six_filename}"
    print(f"{sue_change0_path=}")
    sue_changeunit = changeunit_shop(
        _giver=sue_text,
        _change_id=x_change_id,
        _atoms_dir=sue_filehub.atoms_dir(),
        _changes_dir="src/world",
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_filehub.save_change_file(sue_changeunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"ChangeUnit file cannot be saved because changeunit._changes_dir is incorrect: {sue_changeunit._changes_dir}. It must be {sue_filehub.changes_dir()}."
    )


def test_FileHub_save_change_file_RaisesErrorIfChangeUnit_giver_IsWrong(
    env_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    x_change_id = 6
    six_filename = get_json_filename(x_change_id)
    sue_change0_path = f"{sue_filehub.changes_dir()}/{six_filename}"
    print(f"{sue_change0_path=}")
    bob_text = "Bob"
    sue_changeunit = changeunit_shop(
        _giver=bob_text,
        _change_id=x_change_id,
        _atoms_dir=sue_filehub.atoms_dir(),
        _changes_dir=sue_filehub.changes_dir(),
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_filehub.save_change_file(sue_changeunit, correct_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"ChangeUnit file cannot be saved because changeunit._giver is incorrect: {sue_changeunit._giver}. It must be {sue_text}."
    )


def test_FileHub_save_change_file_RaisesErrorIf_replace_IsFalse(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    x_change_id = 0
    six_filename = get_json_filename(x_change_id)
    sue_changeunit = changeunit_shop(
        _giver=sue_text,
        _change_id=x_change_id,
        _atoms_dir=sue_filehub.atoms_dir(),
        _changes_dir=sue_filehub.changes_dir(),
    )
    saved_changeunit = sue_filehub.save_change_file(sue_changeunit)

    print(f"{sue_filehub.change_file_path(x_change_id)=}")
    assert sue_filehub.change_file_exists(x_change_id)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_filehub.save_change_file(
            saved_changeunit, replace=False, correct_invalid_attrs=False
        )
    assert (
        str(excinfo.value)
        == f"ChangeUnit file {six_filename} already exists and cannot be saved over."
    )


def test_FileHub_validate_changeunit_ReturnsObjWithAttributesFixed(
    env_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    two_int = 2
    two_filename = get_json_filename(two_int)
    sue_change2_path = f"{sue_filehub.changes_dir()}/{two_filename}"
    print(f"{sue_change2_path=}")

    # WHEN
    invalid_sue_changeunit = changeunit_shop(
        _giver="Bob",
        _change_id=sue_filehub._get_next_change_file_number() - 5,
        _atoms_dir=f"{sue_filehub.econs_dir()}/swimming",
        _changes_dir=f"{sue_filehub.econs_dir()}/swimming",
    )
    valid_changeunit = sue_filehub.validate_changeunit(invalid_sue_changeunit)

    # THEN
    assert valid_changeunit._atoms_dir == sue_filehub.atoms_dir()
    assert valid_changeunit._changes_dir == sue_filehub.changes_dir()
    assert valid_changeunit._change_id == sue_filehub._get_next_change_file_number()
    correct_sue_changeunit = changeunit_shop(
        _giver=sue_text,
        _change_id=sue_filehub._get_next_change_file_number(),
        _atoms_dir=sue_filehub.atoms_dir(),
        _changes_dir=sue_filehub.changes_dir(),
    )
    assert valid_changeunit == correct_sue_changeunit


def test_FileHub_save_change_file_SaveCorrectObj_correct_invalid_attrs_IsTrue(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    next_int = sue_filehub._get_next_change_file_number()
    next_filename = get_json_filename(next_int)
    sue_change2_path = f"{sue_filehub.changes_dir()}/{next_filename}"
    print(f"{sue_change2_path=}")
    assert sue_filehub.change_file_exists(next_int) == False

    # WHEN
    invalid_sue_changeunit = changeunit_shop(
        _giver="Bob",
        _change_id=sue_filehub._get_next_change_file_number() - 5,
        _atoms_dir=f"{sue_filehub.econs_dir()}/swimming",
        _changes_dir=f"{sue_filehub.econs_dir()}/swimming",
    )
    sue_filehub.save_change_file(invalid_sue_changeunit)

    # THEN
    assert sue_filehub.change_file_exists(next_int)
    two_file_json = open_file(sue_filehub.changes_dir(), next_filename)


def test_FileHub_create_new_changeunit_ReturnsObjWithCorrect_change_id_WhenNochangeFilesExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)

    # WHEN
    delete_dir(sue_filehub.changes_dir())
    sue_changeunit = sue_filehub._create_new_changeunit()

    # THEN
    assert sue_changeunit._giver == sue_text
    assert sue_changeunit._change_id == init_change_id()
    assert sue_changeunit._change_id == 0
    assert sue_changeunit._change_id == sue_filehub._get_next_change_file_number()
    assert sue_changeunit._faces == set()
    assert sue_changeunit._atoms_dir == sue_filehub.atoms_dir()
    assert sue_changeunit._changes_dir == sue_filehub.changes_dir()


def test_FileHub_create_new_changeunit_ReturnsObjWithCorrect_change_id_WhenchangeFilesExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    delete_dir(sue_filehub.changes_dir())

    zero_changeunit = get_sue_changeunit()
    zero_changeunit._change_id = sue_filehub._get_next_change_file_number()
    zero_changeunit._atoms_dir = sue_filehub.atoms_dir()
    zero_changeunit._changes_dir = sue_filehub.changes_dir()
    sue_filehub.save_change_file(zero_changeunit)

    # WHEN
    sue_changeunit = sue_filehub._create_new_changeunit()

    # THEN
    assert sue_changeunit._giver == sue_text
    assert sue_changeunit._change_id == init_change_id() + 1
    assert sue_changeunit._change_id == 1
    assert sue_changeunit._change_id == sue_filehub._get_next_change_file_number()
    assert sue_changeunit._faces == set()
    assert sue_changeunit._atoms_dir == sue_filehub.atoms_dir()
    assert sue_changeunit._changes_dir == sue_filehub.changes_dir()


def test_FileHub_get_changeunit_ReturnsCorrectObjWhenFilesDoesExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    yao_text = "yao"
    x0_changeunit = sue_filehub._create_new_changeunit()
    x0_changeunit.set_face(yao_text)
    sue_filehub.save_change_file(x0_changeunit)
    bob_text = "Bob"
    x1_changeunit = sue_filehub._create_new_changeunit()
    x1_changeunit.set_face(bob_text)
    sue_filehub.save_change_file(x1_changeunit)

    # WHEN
    y0_changeunit = sue_filehub.get_changeunit(x0_changeunit._change_id)
    y1_changeunit = sue_filehub.get_changeunit(x1_changeunit._change_id)

    # THEN
    assert y0_changeunit != None
    assert y1_changeunit != None
    assert yao_text in y0_changeunit._faces
    assert bob_text not in y0_changeunit._faces
    assert bob_text in y1_changeunit._faces


def test_FileHub_get_changeunit_RaisesExceptionWhenFileDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    yao_text = "yao"
    x0_changeunit = sue_filehub._create_new_changeunit()
    x0_changeunit.set_face(yao_text)
    sue_filehub.save_change_file(x0_changeunit)
    bob_text = "Bob"
    x1_changeunit = sue_filehub._create_new_changeunit()
    x1_changeunit.set_face(bob_text)
    sue_filehub.save_change_file(x1_changeunit)

    # WHEN / THEN
    six_file_number = 6
    with pytest_raises(Exception) as excinfo:
        sue_filehub.get_changeunit(six_file_number)
    assert (
        str(excinfo.value)
        == f"ChangeUnit file_number {six_file_number} does not exist."
    )


def test_FileHub_del_change_file_DeleteschangejsonAndNotAgendaAtomjsons(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    six_int = 6
    sue_changeunit = changeunit_shop(
        _giver=sue_text,
        _change_id=six_int,
        _atoms_dir=sue_filehub.atoms_dir(),
        _changes_dir=sue_filehub.changes_dir(),
    )
    sue_changeunit._bookunit.set_agendaatom(get_atom_example_ideaunit_knee())
    zero_int = 0
    assert sue_filehub.change_file_exists(six_int) == False
    assert sue_filehub.atom_file_exists(zero_int) == False

    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    sue_filehub.save_change_file(sue_changeunit, correct_invalid_attrs=False)

    print(f"{dir_files(sue_filehub.atoms_dir())}")
    assert sue_filehub.change_file_exists(six_int)
    assert sue_filehub.atom_file_exists(zero_int)

    # WHEN
    sue_filehub._del_change_file(sue_changeunit._change_id)

    # THEN
    assert sue_filehub.change_file_exists(six_int) == False
    assert sue_filehub.atom_file_exists(zero_int)


def test_FileHub_save_change_file_CanCreateAndModify3changeunits(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    delete_dir(sue_filehub.changes_dir())
    delete_dir(sue_filehub.atoms_dir())
    set_dir(sue_filehub.changes_dir())
    set_dir(sue_filehub.atoms_dir())
    assert len(dir_files(sue_filehub.changes_dir())) == 0
    assert len(dir_files(sue_filehub.atoms_dir())) == 0

    # WHEN
    sue_filehub.save_change_file(sue_2atomunits_changeunit())
    sue_filehub.save_change_file(sue_3atomunits_changeunit())
    sue_filehub.save_change_file(sue_4atomunits_changeunit())

    # THEN
    assert len(dir_files(sue_filehub.changes_dir())) == 3
    assert len(dir_files(sue_filehub.atoms_dir())) == 9


def test_FileHub_save_change_file_ReturnsValidObj(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    sue2_changeunit = sue_2atomunits_changeunit()
    sue2_changeunit._atoms_dir = f"{sue_filehub.econs_dir()}/swimming"
    sue2_changeunit._changes_dir = f"{sue_filehub.econs_dir()}/swimming"
    sue2_changeunit._giver = "Bob"
    sue2_changeunit._change_id = sue_filehub._get_next_change_file_number() - 5
    prev_sue2_changeunit = copy_deepcopy(sue2_changeunit)

    # WHEN
    valid_changeunit = sue_filehub.save_change_file(sue2_changeunit)

    # THEN
    assert valid_changeunit._changes_dir != prev_sue2_changeunit._changes_dir
    assert valid_changeunit._changes_dir == sue_filehub.changes_dir()
    assert valid_changeunit._atoms_dir == sue_filehub.atoms_dir()
    assert valid_changeunit._change_id != prev_sue2_changeunit._change_id


def test_FileHub_create_save_change_file_SaveCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    two_int = 2
    three_int = 3
    print(f"{sue_filehub.change_file_path(two_int)=}")
    print(f"{sue_filehub.change_file_path(three_int)=}")
    sue_changeunit = changeunit_shop(
        _giver=sue_text,
        _change_id=two_int,
        _atoms_dir=sue_filehub.atoms_dir(),
        _changes_dir=sue_filehub.changes_dir(),
    )
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    sue_filehub.save_change_file(sue_changeunit, correct_invalid_attrs=False)
    assert sue_filehub.change_file_exists(two_int)
    assert sue_filehub.change_file_exists(three_int) == False

    # WHEN
    before_agenda = sue_filehub.default_duty_agenda()
    bob_text = "Bob"
    after_agenda = copy_deepcopy(before_agenda)
    after_agenda.add_partyunit(bob_text)
    sue_filehub.create_save_change_file(before_agenda, after_agenda)

    # THEN
    assert sue_filehub.change_file_exists(three_int)


def test_FileHub_merge_any_changes_ReturnsSameObj(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    duty_agenda = sue_filehub.get_duty_agenda()
    duty_agenda._last_change_id is None

    # WHEN
    new_agenda = sue_filehub._merge_any_changes(duty_agenda)

    # THEN
    assert new_agenda == duty_agenda


def test_FileHub_merge_any_changes_ReturnsObj_WithSinglechangeModifies_1atom(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    sue_filehub.save_change_file(sue_1atomunits_changeunit())
    duty_agenda = sue_filehub.get_duty_agenda()
    print(f"{duty_agenda._real_id=}")
    sports_text = "sports"
    sports_road = duty_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = duty_agenda.make_road(sports_road, knee_text)
    assert duty_agenda.idea_exists(sports_road) == False

    # WHEN
    new_agenda = sue_filehub._merge_any_changes(duty_agenda)

    # THEN
    assert new_agenda != duty_agenda
    assert new_agenda.idea_exists(sports_road)


def test_FileHub_merge_any_changes_ReturnsObj_WithSinglechangeModifies_2atoms(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    sue_filehub.save_change_file(sue_2atomunits_changeunit())
    duty_agenda = sue_filehub.get_duty_agenda()
    print(f"{duty_agenda._real_id=}")
    sports_text = "sports"
    sports_road = duty_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = duty_agenda.make_road(sports_road, knee_text)
    assert duty_agenda.idea_exists(sports_road) == False
    assert duty_agenda.idea_exists(knee_road) == False

    # WHEN
    new_agenda = sue_filehub._merge_any_changes(duty_agenda)

    # THEN
    assert new_agenda != duty_agenda
    assert new_agenda.idea_exists(sports_road)
    assert new_agenda.idea_exists(knee_road)
