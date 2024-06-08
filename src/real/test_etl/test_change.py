from src._instrument.file import open_file, dir_files, delete_dir, set_dir, save_file
from src._road.jaar_config import init_change_id
from src.change.change import changeunit_shop, get_json_filename
from src.change.filehub import filehub_shop
from src.real.examples.example_atoms import get_atom_example_ideaunit_knee
from src.real.examples.example_changes import (
    get_sue_changeunit,
    sue_1atomunits_changeunit,
    sue_2atomunits_changeunit,
    sue_3atomunits_changeunit,
    sue_4atomunits_changeunit,
)
from src.real.admin_duty import (
    initialize_change_duty_files,
    get_duty_file_agenda,
    append_changes_to_duty_file,
    add_pledge_change,
)
from src.real.admin_change import _merge_changes_into_agenda
from src.real.examples.real_env_kit import reals_dir_setup_cleanup
from pytest import raises as pytest_raises
from copy import deepcopy as copy_deepcopy


def test_FileHub_merge_changes_into_agenda_ReturnsSameObj(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(None, None, sue_text)
    initialize_change_duty_files(sue_filehub)
    duty_agenda = get_duty_file_agenda(sue_filehub)
    duty_agenda._last_change_id is None

    # WHEN
    new_agenda = _merge_changes_into_agenda(sue_filehub, duty_agenda)

    # THEN
    assert new_agenda == duty_agenda


def test_merge_changes_into_agenda_ReturnsObj_WithSinglechangeModifies_1atom(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(None, None, sue_text)
    initialize_change_duty_files(sue_filehub)
    sue_filehub.save_change_file(sue_1atomunits_changeunit())
    duty_agenda = get_duty_file_agenda(sue_filehub)
    print(f"{duty_agenda._real_id=}")
    sports_text = "sports"
    sports_road = duty_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = duty_agenda.make_road(sports_road, knee_text)
    assert duty_agenda.idea_exists(sports_road) == False

    # WHEN
    new_agenda = _merge_changes_into_agenda(sue_filehub, duty_agenda)

    # THEN
    assert new_agenda != duty_agenda
    assert new_agenda.idea_exists(sports_road)


def test_merge_changes_into_agenda_ReturnsObj_WithSinglechangeModifies_2atoms(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(None, None, sue_text)
    initialize_change_duty_files(sue_filehub)
    sue_filehub.save_change_file(sue_2atomunits_changeunit())
    duty_agenda = get_duty_file_agenda(sue_filehub)
    print(f"{duty_agenda._real_id=}")
    sports_text = "sports"
    sports_road = duty_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = duty_agenda.make_road(sports_road, knee_text)
    assert duty_agenda.idea_exists(sports_road) == False
    assert duty_agenda.idea_exists(knee_road) == False

    # WHEN
    new_agenda = _merge_changes_into_agenda(sue_filehub, duty_agenda)

    # THEN
    assert new_agenda != duty_agenda
    assert new_agenda.idea_exists(sports_road)
    assert new_agenda.idea_exists(knee_road)


def test_append_changes_to_duty_file_AddschangesToDutyFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(None, None, sue_text)
    initialize_change_duty_files(sue_filehub)
    sue_filehub.save_change_file(sue_2atomunits_changeunit())
    duty_agenda = get_duty_file_agenda(sue_filehub)
    print(f"{duty_agenda._real_id=}")
    sports_text = "sports"
    sports_road = duty_agenda.make_l1_road(sports_text)
    knee_text = "knee"
    knee_road = duty_agenda.make_road(sports_road, knee_text)
    assert duty_agenda.idea_exists(sports_road) == False
    assert duty_agenda.idea_exists(knee_road) == False

    # WHEN
    new_agenda = append_changes_to_duty_file(sue_filehub)

    # THEN
    assert new_agenda != duty_agenda
    assert new_agenda.idea_exists(sports_road)
    assert new_agenda.idea_exists(knee_road)


def test_add_pledge_change_Addspledgechange(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(None, None, sue_text)
    initialize_change_duty_files(sue_filehub)
    old_sue_duty = get_duty_file_agenda(sue_filehub)
    clean_text = "clean"
    clean_road = old_sue_duty.make_l1_road(clean_text)
    one_int = 1
    print(f"{sue_filehub.change_file_path(one_int)=}")
    assert sue_filehub.change_file_exists(one_int) == False
    old_sue_duty = get_duty_file_agenda(sue_filehub)
    assert old_sue_duty.idea_exists(clean_road) == False

    # WHEN
    add_pledge_change(sue_filehub, clean_road)

    # THEN
    assert sue_filehub.change_file_exists(one_int)
    new_sue_duty = get_duty_file_agenda(sue_filehub)
    assert new_sue_duty.idea_exists(clean_road)


def test_add_pledge_change_SetsDutyAgendapledgeIdea_suffgroup(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(None, None, sue_text)
    initialize_change_duty_files(sue_filehub)
    old_sue_duty = get_duty_file_agenda(sue_filehub)
    clean_text = "clean"
    clean_road = old_sue_duty.make_l1_road(clean_text)
    assert old_sue_duty.idea_exists(clean_road) == False

    # WHEN
    bob_text = "Bob"
    add_pledge_change(sue_filehub, clean_road, x_suffgroup=bob_text)

    # THEN
    new_sue_duty = get_duty_file_agenda(sue_filehub)
    assert new_sue_duty.idea_exists(clean_road)
    clean_idea = new_sue_duty.get_idea_obj(clean_road)
    print(f"{clean_idea._assignedunit._suffgroups=}")
    assert clean_idea._assignedunit.suffgroup_exists(bob_text)
