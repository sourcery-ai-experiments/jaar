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
    sue_1atomunits_giftunit,
    sue_2atomunits_giftunit,
    sue_3atomunits_giftunit,
    sue_4atomunits_giftunit,
    sue_carm_party_giftunit,
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
from copy import deepcopy as copy_deepcopy


def test_PersonUnit_save_giftunit_file_SaveCorrectObj(worlds_dir_setup_cleanup):
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
        _gifter=sue_text,
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
    worlds_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_gift0_path = f"{sue_person._gifts_dir}/{six_filename}"
    print(f"{sue_gift0_path=}")
    sue_giftunit = giftunit_shop(
        _gifter=sue_text,
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
    worlds_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_gift0_path = f"{sue_person._gifts_dir}/{six_filename}"
    print(f"{sue_gift0_path=}")
    sue_giftunit = giftunit_shop(
        _gifter=sue_text,
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


def test_PersonUnit_giftunit_file_exists_ReturnsCorrectObj(worlds_dir_setup_cleanup):
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
        _gifter=sue_person.person_id,
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


def test_PersonUnit_save_giftunit_file_RaisesErrorIfGiftUnit_gifter_IsWrong(
    worlds_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    x_gift_id = 6
    six_filename = get_json_filename(x_gift_id)
    sue_gift0_path = f"{sue_person._gifts_dir}/{six_filename}"
    print(f"{sue_gift0_path=}")
    bob_text = "Bob"
    sue_giftunit = giftunit_shop(
        _gifter=bob_text,
        _gift_id=x_gift_id,
        _atoms_dir=sue_person._atoms_dir,
        _gifts_dir=sue_person._gifts_dir,
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_person.save_giftunit_file(sue_giftunit, change_invalid_attrs=False)
    assert (
        str(excinfo.value)
        == f"GiftUnit file cannot be saved because giftunit._gifter is incorrect: {sue_giftunit._gifter}. It must be {sue_person.person_id}."
    )


def test_PersonUnit_save_giftunit_file_RaisesErrorIf_replace_IsFalse(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    x_gift_id = 0
    six_filename = get_json_filename(x_gift_id)
    sue_giftunit = giftunit_shop(
        _gifter=sue_text,
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


def test_PersonUnit_get_valid_giftunit_ReturnsObjWithAttributesFixed(
    worlds_dir_setup_cleanup,
):
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
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
    sue_person = personunit_shop(sue_text)
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
    sue_person.save_giftunit_file(invalid_sue_giftunit)

    # THEN
    assert os_path_exists(sue_gift2_path)
    two_file_json = open_file(sue_person._gifts_dir, next_filename)


def test_PersonUnit_get_max_gift_file_number_ReturnsCorrectObj(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)

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
    sue_person.save_giftunit_file(sue6_giftunit, change_invalid_attrs=False)
    sue_person.save_giftunit_file(sue2_giftunit, change_invalid_attrs=False)

    # WHEN / THEN
    assert sue_person.get_max_gift_file_number() == six_int
    assert sue_person.get_next_gift_file_number() == 7


def test_PersonUnit_get_new_giftunit_ReturnsObjWithCorrect_gift_id_WhenNoGiftFilesExist(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)

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
    sue_person = personunit_shop(sue_text)
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
    sue_person = personunit_shop(sue_text)
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
    sue_person = personunit_shop(sue_text)
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
    sue_person = personunit_shop(sue_text)
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
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    assert len(dir_files(sue_person._gifts_dir)) == 0
    assert len(dir_files(sue_person._atoms_dir)) == 0

    # WHEN
    sue_person.save_giftunit_file(sue_2atomunits_giftunit())
    sue_person.save_giftunit_file(sue_3atomunits_giftunit())
    sue_person.save_giftunit_file(sue_4atomunits_giftunit())

    # THEN
    assert len(dir_files(sue_person._gifts_dir)) == 3
    assert len(dir_files(sue_person._atoms_dir)) == 9


def test_PersonUnit_save_giftunit_file_ReturnsValidObj(worlds_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    sue2_giftunit = sue_2atomunits_giftunit()
    sue2_giftunit._atoms_dir = f"{sue_person.person_dir}/swimming"
    sue2_giftunit._gifts_dir = f"{sue_person.person_dir}/swimming"
    sue2_giftunit._gifter = "Bob"
    sue2_giftunit._gift_id = sue_person.get_next_gift_file_number() - 5
    prev_sue2_giftunit = copy_deepcopy(sue2_giftunit)

    # WHEN
    valid_giftunit = sue_person.save_giftunit_file(sue2_giftunit)

    # THEN
    assert valid_giftunit._gifts_dir != prev_sue2_giftunit._gifts_dir
    assert valid_giftunit._gifts_dir == sue_person._gifts_dir
    assert valid_giftunit._atoms_dir == sue_person._atoms_dir
    assert valid_giftunit._gift_id != prev_sue2_giftunit._gift_id


def test_PersonUnit_apply_new_giftunits_agenda_ReturnsObj_NoChange(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    gut_agenda = sue_person.get_gut_file_agenda()
    gut_agenda._last_gift_id is None

    # WHEN
    new_agenda = sue_person._apply_new_giftunits_agenda(gut_agenda)

    # THEN
    assert new_agenda == gut_agenda


def test_PersonUnit_apply_new_giftunits_agenda_ReturnsObj_WithSingleGiftChanges_1atom(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    sue_person.save_giftunit_file(sue_1atomunits_giftunit())
    # sue_person.save_giftunit_file(sue_3atomunits_giftunit())
    # sue_person.save_giftunit_file(sue_4atomunits_giftunit())
    gut_agenda = sue_person.get_gut_file_agenda()
    print(f"{gut_agenda._world_id=}")
    sports_text = "sports"
    sports_road = gut_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = gut_agenda.make_road(sports_road, knee_text)
    assert gut_agenda.idea_exists(sports_road) == False

    # WHEN
    new_agenda = sue_person._apply_new_giftunits_agenda(gut_agenda)

    # THEN
    assert new_agenda != gut_agenda
    assert new_agenda.idea_exists(sports_road)


def test_PersonUnit_apply_new_giftunits_agenda_ReturnsObj_WithSingleGiftChanges_2atoms(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    sue_person.save_giftunit_file(sue_2atomunits_giftunit())
    # sue_person.save_giftunit_file(sue_3atomunits_giftunit())
    # sue_person.save_giftunit_file(sue_4atomunits_giftunit())
    gut_agenda = sue_person.get_gut_file_agenda()
    print(f"{gut_agenda._world_id=}")
    sports_text = "sports"
    sports_road = gut_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = gut_agenda.make_road(sports_road, knee_text)
    assert gut_agenda.idea_exists(sports_road) == False
    assert gut_agenda.idea_exists(knee_road) == False

    # WHEN
    new_agenda = sue_person._apply_new_giftunits_agenda(gut_agenda)

    # THEN
    assert new_agenda != gut_agenda
    assert new_agenda.idea_exists(sports_road)
    assert new_agenda.idea_exists(knee_road)


def test_PersonUnit_update_gut_from_gifts_DoesNotChangeGut(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    old_gut_agenda = sue_person.get_gut_file_agenda()

    # WHEN
    sue_person.update_gut_from_gifts()

    # THEN
    new_gut_agenda = sue_person.get_gut_file_agenda()
    assert new_gut_agenda == old_gut_agenda
    assert new_gut_agenda._last_gift_id is None


def test_PersonUnit_update_gut_from_gifts_ChangesWith1GiftUnit(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    sue_person.save_giftunit_file(sue_2atomunits_giftunit())
    # sue_person.save_giftunit_file(sue_3atomunits_giftunit())
    # sue_person.save_giftunit_file(sue_4atomunits_giftunit())
    gut_agenda = sue_person.get_gut_file_agenda()
    print(f"{gut_agenda._world_id=}")
    sports_text = "sports"
    sports_road = gut_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = gut_agenda.make_road(sports_road, knee_text)
    old_gut_agenda = sue_person.get_gut_file_agenda()

    # WHEN
    sue_person.update_gut_from_gifts()

    # THEN
    new_gut_file = sue_person.get_gut_file_agenda()
    assert new_gut_file != old_gut_agenda
    assert new_gut_file._last_gift_id == 0
    assert new_gut_file.idea_exists(knee_road)
    assert new_gut_file.idea_exists(sports_road)


def test_PersonUnit_update_gut_from_gifts_ChangesWith2GiftUnit(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    sue_person.save_giftunit_file(sue_carm_party_giftunit())
    sue_person.save_giftunit_file(sue_4atomunits_giftunit())
    gut_agenda = sue_person.get_gut_file_agenda()
    print(f"{gut_agenda._world_id=}")
    sports_text = "sports"
    sports_road = gut_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = gut_agenda.make_road(sports_road, knee_text)
    carm_text = "Carmen"
    old_gut_agenda = sue_person.get_gut_file_agenda()
    assert old_gut_agenda._last_gift_id is None
    assert old_gut_agenda.idea_exists(knee_road) == False
    assert old_gut_agenda.idea_exists(sports_road) == False
    assert old_gut_agenda.get_party(carm_text) is None
    assert old_gut_agenda._party_creditor_pool is None
    # print(f"{dir_files(sue_person._gifts_dir).keys()=}")

    # WHEN
    sue_person.update_gut_from_gifts()

    # THEN
    new_gut_agenda = sue_person.get_gut_file_agenda()
    assert new_gut_agenda != old_gut_agenda
    assert new_gut_agenda._last_gift_id == 1
    assert new_gut_agenda.idea_exists(knee_road)
    assert new_gut_agenda.idea_exists(sports_road)
    assert new_gut_agenda.get_party(carm_text) != None
    assert new_gut_agenda._party_creditor_pool == 77


def test_PersonUnit_update_gut_from_gifts_2GiftUnitsWithOneAlreadyApplied(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(sue_text)
    first_gut_agenda = sue_person.get_gut_file_agenda()
    sports_text = "sports"
    sports_road = first_gut_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = first_gut_agenda.make_road(sports_road, knee_text)
    carm_text = "Carmen"
    assert first_gut_agenda._last_gift_id is None
    assert first_gut_agenda.idea_exists(knee_road) == False
    assert first_gut_agenda.idea_exists(sports_road) == False
    assert first_gut_agenda.get_party(carm_text) is None
    assert first_gut_agenda._party_creditor_pool is None

    # WHEN
    sue_person.save_giftunit_file(sue_carm_party_giftunit())
    sue_person.save_giftunit_file(sue_4atomunits_giftunit())
    first_gut_agenda.set_last_gift_id(0)
    sue_person._save_gut_file(first_gut_agenda)
    sue_person.update_gut_from_gifts()

    # THEN
    second_gut_agenda = sue_person.get_gut_file_agenda()
    print(f"{first_gut_agenda._world_id=}")
    assert second_gut_agenda._last_gift_id == 1
    assert second_gut_agenda.idea_exists(knee_road)
    assert second_gut_agenda.idea_exists(sports_road)
    assert second_gut_agenda.get_party(carm_text) is None
    assert second_gut_agenda._party_creditor_pool is None
