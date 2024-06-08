from src.change.filehub import filehub_shop
from src.real.examples.example_changes import sue_2atomunits_changeunit
from src.real.admin_duty import (
    initialize_change_duty_files,
    append_changes_to_duty_file,
    add_pledge_change,
)


def test_append_changes_to_duty_file_AddschangesToDutyFile(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(None, None, sue_text)
    initialize_change_duty_files(sue_filehub)
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
    old_sue_duty = sue_filehub.get_duty_agenda()
    clean_text = "clean"
    clean_road = old_sue_duty.make_l1_road(clean_text)
    one_int = 1
    print(f"{sue_filehub.change_file_path(one_int)=}")
    assert sue_filehub.change_file_exists(one_int) == False
    old_sue_duty = sue_filehub.get_duty_agenda()
    assert old_sue_duty.idea_exists(clean_road) == False

    # WHEN
    add_pledge_change(sue_filehub, clean_road)

    # THEN
    assert sue_filehub.change_file_exists(one_int)
    new_sue_duty = sue_filehub.get_duty_agenda()
    assert new_sue_duty.idea_exists(clean_road)


def test_add_pledge_change_SetsDutyAgendapledgeIdea_suffgroup(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(None, None, sue_text)
    initialize_change_duty_files(sue_filehub)
    old_sue_duty = sue_filehub.get_duty_agenda()
    clean_text = "clean"
    clean_road = old_sue_duty.make_l1_road(clean_text)
    assert old_sue_duty.idea_exists(clean_road) == False

    # WHEN
    bob_text = "Bob"
    add_pledge_change(sue_filehub, clean_road, x_suffgroup=bob_text)

    # THEN
    new_sue_duty = sue_filehub.get_duty_agenda()
    assert new_sue_duty.idea_exists(clean_road)
    clean_idea = new_sue_duty.get_idea_obj(clean_road)
    print(f"{clean_idea._assignedunit._suffgroups=}")
    assert clean_idea._assignedunit.suffgroup_exists(bob_text)
