from src._road.road import get_default_real_id_roadnode as root_label
from src.change.filehub import filehub_shop
from src.change.special_func import add_pledge_change
from src.change.examples.change_env import (
    env_dir_setup_cleanup,
    get_change_temp_env_dir as env_dir,
)


def test_add_pledge_change_Addspledgechange(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    sue_filehub.initialize_change_duty_files()
    old_sue_duty = sue_filehub.get_duty_agenda()
    clean_text = "clean"
    clean_road = old_sue_duty.make_l1_road(clean_text)
    one_int = 1
    print(f"{sue_filehub.change_file_path(one_int)=}")
    assert sue_filehub.change_file_exists(one_int) is False
    old_sue_duty = sue_filehub.get_duty_agenda()
    assert old_sue_duty.idea_exists(clean_road) is False

    # WHEN
    add_pledge_change(sue_filehub, clean_road)

    # THEN
    assert sue_filehub.change_file_exists(one_int)
    new_sue_duty = sue_filehub.get_duty_agenda()
    assert new_sue_duty.idea_exists(clean_road)


def test_add_pledge_change_SetsDutyAgendapledgeIdea_suffgroup(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    sue_filehub.initialize_change_duty_files()
    old_sue_duty = sue_filehub.get_duty_agenda()
    clean_text = "clean"
    clean_road = old_sue_duty.make_l1_road(clean_text)
    assert old_sue_duty.idea_exists(clean_road) is False

    # WHEN
    bob_text = "Bob"
    add_pledge_change(sue_filehub, clean_road, x_suffgroup=bob_text)

    # THEN
    new_sue_duty = sue_filehub.get_duty_agenda()
    assert new_sue_duty.idea_exists(clean_road)
    clean_idea = new_sue_duty.get_idea_obj(clean_road)
    print(f"{clean_idea._assignedunit._suffgroups=}")
    assert clean_idea._assignedunit.suffgroup_exists(bob_text)
